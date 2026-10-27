# TLS certificate expiry warning

Document ID: gateway-tls-expiry
Service: gateway

## Symptoms
Edge certificates approach expiration or handshakes fail. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Inspect certificate notAfter dates and the certificate chain served at the edge; confirm renewal job status.

## Mitigation
Renew the certificate through the managed certificate workflow and deploy the updated chain to all edge regions.

## Verification
Check handshake success from two regions and verify the new certificate expiration date.

## Escalation
Escalate to security operations if the issuer rejects renewal.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
