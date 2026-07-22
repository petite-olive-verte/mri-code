---
name: mri-code-issue
model: opus
description: >-
  Alternate entry point of the mri pipeline: start the flow from a GitHub issue instead of a
  brainstorm. Fetches the issue, and — when it is too thin to act on — enriches it WITH the user
  and writes the refined issue back to GitHub. The issue itself is the source of truth (no local
  brief.md); it just inits progress tracking and hands off to the same per-issue flow. Invoked by
  /mri-code-issue.
disable-model-invocation: true
---

# mri-code-issue — start the flow from a GitHub issue

> ┌─ mri devtools ─┐

**Alternate front door of the pipeline.** Instead of `/mri-code-brainstorm`, take an existing
**GitHub issue** as the source of intent. One issue = one journey through the same flow
(`design → devplan → scaffold → implement → review → finish`), tracked in its own
`.mri_code/docs/<issue-slug>/` folder. Run `/mri-code-issue` once per issue to work several in
parallel, each with its own `progress.md`.

**The issue is the source of truth** (see `AGENTS.md` → *Issue-driven journeys*). The brief and,
later, the technical design live **in the GitHub issue**, not in local `brief.md`/`spec.md`. This
step writes **no** brief file — after enrichment, the issue body *is* the brief. Only `progress.md`
(and later `plan.md`) is kept locally, as operational state.

**Announce at start:** "I'm using mri-code-issue to start the flow from a GitHub issue."

Communicate in the configured language and write the brief in the configured document language
(see `AGENTS.md`).

## Access
Uses the **`gh` CLI** (already authenticated on the machine). Before anything else, verify it:

```bash
gh auth status
```

If `gh` is missing or not authenticated, stop and tell the user to install/`gh auth login` first —
do not fall back to scraping the web UI.

## Step 1 — Resolve the issue
Input `$ARGUMENTS` may be an issue **number** (`42`), a `#42`, or a full **URL**. If empty, list
open issues and let the user pick one:

```bash
gh issue list --state open --limit 20
```

Fetch the full issue (adapt `--repo` if the URL points to another repo):

```bash
gh issue view <number> --json number,title,body,url,labels,state,milestone,assignees,comments
```

Read the body **and the comments** — clarifications often live in the thread, not the description.

## Step 2 — Assess whether it is actionable
Judge the issue against what `/mri-code-design` will need. A **DETAILED** issue makes the intent,
the expected outcome, and the boundaries clear enough to design against. Look for:

- **Problem / goal** — what pain or need, for whom. Not just a title.
- **Expected outcome** — what "done" looks like; acceptance criteria if any.
- **Scope** — what is in, what is explicitly out.
- **Context** — constraints, affected area of the codebase, links.

Classify it:
- **DETAILED** → skip Step 3, go straight to Step 4.
- **UNDER-SPECIFIED** → Step 3 (enrich). State briefly *which* of the above are missing.

Do not invent requirements to make an issue look complete — surface the gaps.

## Step 3 — Enrich the issue (only if UNDER-SPECIFIED)
Close the gaps **with the user**, then reflect the result back into the GitHub issue.

1. **Elicit** — ask **one question at a time**, in dependency order, targeting only the missing
   pieces from Step 2. Offer your best-guess answer with each question (easier to confirm/correct
   than an open prompt). Keep it tight; this is not a full brainstorm — for deep ideation suggest
   `/mri-code-brainstorm`, for adversarial pressure `/mri-code-forge`.
2. **Draft the refined issue body** — rewrite the description so it is actionable: a clear
   problem/goal, expected outcome + acceptance criteria, scope (in/out), and any context. Preserve
   the author's original intent and any useful existing content; append a short
   `— Refined via mri-code (<date>)` marker so the edit is traceable.
3. **APPROVAL GATE (outward-facing write).** Editing a GitHub issue is visible to everyone
   watching it. **Show the user the exact new body and get explicit approval before writing.** Never
   push the edit silently.
4. **Write it back** to GitHub only after approval:

   ```bash
   gh issue edit <number> --body-file <path-to-refined-body>
   ```

   If the user prefers not to overwrite the description, offer to post the refinement as a **comment**
   instead (`gh issue comment <number> --body-file ...`). If they decline any write-back, fall back
   to a local `.mri_code/docs/<issue-slug>/notes.md` holding the enrichment, and warn that the
   GitHub issue is now out of sync with the working brief.

## Step 4 — Confirm the issue carries the brief (no local file)
After Step 2/3 the issue body should read as a brief: problem/goal, expected outcome + acceptance
criteria, scope (in/out), context. If a DETAILED issue already covers this, good — nothing to write.
**Do not create `brief.md`.** The issue *is* the brief; the rest of the pipeline will read it with
`gh issue view`.

## Step 5 — Initialize tracking
Derive the project slug: `issue-<number>-<short-title-slug>` (kebab-case, ~4 words).
Create/refresh `.mri_code/docs/<issue-slug>/progress.md` using the canonical schema (see
`/mri-code-resume`), with the **issue** step done **and a `## Source` block** — its presence is how
every downstream skill knows this journey is issue-driven and where to read the brief/design:

```markdown
# Journey — issue-<number>-<slug>   (updated: <date> · last step: /mri-code-issue)

## Source
- **Issue:** #<number> — <title>
- **URL:** <url>
- **Repo:** <owner/repo>
- **Suggested branch:** issue-<number>-<short-title-slug>
- **Brief & design live in the issue** (not in this folder).

## Steps
- [x] issue (#<number>, enriched: <yes/no>)
- [ ] design → into the issue
- [ ] devplan → plan.md
- [ ] scaffold
- [ ] implement
- [ ] review
- [ ] finish

## Next step
/mri-code-design (reads the issue, writes the design back into it)
```

`issue` replaces `brainstorm`/`forge` as the first line for issue-driven journeys; the rest of the
pipeline is unchanged.

## Step 6 — Handoff
Recap in two lines: the issue, whether it was enriched (and written back to GitHub), and that the
brief lives in the issue. Then: "**Next step → `/mri-code-design`** (suggested model: **Opus** — see
`.mri_code/models.md`)." Do not launch it yourself.

## Red flags
**Never:**
- Edit or comment on the GitHub issue without explicit user approval (outward-facing write).
- Invent requirements to make a thin issue look complete — name the gaps instead.
- Fall back to scraping the web UI when `gh` is unavailable — stop and tell the user.
- Start writing code or scaffolding here — this step only frames the work.

**Always:**
- Verify `gh auth status` first.
- Read the issue comments, not just the description.
- Show the exact refined body and get approval before `gh issue edit`.
- Give each issue its own `.mri_code/docs/<issue-slug>/` journey.

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Opus (framing / enrichment) — see `.mri_code/models.md`.
