---
name: fact-ledger
description: Turn an analysis into a ledger of checked facts, then write prose that references facts by id instead of containing numbers. Use whenever a finding is going into a document, deck, page or email that someone outside the team will read. Prevents invented figures and makes every number traceable.
---

# Never type a number into prose

A language model that writes "revenue rose 14.3 percent" in a sentence is
generating digits. It might be right. You cannot tell by reading it, and neither
can the client. This skill removes the question entirely by splitting the job:

- **code computes**, and writes every result into a ledger
- **the ledger stores** the value plus how it was produced
- **prose references** facts by id, never by value
- **a build step** substitutes the values in at the end
- **a verifier** recomputes everything from the raw files and fails loudly

If a figure is wrong, the fix is always in the computing script. Never in the
document.

## The ledger

One record per fact:

| field | what goes in it |
|---|---|
| `id` | F01, F02, and so on. Stable. Never reused. |
| `label` | what it measures, in words a client would use |
| `value` | the number, as computed, not rounded for display |
| `unit` | percent, calls, £, points, people |
| `method` | the calculation in one sentence, naming the columns |
| `sources` | which raw files it came from |
| `n` | the sample size the figure rests on |
| `note` | anything a sceptic would need, such as what was excluded |

Write it to JSON or to a sheet. Either works. What matters is that it exists as
a separate artefact from the prose.

## Writing the prose

Write sentences with placeholders: `Unanswered calls run at {F05} inside the
window against {F06} outside it.` Then substitute at build time.

Two hard rules while writing:

- **The sample size rule.** Any sentence carrying a percentage also carries its
  n, or sits next to it. Anything computed on under five percent of the base is
  labelled indicative and is never ranked against the rest.
- **The causal language gate.** The words *drove*, *because*, *caused*, *led to*
  and *explains* require a fact that decomposes the change. If no such fact
  exists, the sentence says *coincided with* or *is associated with*, or it does
  not get written.
- **The scope rule.** Citing a fact id correctly is not the same as making a
  true claim about it. Before the sentence around a placeholder ships, reread
  it against that fact's own `method` field and check the scope, timeframe and
  denominator actually match. A real build did this wrong: it wrote "new
  patient calls go unanswered inside this one hour, every week" next to a fact
  whose method was "calls not answered, divided by 26 weeks in the export,"
  which is the whole day, not one hour. The number was correctly looked up.
  The sentence claimed something the fact never measured. This is exactly the
  failure `sceptic`'s "check the denominator" step exists to catch, so if
  `storywright` is composing without a sceptic pass already run against this
  exact prose, it re-reads its own sentences against `method` before calling a
  beat finished.

## The verifier

A second script that reads the raw files, recomputes every fact independently,
and compares. It should be able to fail. If it never fails, it is not checking
anything. Run it as the last step before anything is shown to anyone.

## What to hand over

- the ledger
- the prose with its placeholders still visible
- the rendered version
- the verifier's output

Showing the placeholder version beside the rendered version is the single most
convincing thing you can put in front of a client. It shows them that nobody
typed the number.
