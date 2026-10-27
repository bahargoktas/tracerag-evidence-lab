# Search index freshness regression

Document ID: search-index-stale
Service: search

## Symptoms
Recent records do not appear in search results. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect ingestion checkpoint, indexing queue age, and refresh interval configuration.

## Mitigation
Restore the indexing worker from the last confirmed checkpoint and replay missing change events idempotently.

## Verification
Verify sampled newly created record IDs are searchable and index lag is under five minutes.

## Escalation
Escalate to the ingestion team if source events are missing.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
