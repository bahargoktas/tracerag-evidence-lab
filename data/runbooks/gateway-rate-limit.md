# Unexpected gateway rate limiting

Document ID: gateway-rate-limit
Service: gateway

## Symptoms
Legitimate clients receive http 429 despite ordinary request volume. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Check token bucket policy version, client identity mapping, and rate limit counters by route.

## Mitigation
Restore the last approved token bucket quota for affected client tiers; do not disable global abuse controls.

## Verification
Verify 429 rates fall for affected clients while protective limits remain active.

## Escalation
Escalate to API governance if the client tier mapping is ambiguous.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
