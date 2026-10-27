# Search analyzer version drift

Document ID: search-analyzer-drift
Service: search

## Symptoms
Same query produces inconsistent tokenization across indices. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Compare analyzer settings and token outputs between the old and new index aliases.

## Mitigation
Rebuild the affected index with the approved analyzer definition and switch aliases after validation.

## Verification
Verify tokenization examples and top result consistency before and after alias cutover.

## Escalation
Escalate to search relevance owners if ranking changes exceed the acceptance threshold.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
