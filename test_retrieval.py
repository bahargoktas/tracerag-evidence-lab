from pathlib import Path
import pytest
from tracerag.data import load_chunks
from tracerag.retrieval import RunbookIndex, tokenize

ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture(scope='module')
def index():
    return RunbookIndex(load_chunks(ROOT / 'data/runbooks'))


def test_tokenizer_ignores_common_stopwords():
    assert tokenize('The Kafka consumer is behind') == ['kafka', 'consumer']


@pytest.mark.parametrize('mode', ['bm25', 'tfidf', 'hybrid'])
def test_modes_find_relevant_doc(index, mode):
    hits = index.retrieve('JWKS cache key rotation signature validation', k=3, mode=mode)
    assert hits and hits[0].doc_id == 'identity-jwks-cache'
    assert len({h.doc_id for h in hits}) == len(hits)


def test_evidence_is_verbatim(index):
    hit = index.evidence('JWKS cache key rotation signature validation', threshold=0.0)
    assert hit is not None
    source = (ROOT / hit.path).read_text(encoding='utf-8')
    assert hit.excerpt in source
    assert hit.doc_id in hit.citation


def test_abstains_on_nonsense(index):
    assert index.evidence('xyzzy qwerty 123xyz', threshold=0.2) is None


def test_empty_query_and_invalid_mode(index):
    assert index.retrieve('   ') == []
    with pytest.raises(ValueError, match='Unknown retrieval mode'):
        index.retrieve('kafka lag', mode='unknown')
