# Gateway tail latency regression

Document ID: gateway-tail-latency
Service: gateway

## Symptoms
P99 response latency rises while median latency remains flat. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Compare p99 by route and region, inspect connection pool wait time, and check retry amplification.

## Mitigation
Reduce retry attempts to the approved baseline and restore connection pool limits from the last known good configuration.

## Verification
Verify p99 returns below 800 milliseconds and retry volume normalizes for twenty minutes.

## Escalation
Escalate to platform networking if pool waits stay elevated.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
