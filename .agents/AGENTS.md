# Security Logging Copilot Plugin Rules

This workspace configures the Antigravity developer environment and guidelines for the Security Logging Copilot Plugin project.

## Agent Behavior & Workflow Guidelines

### Planning and Execution
- **Load SDD Context First**: At the start of any planning or execution task, read the following SDD documents before taking any action:
  - [`.specify/memory/constitution.md`](.specify/memory/constitution.md) — non-negotiable rules, architectural constraints, and behavior standards.
  - [`.specify/project-context.md`](.specify/project-context.md) — technology stack, directory layout, and deployment pipelines.
  - All relevant specifications under [`specs/`](specs/) for the area being changed.
- Always check the Workspace Customizations Root (`.agents/`) for project-scoped rules.
- Follow the planning workflow for any major changes, architectural designs, or complex refactorings.
- Maintain the task tracking document at `task.md` in the agent's conversation/brain artifacts during execution, updating task statuses (`[ ]`, `[/]`, `[x]`) as progress is made.
- Document implementation summaries in a `walkthrough.md` artifact after completion.

### Git Development Standards
- **Branch/Worktree Isolation**: Always isolate work off of a dedicated `feature/` or `bugfix/` branch, or via a git worktree. Do not commit major changes directly to main.
- **Branch Naming**: Use descriptive prefixes like `feature/`, `bugfix/`, `hotfix/`, `chore/` followed by a concise description (e.g., `feature/add-logging-middleware`).
- **Commit Frequency**: Always commit incrementally after completing any major sub-tasks or logical changes.
- **Commit Messages**: Use Conventional Commits formatting:
  - `<type>(<scope>): <short description>`
  - Types: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`.
  - Provide a detailed body in the commit message if the changes are complex.
- **Code Reviews**: Ensure all code changes are verified, documented, and have corresponding test updates.
- **Post-Merge Cleanup**: Always clean up and delete/prune the branch or git worktree locally and remotely after merging the changes back into the main branch.

## Coding & Security Guidelines

### Security Logging Best Practices
- **Data Protection**: Never log sensitive data such as:
  - Plaintext passwords or secrets
  - Credit card numbers / payment details
  - Personally Identifiable Information (PII) without hashing or masking
  - Auth tokens, session cookies, or API keys
- **Log Context**: Every security-relevant log entry must include:
  - Timestamp (ISO 8601 UTC format)
  - Event category (Authentication, Authorization, Data Access, Configuration Change)
  - Subject/Actor identifier (e.g., hashed user ID or session ID)
  - Action performed and Target resource
  - Outcome (Success/Failure/Error)
- **Error Handling**: Do not expose raw system stack traces in client-facing logs or messages. Log stack traces only in internal debug streams.
- **Immutability & Integrity**: Ensure logs are structured (e.g., JSON format) to ease ingestion and prevent log injection attacks (e.g., CRLF injection).

### TypeScript / JavaScript Standards (if applicable)
- Use strict TypeScript mode.
- Avoid the `any` type; use `unknown` or specific interfaces/types.
- Ensure proper async/await error handling with try/catch blocks.

## Custom Workspace Skills & Subagent Guidelines

### Spec Alignment & BDD Verification (Spec Alignment Subagent)
- When changes are proposed to features, ensure `specs/security-logging-plugin.spec.md` is updated.
- Before committing, invoke a subagent or use local scripts to check that every acceptance criterion has a matching Gherkin scenario in `specs/features/*.feature`.

### Plugin Quality & Standards Verification (QA & Validation Subagent)
- **Plugin Manifests**: Verify `plugin.json` and `marketplace.json` formatting.
- **Skill Compliance**: Use the `agentskills-frontmatter-enforcer` skill to verify that all new or modified `SKILL.md` files strictly comply with the `agentskills.io` standard (valid frontmatter, unique names, no files > 500 lines).
- **Execution Check**: Run the `plugin-validator` skill (`python3 security-logging-advisor/scripts/validate-plugin.py`) before staging or finalizing any changes.

### GitHub Integration & MCP
- Leverage the **`github-mcp-server`** when executing git standards, automating issues, searching other repositories for reference code, or drafting release PRs.
- For non-interactive tasks (like scanning for dependencies or issues), run tasks asynchronously in the background.

### Model Selection & Cost Balancing
- **Task-based Model Preference**: Match the active model's reasoning capabilities with the complexity of the current task to balance performance and token cost:
  - **Tier 1 (Architectural Reasoning & Synthesis)**: Use `Gemini 3.5 Pro`, `Claude 3.5 Sonnet`, or `GPT-5.5 Pro / GPT-4o`.
  - **Tier 2 (Repository Context Collection)**: Use `Gemini 3.5 Flash`, `Claude 3.5 Haiku / Sonnet`, or `GPT-4o-mini`.
  - **Tier 3 (Local Validation & Checking)**: Use `Gemini 1.5 Flash / Flash-8B`, `Claude 3.5 Haiku`, or `GPT-4o-mini`.
- **Model Toggling**: If executing heavy validation loops or large-scale file reads, prompt the user or toggle commands (such as `/model` or `/fast`) to run the workspace-skills on faster, lower-cost models.

### Clean Git Workspace Maintenance
- **Worktree Cleanup**: After completing git workflows (checkout, commit, merge, push), check for temporary or secondary worktrees using `git worktree list`.
- **Pruning**: Proactively remove any stale or unused local worktrees using `git worktree remove <path>` and delete the associated local branch using `git branch -d <branch_name>` (or `git branch -D` if fully verified and merged) to prevent workspace pollution.


