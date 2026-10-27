# Kafka consumer lag growth

Document ID: stream-consumer-lag
Service: stream

## Symptoms
Stream processing falls behind incoming events. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect partition lag, consumer group rebalances, processing duration, and partition skew.

## Mitigation
Scale consumers up to the partition count and address slow handlers without resetting offsets.

## Verification
Verify consumer lag declines consistently and processed event counts increase.

## Escalation
Escalate to streaming infrastructure if broker fetch latency is elevated.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
