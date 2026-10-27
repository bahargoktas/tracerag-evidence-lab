# Cross-region replication delay

Document ID: storage-replication-lag
Service: storage

## Symptoms
New objects appear late in the disaster recovery region. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect replication backlog, destination permissions, and replication status metadata.

## Mitigation
Restore the approved replication role permissions and prioritize the existing backlog without bypassing integrity checks.

## Verification
Verify sampled object checksums match in both regions and backlog age falls.

## Escalation
Escalate to disaster recovery owners if recovery objectives are at risk.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
