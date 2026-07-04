---
name: mri-code-meta-prompt
description: Turns a vague request into a precise, structured, ready-to-use prompt for an LLM/agent. One-off tool, outside the idea->code pipeline; invoked explicitly (command /meta-prompt).
disable-model-invocation: true
---

# mri-code-meta-prompt — vague → precise

> ┌─ mri devtools ─┐

Turn a fuzzy request into a **precise, structured prompt**, ready to paste into an agent.
**Standalone** tool: use on demand, independently of the brainstorm→spec→implement flow.

## Procedure
1. **Remove the ambiguity first.** If the request is under-specified, ask **1 to 3 targeted questions**
   (audience, scope, format, constraints). If the user wants to move fast, instead state
   **explicit assumptions** and continue.
2. **Build the optimized prompt** with, as relevant, these sections:
   - **Role**: who the agent should embody.
   - **Objective**: the expected result, in one sentence.
   - **Context**: the necessary info (and only that).
   - **Constraints / requirements**: what must / must not be done.
   - **Output format**: structure, length, language.
   - **Acceptance criteria**: how to judge that it succeeded.
   - **Examples** (few-shot) only if a precise format must be imitated.
3. **Reasoning**: for a complex task, add a zero-shot CoT trigger
   ("think step by step before answering") rather than examples.
4. **Concision**: cut anything that doesn't help the task (noise degrades the results).

## Output
Return the final prompt **in a code block** (copyable as-is). If you asked questions,
first provide an "assumptions" version usable immediately, then offer to refine.

## Reminders
- To build an **application**, don't go through here: use the brainstorm → spec
  flow (the spec is already the precise instruction). This meta-prompt is for **one-off
  prompts** outside a project.

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Opus — see `.mri_code/models.md`.
