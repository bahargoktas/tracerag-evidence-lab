"""Document-level ranking metrics and conservative evidence decision audit."""
from __future__ import annotations

from dataclasses import dataclass
import math
from statistics import mean
from typing import Any

from .data import Question
from .retrieval import RunbookIndex


@dataclass
class EvaluationResult:
    metrics: dict[str, Any]
    rows: list[dict[str, Any]]


def ranking_metrics(ranked: list[str], gold: tuple[str, ...], k: int) -> tuple[float, float, float]:
    """Recall@k, reciprocal rank@k, binary relevance nDCG@k."""
    if not gold:
        raise ValueError('Ranking metrics require at least one relevant document')
    top = ranked[:k]
    relevant = set(gold)
    recall = len(relevant.intersection(top)) / len(relevant)
    rr = next((1 / (i + 1) for i, doc in enumerate(top) if doc in relevant), 0.0)
    dcg = sum(1 / math.log2(i + 2) for i, doc in enumerate(top) if doc in relevant)
    ideal = sum(1 / math.log2(i + 2) for i in range(min(len(relevant), k)))
    return recall, rr, dcg / ideal if ideal else 0.0


def evaluate(index: RunbookIndex, questions: list[Question], threshold: float,
             mode: str = 'hybrid') -> EvaluationResult:
    if not questions:
        raise ValueError('No evaluation questions')
    rows = []
    for q in questions:
        hits = index.retrieve(q.query, k=5, mode=mode)
        ranked = [h.doc_id for h in hits]
        top = hits[0] if hits else None
        answered = bool(top and top.confidence >= threshold)
        citation_correct = bool(answered and top and top.doc_id in q.gold_doc_ids)
        row: dict[str, Any] = {
            'qid': q.qid, 'split': q.split, 'query': q.query,
            'answerable': q.answerable, 'gold_doc_ids': list(q.gold_doc_ids),
            'top_doc_id': top.doc_id if top else None,
            'top_section': top.section if top else None,
            'confidence': round(top.confidence, 6) if top else 0.0,
            'answered': answered, 'citation_correct': citation_correct,
            'decision_correct': answered == q.answerable,
            'outcome_correct': citation_correct if q.answerable else not answered,
        }
        if q.answerable:
            for k in (1, 3, 5):
                recall, rr, ndcg = ranking_metrics(ranked, q.gold_doc_ids, k)
                row[f'recall@{k}'] = recall
                row[f'mrr@{k}'] = rr
                row[f'ndcg@{k}'] = ndcg
        rows.append(row)
    answerable = [r for r in rows if r['answerable']]
    unsupported = [r for r in rows if not r['answerable']]
    attempted = [r for r in rows if r['answered']]
    metrics: dict[str, Any] = {
        'mode': mode, 'threshold': threshold,
        'n_questions': len(rows), 'n_answerable': len(answerable),
        'n_unsupported': len(unsupported),
        'answer_coverage': mean(r['answered'] for r in rows),
        'decision_accuracy': mean(r['decision_correct'] for r in rows),
        'supported_response_accuracy': mean(r['outcome_correct'] for r in rows),
        'citation_precision': mean(r['citation_correct'] for r in attempted) if attempted else None,
        'citation_recall': mean(r['citation_correct'] for r in answerable) if answerable else None,
        'unsupported_false_answer_rate': mean(r['answered'] for r in unsupported) if unsupported else None,
    }
    for k in (1, 3, 5):
        for name in ('recall', 'mrr', 'ndcg'):
            metrics[f'{name}@{k}'] = mean(r[f'{name}@{k}'] for r in answerable) if answerable else None
    return EvaluationResult(metrics, rows)


def choose_threshold(index: RunbookIndex, dev_questions: list[Question],
                     mode: str = 'hybrid') -> dict[str, Any]:
    """Tune only on development questions; favor conservative ties."""
    if not dev_questions or any(q.split != 'dev' for q in dev_questions):
        raise ValueError('Threshold tuning is restricted to development questions')
    # Search a fixed grid. Threshold is cosine similarity, not a probability.
    grid = [round(i / 100, 2) for i in range(5, 71)]
    ranked = []
    for threshold in grid:
        result = evaluate(index, dev_questions, threshold, mode)
        m = result.metrics
        answerable = [r for r in result.rows if r['answerable']]
        unsupported = [r for r in result.rows if not r['answerable']]
        true_answer_rate = mean(r['citation_correct'] for r in answerable) if answerable else 0
        abstain_rate = mean(not r['answered'] for r in unsupported) if unsupported else 0
        balanced = (true_answer_rate + abstain_rate) / 2
        ranked.append((balanced, m['supported_response_accuracy'], threshold))
    best = max(ranked)
    return {
        'mode': mode, 'threshold': best[2],
        'selection': 'max balanced (correct citation on answerable, abstain on unsupported); ties prefer higher threshold',
        'development_balanced_score': round(best[0], 6),
        'development_supported_response_accuracy': round(best[1], 6),
        'development_question_count': len(dev_questions),
        'warning': 'Similarity score is not a calibrated probability. Test split was not used to tune.'
    }
