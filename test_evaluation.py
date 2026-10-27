from pathlib import Path
import pytest
from tracerag.data import load_chunks, load_questions, Question
from tracerag.retrieval import RunbookIndex
from tracerag.evaluation import ranking_metrics, evaluate, choose_threshold

ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture(scope='module')
def data():
    chunks = load_chunks(ROOT / 'data/runbooks')
    return RunbookIndex(chunks), load_questions(ROOT / 'data/evaluation/queries.jsonl', {c.doc_id for c in chunks})


def test_ranking_metrics_known_values():
    recall, rr, ndcg = ranking_metrics(['x', 'target', 'y'], ('target',), 3)
    assert recall == 1.0
    assert rr == 0.5
    assert ndcg == pytest.approx(1 / 1.584962500721156)


def test_ranking_metrics_reject_unsupported():
    with pytest.raises(ValueError):
        ranking_metrics(['x'], (), 1)


def test_dev_only_tuning(data):
    index, questions = data
    dev = [q for q in questions if q.split == 'dev']
    tuned = choose_threshold(index, dev)
    assert 0.05 <= tuned['threshold'] <= 0.7
    with pytest.raises(ValueError, match='development'):
        choose_threshold(index, questions)


def test_evaluation_counts_and_ranges(data):
    index, questions = data
    test = [q for q in questions if q.split == 'test']
    result = evaluate(index, test, 0.2)
    assert result.metrics['n_questions'] == len(test)
    assert 0 <= result.metrics['recall@3'] <= 1
    assert 0 <= result.metrics['supported_response_accuracy'] <= 1
    assert all('top_doc_id' in row for row in result.rows)
