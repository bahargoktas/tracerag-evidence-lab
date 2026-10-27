# Object storage access denied

Document ID: storage-object-403
Service: storage

## Symptoms
Object downloads return 403 for a newly deployed service. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect workload identity, bucket policy conditions, and object key prefix against the requested resource.

## Mitigation
Restore the approved least-privilege policy binding for the workload identity; do not grant public bucket access.

## Verification
Verify the service can read the intended prefix and remains denied for unrelated prefixes.

## Escalation
Escalate to cloud security if the policy was intentionally revoked.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
