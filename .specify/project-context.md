# Project Context: Security Logging Advisor

This document provides a feature-complete snapshot of the repository context to guide AI agents in understanding the codebase structure, technologies, and boundaries.

---

## 1. Technology Stack and Ecosystem

- **Ecosystem**: GitHub Copilot plugin and agent package, with cross-compatibility for Claude Code workflows.
- **Programming Languages**:
  - **Python (v3.x)**: Used for deterministic repository static scanning and pre-release plugin validation scripts.
  - **HCL (Terraform)**: (Noted in workspace files).
  - **Markdown / JSON**: Used for configuration, agent instructions, templates, and specifications.
- **Framework Specifications**:
  - GitHub Copilot plugin manifest rules (`plugin.json`, `marketplace.json`).
  - Spec-kit driven development structure (located under `.specify/`).

---

## 2. Directory Layout & Key Files

```text
/
├── .github/
│   └── plugin/
│       └── marketplace.json       # GitHub Copilot marketplace metadata
├── .claude-plugin/
│   └── marketplace.json           # Claude plugin metadata
├── .specify/
│   └── memory/
│       └── constitution.md        # Non-negotiable repository rules
├── specs/
│   └── security-logging-plugin.spec.md # Feature specification for the plugin
├── security-logging-advisor/
│   ├── plugin.json                # Plugin definition manifest
│   ├── CHANGELOG.md               # Version log history
│   ├── agents/
│   │   └── security-logging-advisor.agent.md # Core agent system prompt
│   ├── docs/                      # User, Maintainer, Rollout guides
│   │   ├── INSTALL.md
│   │   ├── ENTERPRISE_ROLLOUT.md
│   │   ├── SECURITY_PRIVACY.md
│   │   ├── TROUBLESHOOTING.md
│   │   ├── MAINTAINERS.md
│   │   └── architecture.md
│   ├── examples/                  # Logger configurations (Pino, Structlog)
│   ├── scripts/                   # Scan and validation utilities
│   │   ├── collect-repository-context.py
│   │   └── validate-plugin.py
│   ├── skills/                    # Modular agent capabilities
│   │   ├── repository-context/
│   │   │   └── SKILL.md
│   │   └── logging-recommendations/
│   │       └── SKILL.md
│   └── templates/                 # Output context and recommendations layouts
│       ├── logging-recommendations.md
│       └── repository-context.md
├── LICENSE                        # PolyForm Noncommercial 1.0.0 license
├── README.md                      # General introduction
└── .gitignore                     # Git tracking exclusions
```

---

## 3. Deployment & Validation Pipelines

- **Local Execution**: The plugin runs locally on developer workstations using standard Python 3.
- **Code Validation**:
  - Run the validator script to verify plugin manifest formatting, skill markdown frontmatter properties, and file structures:
    ```bash
    python3 security-logging-advisor/scripts/validate-plugin.py
    ```
- **Context Collection**:
  - Run the scanner script to analyze project languages and frameworks:
    ```bash
    python3 security-logging-advisor/scripts/collect-repository-context.py .
    ```
