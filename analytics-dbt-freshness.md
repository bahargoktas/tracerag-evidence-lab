# Analytics model freshness failure

Document ID: analytics-dbt-freshness
Service: analytics

## Symptoms
Dbt source freshness checks fail before scheduled reporting. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect source loaded_at timestamps, upstream ingestion status, and the dbt freshness threshold.

## Mitigation
Repair the delayed ingestion job and rerun the affected dbt models in dependency order.

## Verification
Verify freshness checks pass and row counts match the expected source window.

## Escalation
Escalate to the data producer if upstream events have stopped.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
