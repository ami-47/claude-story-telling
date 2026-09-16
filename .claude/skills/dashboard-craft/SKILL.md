---
name: dashboard-craft
description: The visual rules for the Northgate "conventional dashboard" artifact, the cold-open contrast piece in RUNBOOK.md. Use whenever building or editing output/dashboard/dashboard.html (or a rehearsal/dashboard/ dry run of it). Covers palette, card system, chart form and the honesty rules that stop a dashboard from becoming a mockup.
---

# Dashboard craft

This is a *different artifact* from the story page. `story-craft` governs
`story.template.html`, a scrolling five-beat narrative built once from
`answers/facts.json`. This skill governs the operations dashboard: a single
static screen meant to look like the kind of tool a practice manager already
owns, full of tiles, and answering none of the actual question. That contrast
is the entire teaching point of the cold open. It must look genuinely
competent, not like a straw man.

Read `fact-ledger` before writing a single number. Every figure on this page
still comes from `answers/facts.json` by fact id, same discipline as the
story page: no invented trend arrows, no invented "vs last month", no
invented percentages. If the data does not support a comparison, the tile
does not claim one.

## Colour

Pinned to a two-hue brand kit, teal and green, each carried as a base plus
three lighter tints, exactly like a client-supplied mini brand guide. Not
five unrelated accents: two families, each with its own depth ramp, and
severity or category is signalled by *which tint in the family*, not by
reaching for a new hue.

| Token | Hex | Role |
|---|---|---|
| `--bg` | `#F1F5F3` | page ground |
| `--surface` | `#FFFFFF` | card ground |
| `--line` | `#E7ECE8` | hairline borders |
| `--ink` | `#122420` | text |
| `--ink-2` | `#5B6B60` | secondary text |
| `--teal-1` | `#025864` | base teal, darkest: the one dark KPI tile, sidebar mark, primary buttons, the "up" series in a diverging chart |
| `--teal-2` | `#3D7581` | tint: mid-severity watchlist dots, secondary chart marks |
| `--teal-3` | `#7FA3AC` | tint: muted UI accents, chart gridlines |
| `--teal-4` | `#BFD2D6` | tint: pale badge backgrounds behind `--teal-1` text |
| `--green-1` | `#00D47E` | base bright green, graphics only (bars, rings, dots): fails white-text contrast, never a card fill with text on it |
| `--green-deep` | `#026B44` | the text-safe, dark version of the brand green: the one green KPI tile, status pill text, the "down" series in a diverging chart |
| `--green-tint` | `#CFF4DE` | pale badge background behind `--green-deep` text |

Checked numerically, not by eye: `--teal-1` clears 8.1:1 for white text,
`--green-deep` clears 6.6:1. `--green-1` clears only 2.0:1 against white, so
it is graphics-only: bar fills, the donut ring, dots on a light background,
never a solid tile carrying white text.

Severity or category within one chart or list uses depth, not a new hue:
worst gets `--teal-1`, mid gets `--teal-2`, best gets `--green-1`. That is
still a defensible visual language, it just comes from a shade ramp instead
of a five-colour palette. If a build reaches for anything outside these two
families, that is the rainbow-slop failure this table exists to prevent.

## Layout

- sidebar (fixed, ~230px), search bar, avatar identity block: this is what
  signals "real tool" fastest, more than any single chart does
- KPI row, four tiles: one solid `--teal-1` (the headline total), one solid
  `--green-deep` (the second brand hue, doesn't have to mean "good", the
  brand guide doesn't assign valence to its own colours), two plain white
  tiles with a teal or green accent icon. Never four white tiles, never four
  coloured ones
- an asymmetric content grid (roughly `1.6fr 1fr 1fr`), not a uniform grid of
  equal cards. Uniform grids are what make dashboards look like placeholder
  layouts
- large radius throughout, 18 to 22px on cards, 999px on pills and buttons,
  soft shadow (`0 1px 2px rgba(0,0,0,.04), 0 12px 28px -14px rgba(0,0,0,.14)`),
  never a hard drop shadow

## Chart form

Same discipline as `story-craft`: pick the form by the job.

- **two related counts across a category** (answered vs unanswered, per
  hour) → a **diverging bar**, one series rising from a zero baseline in
  `--teal-1`, the other falling below it in `--green-1`, exactly the
  income-vs-expense cash-flow pattern from a finance dashboard. This is the
  one chart type this dashboard gets right almost by accident, which is part
  of the point: a pretty chart is not the same as an answer, because the
  chart still won't tell you *why* the split happens
- **a single share of a whole** → a ring, exactly as in `story-craft`
- **a list of scoped rates** → a row list with a coloured dot per row, depth
  by severity (`--teal-1` high, `--teal-2` mid, `--green-1` low), never a bar
  chart with five bars of different unrelated denominators sitting on one
  axis, because that silently implies they are comparable

## Content honesty

This page's entire job is to look complete while omitting the thing that
actually matters (the scoped, time-of-day answer). That only works if
everything it *does* show is true:

- every number traces to a real fact id or a direct aggregate of
  `series.by_hour` / `rota.csv`, same as the story page
- team members, shift times and break times come from `data/rota.csv`
  verbatim, never invented
- no fabricated period-over-period comparison. If `facts.json` has no prior
  period, no tile claims a percentage change against one
- a caption states its own scope (`whole period`, `12:30 to 13:30`, `New
  Patients line`) the same way a `data-fact` caption does in the story page,
  because the entire cold-open beat depends on the room being able to later
  ask "which of these tiles actually says what happened at lunch" and get a
  real answer: none of them

## Before calling a build finished

Run both scanners and read the result, don't just trust the exit code:

    python3 ~/.claude/skills/tastemaker/scripts/anti_slop_scan.py output/dashboard/dashboard.html
    python3 ~/.claude/skills/tastemaker/scripts/audit_motion.py output/dashboard/dashboard.html

(a rehearsal build not meant to overwrite the real one goes under
`rehearsal/dashboard/` instead, same two commands, different path)

Then screenshot it yourself (Playwright, full page, real viewport width, not
just a static wait) and look at the image before reporting anything as
finished. Count the hue families: exactly two, teal and green, not a third
accent (an amber, a coral, a purple) quietly introduced in a chart or a
badge that the table above doesn't name.
