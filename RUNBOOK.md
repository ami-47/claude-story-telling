# Runbook

For whoever is driving. Everything below is what to do and what to say, in
order.

## Before the room

    python3 generate_calls.py --seed 42
    python3 verify_calls.py
    python3 build_story.py

Then build the dashboard once, offstage — Demo 3 in `prompts/DEMO.md` (uses
the `dashwright` agent and the `dashboard-craft` skill). It writes to
`output/dashboard/dashboard.html`. Rebuilding it live in front of the room is
not the point; the story build is the live moment, the dashboard is a prop
that has to already exist.

**Local files stay in the repo either way.** Supabase (Demo 2) is an
additional live stage layered on top of the same verified facts, not a
replacement for the local pipeline (Demo 1): `data/*.csv` and
`answers/facts.json` are what the database was loaded from, and they are the
backup if the database, the network or the MCP auth misbehaves in front of
the room. If Supabase is unreachable on the day, skip Demo 2 and run the
rest exactly as written; nothing else in the session depends on it.

If you are using Demo 2, open the Supabase project dashboard the day before
and run one query, or it will have paused. Free projects pause after about
seven days of low activity. Then load it:

    python3 load_to_supabase.py

Authenticate the MCP server once, in a normal terminal, not an IDE extension:

    claude
    /mcp

Select supabase, then Authenticate. A browser opens. No token needed.

Run every demo once yourself before the room. When the page is finished, copy
`output/story.html` and `output/story.artifact.html` into `fallback/` before
you touch anything again — `output/` gets overwritten by every later build, so
`fallback/` is the only copy that survives a stall.

Have `output/story.html`, `output/dashboard/dashboard.html`,
`arch/pipeline.html` and `prompts/DEMO.md` open in tabs before you start.
Copy each prompt from the DEMO.md tab, never retype one from memory.

---

## Open cold
### about 90 seconds, no explanation first

Four steps, in this order:

    1 · Open output/story.html. Scroll it end to end. Say nothing.
    2 · Ask: what would you do on Monday?
    3 · Open output/dashboard/dashboard.html (Demo 3). Same data, same build.
    4 · Ask again. Let the silence sit.

Do not explain what they are looking at before they look at it. The story
gives them enough to answer step 2. The dashboard, built from the identical
ledger, does not, and the point is that the gap is not in the data, it is in
the argument. Do not rescue the silence after step 4.

---

## Demo 1 · Generate insights directly from the files

**Setup, before it runs.** From a spreadsheet to a finding. We open a set of
raw operational files, profile them, and get to one claim worth putting in
front of the client.

**What to watch**
- The files are exactly what a client would send
- Nothing is cleaned beforehand
- Watch where it asks rather than guesses

**While profiling runs.** This is the step everyone skips. You have a client
waiting, so you go straight to the answer, and three weeks later somebody
finds the join dropped four hundred rows and the engagement is suspect.
Profiling costs one prompt.

**The beat to land.** Point at the trailing whitespace on the line names and
the duplicated call ids. Neither produces an error. Pandas does not warn
you. The rows simply vanish and every number downstream is quietly wrong.
Ask the room how they would have caught it.

**While computing runs.** A model that writes a percentage into a sentence
is generating digits. It might be right. You cannot tell by reading it, and
neither can your client. That is why code computes and the ledger stores.

**What should appear.** Roughly one call in seven never reaches a person,
and it is not spread evenly. Around 54 percent inside the lunch hour against
about 7 percent outside it, with the whole day's damage concentrated in that
one window.

**If it declares a service line or a channel catastrophic, let it sit.** Ask
the room what they would do about it. Then reveal the sample size. That beat
sells Demo 4 better than any explanation of Demo 4.

**Debrief.** One claim, traced back to the rows it came from.
- The clean up happened in code, so it can be rerun
- The number can be recomputed on demand
- The first answer was not the useful one — the practice director's belief
  ("not enough people are finding us") gets tested here and doesn't hold;
  the real number is about who answers the phone, not who calls it

**What we got.** The client sent us this file. We sent back a claim, and the
code that produced it.

---

## Demo 2 · Do the same with MCP
### optional, skip it entirely if Supabase is asleep or the wifi is bad

**Setup, before it runs.** The same question against live data. Same
question, but connected to the source rather than a file somebody exported.

**What to watch**
- No export step and no stale data
- Access is the constraint, not capability
- Same method, different plumbing

**Why it is here.** Demo 1 produced an answer, once, from a snapshot. This
produces a source the practice can keep asking. It is also the only place in
the session where the third architecture (question in English, database
answers it) is shown rather than described.

**The beat to land.** Open the `v_calls` view and read the definition line
out loud. Unanswered means missed, abandoned or voicemail, written once, in
the database, where everyone hits it.

Then ask the room: how many different definitions of one metric are
floating around your clients right now? That question is why the view
matters, and it is the reason two people in the same firm quote two
different numbers.

**What to point at.** The question was in English. The SQL is on screen.
The database did the arithmetic. Nobody wrote a query, and anybody can read
one. It should come back the exact same 53.8 / 6.6 percent Demo 1 already
found — say that out loud, since same answer, different mechanism is the
point.

