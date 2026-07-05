# Troubleshooting Guide: Security Logging Advisor

This document provides quick fixes and debugging steps for common issues encountered when installing, updating, or running the **Security Logging Advisor** plugin.

## 1. Scanner Fails to Execute
**Symptom**: Running the scan produces permission errors or python interpreter execution failures.
- **Fix**: Check that python3 is installed and ensure files are marked executable:
  ```bash
  python3 --version
  chmod +x security-logging-advisor/skills/repository-context/scripts/collect-repository-context.py
  ```
- **Symptom**: Large codebase triggers memory pressure or long execution times.
  - **Fix**: Verify that standard directories like `node_modules/`, `.git/`, `venv/`, and build artifacts are excluded in the `collect-repository-context.py` script. You can manually test exclusions by running:
    ```bash
    python3 security-logging-advisor/skills/repository-context/scripts/collect-repository-context.py ./your-repo
    ```

## 2. Manifest/Marketplace Discovery Errors
**Symptom**: `@security-logging-advisor` does not appear in VS Code Copilot agent panel or CLI.
- **Fix 1**: Ensure you have successfully registered the agent locally:
  ```bash
  gh copilot agent register --local-path ./security-logging-advisor
  ```
- **Fix 2**: For enterprise rollout issues, verify that `copilot/managed-settings.json` is placed in the main branch of the `.github-private` repository and matches standard JSON syntax. Run validation:
  ```bash
  python3 security-logging-advisor/scripts/validate-plugin.py
  ```

## 3. Empty or Truncated Output Reports
**Symptom**: Generated report `docs/security/logging-recommendations.md` is empty or missing data.
- **Fix**: Ensure that the target directory has read permissions and that your shell has permission to write files under `docs/security/`. Create the directory manually if necessary:
  ```bash
  mkdir -p docs/security
  ```
