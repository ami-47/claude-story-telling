# Northgate Health · data story pipeline

You are working on a client engagement. Four raw files in `data/` describe six
months of inbound calls at a private clinic, plus the rota, the CRM enquiries
and the ad spend behind them.

## How work is done here

Four stages, in order. Do not skip one because the answer seems obvious.

1. **Profile.** Use the `data-profile` skill. Describe the data. Analyse nothing.
2. **Compute.** Use the `analyst` subagent and the `fact-ledger` skill. Code
   produces every figure. Nothing is calculated in prose.
3. **Attack.** Use the `sceptic` subagent. Try to break the finding before a
   client does.
4. **Compose.** Use the `storywright` subagent and the `story-craft` skill.
   Five beats. Placeholders, not numbers.

## Hard rules

- **Never type a number into prose.** Write `{F05}` and let the build step
  substitute it. If the fact does not exist, ask for it.
- **State the n beside every percentage.** Anything under five percent of the
  base is labelled indicative and never ranked against the rest.
- **Causal words need a decomposition fact.** Drove, because, caused, explains.
  If no such fact exists, write "coincided with", or do not write the sentence.
- **Say what you could not rule out.** Every story ends on something genuinely
  unresolved. If everything resolves, something has been hidden.

## The existing story

`story.template.html` and `build_story.py` already produce a finished story on
the missed calls question. Read them before building a second one. The pattern
is: template holds placeholders, `verify_calls.py` writes the ledger,
`build_story.py` substitutes. Follow it rather than inventing a new one.

## Regenerating

    python3 generate_calls.py --seed 42     # reproducible raw files
    python3 verify_calls.py                 # the ledger
    python3 build_story.py                  # the page

The generator simulates a queue against the rota. No rate is asserted anywhere
in it. If someone asks whether the answer was invented, that file is the proof.
