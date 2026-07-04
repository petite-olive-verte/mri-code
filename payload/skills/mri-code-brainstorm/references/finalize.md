# Wrap-Up: synthesis & brief

Load this when the user is exhausted or the topic is mined out. Your session notes are the raw material; everything
here derives from them.

## Synthesis (in two steps, in order)
1. **Hold up the mirror first.** Reflect back a live sample of *their* ideas — deliberately
   include the odd/buried ones, not just the recent obvious ones. Ask what they see
   now: conclusions, synergies, themes, the few that really matter. Let them
   connect first — their pattern recognition is the point.
2. **Then add the connections they'd miss.** Lean in
   creatively — not fresh raw ideas, but the non-obvious links: that idea from technique 1 resolves the tension of
   technique 4; those three are one idea under three hats; that wildcard is the real breakthrough.

## Producing the brief
Write **`.mri_code/docs/<project>/brief.md`** building on `assets/brief-template.md` (adapt
aggressively: drop sections that don't earn their place, add what the product demands).
Write the document in the configured document language (see AGENTS.md).
The brief must contain, at a minimum: problem, users, solution/value, scope (in/out),
**measurable success criteria**, and the open assumptions/risks. It's the handoff artifact for
`/mri-code-forge` (challenge) then `/mri-code-design`.

No HTML keepsake nor external log: the `brief.md` **is** the deliverable. Stay concise and on
point — the token budget matters for the rest of the pipeline.

## End
Update `progress.md` (brainstorm → `[x]`), then indicate what's next:
"Next step → `/mri-code-forge` to harden the idea, or `/mri-code-design` if it's already solid."
