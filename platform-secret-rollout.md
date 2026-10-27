# Secret rotation not propagated

Document ID: platform-secret-rollout
Service: platform

## Symptoms
Applications continue using an outdated secret after rotation. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect secret resource versions, deployment reload mechanism, and mounted volume update timing.

## Mitigation
Trigger the documented rolling restart for workloads that require restart to load rotated secrets.

## Verification
Verify new connections authenticate with the rotated credential and old credentials are retired on schedule.

## Escalation
Escalate to security operations if a secret was exposed.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
