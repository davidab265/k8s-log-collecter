# Security Policy

## Supported Versions

We actively support and release security fixes for the latest version on the `main` branch.

| Version              | Supported          |
| -------------------- | ------------------ |
| latest (`main`)      | :white_check_mark: |

---

## Reporting a Vulnerability

If you believe you have found a security vulnerability:

1. **Do NOT open a public GitHub issue.**
2. Report the vulnerability privately via **GitHub Private Vulnerability Reporting** on the repository:
   - Navigate to the repository's **Security** tab.
   - Click **Report a vulnerability**.

### What to Include in Your Report

To help us triage and resolve the issue quickly, please provide:

- A clear description of the vulnerability.
- Steps to reproduce or proof-of-concept code.
- Potential impact (e.g. log injection, credential exposure, excessive RBAC scope).
- Any proposed remediation, if you have one.

---

## What to Expect

- **Acknowledgment**: Within 48 hours of receipt.
- **Triage & Assessment**: Within 5 business days, including a severity estimate.
- **Fix & Disclosure**: We will collaborate on a coordinated disclosure timeline, typically 30–90 days, allowing users to update before public details are released.

---

## Deployment Security Notes

- The provided `rbac.yaml` grants **read-only** access to pods and pod logs within a single namespace. Do not widen the scope unless strictly necessary.
- `LOKI_URL` should point to a cluster-internal endpoint; avoid exposing the collector to external networks.
- Never commit real registry credentials, cluster endpoints, or secrets to this repository.
