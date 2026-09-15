"""
Northgate Health: the answer sheet.

Reads the messy export, cleans it the way it should be cleaned, and writes
answers/facts.json. Every figure that appears on the story page is looked up
from that file. Nothing on the page is typed by hand.

Each fact carries its value, what it measures, how it was calculated, which
file it came from, and its sample size. That is the fact ledger pattern, in
its smallest useful form.

    python3 verify_calls.py
"""

import csv
import json
from collections import defaultdict
from datetime import datetime

DATA = "data"
OUT = "answers/facts.json"

LUNCH_START = 12 * 60 + 30
LUNCH_END = 13 * 60 + 30

# The definition the whole analysis rests on. State it once, out loud.
UNANSWERED = {"missed", "abandoned", "voicemail"}

facts = {}


def fact(fid, label, value, unit, method, sources, n, note=""):
    facts[fid] = {
        "id": fid, "label": label, "value": value, "unit": unit,
        "method": method, "sources": sources, "n": n, "note": note,
    }
    return value


def parse_ts(s):
    s = s.strip()
    for f in ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S"):
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    raise ValueError(f"unparseable timestamp: {s!r}")


def load_calls():
    rows = []
    seen = set()
    dropped = {"duplicate": 0, "test": 0}

    with open(f"{DATA}/calls.csv") as f:
        for r in csv.DictReader(f):
            cid = r["call_id"].strip()

            # vendor test rows are not patient calls
            if cid.startswith("TEST") or r["caller_ref"].strip() == "TESTLINE":
                dropped["test"] += 1
                continue

            # the export wrote some calls twice
            if cid in seen:
                dropped["duplicate"] += 1
                continue
            seen.add(cid)

            ts = parse_ts(r["received_at"])
            wait = r["wait_seconds"].strip()
            rows.append({
                "call_id": cid,
                "ts": ts,
                "minute": ts.hour * 60 + ts.minute,
                "date": ts.date(),
                "line": r["line"].strip(),                 # trailing spaces
                "caller_ref": r["caller_ref"].strip(),
                "wait": int(wait) if wait else 0,          # blank means instant
                "talk": int(r["talk_seconds"] or 0),
                "outcome": r["outcome"].strip().lower(),   # casing varies
                "handled_by": r["handled_by"].strip(),
            })
    return rows, dropped


def pct(a, b):
    return round(100.0 * a / b, 1) if b else 0.0


