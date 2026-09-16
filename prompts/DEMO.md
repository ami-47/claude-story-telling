# The prompts

Four demos. Each one below is a set of prompts to paste into Claude Code, in
order, one at a time — wait for one to finish before pasting the next.
What to say while each one runs is in `RUNBOOK.md`.

Start Claude Code in this folder first, so it picks up `.claude/`.

---

# Demo 1 · Generate insights directly from the files

Prompts to Claude Code, using only the raw files in `data/`. No database.

> Four files from a client are in `data/`. Northgate Health, a private clinic,
> six months of inbound calls plus the rota, CRM enquiries and ad spend.
>
> Profile them. Do not analyse anything and do not tell me about missed calls.
>
> I want to know what I am holding before I trust it: what would break a join,
> what is in there that is not a real patient call, which categories are the
> same thing under two names, and which of these problems produce no error if I
> get them wrong.

> Now clean and join properly, handling everything you just found. Write the
> code to a file. Show me row counts before and after every join.
>
> The practice director believes the problem is that not enough people are
> finding the clinic. Test that.
>
> Work out what share of calls never reach a person, and whether that share is
> even across the day. Report the sample size beside every figure, and write
> every result into the ledger with its method and its sources.

**Where it saves.** The cleaning code goes into a file you can rerun.
Every figure goes into `answers/facts.json`, the ledger — this is the file
every later demo reads from, so Demo 1 has to run before Demos 3 and 4.

**What it should find.** ~14.2% of calls unanswered overall; 53.8% inside the
12:30–13:30 window against 6.6% outside it. Demo 2 reproduces this same
number a different way.

---

# Demo 2 · Do the same with MCP
### optional, needs Supabase set up first — see SUPABASE.md

Prompts to Claude Code, using the Supabase MCP server instead of the files.
Needs the data already loaded into Postgres (a one-time step done before the
session, not live) and the MCP server authenticated (`claude`, then `/mcp`,
then Authenticate).

> The cleaned tables are already in Postgres. Using the Supabase tools, list
> what is in the `northgate` schema and read me the definition that the
> `v_calls` view carries. Do not query anything yet.

> What share of calls went unanswered, inside the 12:30-13:30 window and
> outside it? Show me the SQL before you run it, and show the result beside
> it. Use the view. Do not redefine unanswered inside your own query.

**It should come back 53.8% and 6.6%, matching Demo 1 exactly.** If it
doesn't, something is wrong (the view's definition drifted from the local
computation, or the database load is stale) and needs fixing before this is
shown, not explained away on the day.

If there's time, extend it with two more of the same shape:

> Which half hour of the day is worst, and how many calls does that rest on?
> And which line is hit hardest?

**Where it saves.** Nothing, by design. This demo only reads from the
database and prints results in the conversation — it doesn't write to
`answers/facts.json` or any file. That's the point of it: a source you can
keep asking, not a new snapshot to maintain.

**If Supabase is unreachable, skip this demo entirely.** Nothing later
depends on it.

---

# Demo 3 · Dashboard

One prompt to Claude Code, run once before the session, not live. Needs
Demo 1 to have already populated `answers/facts.json`.

> Use the dashwright. Build the conventional operations dashboard at
> `output/dashboard/dashboard.html`: a sidebar, a KPI row, a few charts,
> the kind of tool a practice manager already owns. Every number still comes
> from the ledger, by fact id, same discipline as the story. Screenshot it
> yourself before telling me it's done.

**Where it saves.** `output/dashboard/dashboard.html`. This is a prop, built
once and left alone — never rebuilt live.

**What it produces.** The same facts as Demo 1, laid out as a dashboard that
looks complete and answers nothing about why the lunch hour is different.

---

# Demo 4 · Skills-based creation of the storytelling page

Prompts to Claude Code, using the ledger Demo 1 wrote.

> Use the sceptic. Recompute the headline your own way from the raw files
> first, before reading the analysis.
>
> Then name three other things that could produce this pattern and test each
> one. Tell me which you ruled out, how, and what this data cannot settle at
> all. Give me a verdict.

> Use the storywright. Write the story in five beats: the belief, the question,
> the reveal, the mechanism, and the decision with its uncertainty.
>
> Every sentence carrying a figure references it by fact id, not by value. Then
> build the page from `story.template.html` and the ledger, and tell me if any
> number on the page was not looked up.

**Where it saves.** The sceptic's verdict stays in the conversation only —
it doesn't write a file. The storywright's page saves to `output/story.html`
and `output/story.artifact.html`.

**What it produces.** The same facts as Demos 1–3, now with the mechanism
and a decision attached. This is the page the session opens with.

---

# The second case

Run Demo 1 again, then the sceptic half of Demo 4 (skip the storywright half
— see below for why). One different question. Shows that the folder is the
deliverable, not the story.

> Different question, same pipeline. `marketing_spend.csv` and `enquiries.csv`
> hold six months of paid channels and what came of them.
>
> Which channel actually produced patients, rather than clicks? Profile,
> compute, then use the sceptic. Watch the sample sizes and watch the ranking
> change depending on which denominator you use.

**Why not the storywright half too.** Demo 1 through the sceptic genuinely
generalises — fresh code, fresh ledger, fresh verdict, whatever the question.
Composing a finished page doesn't, not with this pipeline: `story.template.html`
is one specific, hand-written page about the missed-calls story, and
`build_story.py` only ever substitutes fact values into that same fixed
prose. Pointed at a different question, it would either break (referencing a
fact id that doesn't exist) or silently show new numbers next to old,
unrelated sentences — exactly the kind of quiet mismatch this whole kit
exists to prevent. A genuinely different story page means writing a new
template by hand, which is real work, not a one-prompt live demo. Don't
imply otherwise on stage.
