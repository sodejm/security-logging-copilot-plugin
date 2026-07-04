# Maintainer Guidelines: Security Logging Advisor

This guide outlines code review standards, release procedures, and lifecycle policies for maintainers of the **Security Logging Advisor** plugin.

## 1. Code Review Checklist
Before approving Pull Requests (PRs) or changes to this repository, verify that:
- [ ] No hardcoded secrets, credentials, or personal keys are introduced in example files or mock configurations.
- [ ] Any script modifications in `scripts/` are checked for cross-platform compatibility (macOS, Linux, and Windows/PowerShell via Python).
- [ ] New dependencies are added to the validation scripts if necessary.
- [ ] The validation script passes successfully:
  ```bash
  python3 security-logging-advisor/scripts/validate-plugin.py
  ```

## 2. Release & Versioning Policy
This plugin follows [Semantic Versioning 2.0.0](https://semver.org/).

1. **Changelog**: Add entry to [CHANGELOG.md](file:///Users/justinsoderberg/Development/security-logging-copilot-plugin/security-logging-advisor/CHANGELOG.md).
2. **Version Bump**: Increment version in:
   - `security-logging-advisor/plugin.json`
   - `.github/plugin/marketplace.json`
   - `.claude-plugin/marketplace.json`
3. **Release Tag**: Create a git release tag corresponding to the version (e.g. `v1.0.0`):
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

## 3. Marketplace Sync Pipeline
On tag creation, the enterprise CI/CD workflow:
1. Installs clean Python dependencies and runs tests.
2. Executes `validate-plugin.py`.
3. Auto-registers the new version with the enterprise GitHub private marketplace registry by copying files into the registry root database.
