# The four prompts

Paste in order. Each runs for a minute or two, which is teaching time rather
than dead air. What to say over each one is in `RUNBOOK.md`.

Start Claude Code in this folder first, so it picks up `.claude/`.

---

## 1 · Profile

> Four files from a client are in `data/`. Northgate Health, a private clinic,
> six months of inbound calls plus the rota, CRM enquiries and ad spend.
>
> Profile them. Do not analyse anything and do not tell me about missed calls.
>
> I want to know what I am holding before I trust it: what would break a join,
> what is in there that is not a real patient call, which categories are the
> same thing under two names, and which of these problems produce no error if I
> get them wrong.

---

## 2 · Compute

> Now clean and join properly, handling everything you just found. Write the
> code to a file. Show me row counts before and after every join.
>
> The practice director believes the problem is that not enough people are
> finding the clinic. Test that.
>
> Work out what share of calls never reach a person, and whether that share is
> even across the day. Report the sample size beside every figure, and write
> every result into the ledger with its method and its sources.

---

## 3 · Attack

> Use the sceptic. Recompute the headline your own way from the raw files
> first, before reading the analysis.
>
> Then name three other things that could produce this pattern and test each
> one. Tell me which you ruled out, how, and what this data cannot settle at
> all. Give me a verdict.

---

## 4 · Compose

> Use the storywright. Write the story in five beats: the belief, the question,
> the reveal, the mechanism, and the decision with its uncertainty.
>
> Every sentence carrying a figure references it by fact id, not by value. Then
> build the page from `story.template.html` and the ledger, and tell me if any
> number on the page was not looked up.

---

# The second case

Same four prompts, one different question. This is the part that shows the
folder is the deliverable rather than the story.

> Different question, same pipeline. `marketing_spend.csv` and `enquiries.csv`
> hold six months of paid channels and what came of them.
>
> Which channel actually produced patients, rather than clicks? Run the four
> stages. Watch the sample sizes.
