# Enterprise Rollout Guide: Security Logging Advisor

This guide outlines the steps required for enterprise platform owners to deploy the **Security Logging Advisor** plugin globally across the organization (approx. 2,000 developers).

## 1. Global Enterprise Configuration

In an enterprise GitHub organization, default plugins can be configured centrally by creating or updating files in the global `.github-private` management repository.

### Configuration file: `copilot/managed-settings.json`

To automatically configure or suggest the plugin to all developers, append the plugin metadata to `copilot/managed-settings.json` in your organization's `.github-private` repo.

```json
{
  "enterprise_settings": {
    "copilot": {
      "plugins": {
        "allowed_plugins": [
          "enterprise-security-engineering/security-logging-advisor"
        ],
        "default_enabled_plugins": [
          "enterprise-security-engineering/security-logging-advisor"
        ],
        "marketplace_source": "internal-github-marketplace"
      }
    }
  }
}
```

## 2. Release & Registration Pipeline

1. **Repository Push**: Publish code changes to the internal repository `https://github.com/internal-enterprise/security-logging-copilot-plugin`.
2. **Release Hook**: The repository's CI pipeline triggers on new git tags (e.g. `v1.0.0`) and executes:

   ```bash
   python3 security-logging-advisor/scripts/validate-plugin.py
   ```

3. **Marketplace Publishing**: If validation passes, the CI commits/publishes the metadata in `.github/plugin/marketplace.json` to the internal GitHub enterprise marketplace registrar.

## 3. Communication and Adoption

- **Automatic Enablement**: Because of the `default_enabled_plugins` directive, developers will automatically see the `@security-logging-advisor` agent in their VS Code/GitHub Copilot chats and Copilot CLI.
- **Repository Onboarding**: Encourage teams to run the logging advisor on their repositories to generate baseline checklists:

  ```bash
  gh copilot run @security-logging-advisor "analyze this repository"
  ```
