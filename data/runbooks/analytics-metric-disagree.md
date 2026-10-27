# Metric definition discrepancy

Document ID: analytics-metric-disagree
Service: analytics

## Symptoms
Two dashboards report different active customer counts. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Compare metric grain, timezone boundaries, filters, and distinct-key definitions in the semantic layer.

## Mitigation
Align both dashboards to the approved metric definition and rebuild cached aggregates.

## Verification
Verify identical filter windows produce matching counts in both dashboards.

## Escalation
Escalate to analytics governance if metric ownership is disputed.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
