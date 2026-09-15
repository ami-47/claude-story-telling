"""
Northgate Health: reproducible synthetic dataset for the Session 6 demo.

The point of this file is that the dataset is not asserted, it is SIMULATED.
Calls arrive against a rota. A call is answered only if a receptionist is free
at that minute. Nobody types a missed call rate anywhere in this file. The rate
that shows up in the data is whatever the queue produces.

That matters for the session: when a student asks "did you just make the
answer up", the answer is no, and this file is the proof.

Usage
    python3 generate_calls.py --seed 42
    python3 generate_calls.py --seed 42 --clean     (no messiness, for checking)

Outputs into data/
    calls.csv             raw phone system export, deliberately messy
    rota.csv              who was on reception, and when
    enquiries.csv         web and phone enquiries from the CRM
    marketing_spend.csv   monthly ad spend by channel
    _meta.json            seed, version, row counts
"""

import argparse
import csv
import json
import random
from datetime import date, datetime, timedelta

VERSION = "1.0"

START = date(2026, 1, 5)
END = date(2026, 6, 30)

BANK_HOLIDAYS = {
    date(2026, 4, 3), date(2026, 4, 6),
    date(2026, 5, 4), date(2026, 5, 25),
}

OPEN_MIN = 8 * 60          # 08:00
CLOSE_MIN = 18 * 60        # 18:00

LINES = ["Main", "New Patients", "Billing"]
LINE_WEIGHTS = [0.52, 0.36, 0.12]

# Reception rota. This is the mechanism. Three of the four take their break at
# the same time, which is also the busiest hour of the day for inbound calls.
SHIFTS = [
    # staff_id, name, shift start, shift end, break start, break end
    ("R01", "Priya Nandakumar", 8 * 60, 16 * 60 + 30, 12 * 60 + 30, 13 * 60 + 30),
    ("R02", "Tom Beckett", 8 * 60, 16 * 60 + 30, 12 * 60 + 30, 13 * 60 + 30),
    ("R03", "Hannah Osei", 9 * 60 + 30, 18 * 60, 12 * 60 + 30, 13 * 60 + 30),
    ("R04", "Marco Ferreira", 9 * 60 + 30, 18 * 60, 13 * 60 + 30, 14 * 60 + 30),
]


def working_days():
    d = START
    while d <= END:
        if d.weekday() < 5 and d not in BANK_HOLIDAYS:
            yield d
        d += timedelta(days=1)


def arrival_weight(minute):
    """
    Relative call volume by minute of day. Two things drive the shape:
    the morning rush when the clinic opens, and the lunchtime spike, because
    patients ring their clinic during their own break. The lunch spike is the
    whole reason this dataset has a story in it.
    """
    h = minute / 60.0
    w = 0.25
    # morning rush, 08:30 to 11:00
    w += 1.05 * gauss_bump(h, 9.6, 1.05)
    # lunchtime spike, 12:30 to 13:30
    w += 1.25 * gauss_bump(h, 13.0, 0.38)
    # smaller end of day bump
    w += 0.55 * gauss_bump(h, 16.6, 0.85)
    return w


def gauss_bump(x, mu, sigma):
    return pow(2.718281828, -((x - mu) ** 2) / (2 * sigma * sigma))


def build_day_minutes(rng, n_calls):
    minutes = list(range(OPEN_MIN, CLOSE_MIN))
    weights = [arrival_weight(m) for m in minutes]
    return sorted(rng.choices(minutes, weights=weights, k=n_calls))


def staff_free_at(minute):
    """Receptionists on shift and not on break at this minute."""
    out = []
    for sid, _name, s, e, bs, be in SHIFTS:
        if s <= minute < e and not (bs <= minute < be):
            out.append(sid)
    return out


def handle_seconds(rng, line):
    """Talk time. New patient calls take longer, they are taking details."""
    base = {"Main": 190, "New Patients": 305, "Billing": 240}[line]
    v = rng.lognormvariate(0, 0.45) * base
    return int(max(35, min(1500, v)))


