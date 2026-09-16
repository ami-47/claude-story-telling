# Session 6 · From client data to a defensible story

Everything needed to run the live build, in one folder.

## What is here

    data/                 four raw client files, deliberately messy
    generate_calls.py     rebuilds them from a seed, reproducibly
    verify_calls.py       the answer sheet, writes answers/facts.json
    build_story.py        substitutes the ledger into the page template
    story.template.html   the page, holding placeholders, containing no numbers
    arch/pipeline.html    the architecture map
    .claude/skills/       data-profile · fact-ledger · story-craft · dashboard-craft
    .claude/agents/       analyst · sceptic · storywright · dashwright
    prompts/DEMO.md       the four live prompts, plus the offstage cold-open build
    RUNBOOK.md            what to type, what to say, what to do if it stalls
    output/               where every build lands, overwritten every run
    output/dashboard/     the cold-open dashboard, built offstage, once
    fallback/             a saved copy of a working build, never overwritten
    rehearsal/dashboard/  proof-of-concept dry runs only, not the real prop
    load_to_supabase.py   pushes the cleaned tables into Postgres, optional
    SUPABASE.md           ten minute setup for the database stage

## Running it

    cd northgate
    python3 generate_calls.py --seed 42
    python3 verify_calls.py
    python3 build_story.py
    open output/story.html

Then start Claude Code in this folder. It reads `.claude/` at session start, so
the skills and subagents are live immediately.

## The point of the folder

Nothing in `.claude/` mentions clinics, calls, or Northgate. Point it at a
different client's data and the same four stages run. That is the deliverable.
The story page is only the proof that it works.

## A note on the data

It is synthetic and it is simulated, not asserted. `generate_calls.py` runs a
queue: calls arrive against the rota, and a call is answered only if a
receptionist is free that minute. No missed call rate is written anywhere in it.
Whatever rate the analysis finds is whatever the queue produced.
