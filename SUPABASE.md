# Adding Supabase

Two separate jobs, two separate mechanisms. Getting this split right is most of
the setup.

| Job | When | How |
|---|---|---|
| **Load** the cleaned tables | Once, before the session | Connection string, `load_to_supabase.py` |
| **Query** them | Live, on stage | Supabase MCP server, read only |

Loading through MCP is not practical: `execute_sql` runs one statement at a
time and there is no bulk path, so nine thousand rows would take thousands of
calls. Querying through a python script is possible but worse on stage, because
an MCP tool call is visible and legible where a script is not.

---

## Part one, loading, once

### 1, get the connection string

Supabase dashboard, your project, **Connect** at the top of the page.

Choose **Session pooler**, not Direct. Direct connections are IPv6 only unless
you pay for the IPv4 add on, and most laptops and nearly all conference wifi are
IPv4. The session pooler is IPv4 on every plan including free. Port 5432.

    postgresql://postgres.abcdefghijklm:YOUR-PASSWORD@aws-0-eu-west-2.pooler.supabase.com:5432/postgres

### 2, put it in .env

    cp .env.example .env

Paste it after `SUPABASE_DB_URL=`. Percent encode any `@`, `:` or `/` in the
password. `.env` is already gitignored.

### 3, install and load

    pip install "psycopg[binary]" python-dotenv
    python3 generate_calls.py --seed 42     # if you have not already
    python3 load_to_supabase.py

Four row counts and a view count means it worked. Go and look in the table
editor: there is now a `northgate` schema.

---

## Part two, querying, live

`.mcp.json` is already in this folder, pointed at our own Supabase project ref,
so the instructor does not have to edit anything before the session. It points
at the remote Supabase MCP server, **read only**, scoped to **one project**,
with only the `database` and `docs` feature groups enabled.

**If you fork this repo for a different client's data, swap the ref.** Open
`.mcp.json` and replace the `project_ref` value with the string in your own
dashboard URL, `dashboard/project/<this bit>`. The ref alone grants no access
by itself, since every person still authenticates separately over OAuth, but
it does identify which project is being pointed at, so treat it the same way
you would any other identifier you'd rather not publish unnecessarily.

### Authenticate, once

In a normal terminal, not an IDE extension:

    claude
    /mcp

Select `supabase`, then Authenticate. A browser opens, you log in, you grant
access. No personal access token needed.

After that the Supabase tools appear in Claude Code automatically whenever it
starts in this folder.

---

## What is in the database, and why

**Four tables**, holding the **cleaned** data. Not the raw export. The raw
export stays messy on disk, because profiling it is the strongest teaching beat
in the session and a clean database would delete it.

**One view, `v_calls`.** This is the part worth the setup. It carries the agreed
definition of unanswered, once:

    c.outcome in ('missed','abandoned','voicemail') as is_unanswered

Every query uses the view instead of re deciding what the metric means. That is
a semantic layer in six lines of SQL, and it answers the question every
consultant eventually hits: why do two people in the same firm quote two
different numbers for the same thing.

---

## Before the session

**Free projects pause after about seven days of low activity.** Opening the
dashboard or running a query counts. Open it the day before, run one query, and
it will be awake. If it has paused, Resume brings it straight back with the data
intact.

---

## Security, worth thirty seconds on stage

**The MCP server is read only and scoped to one project.** Claude cannot drop a
table here even if a prompt told it to, and it cannot see anything else on the
account. Say that out loud, because it is the first thing a client's IT team
asks.

**Supabase's own warning is worth repeating too.** Instructions hidden inside
data a model reads can try to steer it into running queries it should not.
Read only mode and project scoping are what contain that, which is exactly why
both are switched on here.

**The loading credential is different and less safe.** The string in `.env` is a
full database password: unscoped, not read only, not revocable per person. It is
used once, offstage, by a script. For a real client engagement you would issue a
read only role instead:

    create role analyst_ro login password 'something-long';
    grant usage on schema northgate to analyst_ro;
    grant select on all tables in schema northgate to analyst_ro;
