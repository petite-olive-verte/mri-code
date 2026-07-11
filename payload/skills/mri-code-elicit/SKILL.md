---
name: mri-code-elicit
model: opus
description: >-
  Prompts reconsidering, refining, and improving the last produced output (yours or a doc).
  On-demand deepening/critique (Socratic, first principles, pre-mortem, red-team…).
  Invoked by /mri-code-elicit.
disable-model-invocation: true
---

# mri-code-elicit — deepen/critique an output

> ┌─ mri devtools ─┐

**Goal**: improve the **last output** (a section of a brief/spec/plan, a decision, a piece of
code) by applying an elicitation method, then feeding the improved version back in.

## How to do it
1. **Take the content to deepen** (the recent output, or whatever the user points to). Empty → ask.
2. **Choose 1-2 methods** suited to the content and the risk (don't dump the whole menu; propose and explain in one line).
3. **Apply** the method interactively, one pass at a time; surface the weaknesses/blind spots.
4. **Feed back in**: propose the improved version of the content, the user keeps control (accept/revise).

## Method menu (curated)
- **Socratic** — question each premise down to its foundation.
- **First principles** — rebuild from the base truths, without copying the existing.
- **Pre-mortem** — "it's a failure in 6 months, why?" → risks.
- **Red team** — attack the proposal like an adversary (abuse, workarounds, edge cases).
- **Defend the counter-argument** — argue the opposite position to test robustness.
- **Multiple perspectives** — re-read through novice / expert / maintainer / payer.
- **Widen / narrow** — zoom out (context, alternatives) then zoom in (detail, edge cases).
- **Assumption testing** — list the assumptions; for each, a low-effort test that validates/kills it.

## Halt
Zero improvement found = suspicious → re-analyze or ask. Empty/unreadable content → stop.

## Tracking
Optional skill: log the call in `.mri_code/docs/<project>/progress.md` ("Optional
calls" section). Then return to the calling step.

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Opus (depth of critique) — see `.mri_code/models.md`.
