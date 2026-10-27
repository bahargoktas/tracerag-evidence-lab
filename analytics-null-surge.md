# Unexpected null field surge

Document ID: analytics-null-surge
Service: analytics

## Symptoms
A required event field becomes null for a large fraction of records. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect producer version changes, schema validation results, and null rate by source partition.

## Mitigation
Quarantine affected partitions and roll back the producer mapping regression before replay.

## Verification
Verify required-field completeness returns above 99.5 percent and quarantined records are accounted for.

## Escalation
Escalate to data quality owners if missing values cannot be reconstructed.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
