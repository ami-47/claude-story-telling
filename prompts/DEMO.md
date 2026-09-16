# The prompts

Four demos. Paste each `>` block in order, one at a time, waiting for it to
finish before pasting the next. What to say while each one runs is in
`RUNBOOK.md`. Everything outside a `>` block here is context for whoever is
driving, not something to paste.

Start Claude Code in this folder first, so it picks up `.claude/`.

---

# Demo 1 · Generate insights directly from the files
### Slides 14-15 · local CSVs, no database

The baseline. Everything below comes from `data/*.csv` on disk, read and
computed fresh, no prior answer trusted.

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

**What this produces.** ~14.2% of calls unanswered overall; 53.8% inside the
12:30-13:30 window against 6.6% outside it. This is the number Demo 2
reproduces through a different mechanism.

---

# Demo 2 · Do the same with MCP
### Slide 16 · optional, needs Supabase set up. See SUPABASE.md

Same headline, same underlying rows, asked through the Supabase MCP server
instead of read off disk. It is additional, not a replacement for Demo 1: if
the database or the network is unreachable, skip this demo entirely and keep
going, nothing later depends on it.

> The cleaned tables are already in Postgres. Using the Supabase tools, list
> what is in the `northgate` schema and read me the definition that the
> `v_calls` view carries. Do not query anything yet.

Then, the direct mirror of Demo 1's headline number, so the room can compare
the two side by side:

> What share of calls went unanswered, inside the 12:30-13:30 window and
> outside it? Show me the SQL before you run it, and show the result beside
> it. Use the view. Do not redefine unanswered inside your own query.

**It should come back 53.8% and 6.6%, matching Demo 1 exactly.** If it
doesn't, something is wrong (the view's definition has drifted from the local
computation, or the load is stale) and it needs fixing before this stage is
shown live, not explained away on stage.

If there's time, extend it:

> Two more, the same way: which half hour of the day is worst, and how many
> calls does that rest on? And which line is hit hardest?

**Why this stage exists.** Demo 1 produced an answer once, from a snapshot.
This produces something the practice can keep asking, from a source, with one
definition of "unanswered" written once in the view rather than re-decided by
every query.

---

# Demo 3 · Dashboard
### builds the prop for Slide 01, not shown as a prompt live

Run this once, before the room, straight after `answers/facts.json` is
populated by Demo 1. It produces the artifact Slide 01 ("Before slide one")
opens on, alongside `output/story.html` from Demo 4.

> Use the dashwright. Build the conventional operations dashboard at
> `output/dashboard/dashboard.html`: a sidebar, a KPI row, a few charts,
> the kind of tool a practice manager already owns. Every number still comes
> from the ledger, by fact id, same discipline as the story. Screenshot it
> yourself before telling me it's done.

**What this produces.** The same facts as Demo 1 and Demo 4, laid out as a
competent-looking conventional dashboard that answers nothing about the
lunch-hour mechanism. That contrast is Slide 01's whole cold open.

---

# Demo 4 · Skills-based creation of the storytelling page
### Slides 17-20

## 3 · Attack

> Use the sceptic. Recompute the headline your own way from the raw files
> first, before reading the analysis.
>
> Then name three other things that could produce this pattern and test each
> one. Tell me which you ruled out, how, and what this data cannot settle at
> all. Give me a verdict.

## 4 · Compose

> Use the storywright. Write the story in five beats: the belief, the question,
> the reveal, the mechanism, and the decision with its uncertainty.
>
> Every sentence carrying a figure references it by fact id, not by value. Then
> build the page from `story.template.html` and the ledger, and tell me if any
> number on the page was not looked up.

**What this produces.** `output/story.html`, the same facts as Demos 1-3, now
with the mechanism and a decision. This is the page Slide 01 opens with.

---

# The second case
### Slide 22

Same four prompts (Demo 1 and Demo 4 only; Demo 2 and 3 don't need repeating
to make the point), one different question. This is the part that shows the
folder is the deliverable rather than the story.

> Different question, same pipeline. `marketing_spend.csv` and `enquiries.csv`
> hold six months of paid channels and what came of them.
>
> Which channel actually produced patients, rather than clicks? Run the four
> stages. Watch the sample sizes.