def simulate_day(rng, day, call_seq):
    """
    Discrete event queue. Each receptionist is busy until a release minute.
    A call is answered if someone is free, rings out to voicemail if the
    caller waits, or is abandoned if they hang up first.
    """
    n = max(40, int(rng.gauss(74, 9)))
    if day.weekday() == 0:
        n = int(n * 1.18)          # Monday is always heavier
    if day.weekday() == 4:
        n = int(n * 0.92)

    busy_until = {sid: -1 for sid, *_ in SHIFTS}
    rows = []

    for minute in build_day_minutes(rng, n):
        line = rng.choices(LINES, weights=LINE_WEIGHTS)[0]
        on_duty = staff_free_at(minute)
        free = [s for s in on_duty if busy_until[s] <= minute]

        call_seq[0] += 1
        cid = f"C{call_seq[0]:06d}"
        caller = f"P{rng.randint(1, 4200):05d}"

        if free:
            who = rng.choice(free)
            wait = int(abs(rng.gauss(9, 7)))
            talk = handle_seconds(rng, line)
            busy_until[who] = minute + (wait + talk) / 60.0 + rng.uniform(0.5, 2.0)
            outcome = "answered"
        else:
            who = ""
            talk = 0
            # nobody free. Caller either hangs up quickly or waits out the ring.
            if rng.random() < 0.46:
                outcome = "abandoned"
                wait = int(abs(rng.gauss(22, 14)))
            else:
                outcome = "voicemail"
                wait = int(abs(rng.gauss(51, 16)))

        ts = datetime.combine(day, datetime.min.time()) + timedelta(
            minutes=minute, seconds=rng.randint(0, 59)
        )
        rows.append({
            "call_id": cid,
            "received_at": ts,
            "line": line,
            "caller_ref": caller,
            "wait_seconds": wait,
            "talk_seconds": talk,
            "outcome": outcome,
            "handled_by": who,
        })
    return rows


def messy(rng, rows):
    """
    Make the export look like a real export. Every item here is something a
    phone system genuinely does, and every one of them changes the answer if
    you do not deal with it.
    """
    out = []
    for r in rows:
        r = dict(r)

        # 1. outcome casing is inconsistent across firmware versions
        if rng.random() < 0.30:
            r["outcome"] = r["outcome"].upper()
        elif rng.random() < 0.30:
            r["outcome"] = r["outcome"].capitalize()

        # 2. two timestamp formats, the export changed halfway through March
        if r["received_at"].date() < date(2026, 3, 16):
            r["received_at"] = r["received_at"].strftime("%d/%m/%Y %H:%M:%S")
        else:
            r["received_at"] = r["received_at"].strftime("%Y-%m-%d %H:%M:%S")

        # 3. instant pickups export a blank wait rather than a zero
        if r["outcome"].lower() == "answered" and r["wait_seconds"] <= 2:
            r["wait_seconds"] = ""

        # 4. trailing whitespace on the line name
        if rng.random() < 0.08:
            r["line"] = r["line"] + " "

        out.append(r)

    # 5. duplicated rows. The export retried and wrote some calls twice.
    dupes = rng.sample(out, k=int(len(out) * 0.012))
    out.extend([dict(d) for d in dupes])

    # 6. vendor test rows left in the export
    for i in range(3):
        out.append({
            "call_id": f"TEST{i:03d}",
            "received_at": "2026-02-11 03:14:00",
            "line": "Main",
            "caller_ref": "TESTLINE",
            "wait_seconds": 0,
            "talk_seconds": 0,
            "outcome": "answered",
            "handled_by": "SYSTEM",
        })

    out.sort(key=lambda r: r["call_id"])
    return out


# Channel economics. This is the mechanism behind the second story.
# Cheap clicks and expensive patients are not the same thing, and the ranking
# reverses depending on which denominator you use. Nothing here is a target;
# the figures in the analysis are whatever these rates produce.
CHANNELS = {
    #                cpc,  click to enquiry, enquiry to patient
    "Paid search":  (3.10, 0.055, 0.34),
    "Paid social":  (1.35, 0.028, 0.12),
    "Directories":  (2.40, 0.085, 0.52),
}

# Monthly budget. In April they raised search and social and left directories
# alone, which is the decision the story ends up questioning.
SPEND_PLAN = {
    1: {"Paid search": 5200, "Paid social": 2100, "Directories": 900},
    2: {"Paid search": 5400, "Paid social": 2050, "Directories": 900},
    3: {"Paid search": 5300, "Paid social": 2200, "Directories": 900},
    4: {"Paid search": 7900, "Paid social": 3100, "Directories": 950},
    5: {"Paid search": 8200, "Paid social": 3250, "Directories": 950},
    6: {"Paid search": 8100, "Paid social": 3300, "Directories": 950},
}


def build_spend(rng):
    rows = []
    for m, plan in SPEND_PLAN.items():
        for channel, spend in plan.items():
            cpc = CHANNELS[channel][0]
            clicks = int(spend / (cpc * rng.uniform(.94, 1.06)))
            rows.append({
                "month": f"2026-{m:02d}", "channel": channel,
                "spend_gbp": spend,
                "impressions": int(clicks * rng.uniform(22, 31)),
                "clicks": clicks,
            })
    return rows


