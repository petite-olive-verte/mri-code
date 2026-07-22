---
name: mri-code-finish
model: sonnet
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
disable-model-invocation: true
---

# mri-code-finish — finish a development branch

> ┌─ mri devtools ─┐

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Detect environment → **Reconcile docs with what shipped** → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using mri-code-finish to complete this work."

## The Process

### Step 1: Verify Tests

**Before presenting options, verify tests pass** (apply `mri-code-verify` — evidence before any "done" claim):

```bash
uv run pytest
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 2.

### Step 2: Detect Environment

**Determine workspace state before presenting options:**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

This determines which menu to show and how cleanup works:

| State | Menu | Cleanup |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` (normal repo) | Standard 4 options | No worktree to clean up |
| `GIT_DIR != GIT_COMMON`, named branch | Standard 4 options | Provenance-based (see Step 6) |
| `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 3 options (no merge) | No cleanup (externally managed) |

**Also detect an originating GitHub issue.** If the journey was started by `/mri-code-issue`, the
`## Source` block in `.mri_code/docs/<project>/progress.md` carries the issue number, URL and
suggested branch. Read it now: if present, the PR path (Option 2) links and closes the issue, and a
new branch is named after it.

### Step 3: Determine Base Branch

**Integrate into the project's integration branch, not a hardcoded `main`.** Many teams use a
git-flow `develop` branch (features → `develop`; only releases → `main`). Resolve the target in this
order and **respect it for both the local merge (Option 1) and the PR base (Option 2)**:

