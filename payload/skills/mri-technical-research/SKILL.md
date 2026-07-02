---
name: mri-technical-research
description: >-
  Technical research: feasibility, architecture options, libraries, integration patterns.
  On-demand, suggested after /mri-forge.
  Invoked by /mri-technical-research.
disable-model-invocation: true
---

# mri-technical-research — technical research

> ┌─ mri devtools ─┐

**Goal**: assess feasibility and technical options (before freezing the design).
**⛔ Prerequisite**: web search (WebSearch/MCP); otherwise abort and warn.

## Flow
1. **Scope**: the technical question (feasibility, tech/library choice, integration, performance).
2. **Research** (web, cited sources): architecture options and trade-offs, candidate libraries/tools
   (maturity, license, community), integration patterns, known risks/limitations, benchmarks.
3. **Synthesize**: comparison of options + reasoned recommendation.
4. **Write** `.mri_devtools/docs/<project>/research-technical.md` (findings + sources).
   Write the document in the configured document language (see AGENTS.md).

## Follow-up
Optional: log the call in `progress.md`. Return to the flow (typically `/mri-design`).

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Sonnet (web research) — see `.mri_devtools/models.md`.
