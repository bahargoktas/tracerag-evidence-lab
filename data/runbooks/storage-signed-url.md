# Presigned URL expiration failures

Document ID: storage-signed-url
Service: storage

## Symptoms
Clients report expired download links before completing transfers. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Compare signed URL expiry timestamps, client clock skew, and transfer duration distribution.

## Mitigation
Issue fresh short-lived signed URLs through the normal application flow and correct client-side refresh handling.

## Verification
Verify a download completes within the approved validity window without broadening bucket permissions.

## Escalation
Escalate to application engineering if client clocks remain inaccurate.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
