# Error analysis — frozen held-out test set

This document describes observed results after tuning the similarity threshold **only on 12 development questions**. The frozen threshold is `0.24`. Recompute results with `python -m tracerag.cli evaluate --split test`.

## Why a 100% document Recall@1 can coexist with 71.9% supported response accuracy

The hybrid retriever ranks the gold document first for all 24 answerable test queries. However, the evidence gate checks the cosine similarity of the selected section. For 7 answerable questions, that similarity is below 0.24; the system therefore abstains. Among the 8 unsupported test questions, 2 cross the threshold and receive irrelevant citations. The remaining 6 are correctly rejected.

This gives 17 correctly cited answerable questions + 6 correct abstentions = 23 / 32 = 0.71875 supported response accuracy. It also gives 2 / 8 = 0.25 unsupported false-answer rate.

## Representative errors

- `Q004`: Gateway rate-limiting runbook ranked first but similarity = 0.151. Correct evidence was missed.
- `Q006`: JWKS cache runbook ranked first but similarity = 0.225. Correct evidence was missed.
- `Q026`: HPA oscillation runbook ranked first but similarity = 0.201. Correct evidence was missed.
- `U002`: DNSSEC key rollover question incorrectly mapped to the JWKS key-rotation runbook (0.289). Both mention key rotation, but the runbook does not cover DNSSEC.
- `U003`: Apple push notification signing-key question incorrectly mapped to JWKS (0.434). Strong lexical overlap is not sufficient evidence.

## Challenge set

The additional challenge suite is **not used for tuning**. The hybrid system obtains document Recall@1 = 1.0 on its 12 answerable questions but supported response accuracy = 0.8 across all 20 questions. Two unsupported questions receive false citations. These figures are from synthetic, authored queries and should not be generalized.

## Experiments

1. Inspect per-query confidence distributions. Can a single cosine threshold separate supported and unsupported questions?
2. Add section-level relevance labels. Does a correct document ID imply a correct evidence section?
3. Create genuinely independently written user queries and compare BM25, TF-IDF, and hybrid again.
4. Add semantic embeddings, keeping the same dev/test split, then compare false-answer rates as well as Recall@k.
5. Perform bootstrapped uncertainty intervals on the 32-question test set, noting that the queries are not independent samples from a production population.

## Section-level evidence can still be wrong

The `ask` command returns a **single highest-ranked section** from the top document. For the query "How should JWKS caches be refreshed after signing key rotation?", the retrieved document is correct but the selected section is `Escalation`, not `Mitigation`. The section mentions contacting identity security if a signing key is missing; it does not provide the requested cache-refresh procedure. The current document-level relevance labels cannot detect this failure. Adding section- or span-level annotations and reranking within a document is an explicit next step.
