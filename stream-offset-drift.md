# Consumer offset position anomaly

Document ID: stream-offset-drift
Service: stream

## Symptoms
Consumer resumes from an unexpected offset after deployment. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Compare committed offsets, consumer group IDs, and deployment configuration history.

## Mitigation
Restore the intended consumer group configuration and use a reviewed offset adjustment only if required.

## Verification
Verify no gaps or duplicate business events using downstream event IDs.

## Escalation
Escalate to data integrity owners before any offset rewind.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
