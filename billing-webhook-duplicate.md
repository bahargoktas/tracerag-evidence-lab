# Duplicate billing webhooks

Document ID: billing-webhook-duplicate
Service: billing

## Symptoms
Downstream invoices are created twice for a single billing event. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect event IDs and idempotency-key persistence; compare delivery attempts with invoice creation records.

## Mitigation
Replay only events that have no successful idempotency record after restoring the idempotency store.

## Verification
Confirm each event ID maps to one invoice and duplicate deliveries produce no additional records.

## Escalation
Escalate to billing operations for any affected customer ledger.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
