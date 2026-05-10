# Ledger Specification

## Purpose

Use ledgers as the reusable memory layer for the skill. The point of ledgers is to avoid repeatedly feeding the full novel back into the model after the first structured pass.

## Token-Efficiency Principle

After packet notes and phase notes are filled:

- prefer ledgers over raw packets
- prefer compression passes over ledgers when drafting final output
- only reopen raw packet text when a specific ambiguity still matters

Do not rebuild understanding from scratch if the ledgers already capture it.

## Packet Note Sections

Each packet note should include:

- `Story Role`
- `Main Plot Events`
- `Character Updates`
- `Relationship Updates`
- `World Or Background Updates`
- `Subplot Updates`
- `Foreshadowing Or Payoff`
- `Ending Impact`
- `Unresolved Threads`
- `Source Certainty Notes`

## Phase Note Sections

Each phase note should include:

- `Main Plot Progress`
- `Main Characters In Motion`
- `Subplot Movement`
- `Background Or World Updates`
- `Turning Points`
- `Ending Relevance`
- `Unresolved Threads Carried Forward`
- `Suggested One Paragraph Phase Summary`

## Core Ledgers

The workspace should maintain:

- `main-plot-ledger.md`
- `character-ledger.md`
- `relationship-ledger.md`
- `subplot-ledger.md`
- `world-ledger.md`
- `foreshadow-ledger.md`
- `ending-ledger.md`
- `unresolved-ledger.md`

## Ledger Use By Mode

### `full-html`

Prioritize:

- world ledger
- character ledger
- relationship ledger
- subplot ledger
- ending ledger

### `medium-outline`

Prioritize:

- main plot ledger
- subplot ledger
- ending ledger
- phase summaries

### `short-outline`

Prioritize:

- compression passes
- short-outline canon

Do not go back to raw packets unless a crucial plot dependency is still unclear.
