from pathlib import Path
import pytest
from tracerag.data import load_chunks, load_questions

ROOT = Path(__file__).resolve().parents[1]


def test_runbooks_have_unique_doc_ids_and_sections():
    chunks = load_chunks(ROOT / 'data/runbooks')
    ids = {c.doc_id for c in chunks}
    assert len(ids) == 32
    assert len(chunks) >= 32 * 5
    assert all(c.text and c.section and c.path.endswith('.md') for c in chunks)


def test_gold_labels_exist_and_splits_do_not_overlap():
    chunks = load_chunks(ROOT / 'data/runbooks')
    questions = load_questions(ROOT / 'data/evaluation/queries.jsonl', {c.doc_id for c in chunks})
    assert len(questions) == 44
    assert {q.qid for q in questions if q.split == 'dev'}.isdisjoint(
        {q.qid for q in questions if q.split == 'test'})
    assert sum(q.answerable for q in questions) == 32
    assert sum(not q.answerable for q in questions) == 12


def test_missing_corpus_raises(tmp_path):
    with pytest.raises(ValueError, match='No Markdown'):
        load_chunks(tmp_path)
