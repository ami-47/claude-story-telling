---
name: story-craft
description: The visual and motion rules for a Snapdrum data story page. Use whenever building or editing an HTML data story, report page or animated chart. Covers type scale, spacing rhythm, easing curves, durations, chart form and the things that must never ship.
---

# Story craft

House rules for a data story page. These are values, not ranges. `cubic-bezier(.23,1,.32,1)`
is not `cubic-bezier(.4,0,.2,1)`, and `0.96` is not `0.95`.

Distilled from `emilkowalski/skills` (motion), `jakubkrehel/skills` (type and
interface), `ConardLi/garden-skills` (Tufte chart recipe) and
`codeswithroh/tastemaker` (spacing rhythm), all MIT licensed, plus the bundled
`dataviz` skill, which is the authority on colour and chart form. Read `dataviz`
before writing the first line of chart code.

## Form comes before colour

Pick the chart by the job, not by habit.

- change over time, two series compared → **lines**, indexed to a common base, with
  the gap between them shaded, because the gap is the story
- one value against a clock or a category → **bars**
- a distribution, or the shape of raw records → **dots**, one mark per record
- the mechanism behind a finding → **two panels sharing one axis**, stacked, the
  second one hanging downward if it is the inverse of the first
- one share of a whole, and only one → **a ring**, the number counting up inside
  it in sync with the stroke. Never a multi slice pie. If there are more than
  two categories to show as parts of a whole, that is bars, not a ring.
- a single headline → **no chart**. Set the number at 90 to 230px and let it carry
  the section on its own.

Never a dual axis. Two measures on different scales become two panels or an index.

## Chart marks

- bars: flat tops, `rx:2`, a 2px surface gap between neighbours, no 3D caps, no
  gradients, no drop shadows
- lines: 2.5px, round caps and joins, 3.5px dots filled with the page ground and
  stroked in the series colour
- gridlines never darker than `rgba(ink,.09)`, dashed `2 4`; the baseline or the
  index line may go to `.22`
- **direct labels at the end of a series instead of a legend box** whenever there
  are four series or fewer
- axis labels in mono at 10 to 11px, muted ink, never the series colour
- `font-variant-numeric: tabular-nums` on every value that changes or is compared
- state the n beside any percentage, and grey plus label anything under five
  percent of the base rather than hiding it

## Colour

`dataviz` covers the general method. This page has its own settled identity on
top of it, pinned here so it stops drifting build to build. Light and warm,
never navy, never dark mode, never the cream paper plus terracotta serif combo
that reads as generated on sight.

| Token | Hex | Role |
|---|---|---|
| `--marble` | `#FBF7F1` | base ground |
| `--marble-2` | `#DEF0E9` | calm and data sections, a light teal wash |
| `--marble-3` | `#FBEED3` | decision sections, a light gold wash |
| `--wash-coral` | `#FCE2D8` | tension sections, a light coral wash |
| `--wash-plum` | `#F3E3EF` | the uncertainty section, a light plum wash |
| `--ink` | `#271C15` | text, warm near black |
| `--ink-2` | `#5B4A3E` | secondary text |
| `--action` | `#E1421F` | the one accent large text and chart marks are allowed |
| `--action-deep` | `#A8330F` | the same accent, darkened, for any small text under 18px |
| `--sea` | `#0B7A62` | secondary series colour |
| `--premium` | `#B9790A` | tertiary series colour, decision charts |
| `--premium-deep` | `#8F5C05` | small text version of the above |

Every wash is light enough that ink clears 4.5:1 against it. Checked
numerically before use, not by eye. A bright accent may sit on large text (24px
or bolder) at the 3:1 large text floor; anything smaller uses the `-deep`
variant of that colour, never the bright one. No section is ever filled solid
with an accent colour, and no section is ever dark.

## Type

| Role | Size | Leading | Weight |
|---|---|---|---|
| Display | clamp(46, 8.4vw, 124) | .92 | 800 |
| Section head | clamp(32, 4.6vw, 62) | 1.04 | 800 |
| Card head | clamp(21, 2.2vw, 28) | 1.15 | 700 |
| Lead | clamp(18, 1.9vw, 23) | 1.5 | 400 |
| Body | 17 | 1.55 | 400 |
| Label, mono | 11 to 12 | 1.4 | 400 to 500 |

- letter spacing: display `-.035em`, section heads `-.025em`, mono labels
  `.18em` with uppercase, body none
