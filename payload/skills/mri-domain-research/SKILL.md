---
name: mri-domain-research
description: >-
  Domain/industry research: expertise, terminology, patterns, regulatory constraints.
  On-demand, suggested after /mri-forge.
  Invoked by /mri-domain-research.
---

# mri-domain-research — domain research

> ┌─ mri devtools ─┐

**Goal**: acquire/validate expertise in an unfamiliar domain to avoid design mistakes.
**⛔ Prerequisite**: web search (WebSearch/MCP); otherwise abort and warn.

## Flow
1. **Scope**: the domain/industry, what we need to understand/validate.
2. **Research** (web, cited sources): key terminology and concepts, domain patterns and best practices,
   players/standards, constraints (regulatory, business), classic pitfalls.
3. **Synthesize**: glossary, domain rules, implications for the idea/design.
4. **Write** `.mri_devtools/docs/<project>/research-domain.md` (findings + sources).
   Write the document in the configured document language (see AGENTS.md).

## Follow-up
Optional: log the call in `progress.md`. Return to the flow (typically `/mri-design`).
