"""Command line interface for TraceRAG."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .data import load_chunks, load_questions
from .evaluation import choose_threshold, evaluate
from .reporting import create_report, write_json
from .retrieval import RunbookIndex

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='tracerag', description='Offline runbook evidence retrieval and audit')
    p.add_argument('--root', type=Path, default=PROJECT_ROOT, help='Project directory')
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('check-data', help='Validate corpus and gold labels')
    tune = sub.add_parser('tune', help='Choose evidence threshold using dev split only')
    tune.add_argument('--out', type=Path, default=Path('config/threshold.json'))
    ev = sub.add_parser('evaluate', help='Generate benchmark reports')
    ev.add_argument('--split', choices=('dev', 'test', 'challenge'), default='test')
    ev.add_argument('--out', type=Path, default=Path('reports'))
    ask = sub.add_parser('ask', help='Retrieve verbatim evidence with a citation')
    ask.add_argument('--query', required=True)
    ask.add_argument('--mode', choices=('hybrid', 'bm25', 'tfidf'), default='hybrid')
    ask.add_argument('--top-k', type=int, default=3)
    return p


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = args.root.resolve()
    chunks = load_chunks(root / 'data/runbooks')
    index = RunbookIndex(chunks)
    ids = {c.doc_id for c in chunks}
    questions = load_questions(root / 'data/evaluation/queries.jsonl', ids)
    challenge = load_questions(root / 'data/evaluation/challenge.jsonl', ids)

    if args.command == 'check-data':
        print(json.dumps({'documents': len(ids), 'chunks': len(chunks),
                          'questions': len(questions), 'dev': sum(q.split == 'dev' for q in questions),
                          'test': sum(q.split == 'test' for q in questions),
                          'challenge': len(challenge)}, indent=2))
        return 0
    if args.command == 'tune':
        config = choose_threshold(index, [q for q in questions if q.split == 'dev'])
        out = resolve(root, args.out)
        write_json(out, config)
        print(f'Development-only threshold written to {out}: {config["threshold"]:.2f}')
        return 0

    config_path = root / 'config/threshold.json'
    if not config_path.exists():
        raise FileNotFoundError('Missing threshold configuration; run `python -m tracerag.cli tune` first')
    config = json.loads(config_path.read_text(encoding='utf-8'))
    threshold = float(config['threshold'])
    if args.command == 'evaluate':
        subset = challenge if args.split == 'challenge' else [q for q in questions if q.split == args.split]
        results = {mode: evaluate(index, subset, threshold, mode) for mode in ('bm25', 'tfidf', 'hybrid')}
        out = resolve(root, args.out)
        create_report(out, results, args.split)
        print(json.dumps({'split': args.split, 'metrics': {m: r.metrics for m, r in results.items()}}, indent=2))
        print(f'Reports saved to {out}')
        return 0
    if args.command == 'ask':
        hits = index.retrieve(args.query, k=args.top_k, mode=args.mode)
        selected = index.evidence(args.query, threshold, mode=args.mode)
        output = {
            'query': args.query, 'mode': args.mode,
            'similarity_threshold': threshold,
            'abstained': selected is None,
            'notice': 'Verbatim runbook evidence, not a generated or verified answer.',
            'evidence': None if selected is None else {
                'citation': selected.citation, 'path': selected.path,
                'excerpt': selected.excerpt, 'similarity': round(selected.confidence, 4)},
            'retrieved': [{'doc_id': h.doc_id, 'section': h.section,
                           'similarity': round(h.confidence, 4)} for h in hits],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return 0
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
