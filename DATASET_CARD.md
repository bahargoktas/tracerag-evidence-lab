# Synthetic incident-runbook benchmark

This repository contains 32 **original, synthetic** incident response runbooks (8 service areas × 4 scenarios) and 44 evaluation questions (32 answerable and 12 intentionally unsupported). No operational secrets, patient data, or proprietary documentation are included.

The fixed development split has 8 answerable + 4 unsupported questions. The held-out test split has 24 answerable + 8 unsupported questions. The corpus is shared across splits; **queries** are separated. Development queries may be used to choose a confidence threshold, but test queries must not be used for tuning.

Each answerable question has a document-level gold ID. There are no annotated answer spans; retrieval metrics measure finding the relevant **document**, not factual answer quality. Unsupported questions have no gold document. Because runbooks are synthetic and small, metrics must not be interpreted as real-world production performance.

The dataset was authored for this project and is distributed under the repository MIT license.

A separate `challenge.jsonl` contains 20 manually authored stress questions (12 answerable, 8 unsupported). It is evaluated without changing the threshold. It is not a large-scale adversarial benchmark.