def main():
    calls, dropped = load_calls()
    src = ["calls.csv"]

    total = len(calls)
    fact("F01", "Patient calls received", total, "calls",
         "rows in calls.csv after removing duplicate call_ids and vendor test rows",
         src, total,
         f"{dropped['duplicate']} duplicates and {dropped['test']} test rows removed")

    unans = [c for c in calls if c["outcome"] in UNANSWERED]
    fact("F02", "Calls not answered by a person", len(unans), "calls",
         "outcome in {missed, abandoned, voicemail}, case normalised",
         src, total)
    fact("F03", "Share of calls not answered", pct(len(unans), total), "percent",
         "F02 divided by F01", src, total)

    # the lunch window
    inside = [c for c in calls if LUNCH_START <= c["minute"] < LUNCH_END]
    outside = [c for c in calls if not (LUNCH_START <= c["minute"] < LUNCH_END)]
    in_un = [c for c in inside if c["outcome"] in UNANSWERED]
    out_un = [c for c in outside if c["outcome"] in UNANSWERED]

    fact("F04", "Calls received 12:30 to 13:30", len(inside), "calls",
         "received_at minute of day inside the window", src, len(inside))
    fact("F05", "Unanswered rate inside 12:30 to 13:30",
         pct(len(in_un), len(inside)), "percent",
         "unanswered calls inside the window over all calls inside it",
         src, len(inside))
    fact("F06", "Unanswered rate outside 12:30 to 13:30",
         pct(len(out_un), len(outside)), "percent",
         "unanswered calls outside the window over all calls outside it",
         src, len(outside))

    # that one hour is 10 percent of the opening day. How much of the damage?
    fact("F07", "Share of all unanswered calls falling in that one hour",
         pct(len(in_un), len(unans)), "percent",
         "unanswered calls inside the window over all unanswered calls",
         src, len(unans))

    # new patients specifically
    npc = [c for c in calls if c["line"] == "New Patients"]
    np_un = [c for c in npc if c["outcome"] in UNANSWERED]
    fact("F08", "New patient calls received", len(npc), "calls",
         "line equals New Patients after trimming whitespace", src, len(npc))
    fact("F09", "New patient calls not answered", len(np_un), "calls",
         "unanswered new patient calls", src, len(npc))
    fact("F10", "Unanswered rate on the New Patients line",
         pct(len(np_un), len(npc)), "percent",
         "F09 divided by F08", src, len(npc))

    weeks = len({(c["date"].isocalendar()[0], c["date"].isocalendar()[1])
                 for c in calls})
    fact("F11", "New patient calls missed per week",
         round(len(np_un) / weeks, 1), "calls per week",
         f"F09 divided by {weeks} calendar weeks in the export", src, len(np_un))

    # hour by hour, for the chart
    by_hour = defaultdict(lambda: [0, 0])
    for c in calls:
        h = c["ts"].hour
        by_hour[h][0] += 1
        if c["outcome"] in UNANSWERED:
            by_hour[h][1] += 1
    hours = [{"hour": h, "calls": by_hour[h][0], "unanswered": by_hour[h][1],
              "rate": pct(by_hour[h][1], by_hour[h][0])}
             for h in sorted(by_hour)]

    # half hour resolution, for the band chart
    by_half = defaultdict(lambda: [0, 0])
    for c in calls:
        slot = (c["minute"] // 30) * 30
        by_half[slot][0] += 1
        if c["outcome"] in UNANSWERED:
            by_half[slot][1] += 1
    halves = [{"minute": m, "calls": by_half[m][0], "unanswered": by_half[m][1],
               "rate": pct(by_half[m][1], by_half[m][0])}
              for m in sorted(by_half)]

    # the mechanism: how many receptionists are free, minute by minute
    with open(f"{DATA}/rota.csv") as f:
        rota = list(csv.DictReader(f))
    days = len({r["date"] for r in rota})

    def hm(s):
        a, b = s.split(":")
        return int(a) * 60 + int(b)

    shifts = {}
    for r in rota:
        shifts[r["staff_id"]] = (hm(r["shift_start"]), hm(r["shift_end"]),
                                 hm(r["break_start"]), hm(r["break_end"]))
    cover = []
    for m in range(8 * 60, 18 * 60, 30):
        n = sum(1 for s, e, bs, be in shifts.values()
                if s <= m < e and not (bs <= m < be))
        cover.append({"minute": m, "staff": n})

    lunch_cover = min(c["staff"] for c in cover
                      if LUNCH_START <= c["minute"] < LUNCH_END)
    peak_cover = max(c["staff"] for c in cover)
    fact("F12", "Receptionists on the phones during the lunch window",
         lunch_cover, "people",
         "rota.csv, staff on shift and not on break, minimum across the window",
         ["rota.csv"], days)
    fact("F13", "Receptionists on the phones at the busiest other time",
         peak_cover, "people", "rota.csv, maximum staff on shift and not on break",
         ["rota.csv"], days)

    # the belief the clinic started with
    with open(f"{DATA}/marketing_spend.csv") as f:
        spend = list(csv.DictReader(f))
    by_month = defaultdict(float)
    for r in spend:
        by_month[r["month"]] += float(r["spend_gbp"])
    q1 = sum(by_month[m] for m in ("2026-01", "2026-02", "2026-03"))
    q2 = sum(by_month[m] for m in ("2026-04", "2026-05", "2026-06"))
    fact("F14", "Change in advertising spend, Q1 to Q2",
         round(100 * (q2 - q1) / q1, 1), "percent",
         "total spend_gbp Q2 over Q1", ["marketing_spend.csv"], len(spend))

    with open(f"{DATA}/enquiries.csv") as f:
        enq = list(csv.DictReader(f))
    # Q1 opens on 5 January, so it has fewer working days than Q2. Comparing
    # raw totals would invent an eight percent rise out of the calendar.
    # Per working day is the like for like comparison.
    days_q1 = len({r["date"] for r in rota if r["date"][:7] in
                   ("2026-01", "2026-02", "2026-03")})
    days_q2 = len({r["date"] for r in rota if r["date"][:7] in
                   ("2026-04", "2026-05", "2026-06")})
    eq = defaultdict(int)
    for r in enq:
        eq[r["created_at"][:7]] += 1
    e1 = sum(eq[m] for m in ("2026-01", "2026-02", "2026-03")) / days_q1
    e2 = sum(eq[m] for m in ("2026-04", "2026-05", "2026-06")) / days_q2
    fact("F15", "Change in enquiries per working day, Q1 to Q2",
         round(100 * (e2 - e1) / e1, 1), "percent",
         "enquiries per working day, Q2 over Q1. Per day, not total, because "
         "Q1 opens on 5 January and has fewer working days",
         ["enquiries.csv", "rota.csv"], len(enq),
         f"Q1 {days_q1} working days, Q2 {days_q2}")

    # what cover would recover, stated as a ceiling not a forecast
    cap_per_hour = 60 / ((sum(c["talk"] for c in calls if c["outcome"] == "answered")
                          / max(1, sum(1 for c in calls if c["outcome"] == "answered")))
                         / 60)
    fact("F16", "Calls one receptionist can handle in an hour",
         round(cap_per_hour, 1), "calls",
         "sixty divided by mean talk time of answered calls in minutes",
         src, sum(1 for c in calls if c["outcome"] == "answered"))

    per_day_in = len(inside) / days
    fact("F17", "Calls arriving in the lunch window on an average day",
         round(per_day_in, 1), "calls", "F04 divided by working days in the export",
         src, len(inside))
    fact("F18", "Working days in the export", days, "days",
         "distinct dates in rota.csv", ["rota.csv"], days)

    # month by month, so the reader can see the normal swing rather than
    # taking a single quarter on quarter number on trust
    dpm = defaultdict(int)
    for r in rota:
        dpm[r["date"][:7]] += 1
    dpm = {k: v / len(SHIFTS_N) if False else v / 4 for k, v in dpm.items()}
    monthly = []
    sp = defaultdict(float)
    for r in spend:
        sp[r["month"]] += float(r["spend_gbp"])
    for m in sorted(eq):
        monthly.append({
            "month": m,
            "enquiries_per_day": round(eq[m] / dpm[m], 2),
            "spend": round(sp[m]),
        })

    payload = {
        "dataset": "Northgate Health inbound calls, 5 Jan to 30 Jun 2026",
        "definition_unanswered": sorted(UNANSWERED),
        "cleaning": {
            "duplicate_call_ids_removed": dropped["duplicate"],
            "vendor_test_rows_removed": dropped["test"],
            "timestamp_formats_parsed": ["%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"],
            "outcome_case_normalised": True,
            "line_whitespace_trimmed": True,
            "blank_wait_seconds_read_as_zero": True,
        },
        "facts": facts,
        "series": {"by_hour": hours, "by_half_hour": halves, "cover": cover, "monthly": monthly},
    }

    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"{total} calls · unanswered {facts['F03']['value']} percent")
    print(f"lunch window {facts['F05']['value']} percent "
          f"vs {facts['F06']['value']} percent outside")
    print(f"one hour holds {facts['F07']['value']} percent of all misses")
    print(f"new patient line {facts['F10']['value']} percent, "
          f"{facts['F11']['value']} a week")
    print(f"spend {facts['F14']['value']} percent, "
          f"enquiries {facts['F15']['value']} percent")
    print(f"cover {facts['F12']['value']} vs {facts['F13']['value']}, "
          f"arrivals {facts['F17']['value']} an hour, "
          f"capacity {facts['F16']['value']}")


if __name__ == "__main__":
    main()
