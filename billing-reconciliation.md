# Ledger reconciliation discrepancy

Document ID: billing-reconciliation
Service: billing

## Symptoms
Ledger totals differ from settled transaction totals. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Compare settlement window boundaries, currency rounding rules, and missing transaction IDs.

## Mitigation
Pause downstream publication of the affected reconciliation batch and regenerate it using the approved settlement window.

## Verification
Verify batch-level debit and credit totals balance and sampled transaction IDs match settlement records.

## Escalation
Escalate to finance controls for unresolved monetary discrepancies.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
