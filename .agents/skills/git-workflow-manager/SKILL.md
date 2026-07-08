---
name: git-workflow-manager
description: Manage Git branching (using feature/bugfix branches or worktrees), committing changes, merging, pushing, and branch cleanup.
---

# Git Workflow Manager Skill

This skill outlines the standard commands and procedures for managing the repository's git workflow, ensuring code changes are made in isolation, committed incrementally, merged safely, and cleaned up cleanly.

## 1. Branching & Worktree Isolation

Before starting any major design changes or code modifications, isolate the work:

### Option A: Feature/Bugfix Branches (Standard)
Create and switch to a descriptive branch from the target branch (usually `main`):
```bash
git checkout -b <prefix>/<short-description>
```
*Prefixes*: `feature/`, `bugfix/`, `hotfix/`, `chore/`, `test/`, `docs/`, `refactor/`.

### Option B: Git Worktrees (Advanced/Concurrent tasks)
To work in a clean, separate directory without altering your current directory state:
```bash
git worktree add ../<branch-name-or-directory> -b <prefix>/<short-description>
```

---

## 2. Commit After Major Changes

Commit changes after completing major sub-tasks or logical blocks. Ensure the working directory is clean of unnecessary temp files.

### Conventional Commits Format
```text
<type>(<scope>): <short description>

[Optional body detailing the changes and reason/context]
```
*Types*: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`.

Commit command:
```bash
git add .
git commit -m "<type>(<scope>): <short description>"
```

---

## 3. Merge and Push

Once changes are verified and tests pass:

1. Switch back to the main integration branch:
   ```bash
   git checkout main
   ```
2. Pull the latest remote changes:
   ```bash
   git pull origin main
   ```
3. Merge the feature branch into main:
   ```bash
   git merge <branch-name>
   ```
4. Push the merged commits to remote:
   ```bash
   git push origin main
   ```

---

## 4. Post-Merge Cleanup

Proactively prune branches and worktrees to keep the workspace clean.

### Delete local and remote feature branches:
```bash
git branch -d <branch-name>
git push origin --delete <branch-name>
```

### Remove Git Worktrees:
```bash
git worktree remove ../<worktree-directory>
```
If a branch was tied to the worktree, delete the branch as well.