1. The **constitution** — if `.mri_code/constitution.md` states a branch strategy (e.g. "integrate
   through `develop`"), that wins.
2. The repo's **default branch**: `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`
   (GitHub default is what a PR targets; teams set it to `develop`).
3. Fallback: `develop` if it exists (`git rev-parse --verify develop`), else `main`/`master`.

```bash
BASE=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null \
       || (git rev-parse --verify -q develop >/dev/null && echo develop) || echo main)
git merge-base HEAD "origin/$BASE" 2>/dev/null
```

Confirm with the user if unsure: "This branch integrates into `<BASE>` — correct?" **Never open the
PR or merge into `main` when the project integrates through `develop`.**

### Step 3.5: Reconcile documentation with what shipped

**Before integrating, make the docs tell the truth about what was actually built.** Implementations
drift from the design — new dependencies, revised decisions, pinned versions, moved structure,
adjusted acceptance criteria, gotchas found. Close that loop now so nothing ships stale.

1. **Find the divergences.** Compare the delivered change against:
   - the **design** — `spec.md`, or (issue-driven) the issue's `## Technical design (mri-code)` section;
   - the **plan** — `plan.md`;
   - the **in-repo, code-coupled docs** — README, service ADRs, OpenAPI (see `AGENTS.md` → *Documentation*).

   List what actually changed vs. what was planned (deps added/removed, decisions revised, versions,
   layout moves, acceptance-criteria tweaks). **If nothing diverged, say so and skip to Step 4** — do
   not manufacture doc churn.

2. **Update the design to as-built** (only what diverged):
   - Idea-driven → edit `spec.md` (and `plan.md` if the task shape changed).
   - Issue-driven → add/adjust a short **"As-built / divergences"** note in the issue's
     `## Technical design (mri-code)` section. This is an **outward write — show the diff and get user
     approval** before `gh issue edit`.

3. **Update the in-repo code-coupled docs** (README etc.) if the change altered setup or behavior and
   they drifted — and **commit them on this branch now**, so they integrate *with* the change (Step 5),
   not as a forgotten afterthought.

4. **If issue-driven, re-check the acceptance criteria** on the issue: tick the boxes the work now
   satisfies (`gh issue edit` / a comment), so the issue reflects reality.

5. **Record it** in `progress.md`: a one-line `as-built:` summary of the divergences (or "matched the
   design").

Cross-cutting / product docs that diverged are **not** handled here — they go to the separate doc repo
via `/mri-code-document-sync` (suggested after the merge, below).

### Step 4: Present Options

**Normal repo and named-branch worktree — present exactly these 4 options:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Detached HEAD — present exactly these 3 options:**

```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)
3. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 5: Execute Choice

#### Option 1: Merge Locally

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify tests on merged result
<test command>

# Only after merge succeeds: cleanup worktree (Step 6), then delete branch
```

Then: Cleanup worktree (Step 6), then delete branch:

```bash
git branch -d <feature-branch>
```

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>
```

**Issue-linked work (journey started by `/mri-code-issue`).** When a `## Source` block was detected
in Step 2, the PR was usually **already opened by `/mri-code-review`** (PR review mode). Reuse it —
do not create a duplicate:

```bash
gh pr view --json url,state -q .url 2>/dev/null || gh pr create --base "$BASE" --title "<title>" --body "<summary>

Closes #<number>"
```

The PR body carries `Closes #<number>`, so **merging it closes the issue automatically** — and in the
issue flow the merge typically happens **on GitHub**, after the user has accepted the review
suggestions. Only merge here (`gh pr merge`) if the user explicitly asks. If the branch was created
only at finish time (detached HEAD), name it after the issue's suggested branch
(`issue-<number>-<slug>`) before pushing. If there is no originating issue, create the PR normally
(`gh pr create` or the platform's PR flow) with no `Closes` line.

**Do NOT clean up worktree** — user needs it alive to iterate on PR feedback.

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

Then: Cleanup worktree (Step 6), then force-delete branch:
```bash
git branch -D <feature-branch>
```

### Step 6: Cleanup Workspace

**Only runs for Options 1 and 4.** Options 2 and 3 always preserve the worktree.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

**If `GIT_DIR == GIT_COMMON`:** Normal repo, no worktree to clean up. Done.

**If worktree path is under `.worktrees/` or `worktrees/`:** the mri worktree flow created this worktree — we own cleanup.

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```

**Otherwise:** The host environment (harness) owns this workspace. Do NOT remove it. If your platform provides a workspace-exit tool, use it. Otherwise, leave the workspace in place.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | yes | - | - | yes |
| 2. Create PR | - | yes | yes | - |
| 3. Keep as-is | - | - | yes | - |
| 4. Discard | - | - | - | yes (force) |

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" is ambiguous
- **Fix:** Present exactly 4 structured options (or 3 for detached HEAD)

**Cleaning up worktree for Option 2**
- **Problem:** Remove worktree user needs for PR iteration
- **Fix:** Only cleanup for Options 1 and 4

**Deleting branch before removing worktree**
- **Problem:** `git branch -d` fails because worktree still references the branch
- **Fix:** Merge first, remove worktree, then delete branch

**Running git worktree remove from inside the worktree**
- **Problem:** Command fails silently when CWD is inside the worktree being removed
- **Fix:** Always `cd` to main repo root before `git worktree remove`

**Cleaning up harness-owned worktrees**
- **Problem:** Removing a worktree the harness created causes phantom state
- **Fix:** Only clean up worktrees under `.worktrees/` or `worktrees/`

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request
- Remove a worktree before confirming merge success
- Clean up worktrees you didn't create (provenance check)
- Run `git worktree remove` from inside the worktree

**Always:**
- Verify tests before offering options
- Detect environment before presenting menu
- Present exactly 4 options (or 3 for detached HEAD)
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only
- `cd` to main repo root before worktree removal
- Run `git worktree prune` after removal

## After a successful merge — keep the docs current
Once the work is **merged** (Option 1 locally, or the PR merged on GitHub in the issue flow),
**suggest `/mri-code-document-sync`** (suggested model: **Sonnet**) to update the project's separate
documentation repo so it stays in sync with the change. Do not launch it yourself. Skip the
suggestion for Options 3 (keep as-is) and 4 (discard) — nothing was integrated.

## Tracking (progress.md)
At the **start** of this step, mark it `[~]` in `.mri_code/docs/<project>/progress.md` (create the
file if missing — schema in the `/mri-code-resume` command). At the **end**, set it to `[x]`. This is the
**end of the code pipeline** — the work is integrated. After a merge, the only follow-up is
`/mri-code-document-sync` (docs), suggested above.

---
**User input:** $ARGUMENTS

💡 **Suggested model:** any — see `.mri_code/models.md`.
