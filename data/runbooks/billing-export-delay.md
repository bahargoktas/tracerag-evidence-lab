# Invoice export backlog

Document ID: billing-export-delay
Service: billing

## Symptoms
Daily invoice exports arrive hours late. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect export worker queue depth, batch durations, and object store write latency.

## Mitigation
Increase workers within the approved concurrency ceiling and retry failed export batches by batch ID.

## Verification
Verify queue age falls below thirty minutes and sample exported totals match source records.

## Escalation
Escalate to finance data engineering if totals do not reconcile.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
