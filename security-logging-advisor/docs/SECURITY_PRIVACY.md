# Security and Privacy Policy: Security Logging Advisor

This policy details the security boundaries, data handling protocols, and privacy features designed into the **Security Logging Advisor** plugin to safeguard your source code and telemetry data.

## 1. Local-First Processing

- **Static Analysis**: All repository scanning and signature matching (e.g. executed by `collect-repository-context.py`) occurs entirely on the developer's local machine.
- **Network Boundaries**: The plugin does not transmit code snippets, file contents, or database connection strings to external APIs or unauthorized third-party servers.

## 2. Secrets Handling & Integrity Safeguards

- **Zero Exposure Policy**: If the repository scanner detects credentials, access keys, or private key patterns, it reports the **location** (file path and line number) and remediation steps. It **never** extracts, stores, or includes the raw secret value in the output JSON context or markdown reports.
- **Remediation Over Leakage**: Findings only log metadata, e.g.:
  `[WARN] Potential AWS Access Key ID detected in file: config/production.js on line: 12`

## 3. Telemetry and Data Minimization

- **Strict Redaction**: Recommendations always advise using structured logging with configured redaction keys (such as `password`, `ssn`, `creditCard`, `authorization` headers).
- **Environment Calibration**: Telemetry targets minimal logging in Sandboxes and Development environments to control log storage costs and minimize the footprint of user data outside of production.
- **Correlation Context**: The advisor recommends using correlation/request IDs rather than raw user identities or email addresses to preserve individual privacy while maintaining system trace capabilities.
