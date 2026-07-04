---
name: mri-code-technical-research
description: >-
  Technical research: feasibility, architecture options, libraries, integration patterns.
  On-demand, suggested after /mri-code-forge.
  Invoked by /mri-code-technical-research.
disable-model-invocation: true
---

# mri-code-technical-research — technical research

> ┌─ mri devtools ─┐

**Goal**: assess feasibility and technical options (before freezing the design).
**⛔ Prerequisite**: web search (WebSearch/MCP); otherwise abort and warn.

## Flow
1. **Scope**: the technical question (feasibility, tech/library choice, integration, performance).
2. **Research** (web, cited sources): architecture options and trade-offs, candidate libraries/tools
   (maturity, license, community), integration patterns, known risks/limitations, benchmarks.
3. **Synthesize**: comparison of options + reasoned recommendation.
4. **Write** `.mri_code/docs/<project>/research-technical.md` (findings + sources).
   Write the document in the configured document language (see AGENTS.md).

## Follow-up
Optional: log the call in `progress.md`. Return to the flow (typically `/mri-code-design`).

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Sonnet (web research) — see `.mri_code/models.md`.
