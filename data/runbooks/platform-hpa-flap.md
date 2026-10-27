# Horizontal pod autoscaler oscillation

Document ID: platform-hpa-flap
Service: platform

## Symptoms
Replica count rapidly increases and decreases under stable load. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Compare HPA metric sampling windows, target utilization, and stabilization policies.

## Mitigation
Restore approved HPA stabilization windows and remove noisy custom metric overrides.

## Verification
Verify replica count stabilizes while request latency remains within service objectives.

## Escalation
Escalate to capacity engineering if sustained demand exceeds limits.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
