# Upstream 502 bursts

Document ID: gateway-upstream-502
Service: gateway

## Symptoms
Edge proxy returns 502 after a backend deployment. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect gateway upstream_reset counters and correlate failing routes with backend rollout timestamps. Compare service endpoints against ready pod IPs.

## Mitigation
Roll back the backend deployment if reset counters rose immediately after the release; otherwise drain endpoints that fail readiness checks.

## Verification
Confirm 502 rate below 0.5 percent for fifteen minutes and backend readiness is stable.

## Escalation
Escalate to the owning backend team if resets persist after rollback.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
