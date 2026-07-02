---
name: mri-document-project
description: >-
  Documents an existing (brownfield) project to give the agent context: structure, stack,
  conventions, entry points, how to run/test.  On-demand, ahead of /mri-brainstorm on an existing repo.
---

# mri-document-project — context of an existing project (brownfield)

> ┌─ mri devtools ─┐

**Goal**: when working on an **existing repo** (not greenfield), produce a concise context
document that the following skills will consume, to avoid false assumptions.

## Flow
1. **Explore**: folder structure, `README`, build/config files (`pyproject.toml`,
   `package.json`…), entry points, tests, recent commits. Identify the real stack and conventions.
2. **Map**: main modules and their responsibilities, data flows, external dependencies,
   commands to install/run/test.
3. **Write** `.mri_devtools/docs/<project>/project-context.md`: an **actionable** synthesis (not a dump) —
   "what an agent needs to know before touching this code". Flag fragile areas/debt spotted.

This doc complements `.mri_devtools/constitution.md` (intended rules) by describing what exists (de facto rules).

## Follow-up
Optional: log the call in `progress.md`. Then move on to `/mri-brainstorm` (the idea/evolution
to design on this project).
