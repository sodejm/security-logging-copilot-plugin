# Security Logging Copilot Plugin Rules

This workspace configures the Antigravity developer environment and guidelines for the Security Logging Copilot Plugin project.

## Agent Behavior & Workflow Guidelines

### Planning and Execution
- Always check the Workspace Customizations Root (`.agents/`) for project-scoped rules.
- Follow the planning workflow for any major changes, architectural designs, or complex refactorings.
- Maintain the task tracking document at `task.md` in the agent's conversation/brain artifacts during execution, updating task statuses (`[ ]`, `[/]`, `[x]`) as progress is made.
- Document implementation summaries in a `walkthrough.md` artifact after completion.

### Git Development Standards
- **Branch Naming**: Use descriptive prefixes like `feature/`, `bugfix/`, `hotfix/`, `chore/` followed by a concise description (e.g., `feature/add-logging-middleware`).
- **Commit Messages**: Use Conventional Commits formatting:
  - `<type>(<scope>): <short description>`
  - Types: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`.
  - Provide a detailed body in the commit message if the changes are complex.
- **Code Reviews**: Ensure all code changes are verified, documented, and have corresponding test updates.

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
