# Security Logging Copilot Plugin

Welcome to the **Security Logging Copilot Plugin** repository. This plugin is designed to assist developers in writing secure, compliant, and structured logging statements directly within their development environments.

## Overview

Modern software development requires strict adherence to security and compliance standards (such as OWASP, GDPR, HIPAA, and PCI-DSS). This plugin provides real-time linting, suggestions, and auto-completion for security logging, ensuring sensitive data is never leaked and required audit contexts are always captured.

## Features

- **Sensitive Data Detection**: Identifies potential PII, credentials, and secrets in logging statements.
- **Log Context Validation**: Checks if logging statements contain necessary metadata (actor, action, outcome, timestamps).
- **CRLF Injection Prevention**: Lints for unsafe input concatenation in log messages.
- **Structured Log Formatting**: Promotes JSON or structured logging patterns.

## Getting Started

### Prerequisites

- Node.js (v18 or higher recommended)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/security-logging-copilot-plugin.git
   cd security-logging-copilot-plugin
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Spec-Driven Development (SDD)

This repository follows a strict **Spec-Driven Development** workflow driven by `spec-kit` and the Kaggle production-grade BDD guidelines to guide development:

- **Constitution**: Project rules, security policies, and standards are defined in [.specify/memory/constitution.md](.specify/memory/constitution.md).
- **Project Context**: The system layout and technologies are documented in [.specify/project-context.md](.specify/project-context.md).
- **Feature Specs**: High-level requirements are modeled as specifications inside [specs/security-logging-plugin.spec.md](specs/security-logging-plugin.spec.md).
- **Gherkin Features**: Specific, executable scenarios (Given/When/Then) are defined as BDD feature files under [specs/features/](specs/features/).

## Development and IDE Environment

This repository is optimized for development with the **Antigravity IDE** and **Antigravity 2.0** ecosystem.

- **Workspace Guidelines**: Project-specific rules and agent instructions are defined in [.agents/AGENTS.md](.agents/AGENTS.md).
- **Model Context Protocol (MCP)**: Any custom MCP tools or hooks will be configured in the `.agents/` folder.

## Authors

- **Justin Soderberg** - [sodejm](https://github.com/sodejm)

## License

This project is licensed under the **PolyForm Noncommercial License 1.0.0** - see the [LICENSE](LICENSE) file for details.

