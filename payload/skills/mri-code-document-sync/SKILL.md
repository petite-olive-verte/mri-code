---
name: mri-code-document-sync
model: sonnet
description: >-
  After work is merged, keep the project's SEPARATE documentation repo up to date: figure out what
  user-facing behavior changed, edit the matching docs in the doc repo, and open a PR there. On-demand,
  suggested by /mri-code-finish once the code is merged. Invoked by /mri-code-document-sync.
disable-model-invocation: true
---

# mri-code-document-sync — keep the doc repo up to date after a merge

> ┌─ mri devtools ─┐

**Goal:** once a change is merged, reflect it in the project's **separate documentation repository**
so the docs stay current — without hand-holding. This edits **another GitHub repo** (the doc repo),
not the code repo, and opens a PR there for you to accept (same spirit as `/mri-code-review`:
propose, don't force).

**Scope — cross-cutting / product docs only.** This step handles the docs that live in the *separate*
repo: system architecture spanning services, the shared API reference other repos consume,
product/user guides, onboarding, glossary. **Code-coupled docs** (README, setup/run, service ADRs,
OpenAPI/schema generated from code) are **not** this step's job — they belong *in the code PR* and
should already be updated by `mri-code-implement`/`mri-code-review`. See `AGENTS.md` → *Documentation*.

**Announce at start:** "I'm using mri-code-document-sync to update the documentation repo."

Communicate in the configured language; write docs in the doc repo's own language/style (match what
is already there), falling back to the configured document language (see `AGENTS.md`).

## Access
Uses the **`gh` CLI** (already authenticated). Verify first:

```bash
gh auth status
```

## Step 1 — Locate the doc repo (configured once, then reused)
The target doc repo is remembered in **`.mri_code/document-sync.md`**.

- **If it exists**, read it: it holds the doc repo (GitHub `owner/name` or URL, or a local path) and
  any mapping notes (which part of the docs this project maps to).
- **If it is missing or empty**, ask the user **once**: *"Which repo holds this project's
  documentation?"* (accept an `owner/name`, a full URL, or a local path). Optionally ask which
  section/folder of the docs this project maps to. Then **persist** it:

  ```markdown
  # Documentation sync target
  - **Doc repo:** <owner/name | url | /local/path>
  - **Maps to:** <folder/section in the doc repo, if any>
  - **Style notes:** <tone, format, changelog conventions observed>
  ```

  Subsequent runs reuse this file — no need to ask again (edit it to change the target).

## Step 2 — Determine what changed, and split code-coupled vs cross-cutting
Work out what merged and what it means for the docs — **behavior, not internals**.

- If this journey has a `## Source` block in `progress.md` (issue-driven), start from it: the issue
  `#N` and its merged PR. `gh pr view <N> --json title,body,mergeCommit,files` and
  `gh pr diff <N>` describe the change.
- Otherwise, use the merge itself: `git log --oneline <base>..HEAD` / `git diff <base>..HEAD` since
  the last doc sync.
- **Distill** the change into what a *reader of the docs* must now know: new/changed features, new
  flags or config, changed defaults, new commands, API/behavior changes, removed things. **Skip pure
  refactors, internal renames, test-only changes** — they do not touch the docs.
- **Split the doc impact by coupling** (see `AGENTS.md` → *Documentation*):
  - **Cross-cutting / product** (architecture, shared API reference, product/user guides,
    onboarding) → this is what you sync to the doc repo below.
  - **Code-coupled** (README, service ADR, OpenAPI/schema) → should already be in the merged code
    PR. If you notice it was **missed** there, don't edit the doc repo for it — **flag it** so the
    user fixes it in the code repo (a follow-up PR/commit), and leave it out of the doc PR.

If nothing **cross-cutting** changed, say so and stop — an empty doc PR is noise. (Missed
code-coupled docs are reported, not synced here.)

## Step 3 — Check out the doc repo
Work on an isolated copy of the doc repo (never the code repo's tree):

```bash
# Remote repo → clone into scratch; local path → use it directly and create a branch there
gh repo clone <owner/name> /tmp/doc-sync-<repo> 2>/dev/null || true
cd /tmp/doc-sync-<repo>
git checkout -b docs/<code-repo>-<issue-or-topic>
```

## Step 4 — Map the change to the docs and edit
Explore the doc repo's structure (its `README`, nav/index, folders) and find the pages the change
touches. Then edit them:

- Update the affected pages so they describe the **new** behavior — no stale instructions left.
- Follow the doc repo's existing structure, tone and formatting (this is someone else's repo — match
  it, don't restructure it).
- If there is a `CHANGELOG`/release notes, add an entry referencing the source (`<owner/repo>#<N>`).
- Only touch what the change requires. No unrelated doc rewrites.

## Step 5 — Open a PR on the doc repo (don't merge)
Commit and open a PR **in the doc repo**, linking back to the source so the trail is clear:

```bash
git add -A
git commit -m "docs: <concise change> (<code-repo>#<N>)"
git push -u origin docs/<code-repo>-<issue-or-topic>
gh pr create --title "docs: <concise change>" \
  --body "Documents <owner/code-repo>#<N>.

<1-3 lines: what changed for readers>"
```

Leave it for the user to review and merge — the doc repo is theirs to accept. Do **not** auto-merge
unless the user explicitly asks. If the target is a **local path** with no remote, commit on the
branch and report it instead of pushing.

## Step 6 — Report and track
- Report: "Doc PR opened on `<doc-repo>`: <url> — <k> pages updated. Review and merge when ready."
- Log the call in the code repo's `progress.md` (Optional calls): `document-sync → doc PR <url>`.

## Red flags
**Never:**
- Edit the **code** repo here — this step only touches the doc repo.
- Sync **code-coupled** docs (README, service ADR, OpenAPI/schema) into the doc repo — those belong
  in the code PR. If they were missed, **report** it for a code-repo fix instead.
- Auto-merge the doc PR (unless explicitly asked) — propose, let the user accept.
- Document internal refactors / test-only changes as if they were features.
- Restructure or reformat the doc repo beyond what the change needs.

**Always:**
- Reuse `.mri_code/document-sync.md`; ask for the target only when it is missing.
- Distill to **user-facing** changes before writing.
- Link the doc PR back to the source issue/PR.

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Sonnet (doc writing) — see `.mri_code/models.md`.
