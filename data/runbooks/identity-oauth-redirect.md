# OAuth redirect mismatch

Document ID: identity-oauth-redirect
Service: identity

## Symptoms
Oauth sign-in fails with redirect_uri_mismatch after a release. The on-call team should identify the first affected deployment and affected region before making changes.

## Diagnosis
Compare the registered callback URI to the URI sent by the application, including scheme, host, path, and trailing slash.

## Mitigation
Update the application callback configuration to an already approved registered URI and redeploy the client settings.

## Verification
Complete a sign-in test using the exact production callback and confirm state validation succeeds.

## Escalation
Escalate to identity engineering before adding any new callback domain.

## Safety and scope
This runbook is a synthetic training example. Follow change-management approval and preserve audit records in production environments.
