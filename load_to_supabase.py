"""
Push the cleaned data into Postgres.

This runs AFTER the cleaning, not before. That order is the point: the raw
export stays messy on disk so it can be profiled, and the database holds the
version everyone agrees on.

It also creates one view. That view is where the definition of "unanswered"
lives, once, so that nobody redefines it differently in their own query later.
That is the whole idea of a semantic layer, in about six lines of SQL.

    pip install "psycopg[binary]" python-dotenv
    python3 load_to_supabase.py

Reads SUPABASE_DB_URL from .env.
"""

import csv
import os
import sys
from datetime import datetime

try:
    import psycopg
except ImportError:
    sys.exit('pip install "psycopg[binary]" python-dotenv')

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

URL = os.environ.get("SUPABASE_DB_URL", "").strip()
if not URL:
    sys.exit("SUPABASE_DB_URL is not set. Copy .env.example to .env and fill it in.")

SCHEMA = "northgate"
UNANSWERED = ("missed", "abandoned", "voicemail")


def parse_ts(s):
    s = s.strip()
    for f in ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S"):
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    raise ValueError(f"unparseable timestamp: {s!r}")


def clean_calls():
    """The same cleaning verify_calls.py does. One definition, not two."""
    rows, seen, dropped = [], set(), {"duplicate": 0, "test": 0}
    with open("data/calls.csv") as f:
        for r in csv.DictReader(f):
            cid = r["call_id"].strip()
            if cid.startswith("TEST") or r["caller_ref"].strip() == "TESTLINE":
                dropped["test"] += 1
                continue
            if cid in seen:
                dropped["duplicate"] += 1
                continue
            seen.add(cid)
            wait = r["wait_seconds"].strip()
            rows.append((
                cid, parse_ts(r["received_at"]), r["line"].strip(),
                r["caller_ref"].strip(), int(wait) if wait else 0,
                int(r["talk_seconds"] or 0), r["outcome"].strip().lower(),
                r["handled_by"].strip() or None,
            ))
    return rows, dropped


def read(path, cols):
    with open(path) as f:
        return [tuple(r[c].strip() for c in cols) for r in csv.DictReader(f)]


DDL = f"""
create schema if not exists {SCHEMA};

drop view  if exists {SCHEMA}.v_calls;
drop table if exists {SCHEMA}.calls;
drop table if exists {SCHEMA}.rota;
drop table if exists {SCHEMA}.enquiries;
drop table if exists {SCHEMA}.marketing_spend;

create table {SCHEMA}.calls (
  call_id      text primary key,
  received_at  timestamp not null,
  line         text not null,
  caller_ref   text,
  wait_seconds int,
  talk_seconds int,
  outcome      text not null,
  handled_by   text
);

create table {SCHEMA}.rota (
  date        date not null,
  staff_id    text not null,
  name        text,
  shift_start time, shift_end time,
  break_start time, break_end time,
  primary key (date, staff_id)
);

create table {SCHEMA}.enquiries (
  enquiry_id     text primary key,
  created_at     timestamp not null,
  source         text,
  channel        text,
  caller_ref     text,
  became_patient boolean
);

create table {SCHEMA}.marketing_spend (
  month       text not null,
  channel     text not null,
  spend_gbp   numeric,
  impressions int,
  clicks      int,
  primary key (month, channel)
);

-- The agreed definition, written once. Every query uses this view rather than
-- re deciding what "unanswered" means, which is how two people end up quoting
-- two different numbers to the same client.
create view {SCHEMA}.v_calls as
select
  c.*,
  extract(hour from c.received_at) * 60
    + extract(minute from c.received_at)            as minute_of_day,
  c.outcome in ('missed','abandoned','voicemail')   as is_unanswered,
  (extract(hour from c.received_at) * 60
    + extract(minute from c.received_at)) >= 750
  and (extract(hour from c.received_at) * 60
    + extract(minute from c.received_at)) <  810    as in_lunch_window
from {SCHEMA}.calls c;

comment on view {SCHEMA}.v_calls is
  'Unanswered means outcome in (missed, abandoned, voicemail). Lunch window is 12:30 to 13:30.';
"""


def main():
    calls, dropped = clean_calls()
    rota = read("data/rota.csv", ["date", "staff_id", "name", "shift_start",
                                  "shift_end", "break_start", "break_end"])
    enq = [(a, b, c, d, e or None, f == "Y") for a, b, c, d, e, f in
           read("data/enquiries.csv", ["enquiry_id", "created_at", "source",
                                       "channel", "caller_ref", "became_patient"])]
    spend = [(m, ch, float(s), int(i), int(cl)) for m, ch, s, i, cl in
             read("data/marketing_spend.csv", ["month", "channel", "spend_gbp",
                                               "impressions", "clicks"])]

    with psycopg.connect(URL) as conn:
        with conn.cursor() as cur:
            cur.execute(DDL)
            with cur.copy(f"copy {SCHEMA}.calls from stdin") as cp:
                for r in calls:
                    cp.write_row(r)
            with cur.copy(f"copy {SCHEMA}.rota from stdin") as cp:
                for r in rota:
                    cp.write_row(r)
            with cur.copy(f"copy {SCHEMA}.enquiries from stdin") as cp:
                for r in enq:
                    cp.write_row(r)
            with cur.copy(f"copy {SCHEMA}.marketing_spend from stdin") as cp:
                for r in spend:
                    cp.write_row(r)
        conn.commit()

        with conn.cursor() as cur:
            cur.execute(f"select count(*) from {SCHEMA}.v_calls")
            n = cur.fetchone()[0]

    print(f"loaded into schema '{SCHEMA}'")
    print(f"  calls            {len(calls):>6}  "
          f"({dropped['duplicate']} duplicates and {dropped['test']} test rows removed)")
    print(f"  rota             {len(rota):>6}")
    print(f"  enquiries        {len(enq):>6}")
    print(f"  marketing_spend  {len(spend):>6}")
    print(f"  view v_calls     {n:>6}  rows, carrying the agreed definitions")


if __name__ == "__main__":
    main()
