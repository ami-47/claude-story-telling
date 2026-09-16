# Runbook

For whoever is driving. Everything below is what to do and what to say, in
order, kept in sync with the deck by hand. If this and the deck ever
disagree, the deck is right, and this file should be corrected to match it.

Twenty six slides, roughly two hours.

    Movement one · Why this matters          ~20 min · no terminal · Slides 01-08
    Movement two · Getting at the data       ~14 min · no terminal · Slides 09-12
    Movement three · Build it from the ground up  ~50 min · terminal on screen · Slides 13-20
    Movement four · What you keep            ~22 min · off the terminal · Slides 21-24
    Close                                     ~6 min · Slides 25-26

This runbook covers the driving of Movement three (the live build) and the
Open cold / framework beats either side of it. What to say for the
slides-only movements lives in the deck's own speaker notes.

## Before the room

    python3 generate_calls.py --seed 42
    python3 verify_calls.py
    python3 build_story.py

Then build the cold-open dashboard once, offstage, with prompt 0 in
`prompts/DEMO.md` (uses the `dashwright` agent and the `dashboard-craft`
skill). It writes to `output/dashboard/dashboard.html`. Rebuilding it live
in front of the room is not the point; the story build is the live moment,
the dashboard is a prop that has to already exist.

**Local files stay in the repo either way.** Supabase is an additional live
stage layered on top of the same verified facts, not a replacement for the
local pipeline: `data/*.csv` and `answers/facts.json` are what the database
was loaded from, prompts 1 to 4 all read and write them directly, and they
are the backup if the database, the network or the MCP auth misbehaves in
front of the room. If Supabase is unreachable on the day, skip stage 2b and
run the rest exactly as written; nothing else in the session depends on it.

If you are using the Supabase stage, open the project dashboard the day before
and run one query, or it will have paused. Free projects pause after about
seven days of low activity. Then load it:

    python3 load_to_supabase.py

Authenticate the MCP server once, in a normal terminal, not an IDE extension:

    claude
    /mcp

Select supabase, then Authenticate. A browser opens. No token needed.

Run all four demo prompts once yourself. When the page is finished, copy
`output/story.html` and `output/story.artifact.html` into `fallback/` before
you touch anything again — `output/` gets overwritten by every later build, so
`fallback/` is the only copy that survives a stall.

Have `output/story.html`, `output/dashboard/dashboard.html`,
`arch/pipeline.html` and `prompts/DEMO.md` open in tabs before you start.
Copy each prompt from the DEMO.md tab, never retype one from memory.

---

## Open cold
`Slide 01, before slide one` · about 90 seconds, no explanation first

Four steps, in this order, matching the deck exactly:

    1 · Open output/story.html. Scroll it end to end. Say nothing.
    2 · Ask: what would you do on Monday?
    3 · Open output/dashboard/dashboard.html. Same data, same build.
    4 · Ask again. Let the silence sit.

Do not explain what they are looking at before they look at it. The story
gives them enough to answer step 2. The dashboard, built from the identical
ledger, does not, and the point is that the gap is not in the data, it is in
the argument. Do not rescue the silence after step 4.

---

## Stage 1 · Profile
`Slide 14`

**While it runs.** This is the step everyone skips. You have a client waiting,
so you go straight to the answer, and three weeks later somebody finds the join
dropped four hundred rows and the engagement is suspect. Profiling costs one
prompt.

**The beat to land.** Point at the trailing whitespace on the line names and the
duplicated call ids. Neither produces an error. Pandas does not warn you. The
rows simply vanish and every number downstream is quietly wrong.

Ask the room how they would have caught it.

---

## Stage 2 · Compute
`Slide 15`

**While it runs.** A model that writes a percentage into a sentence is
generating digits. It might be right. You cannot tell by reading it, and neither
can your client. That is why code computes and the ledger stores.

**What should appear.** Roughly one call in seven never reaches a person, and it
is not spread evenly. Around 54 percent inside the lunch hour against about 7
percent outside it, with the whole day's damage concentrated in that one window.

**If it declares a service line or a channel catastrophic, let it sit.** Ask the
room what they would do about it. Then reveal the sample size. That beat sells
stage three better than any explanation of stage three.

---

## Stage 2b · Into the database
`Slide 16` · optional, skip it entirely if Supabase is asleep or the wifi is bad

**Why it is here.** Everything so far produced an answer. This produces a source
the practice can keep asking. It is also the only place in the session where the
third architecture is shown rather than described.

**The beat to land.** Open the `v_calls` view and read the definition line out
loud. Unanswered means missed, abandoned or voicemail, written once, in the
database, where everyone hits it.

Then ask the room: how many different definitions of one metric are floating
around your clients right now? That question is why the view matters, and it is
the reason two people in the same firm quote two different numbers.

**What to point at.** The question was in English. The SQL is on screen. The
database did the arithmetic. Nobody wrote a query, and anybody can read one.

**Thirty seconds on security.** Point out that the server is running
**read only** and **scoped to one project**. Claude cannot drop a table here
even if a prompt told it to, and it cannot see any other project on the account.

Then the honest part: the loading earlier used a full database password, which
is unscoped and not revocable per person. For a real client you issue a read
only role for the analyst. Say it, do not dwell. Their IT team will ask first.

**If it fails, skip it.** Nothing downstream depends on this stage. Everything
after it runs from the CSVs exactly as before.

---

## Stage 3 · Attack
`Slide 17`

**While it runs.** Anyone can find a correlation in twenty seconds now. What a
client pays you for is being able to say what else you ruled out, because that
is the first question a sceptical partner asks.

**What should appear.** The pattern holds across all six months and all five
weekdays. The alternative explanations get tested rather than waved away. And
the honest limit: a call log records the call, not the caller, so the recovered
figure is a ceiling rather than a forecast.

**If the sceptic agrees with everything, say so out loud.** A verifier that never
fails is not checking anything.

---

## Stage 4 · Compose
`Slide 18` · the mechanism is Slide 19, the receipts are Slide 20

**What to point at.** Open the template beside the finished page. Left side has
the placeholders. Right side has the rendered sentence. Nobody typed a number
into the right side.

That is the entire method in one screen.

**The close.** Scroll to the receipts. Every figure, its method, its sources, its
sample size. Ask who in the room could produce that for the last analysis they
sent a client.

---

## The framework
`Slide 21` · point it at the folder, not the story page

Open `.claude/`. Three skills, three subagents (`data-profile`, `fact-ledger`,
`story-craft`; `analyst`, `sceptic`, `storywright`), and not one of them
mentions a clinic, a call or a client. Read one aloud. That is the
generalisable pipeline: point it at a different engagement and the same
four stages run.

(`dashboard-craft` and `dashwright` are a separate pair, used only to build
the cold-open prop offstage before the room, per Slide 01. They are not part
of this count and not part of what "runs on a different client's data.")

Then run the second case (`Slide 22`). Same four prompts, different question,
and it works without anyone rewriting anything.

That is the moment the session stops being a demo.

---

## If something goes wrong

**A generation stalls.** "Let me show you the one I ran this morning." Open
`fallback/story.html`. Keep talking. Do not wait, do not apologise, do not
debug on screen. Debugging live teaches nothing and costs four minutes.
`fallback/dashboard.html` is the same insurance for the cold open, in case
`output/dashboard/` ever gets touched by accident.

**A connector fails.** Skip it. Nothing in the pipeline depends on one. Point at
the architecture map instead and make the same point in words.

**You are running short.** Cut the second case and describe it. The ledger and
the receipts are the teaching content. Everything else is proof.
