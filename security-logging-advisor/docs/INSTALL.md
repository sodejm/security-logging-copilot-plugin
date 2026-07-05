# Installation Guide: Security Logging Advisor

This guide explains how to install and register the **Security Logging Advisor** plugin within your development environment.

## 1. Local Development Installation

For testing, you can load the plugin directly from your local filesystem.

### GitHub Copilot CLI / VS Code Copilot agent support

Load the plugin using your local manifest path:

```bash
gh copilot agent register --local-path ./security-logging-advisor
```

Verify that the agent is registered:

```bash
gh copilot agent list
```

### Claude Code / Claude-compatible workflows

Add the local plugin to your Claude Code workspace:

```bash
claude plugin add --path ./security-logging-advisor
```

---

## 2. Installation from Enterprise Marketplace

Once published to your internal enterprise marketplace, developers can install the plugin directly.

### GitHub Copilot CLI

```bash
gh copilot agent install enterprise-security-engineering/security-logging-advisor
```

### Claude Code

```bash
claude plugin install enterprise-security-engineering/security-logging-advisor
```

---

## 3. Verification

Verify the installation by running the validation or context commands:

```bash
# Validate that the plugin files are intact
python3 security-logging-advisor/scripts/validate-plugin.py

# Run a sample context collection on your active repository
python3 security-logging-advisor/skills/repository-context/scripts/collect-repository-context.py .
```
