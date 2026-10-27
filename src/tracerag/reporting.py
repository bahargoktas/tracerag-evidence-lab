"""Write audit artifacts without network dependencies."""
from __future__ import annotations

import csv
import html
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from .evaluation import EvaluationResult


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def create_report(out: Path, results: dict[str, EvaluationResult], split: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    metrics = {mode: result.metrics for mode, result in results.items()}
    write_json(out / 'metrics.json', {'split': split, 'retrievers': metrics})
    for mode, result in results.items():
        if not result.rows:
            continue
        with (out / f'predictions_{mode}.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(result.rows[0].keys()))
            writer.writeheader()
            for row in result.rows:
                row = {k: json.dumps(v) if isinstance(v, list) else v for k, v in row.items()}
                writer.writerow(row)

    fig, ax = plt.subplots(figsize=(9, 4.8))
    names = list(results)
    xs = range(len(names))
    width = 0.24
    for j, k in enumerate((1, 3, 5)):
        vals = [results[n].metrics[f'recall@{k}'] or 0 for n in names]
        ax.bar([x + (j - 1) * width for x in xs], vals, width=width, label=f'Recall@{k}')
    ax.set_xticks(list(xs), names)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel('Document recall (answerable questions)')
    ax.set_title(f'Retrieval performance — {split} split')
    ax.legend()
    ax.grid(axis='y', alpha=0.25)
    fig.tight_layout()
    fig.savefig(out / 'retrieval_comparison.png', dpi=170)
    plt.close(fig)

    hybrid = results['hybrid']
    fig, ax = plt.subplots(figsize=(8, 4.8))
    yes = [r['confidence'] for r in hybrid.rows if r['answerable']]
    no = [r['confidence'] for r in hybrid.rows if not r['answerable']]
    ax.hist([yes, no], bins=12, label=['Answerable', 'Unsupported'], alpha=0.75)
    ax.axvline(hybrid.metrics['threshold'], linestyle='--', color='black', label='Dev-selected threshold')
    ax.set_xlabel('Top retrieved section TF-IDF cosine similarity (not probability)')
    ax.set_ylabel('Question count')
    ax.set_title(f'Evidence confidence distribution — {split} split')
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / 'confidence_distribution.png', dpi=170)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.8))
    outcomes = [
        ('Correct citation', sum(r['citation_correct'] for r in hybrid.rows if r['answerable'])),
        ('Wrong citation', sum(r['answered'] and not r['citation_correct'] for r in hybrid.rows if r['answerable'])),
        ('Missed answer', sum(not r['answered'] for r in hybrid.rows if r['answerable'])),
        ('Correct abstain', sum(not r['answered'] for r in hybrid.rows if not r['answerable'])),
        ('Unsupported answer', sum(r['answered'] for r in hybrid.rows if not r['answerable'])),
    ]
    ax.barh([label for label, _ in outcomes][::-1], [count for _, count in outcomes][::-1])
    ax.set_xlabel('Number of questions')
    ax.set_title(f'Hybrid evidence decision audit — {split} split')
    ax.grid(axis='x', alpha=0.25)
    fig.tight_layout()
    fig.savefig(out / 'evidence_audit.png', dpi=170)
    plt.close(fig)

    cells = ''
    for mode, m in metrics.items():
        cells += '<tr>' + ''.join(f'<td>{html.escape(str(x))}</td>' for x in (
            mode, f"{m['recall@1']:.3f}", f"{m['recall@3']:.3f}",
            f"{m['mrr@5']:.3f}", f"{m['supported_response_accuracy']:.3f}",
            f"{m['unsupported_false_answer_rate']:.3f}",
        )) + '</tr>'
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TraceRAG evidence audit</title><style>
body{{background:#f4f7fb;color:#152238;font:16px/1.6 system-ui,sans-serif;margin:0}}
main{{max-width:1000px;margin:auto;padding:40px 24px}}
header{{background:#10243a;color:#f9fafb;padding:30px;border-radius:16px}}
header p{{color:#c6d6e8}}.tag{{font-size:12px;letter-spacing:.15em;color:#62ddc2;text-transform:uppercase}}
section{{background:white;padding:24px;margin:22px 0;border-radius:14px;box-shadow:0 3px 15px #15223810}}
img{{width:100%;max-width:850px;display:block;margin:auto}}
table{{border-collapse:collapse;width:100%;overflow-x:auto}}td,th{{padding:10px;text-align:left;border-bottom:1px solid #e6e9f0}}
small{{color:#4b5563}}
</style></head><body><main><header><div class="tag">Offline RAG evaluation</div>
<h1>TraceRAG Evidence Audit</h1><p>Split: {html.escape(split)} · Document-level retrieval · Extractive evidence only</p></header>
<section><h2>Retriever comparison</h2><table><thead><tr><th>Mode</th><th>Recall@1</th><th>Recall@3</th><th>MRR@5</th><th>Supported response accuracy</th><th>Unsupported false-answer rate</th></tr></thead><tbody>{cells}</tbody></table>
<p><small>Scores reflect a small, synthetic benchmark. Citation correctness is evaluated against gold document IDs, not human-labeled answer spans. Confidence is a lexical similarity score, not a calibrated probability.</small></p></section>
<section><h2>Finding the correct runbook</h2><img alt="Document retrieval comparison" src="retrieval_comparison.png"></section>
<section><h2>When should the system abstain?</h2><img alt="Confidence distributions" src="confidence_distribution.png"></section>
<section><h2>Evidence decision audit</h2><img alt="Hybrid answer and abstention counts" src="evidence_audit.png"></section>
<section><h2>Reproduce</h2><code>python -m tracerag.cli evaluate --split {html.escape(split)} --out reports</code><p>Review the CSV files for per-question errors and the JSON file for unrounded aggregate metrics.</p></section>
</main></body></html>'''
    (out / 'index.html').write_text(doc, encoding='utf-8')