- measure capped at 66 characters
- `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs, neither in
  long form
- emphasis is one weight step, never a size change. Never italic, and never a
  second display family used for emphasis. An italic display heading, or a
  word inside one, is one of the most recognisable AI writing tells there is,
  and it has shipped on a real build of this page. Do not repeat it.
- below 18px, weight 400 is the floor
- two families only, three counting mono: one display face for h1, h2, h3 and
  numerals, one body face for everything else, one mono for labels, captions
  and figures. A decorative serif brought in "for one premium line" is the
  fourth family this rule exists to stop. A build has shipped with four
  families before, a display grotesque, an italic serif for emphasis, a body
  sans and a mono. Count the families before calling a build finished.

## Spacing

4px base. Internal spacing is never larger than external spacing: if cards sit
24px apart, each card has at least 24px of padding.

Section padding is weighted by role, not uniform. Connective sections 48 to 64px,
standard 80 to 132px, the question transition and the cover 128 to 192px. Pick one
radius scale and hold it: 4 for chips, 8 for cards. Outer radius equals inner
radius plus padding.

## Motion

```css
--out:   cubic-bezier(.23,1,.32,1);   /* anything entering or leaving */
--inout: cubic-bezier(.77,0,.175,1);  /* something moving on screen */
```

Never `ease-in` on interface. Never the browser's built in `ease-out` on a
deliberate animation.

Durations: press feedback 150ms · a control changing state 150 to 250ms · a
section entering 420ms · a chart drawing itself 950 to 1400ms. Interface stays
under 300ms; a figure that is the content may take longer.

- entry is `opacity` plus `translateY(12px)` plus `blur(4px)`, 100ms between
  groups, 80ms between words when splitting a headline
- exits are shorter than entries, 150ms, `translateY(-12px)`, never a full
  container height and never `scale(.5)`
- press state is `scale(.96)` exactly
- animate `transform` and `opacity` only, plus `stroke-dashoffset` for drawing a
  line and `clip-path` where it genuinely helps. Never width, height, top, left
  or margin
- never `scale(0)` as an entrance on a UI element, a card, a section, a
  callout. Start at `.9` to `.97`. This does not cover a chart mark drawing
  itself: a bar growing from `scaleY(0)` anchored at its own baseline, or a
  line and a ring growing from `stroke-dashoffset`, is the mark being drawn,
  not something entering, and it is exactly what "a chart drawing itself may
  take longer" above is describing. If a reviewer cannot tell your `scale(0)`
  is a chart draw and not an entrance, say so in a comment next to it.
- never `transition: all`. Name the properties

**One shot, not scroll scrubbed.** A section plays its animation once when it
enters the viewport, through an IntersectionObserver at threshold `.3`, and then
stays in its finished state. Scroll driven scrubbing makes a reader hunt for the
frame where the point was visible. Every animated figure carries a **play again**
button so the point can be repeated on demand, which matters when someone is
presenting the page live.

Gate it: `@media (prefers-reduced-motion: reduce)` keeps opacity and drops
transform and blur; hover motion sits inside
`@media (hover:hover) and (pointer:fine)`.

Data the reader is inspecting does not move for decoration. Motion earns its
place by revealing sequence, comparison or scale, and by nothing else.

## Never ship

- a number typed into the page rather than read from the ledger
- a percentage without its n nearby
- `transition: all`, `ease-in` on interface, or `scale(0)` entrances
- a legend where four or fewer series could be labelled directly
- a scroll scrubbed reveal with no way to replay it
- a bar chart of a percentage sharing an axis with a bar chart of money
- a colour that encodes nothing
- an em dash anywhere in shipped copy, including inside a JavaScript string
  used as a placeholder value. Write the word instead ("no change"). This has
  shipped once already, inside a "no recovery this week" placeholder nobody
  thought to check because it was not in the prose.
- an eyebrow on more than roughly a third of the page's sections, numbered or
  not. Numbering ("01 · ...") is the more obvious version of this tell, but
  dropping the number and giving every single section an unnumbered eyebrow
  anyway is the same templated pattern by a different route: a real build has
  done exactly this, all six sections carrying one and none of them numbered,
  which still reads as a formula the moment you count them. If the page needs
  a running sense of place, build one wayfinding element that appears once (a
  rail, a progress dot, a counter) instead of repeating an eyebrow in every
  section head. An eyebrow, numbered or not, is fine on any individual section
  where it earns its place over the heading alone; it is the blanket coverage
  across nearly every section that is the tell, not the eyebrow itself. Count
  them as a fraction of total sections before calling a build finished.

## Before calling a build finished

Read the page back against every bullet in Never ship and the pinned Colour
table above, not just against the section you were just editing. Every item
on that list has shipped for real at least once, each time because it sat
outside whatever the model was focused on at the time: a font count nobody
tallied, a dash inside a string nobody read as copy, a label repeated because
each section looked fine on its own. Count the font families actually loaded.
Grep the built output for the em dash character. Count how many sections
carry a numbered eyebrow. None of these take longer than a minute, and each
one has already been the actual defect in a real build of this page.
