# Model Selection & Runtime Routing Guidelines

This document details the recommended model selections and configurations for the **Security Logging Advisor** plugin across supported AI runtime environments. It serves as a guide to balance reasoning capabilities with computational cost.

---

## 1. Supported Model Families & Recommended Routing

To achieve the best results at the lowest token usage cost, we recommend routing specific tasks to specific model tiers within your chosen model family.

### Recommended Model Mapping

| Task Tier | Gemini Family | Claude Family | GPT-5.5/4 Family |
| :--- | :--- | :--- | :--- |
| **Tier 1: Architectural Reasoning**<br>*(Analyzing codebase logs, identifying logging gaps, generating pine/structlog config templates)* | **Gemini 3.5 Pro** | **Claude 3.5 Sonnet** | **GPT-5.5 Pro / GPT-4o** |
| **Tier 2: Static Context Collection**<br>*(Parsing workspace directories, aggregating files list, analyzing dependency imports)* | **Gemini 3.5 Flash** | **Claude 3.5 Haiku / Sonnet** | **GPT-4o-mini** |
| **Tier 3: Local Script Validation**<br>*(Verifying manifest syntax, validation loops, checking skill file frontmatters)* | **Gemini 1.5 Flash / Flash-8B** | **Claude 3.5 Haiku** | **GPT-4o-mini** |

---

## 2. Dynamic Runtime Environment Verification

AI workflows and local validation scripts can detect their active runtime host to adjust terminal outputs or output format styles.

### Python Detection Snippet

The following script detects the active CLI or IDE host. This can be run in workspace execution workflows:

```python
import os
import sys

def detect_runtime_environment():
    # 1. Claude Code Detection
    if os.environ.get("CLAUDE_CODE") == "1" or os.environ.get("TERM_PROGRAM") == "claude":
        return "Claude Code (CLI)"
    
    # 2. Antigravity TUI/CLI Detection
    if os.environ.get("ANTIGRAVITY") == "1" or os.environ.get("AGY_TUI") == "1":
        return "Google Antigravity"
    
    # 3. GitHub Copilot / VS Code Detection
    if any(k in os.environ for k in ["VSCODE_IPC_HOOK_CLI", "VSCODE_GIT_IPC_HANDLE", "CODESPACES"]):
        return "GitHub Copilot (VS Code)"
    
    return "Standard Shell / Unknown"

if __name__ == "__main__":
    env = detect_runtime_environment()
    print(f"Active Runtime Environment: {env}")
```

---

## 3. Host Platform Configuration Guide

Because Copilot, Claude Code, and Antigravity plugin specifications (`plugin.json`) do not support baking dynamic model-switching directly into the plugin configuration, developers must set their preferred models at the client/session level:

### A. Google Antigravity
*   **TUI Toggle**: Run `/model` inside the Antigravity CLI and select from the list of models (e.g., `gemini-3.5-pro`).
*   **File Config**: Edit `~/.gemini/antigravity-cli/settings.json` and set the `"model"` key:
    ```json
    {
      "model": "gemini-3.5-pro"
    }
    ```
*   **Native Auto-Routing**: Antigravity automatically routes lighter tasks (like background indexing or UI status generation) to Flash models, preserving Pro quotas.

### B. Claude Code
*   **CLI Start Flag**: Start a Claude Code session with the model explicitly set to balance costs:
    ```bash
    claude --model claude-3-5-haiku-latest
    ```
*   **Session Switching**: Within the Claude Code CLI, type `/model` followed by the model name to switch to `claude-3-5-sonnet-latest` for architectural tasks.

### C. GitHub Copilot
*   **Chat Dropdown**: Use the dropdown model selector in the Copilot Chat window in VS Code to switch between GPT-4o, Claude 3.5 Sonnet, and GPT-4o-mini depending on whether you are doing high-level security architecture reviews or basic code formatting.
