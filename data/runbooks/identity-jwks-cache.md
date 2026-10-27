# JWKS key rotation cache issue

Document ID: identity-jwks-cache
Service: identity

## Symptoms
Valid access tokens fail signature validation after key rotation. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Compare token kid values with the published JWKS and inspect verifier cache age across instances.

## Mitigation
Refresh the JWKS cache through the supported cache invalidation mechanism; retain signature verification.

## Verification
Verify new and still-valid old tokens pass signature checks under the documented rotation overlap.

## Escalation
Escalate to identity security if a signing key is missing from the issuer.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
