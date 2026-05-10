# Consistency Check Specification

## Purpose

Use consistency checks to catch two major failure modes:

- hallucination
- omission
- source substitution with external summaries

## What To Check

### Structural coverage

- every packet has a note file
- every phase has a note file and summary
- all required ledgers exist
- all required compression passes exist

### Plot coverage

- the main plot ledger exists and is non-empty
- the ending ledger exists and is non-empty
- later phases are not missing from the final understanding

### Character coverage

- major characters appear in the character ledger
- important relationships appear in the relationship ledger
- ending-relevant characters are not missing from the ending ledger

### Output coverage

For HTML outputs, confirm the main sections exist:

- snapshot
- background-world
- characters
- relationships
- main-plot
- phase-breakdown
- subplots
- ending
- short-outline
- source-notes

### Source-discipline coverage

- if local source or workspace exists, the workflow should not depend on outside plot summaries
- missing local Python must not be treated as a reason to switch to web-based story summaries

## Workflow Rule

Run checks after:

- ledgers are built
- compression passes are built
- HTML is built

If checks fail, fix the workspace before reusing it for later outputs.
