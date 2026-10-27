# Time-based MFA code rejection

Document ID: identity-mfa-time
Service: identity

## Symptoms
Time-based one-time passwords fail across several nodes. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Measure node clock offset against the trusted time source and compare rejected-code timestamps.

## Mitigation
Restore time synchronization on affected nodes; do not expand the accepted MFA time window.

## Verification
Verify clocks are within two seconds and test a fresh code with an approved test account.

## Escalation
Escalate to infrastructure operations if time drift returns.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
