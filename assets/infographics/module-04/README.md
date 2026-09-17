# Module 4 infographics

Four self-contained, interactive HTML pages, no server needed, open any of
them directly in a browser. Linked from `lectures/dsca-module-04.html`'s
speaker notes (slides 5, 6, 8, and 10) and from its own "Before Module 5"
reading list (slide 23), so students in self-study mode can reach them too.

- `zep-graphiti.html`, the temporal knowledge graph mechanism (Zep).
- `mem0.html`, the extract-and-update mechanism (Mem0).
- `secom.html`, segment-then-compress compaction (SeCom).
- `memory-techniques-comparison.html`, all three side by side.

## Where these came from

Each one was fact-checked directly against its source paper (all three are
in `research/module-04/`) before being linked into the course. One error
was found and fixed in each of the first three:

- `zep-graphiti.html`: the ">100% gain" the original caption attributed to
  "cross-session synthesis" was actually the paper's single-session-
  preference category, a 184% gain with GPT-4o. Caption corrected.
- `mem0.html`: two fixes. The search-latency chart mixed Zep's total
  latency (1.29s) into a chart of median search latency (corrected to
  0.51s, with Mem0's own bar corrected to 0.15s to match, and the bars
  resized proportionally). The LOCOMO accuracy panel paired Mem0's
  per-category score (67.1%, Single-Hop) against Zep's whole-dataset
  average; corrected to Mem0's own whole-dataset average (66.9%) for a
  fair comparison.
- `secom.html`: the caption claimed full-history replay "still scores
  lowest" on LOCOMO; the paper's own Table 1 has two lower scores (Zero
  History, Session-Level). Caption corrected to "yet still not the best."
- `memory-techniques-comparison.html` needed no fix: reviewed against all
  three papers and found consistent.

None of these are the paper's own figures; they are built from the papers'
reported numbers. If a paper is revised or a newer version changes a cited
number, re-verify against it before trusting these again.
