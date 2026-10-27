# Tax configuration rollout anomaly

Document ID: billing-tax-rollout
Service: billing

## Symptoms
Tax calculation differs between two deployment regions. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Compare active tax ruleset version, effective date, and region mapping for affected transactions.

## Mitigation
Roll back the inconsistent ruleset version through the controlled configuration release.

## Verification
Verify the same synthetic test invoice yields the same tax result in both regions.

## Escalation
Escalate to the tax compliance owner before changing tax rules.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
