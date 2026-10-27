# Node disk pressure

Document ID: platform-node-disk
Service: platform

## Symptoms
Cluster nodes report diskpressure and evict workloads. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect ephemeral storage usage, container log rotation, and image cache growth.

## Mitigation
Restore log rotation and reclaim approved disposable cache data; avoid deleting persistent volumes.

## Verification
Verify DiskPressure clears and eviction events stop on affected nodes.

## Escalation
Escalate to cluster operations if disk usage remains above threshold.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
