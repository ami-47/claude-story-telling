# Runbook

For whoever is driving. Everything below is what to do and what to say, in order.

## Before the room

    python3 generate_calls.py --seed 42
    python3 verify_calls.py
    python3 build_story.py

Run all four demo prompts once yourself and keep the outputs. If a stage stalls
live, open the saved one and carry on talking. Nobody can tell.

Have `output/story.html`, `arch/pipeline.html` and `prompts/DEMO.md` open in
tabs before you start. Copy each prompt from the DEMO.md tab, never retype one
from memory.

---

## Open cold

Scroll `output/story.html` end to end, saying almost nothing. Then ask the room one
question: **what would you do on Monday?**

Then show the same numbers as a conventional dashboard. Same facts, and nobody
can answer. That contrast is the argument for the whole session and it takes
ninety seconds.

---

## Stage 1 · Profile

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

## Stage 3 · Attack

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

**What to point at.** Open the template beside the finished page. Left side has
the placeholders. Right side has the rendered sentence. Nobody typed a number
into the right side.

That is the entire method in one screen.

**The close.** Scroll to the receipts. Every figure, its method, its sources, its
sample size. Ask who in the room could produce that for the last analysis they
sent a client.

---

## The framework

Open `.claude/`. Three skills, three subagents. Read one of them aloud and point
out that it mentions no clinic, no calls and no client.

Then run the second case. Same four prompts, different question, and it works
without anyone rewriting anything.

That is the moment the session stops being a demo.

---

## If something goes wrong

**A generation stalls.** "Let me show you the one I ran this morning." Open the
saved output. Keep talking. Do not wait, do not apologise, do not debug on
screen. Debugging live teaches nothing and costs four minutes.

**A connector fails.** Skip it. Nothing in the pipeline depends on one. Point at
the architecture map instead and make the same point in words.

**You are running short.** Cut the second case and describe it. The ledger and
the receipts are the teaching content. Everything else is proof.
