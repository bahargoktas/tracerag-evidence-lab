# Dead-letter queue spike

Document ID: stream-dead-letter
Service: stream

## Symptoms
Message failures rapidly accumulate in the dead-letter queue. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Group failed events by exception type and schema version; inspect poison-message samples without logging sensitive payloads.

## Mitigation
Fix the identified parser or validation defect and replay a bounded, audited batch from the dead-letter queue.

## Verification
Verify dead-letter arrival rate returns to baseline and replayed event IDs are processed once.

## Escalation
Escalate to the source service if malformed events continue.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
