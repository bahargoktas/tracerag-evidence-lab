# Unassigned search shards

Document ID: search-shard-unassigned
Service: search

## Symptoms
Search cluster reports unassigned shards and reduced redundancy. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect allocation explain output, disk watermarks, and node availability.

## Mitigation
Free disk through approved retention cleanup or restore missing nodes, then allow normal shard allocation.

## Verification
Verify all required primary shards are assigned and replica allocation progresses.

## Escalation
Escalate to search infrastructure if allocation explain still reports a hard constraint.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
