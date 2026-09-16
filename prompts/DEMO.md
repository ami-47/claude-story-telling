# The four prompts

Paste in order. Each runs for a minute or two, which is teaching time rather
than dead air. What to say over each one is in `RUNBOOK.md`.

Start Claude Code in this folder first, so it picks up `.claude/`.

---

## 0 · The cold open

Run this once, before the room, straight after `answers/facts.json` is
populated. It is not shown as a prompt live: it produces the artifact the
cold open in `RUNBOOK.md` opens on.

> Use the dashwright. Build the conventional operations dashboard at
> `output/dashboard/dashboard.html`: a sidebar, a KPI row, a few charts,
> the kind of tool a practice manager already owns. Every number still comes
> from the ledger, by fact id, same discipline as the story. Screenshot it
> yourself before telling me it's done.

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

## 2b · Put it where it can be asked again
### optional, needs Supabase set up. See SUPABASE.md

The loading happened before the session, offstage. This stage is the querying,
and it runs through the Supabase MCP server, read only. It is additional, not
a replacement for the local files: if the database or the network is
unreachable, skip this stage and keep going, nothing later in the session
depends on it.

> The cleaned tables are already in Postgres. Using the Supabase tools, list
> what is in the `northgate` schema and read me the definition that the
> `v_calls` view carries. Do not query anything yet.

Then:

> Answer these three from the database. Show me the SQL before you run it, and
> show the result beside it.
>
> 1. What share of calls went unanswered, inside the lunch window and outside it?
> 2. Which half hour of the day is worst, and how many calls does that rest on?
> 3. Which line is hit hardest?
>
> Use the view. Do not redefine unanswered inside your own query.

**Why this stage exists.** Everything before it produced an answer. This produces
something the practice can keep asking. The raw export was a snapshot. The
database is a source.

It is also the only moment in the session where the third architecture is shown
rather than described: the question is in English, the SQL is on screen, the
database did the arithmetic, and the connection is read only so nothing can be
damaged by a bad query.

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
