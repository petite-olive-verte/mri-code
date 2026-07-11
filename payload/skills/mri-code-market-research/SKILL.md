---
name: mri-code-market-research
model: sonnet
description: >-
  Market research (competition, customers, trends) on current web data with cited sources.
  On-demand, suggested after /mri-code-forge.
  Invoked by /mri-code-market-research.
disable-model-invocation: true
---

# mri-code-market-research — market research

> ┌─ mri devtools ─┐

**Goal**: produce market research backed by current web data and **cited sources**,
with a clear narrative. **Role**: research facilitator — you bring methodology + web research,
the user brings the domain and the direction.

**⛔ Prerequisite**: web search available (WebSearch/MCP). Otherwise, abort and warn.

## Flow
1. **Scope**: research question, target market/segment, known competitors, what we want to decide.
2. **Research** (web): competitors (positioning, pricing, strengths/weaknesses), customers/segments and
   needs, trends, market size/dynamics. Verify and **cite every source** (URL).
3. **Synthesize**: competitive mapping, opportunities/risks, implications for the idea.
4. **Write** `.mri_code/docs/<project>/research-market.md` (findings + sources). Concise, actionable.
   Write the document in the configured document language (see AGENTS.md).

## Follow-up
Optional: log the call in `progress.md` ("Optional calls" → `research-market.md`). Then return
to the flow (typically `/mri-code-design`).

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Sonnet (web research) — see `.mri_code/models.md`.
