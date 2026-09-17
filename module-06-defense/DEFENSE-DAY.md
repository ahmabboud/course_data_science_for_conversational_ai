# Module 6, the defense day

Module 6 has no lecture deck. It is a live session: each team defends a
working baseline reproduction plus their own novel extension of one
paper, per `PROJECT-REDESIGN.md`. This document is the instructor's own
run-of-show for that day. `scoring-sheet.xlsx` in this same folder is the
fillable rubric and running schedule that goes with it.

The actual number of teams is not fixed. The syllabus's own front matter
says the cohort runs 12 to 21 participants, in 6 to 7 teams of 2 to 3; the
example below uses 8 rows so it comfortably covers that range with room
to spare, not because 8 is the expected count. The instructor's own call
for this session is: run the normal 180-minute block, and use up to 1
more hour if the actual number of teams needs it, rather than compressing
any team's 12 minutes presenting or 12 minutes of questions to fit a
fixed total. Do not chase an exact reconciled minute count the way the
lecture modules do, this session's real constraint is teams times 24
minutes, and that number is not known until teams are finalized.

## The schedule, an adjustable example

| # | Segment | Duration | Planned start | Planned end |
|---|---|---|---|---|
| 1 | Opening and instructions | 15 min | 9:00 | 9:15 |
| 2 | Team 1: present (12) and Q&A (12) | 24 min | 9:15 | 9:39 |
| 3 | Changeover | 3 min | 9:39 | 9:42 |
| 4 | Team 2: present (12) and Q&A (12) | 24 min | 9:42 | 10:06 |
| 5 | Changeover | 3 min | 10:06 | 10:09 |
| 6 | Team 3: present (12) and Q&A (12) | 24 min | 10:09 | 10:33 |
| 7 | Changeover | 3 min | 10:33 | 10:36 |
| 8 | Team 4: present (12) and Q&A (12) | 24 min | 10:36 | 11:00 |
| 9 | Break | 15 min | 11:00 | 11:15 |
| 10 | Team 5: present (12) and Q&A (12) | 24 min | 11:15 | 11:39 |
| 11 | Changeover | 3 min | 11:39 | 11:42 |
| 12 | Team 6: present (12) and Q&A (12) | 24 min | 11:42 | 12:06 |
| 13 | Changeover | 3 min | 12:06 | 12:09 |
| 14 | Team 7: present (12) and Q&A (12) | 24 min | 12:09 | 12:33 |
| 15 | Changeover | 3 min | 12:33 | 12:36 |
| 16 | Team 8: present (12) and Q&A (12) | 24 min | 12:36 | 13:00 |
| 17 | Instructor deliberation and score reconciliation | 15 min | 13:00 | 13:15 |
| 18 | Course close | 15 min | 13:15 | 13:30 |

This example, all 8 rows used, totals 270 minutes, 90 minutes past the
180-minute base, more than the "up to 1 hour" the instructor asked for.
That is the point of showing it at full size: even the top of the
syllabus's own stated range needs real judgment on the day, not a fixed
plan. With 6 teams instead of 8, delete two team rows and their
changeovers and the total drops to about 210 minutes, comfortably inside
1 extra hour. Delete or add rows in `scoring-sheet.xlsx`'s Schedule tab
to match your actual team count; the planned-start and planned-end
columns recalculate automatically from whatever start time you enter, and
there is an Actual start column to fill in live if the day runs ahead or
behind.

A changeover sits between every pair of teams except across the break,
which already serves that purpose. 3 minutes is enough to swap a laptop
or a screen-share link and reset the timer, not enough to debug a demo
that will not run, so confirm with each team beforehand (per the
`PROJECT-REDESIGN.md` deliverables list) that their slides, repository,
and report are already submitted and their demo, if any, is already
working before this day starts.

## Running each team's slot

- **12 minutes presenting.** The team's own cover, up to 6 content
  slides, and references slide, per the slide cap in
  `PROJECT-REDESIGN.md` and `dsca-team-template/slides/README.md`. Hold
  them to it, a team that runs long eats into their own Q&A time, not the
  schedule's.
- **12 minutes of questions.** Any of the three teammates can be asked
  about any part, the baseline paper, the extension, or the code, per the
  redesign's own shared-ownership rule. Spread questions across all three
  teammates deliberately, do not let one person answer everything.
  Good questions to have ready, one per rubric sub-criterion: ask one
  teammate to explain the baseline paper's method without looking at
  slides; ask another what a full-scale validation run would require if
  the team used a smoke test; ask a third what published follow-up work
  on the same baseline they found and how their idea differs from it.

## Scoring

Use `scoring-sheet.xlsx`'s Scoring tab, one row per team, four 25-point
sub-scores (code and reproduction quality, depth of understanding,
motivation and value, result quality), matching `PROJECT-REDESIGN.md`'s
50/50 rubric exactly. The Rubric tab in the same workbook gives four
scoring bands per sub-criterion, since the redesign document names the
criteria but does not fix band language on its own.

Score right after each team's slot, while the defense is fresh, rather
than waiting until every team is done. The sheet's Total and Rank columns
recalculate automatically as you go.

## Before this day

Confirm, per team, before the day starts:

- Idea pitch was approved (should already be true well before Module 6).
- Slides, repository, and report were all submitted in advance, per
  `PROJECT-REDESIGN.md`'s deliverables list, not walked in with on the
  day.
- Any live demo a team plans to run during their 12 minutes has been
  smoke-tested by the team beforehand; this day's schedule has no slack
  for first-time debugging.

Have `research/PROJECT-PAPER-MENU.md` open for reference during Q&A, in
case a question comes up about a paper's own known repository or compute
profile that a team's pitch or report referenced.

## After this day

Grades are not necessarily announced the same day; `PROJECT-REDESIGN.md`
and the syllabus's own Assessment section govern when and how. What this
document's schedule protects is that every team gets an equal, real
defense inside one session, extended by up to an hour if that is what it
takes, rather than a compressed or uneven one.
