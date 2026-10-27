# Kubernetes CrashLoopBackOff

Document ID: platform-crashloop
Service: platform

## Symptoms
Pods restart repeatedly shortly after a new deployment. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect previous container logs, exit codes, readiness probe failures, and recently changed environment variables.

## Mitigation
Roll back the deployment if a new configuration caused the crashes; repair the failing dependency before redeploying.

## Verification
Verify restart counts stop increasing and readiness probes pass across all replicas.

## Escalation
Escalate to service owners if the container exits without useful logs.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
