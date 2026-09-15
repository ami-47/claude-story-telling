---
name: data-profile
description: Profile a folder of client data files before any analysis. Use whenever you are handed CSVs, spreadsheets or an export and asked a question about them. Produces a written profile of every column, every join risk and every row that is not a real transaction. Always run this before answering anything.
---

# Profile before you answer

You have been handed data you did not create. You do not yet know what is in it.
Answering first and checking later is how an engagement gets embarrassed three
weeks in. This skill costs one pass and removes that risk.

## Do not analyse anything in this pass

No totals, no rates, no findings. If you notice a pattern, write it down for
later and keep profiling. The deliverable here is a description of the data, not
an answer about it.

## For every file

Report, in a table:

- row count, column count
- every column: name, inferred type, how many blanks, how many distinct values
- for text columns: the three most common values, and whether any value has
  leading or trailing whitespace
- for date columns: **every distinct format present**, not just the first one
- for numeric columns: min, max, and whether any are stored as text because of
  a currency symbol, thousands separator or comma decimal

## Then answer these six questions explicitly

1. **Can these files be joined?** On which key, and what is the row count before
   and after a naive inner join? Name the rows that would be silently dropped.
2. **Are there duplicate rows or duplicate keys?** How many, and are they exact
   copies or genuine repeats?
3. **Is anything here not a real transaction?** Subtotal rows, test rows written
   by a vendor, adjustment or reversal rows, placeholder records.
4. **Are any categories the same thing under two names?** Trailing whitespace,
   casing, an old code and a new code for one entity, a renamed team.
5. **What is the time span, and is it complete?** Missing weeks, a partial first
   or last month, a format change part way through.
6. **What is small?** Any category holding under five percent of the base. Name
   them now, so that no one is surprised later when one of them tops a ranking.

## Finish with a risk list

One line each, ordered by how much damage it would do if missed. For each, say
what the correct handling is, and flag the ones that produce **no error** if
handled wrongly. Those are the dangerous ones. A join that crashes gets fixed. A
join that quietly drops four hundred rows does not.
