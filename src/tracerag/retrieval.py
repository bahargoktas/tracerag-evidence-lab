"""Three offline retrievers: BM25, TF-IDF and reciprocal-rank fusion."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math
import re

import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .data import Chunk

STOPWORDS = set(ENGLISH_STOP_WORDS)


def tokenize(text: str) -> list[str]:
    return [token for token in re.findall(r'[a-z0-9]+', text.lower())
            if token not in STOPWORDS and len(token) > 1]


@dataclass(frozen=True)
class Hit:
    doc_id: str
    title: str
    section: str
    path: str
    excerpt: str
    score: float
    confidence: float

    @property
    def citation(self) -> str:
        return f'[{self.doc_id} § {self.section}]'


class RunbookIndex:
    """Deterministic in-memory index; no network calls or model downloads."""

    def __init__(self, chunks: list[Chunk]):
        if not chunks:
            raise ValueError('Cannot index an empty corpus')
        self.chunks = chunks
        texts = [c.searchable_text for c in chunks]
        self.vectorizer = TfidfVectorizer(
            lowercase=True, stop_words='english', ngram_range=(1, 2),
            sublinear_tf=True, norm='l2', min_df=1,
        )
        self.matrix = self.vectorizer.fit_transform(texts)
        self.tokens = [tokenize(text) for text in texts]
        self.freqs = [Counter(tokens) for tokens in self.tokens]
        self.lengths = np.asarray([len(tokens) for tokens in self.tokens], dtype=float)
        self.avg_length = float(np.mean(self.lengths))
        self.doc_freq = Counter(token for tokens in self.tokens for token in set(tokens))

    def _bm25(self, query: str, k1: float = 1.5, b: float = 0.75) -> np.ndarray:
        query_tokens = set(tokenize(query))
        scores = np.zeros(len(self.chunks), dtype=float)
        n = len(self.chunks)
        for term in query_tokens:
            df = self.doc_freq.get(term, 0)
            if not df:
                continue
            idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
            for i, frequencies in enumerate(self.freqs):
                tf = frequencies.get(term, 0)
                if tf:
                    norm = k1 * (1 - b + b * self.lengths[i] / self.avg_length)
                    scores[i] += idf * (tf * (k1 + 1)) / (tf + norm)
        return scores

    def _cosine(self, query: str) -> np.ndarray:
        query_vector = self.vectorizer.transform([query])
        return cosine_similarity(query_vector, self.matrix).ravel()

    @staticmethod
    def _ranks(scores: np.ndarray) -> dict[int, int]:
        # Zero scores are not relevant: do not let them collect RRF credit.
        positive = [i for i in range(len(scores)) if scores[i] > 0]
        positive.sort(key=lambda i: (-float(scores[i]), i))
        return {idx: rank + 1 for rank, idx in enumerate(positive)}

    def retrieve(self, query: str, k: int = 5, mode: str = 'hybrid') -> list[Hit]:
        if not query.strip() or k < 1:
            return []
        if mode not in {'bm25', 'tfidf', 'hybrid'}:
            raise ValueError(f'Unknown retrieval mode: {mode}')
        bm25 = self._bm25(query)
        cosine = self._cosine(query)
        if mode == 'bm25':
            scores = bm25
        elif mode == 'tfidf':
            scores = cosine
        else:
            bm_ranks, tf_ranks = self._ranks(bm25), self._ranks(cosine)
            scores = np.zeros(len(self.chunks), dtype=float)
            for i in range(len(self.chunks)):
                scores[i] = (1 / (60 + bm_ranks[i]) if i in bm_ranks else 0) + (
                    1 / (60 + tf_ranks[i]) if i in tf_ranks else 0)
        ordered = sorted(range(len(scores)), key=lambda i: (-float(scores[i]), i))
        hits: list[Hit] = []
        seen_docs: set[str] = set()
        for idx in ordered:
            if scores[idx] <= 0:
                break
            chunk = self.chunks[idx]
            if chunk.doc_id in seen_docs:
                continue
            seen_docs.add(chunk.doc_id)
            hits.append(Hit(
                doc_id=chunk.doc_id, title=chunk.title,
                section=chunk.section, path=chunk.path,
                excerpt=chunk.text, score=float(scores[idx]),
                confidence=float(cosine[idx]),
            ))
            if len(hits) == k:
                break
        return hits

    def evidence(self, query: str, threshold: float, mode: str = 'hybrid') -> Hit | None:
        """Return a verbatim evidence section, or abstain. Not a generated answer."""
        hits = self.retrieve(query, k=1, mode=mode)
        if not hits or hits[0].confidence < threshold:
            return None
        return hits[0]
