---
name: mri-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
disable-model-invocation: true
---

# mri-code-review — request a code review

> ┌─ mri devtools ─┐

Dispatch a code reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history. This keeps the reviewer focused on the work product, not your thought process, and preserves your own context for continued work.

**Core principle:** Review early, review often.

## Two modes (pick by reading `progress.md`)
- **Per-task review — inside `mri-code-implement`.** Local, fast: the reviewer looks at the last
  task's diff and **you fix issues immediately** before the next task. This is the default flow
  described in the sections below. Unchanged.
- **PR review gate — issue-driven journeys, before finish.** When `progress.md` has a `## Source`
  block (started by `/mri-code-issue`), the pipeline's review step runs **on the GitHub Pull
  Request** and posts its findings **as PR review comments, like a human reviewer** — concrete fixes
  as GitHub `suggestion` blocks you can accept in one click. It does **not** auto-fix: you review on
  GitHub and accept/reject. See **[PR review mode](#pr-review-mode-issue-driven)** below.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code reviewer subagent:**

Dispatch a `general-purpose` subagent, filling the template at [code-reviewer.md](code-reviewer.md)

**Placeholders:**
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit

**3. Act on feedback** (per-task mode — for the PR gate, see [PR review mode](#pr-review-mode-issue-driven) instead):
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from .mri_code/docs/<project>/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## PR review mode (issue-driven)

Use this instead of "Act on feedback → fix" when `progress.md` has a `## Source` block. The review
lands **on the PR**; you post comments like a human reviewer and **change nothing locally** — the
user accepts or rejects the suggestions on GitHub.

**1. Ensure the PR exists.** The review happens on a PR, so open one if needed (linked to the issue):

```bash
BRANCH=$(git branch --show-current)
gh pr view --json number >/dev/null 2>&1 || {
  git push -u origin "$BRANCH"
  gh pr create --fill --body "Closes #<N>"   # <N> from progress.md ## Source
}
PR=$(gh pr view --json number -q .number)
BASE_SHA=$(git merge-base origin/HEAD HEAD 2>/dev/null || git rev-parse origin/main)
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch the reviewer** exactly as below (the `code-reviewer.md` template), over
`BASE_SHA..HEAD_SHA` — the PR's diff. Ask it to include a **`Suggested change`** block (exact
replacement lines) for every issue that is a concrete single-hunk fix, with a precise `file:line`.

**3. Post the review on the PR — do NOT edit any file.** Turn the reviewer's findings into one PR
review: a summary body (Strengths + Assessment) plus one **inline comment per issue**. For issues
that carry a `Suggested change`, wrap it in a GitHub suggestion block so the user can accept it with
one click:

````markdown
<why this matters, 1-2 lines>

```suggestion
<exact replacement lines for the commented range>
```
````

Build the review as a JSON payload and submit it in a single call (inline comments need the API, not
`gh pr comment`):

```bash
# review.json: { "event": "...", "body": "<summary>", "comments": [ {"path","line","side":"RIGHT","body"}, ... ] }
gh api --method POST "repos/{owner}/{repo}/pulls/$PR/reviews" --input review.json
```

- **Event:** `REQUEST_CHANGES` if there is any Critical/Important issue, else `APPROVE`; use
  `COMMENT` for a pure FYI. This mirrors a human reviewer's verdict.
- **Anchoring:** a `suggestion` block only works when the comment is anchored to the exact lines it
  replaces. For broader findings (architecture, missing tests) post a plain inline or summary comment
  with no suggestion.
- Findings outside the diff → mention them in the summary body, not as inline comments.

**4. Hand back to the user — stop here.** Report: "Review posted on PR #<N> (<url>): <k> suggestions,
verdict <event>. Review them on GitHub and accept/reject; nothing was changed locally." Do **not**
apply fixes, merge, or proceed. Next step after the user has handled the PR → **`/mri-code-finish`**
(or merge on GitHub, which closes the issue via `Closes #<N>`).

## Integration with the flow

**During `mri-code-implement`:**
- Review after EACH task (this is the per-task review `mri-code-implement` dispatches)
- Catch issues before they compound; fix before moving to the next task

**Ad-hoc:**
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback
- **In PR review mode:** edit files, merge, or "fix and push" — post comments/suggestions only and
  let the human accept or reject on GitHub

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: [code-reviewer.md](code-reviewer.md)

## Tracking (progress.md)
At the **start** of this step, mark it `[~]` in `.mri_code/docs/<project>/progress.md` (create the
file if missing — schema in the `/mri-code-resume` command). At the **end**, set it to `[x]` and suggest
**`/mri-code-finish`** (suggested model: any — mechanical). In **PR review mode**, record the outcome as
`[x] → review on PR #<N> (<k> comments, <event>)` and leave it there — the human acts on GitHub next.

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Sonnet (or Opus for a demanding review) — see `.mri_code/models.md`.
