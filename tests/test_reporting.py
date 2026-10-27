from pathlib import Path
import json

from tracerag.data import load_chunks, load_questions
from tracerag.retrieval import RunbookIndex
from tracerag.evaluation import evaluate
from tracerag.reporting import create_report

ROOT = Path(__file__).resolve().parents[1]


def test_report_writes_html_json_csv_and_figures(tmp_path):
    chunks = load_chunks(ROOT / 'data/runbooks')
    index = RunbookIndex(chunks)
    questions = load_questions(ROOT / 'data/evaluation/queries.jsonl', {c.doc_id for c in chunks})
    dev = [q for q in questions if q.split == 'dev']
    results = {mode: evaluate(index, dev, 0.24, mode) for mode in ('bm25', 'tfidf', 'hybrid')}
    create_report(tmp_path, results, 'dev')
    for name in ('index.html', 'metrics.json', 'predictions_hybrid.csv',
                 'retrieval_comparison.png', 'confidence_distribution.png', 'evidence_audit.png'):
        assert (tmp_path / name).is_file()
        assert (tmp_path / name).stat().st_size > 0
    assert json.loads((tmp_path / 'metrics.json').read_text())['split'] == 'dev'


def test_challenge_labels_are_separate():
    chunks = load_chunks(ROOT / 'data/runbooks')
    cases = load_questions(ROOT / 'data/evaluation/challenge.jsonl', {c.doc_id for c in chunks})
    assert len(cases) == 20
    assert sum(c.answerable for c in cases) == 12
    assert all(c.split == 'challenge' for c in cases)
