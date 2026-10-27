# Orphan multipart upload accumulation

Document ID: storage-multipart-leak
Service: storage

## Symptoms
Unfinished multipart uploads consume increasing storage. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
List incomplete upload age by bucket prefix and compare abort lifecycle rule configuration.

## Mitigation
Re-enable the approved abort-incomplete-multipart lifecycle rule and clean up uploads beyond the retention threshold.

## Verification
Verify incomplete upload count and billed storage trend decline over the next reporting interval.

## Escalation
Escalate to storage engineering if lifecycle actions are not applied.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
