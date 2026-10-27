# Schema registry incompatibility

Document ID: stream-schema-break
Service: stream

## Symptoms
New producer messages are rejected for schema incompatibility. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Compare new schema fields against the compatibility mode and inspect rejected subject versions.

## Mitigation
Revert the incompatible producer schema and release a backward-compatible version with optional defaults.

## Verification
Verify old consumers deserialize new test events and schema registry accepts the new version.

## Escalation
Escalate to data contracts owners before changing compatibility policy.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