**Thirty seconds on security.** Point out that the server is running
**read only** and **scoped to one project**. Claude cannot drop a table here
even if a prompt told it to, and it cannot see any other project on the
account.

Then the honest part: the loading earlier used a full database password,
which is unscoped and not revocable per person. For a real client you issue
a read only role for the analyst. Say it, do not dwell. Their IT team will
ask first.

**If it fails, skip it.** Nothing downstream depends on this demo. Demos 3
and 4 both run from the ledger Demo 1 already wrote.

**Debrief.** Nothing about the analysis. Everything about repeating it.
- Runs again next month with no one emailing a file
- The definitions live in their system, not our spreadsheet
- Worth asking for on day one of an engagement

**What changed.** Ask for access in the kick off, not in week three when you
need it.

---

## Demo 3 · Dashboard

Already built, offstage, before the room (see "Before the room" above).
Nothing to run live — just open `output/dashboard/dashboard.html`, which
already happened in "Open cold."

**Setup, before it's opened.** Same facts, no argument. The same ledger
Demo 1 wrote, laid out as the kind of dashboard the room already owns —
opened before anyone has seen the actual finding, not after.

**What to watch**
- Same analysis as Demo 1, not a new one — every tile traces to the same
  ledger
- A few tiles, each one a real, correctly scoped number
- Looks exactly as finished as the page that follows it

**This is not a "build it because someone will use it weekly" pitch.** That
is a real, separate case for a real dashboard, and it's a fair one to make
with a client — but it isn't what this demo is for. This dashboard exists to
be wrong in one specific, honest way: nothing on it is scoped to the one
hour that matters, and it still looks complete. If someone asks whether a
dashboard like this is worth building for a client, the answer is the
standard one — only if someone will actually look at it on a schedule, not
because it's now cheap to build — but say that as a side note, not the
point of this demo.

**Debrief.** It looks complete. It answers nothing.
- Every tile is true and none of them says why the lunch hour is different
- A dashboard can be honest tile by tile and still miss the whole point
- The gap the room just felt, in "Open cold," was never in the data

**Why this exists.** Not because someone will use it — because it proves the
gap was in the argument, not the numbers.

---

## Demo 4 · Skills-based creation of the storytelling page

**Setup, before it runs.** Writing the client-facing page. Turning the
finding into the page you would actually send, using a skill that holds our
structure.

**What to watch**
- The five beats, applied by the skill: belief, question, reveal, mechanism,
  decision
- Every number pinned to its source
- Same structure whoever runs it

**While the sceptic runs.** Anyone can find a correlation in twenty seconds
now. What a client pays you for is being able to say what else you ruled
out, because that is the first question a sceptical partner asks.

**What should appear.** The pattern holds across all six months and all five
weekdays. The alternative explanations get tested rather than waved away.
And the honest limit: a call log records the call, not the caller, so the
recovered figure is a ceiling rather than a forecast.

**If the sceptic agrees with everything, say so out loud.** A verifier that
never fails is not checking anything.

**While the storywright runs, and after.** Open the template beside the
finished page. Left side has the placeholders. Right side has the rendered
sentence. Nobody typed a number into the right side. That is the entire
method in one screen.

**The close.** Scroll to the receipts. Every figure, its method, its
sources, its sample size. Ask who in the room could produce that for the
last analysis they sent a client.

**Debrief.** The writing is generated. The numbers are not.
- Figures are substituted in, never typed by the model
- A check recomputes them before it goes out
- This is the part that makes it safe to send

**Why it holds up.** This is the artefact the client keeps. Everything
before it was how we got here.

---

## The framework

Open `.claude/`. Three skills, three subagents (`data-profile`,
`fact-ledger`, `story-craft`; `analyst`, `sceptic`, `storywright`), and not
one of them mentions a clinic, a call or a client. Read one aloud.

(`dashboard-craft` and `dashwright` are a separate pair, used only to build
the Demo 3 prop offstage before the room. They are not part of this count.)

**Be precise about what generalises and what doesn't.** Profile, Compute and
the sceptic genuinely do: fresh code, fresh ledger, fresh verdict, whatever
the question. Composing a finished page doesn't, not with this pipeline —
`story.template.html` is one specific, hand-written page, and reusing it for
a different question would silently show new numbers next to old, unrelated
prose. Say that limit out loud rather than let the room assume otherwise;
it's a more honest and more interesting claim than "everything generalises."

Then run the second case (profile, compute, sceptic only — see
`prompts/DEMO.md`). Same prompts, different question, and it works without
anyone rewriting anything, up to the point where a finished page would need
writing.

That is the moment the session stops being a demo.

---

## If something goes wrong

**A generation stalls.** "Let me show you the one I ran this morning." Open
`fallback/story.html`. Keep talking. Do not wait, do not apologise, do not
debug on screen. Debugging live teaches nothing and costs four minutes.
`fallback/dashboard.html` is the same insurance for the cold open, in case
`output/dashboard/` ever gets touched by accident.

**A connector fails.** Skip it. Nothing in the pipeline depends on one.
Point at the architecture map instead and make the same point in words.

**You are running short.** Cut the second case and describe it. The ledger
and the receipts are the teaching content. Everything else is proof.
