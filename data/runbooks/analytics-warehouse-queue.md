# Warehouse query queue saturation

Document ID: analytics-warehouse-queue
Service: analytics

## Symptoms
Dashboard queries wait in a warehouse execution queue. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect queued query classes, concurrency slots, and long-running transformation jobs.

## Mitigation
Move nonurgent transformations to the scheduled batch window and restore workload management quotas.

## Verification
Verify interactive query queue time falls below sixty seconds and critical transformations complete.

## Escalation
Escalate to data platform capacity owners if saturation continues.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
