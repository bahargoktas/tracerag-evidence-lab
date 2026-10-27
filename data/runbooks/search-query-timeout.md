# Search query timeout spike

Document ID: search-query-timeout
Service: search

## Symptoms
Search requests time out during complex filtering. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect slow query logs, cardinality of filters, and query concurrency by tenant.

## Mitigation
Restore query concurrency caps and replace the expensive filter plan with the indexed field variant.

## Verification
Verify p95 search latency and timeout rates recover under representative load.

## Escalation
Escalate to search relevance engineers if the indexed query changes result semantics.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