def build_enquiries(rng, call_rows, spend_rows):
    """
    Two routes in. Paid clicks become web enquiries at a rate that differs by
    channel, and answered calls on the New Patients line become phone enquiries.
    Phone enquiries carry a channel too, because a patient who saw the ad and
    then rang is still that channel's patient. That is why the two stories in
    this dataset are connected rather than separate.
    """
    rows = []
    n = 0

    def add(created, source, channel, caller, patient):
        nonlocal n
        n += 1
        rows.append({
            "enquiry_id": f"E{n:05d}", "created_at": created,
            "source": source, "channel": channel, "caller_ref": caller,
            "became_patient": "Y" if patient else "N",
        })

    days = list(working_days())
    by_month = {}
    for d in days:
        by_month.setdefault(d.strftime("%Y-%m"), []).append(d)

    # web enquiries, derived from paid clicks
    for r in spend_rows:
        ch = r["channel"]
        _cpc, to_enq, to_pat = CHANNELS[ch]
        month_days = by_month.get(r["month"], days)
        for _ in range(int(r["clicks"] * to_enq)):
            d = rng.choice(month_days)
            add(f"{d.isoformat()} {rng.randint(8,21):02d}:{rng.randint(0,59):02d}",
                "Web form", ch, "", rng.random() < to_pat)

    # organic and referral. Referral is deliberately tiny and converts well,
    # so it tops any ranking that ignores sample size.
    for d in days:
        for _ in range(rng.randint(1, 4)):
            add(f"{d.isoformat()} {rng.randint(8,21):02d}:{rng.randint(0,59):02d}",
                "Web form", "Organic", "", rng.random() < 0.29)
        if rng.random() < 0.16:
            add(f"{d.isoformat()} {rng.randint(8,21):02d}:{rng.randint(0,59):02d}",
                "Referral", "Referral", "", rng.random() < 0.63)

    # phone enquiries, capped by who actually got through
    weights = [CHANNELS[c][0] for c in CHANNELS]
    names = list(CHANNELS)
    for r in call_rows:
        if r["outcome"] != "answered" or r["line"] != "New Patients":
            continue
        if rng.random() >= 0.61:
            continue
        ch = rng.choices(names + ["Organic"], weights=weights + [4.0])[0]
        to_pat = CHANNELS[ch][2] if ch in CHANNELS else 0.29
        add(r["received_at"].strftime("%Y-%m-%d %H:%M"), "Phone", ch,
            r["caller_ref"], rng.random() < to_pat)

    rows.sort(key=lambda r: r["created_at"])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--clean", action="store_true",
                    help="skip the messiness, for checking the simulation")
    ap.add_argument("--out", default="data")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    call_seq = [0]

    raw = []
    for day in working_days():
        raw.extend(simulate_day(rng, day, call_seq))

    rota = []
    for day in working_days():
        for sid, name, s, e, bs, be in SHIFTS:
            rota.append({
                "date": day.isoformat(), "staff_id": sid, "name": name,
                "shift_start": f"{s//60:02d}:{s%60:02d}",
                "shift_end": f"{e//60:02d}:{e%60:02d}",
                "break_start": f"{bs//60:02d}:{bs%60:02d}",
                "break_end": f"{be//60:02d}:{be%60:02d}",
            })

    spend = build_spend(rng)
    enquiries = build_enquiries(rng, raw, spend)
    calls_out = raw if args.clean else messy(rng, raw)

    def write(name, rows, fields):
        with open(f"{args.out}/{name}", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    write("calls.csv", calls_out,
          ["call_id", "received_at", "line", "caller_ref",
           "wait_seconds", "talk_seconds", "outcome", "handled_by"])
    write("rota.csv", rota,
          ["date", "staff_id", "name", "shift_start", "shift_end",
           "break_start", "break_end"])
    write("enquiries.csv", enquiries,
          ["enquiry_id", "created_at", "source", "channel", "caller_ref",
           "became_patient"])
    write("marketing_spend.csv", spend,
          ["month", "channel", "spend_gbp", "impressions", "clicks"])

    with open(f"{args.out}/_meta.json", "w") as f:
        json.dump({
            "version": VERSION, "seed": args.seed, "clean": args.clean,
            "generated": datetime.now().isoformat(timespec="seconds"),
            "rows": {"calls": len(calls_out), "rota": len(rota),
                     "enquiries": len(enquiries), "spend": len(spend)},
            "true_calls_before_messiness": len(raw),
        }, f, indent=2)

    print(f"calls {len(calls_out)} (true {len(raw)}) · rota {len(rota)} · "
          f"enquiries {len(enquiries)} · spend {len(spend)}")


if __name__ == "__main__":
    main()
