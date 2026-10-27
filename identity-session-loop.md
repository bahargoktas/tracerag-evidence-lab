# Login redirect loop

Document ID: identity-session-loop
Service: identity

## Symptoms
Browser login repeatedly redirects between application and identity provider. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect SameSite cookie settings, callback host consistency, and session creation logs.

## Mitigation
Restore the approved SameSite and secure cookie policy and align callback hostnames across environments.

## Verification
Verify one clean login completes and the browser retains a session without repeated redirects.

## Escalation
Escalate to the application team if third-party cookie restrictions remain.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
