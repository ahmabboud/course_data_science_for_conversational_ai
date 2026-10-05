"""Builds lectures/dsca-project-guide.html, the student-facing project guide."""
import re, sys
sys.path.insert(0, '.')
from lib import *

OUT = "/Users/ahb/Library/Mobile Documents/com~apple~CloudDocs/Documents/Teaching/LebUniv/Data Science for Conversational AI/course_data_science_for_conversational_ai/lectures/dsca-project-guide.html"
TEMPLATE = "https://github.com/ahmabboud/dsca-team-template"
MENU = "../research/PROJECT-PAPER-MENU.md"
slides = []
SEC = "Guide"

def a(href, text): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, text)

# ============================================================== 1 title
slides.append('''<section class="slide slide--night" data-chrome="none" data-label="Title" data-section="Opening" data-minutes="1">
  <div class="slide__body" style="justify-content:space-between">
    <div class="lu-row" style="justify-content:space-between;align-items:flex-start">
      <div class="lu-lockup"><span class="lu-lockup__mark">LU</span><span class="lu-lockup__text"><span class="lu-lockup__name">Lebanese University</span><span class="lu-lockup__unit">Faculty of Sciences · MSc, Master of Research</span></span></div>
      <div class="lu-tag lu-tag--red" style="background:transparent;color:#FF9AA7;border-color:#96122B">Reference deck · for every module</div>
    </div>
    <div class="lu-stack">
      <div class="lu-eyebrow">Data Science for Conversational AI · Team project</div>
      <h1 class="lu-display" style="max-width:24ch">The team project: a guide</h1>
      <p class="lu-lead" style="max-width:46ch">The topics, how to choose a paper, your repository, what to hand in, the defense, and how you are graded. Come back to it any time.</p>
    </div>
    <div class="lu-row" style="justify-content:space-between;font-size:var(--lu-t-caption);color:var(--lu-on-night-2)">
      <span>About an hour to read through · not a timed session</span>
      <span>Press <kbd>&rarr;</kbd> to begin · <kbd>?</kbd> for shortcuts</span>
    </div>
  </div>
  <template data-notes><p>This deck is a reference for students, not a timed lecture. Use it in the Module 1 kickoff for the parts you need (the picture, the topics, choosing a paper, the pitch), and again before Module 6 (the issues, the report, the slides, the defense, the grading). The minutes on each slide only say how long it takes to go through it once.</p></template>
</section>
''')

# ============================================================== 2 the project in one picture
nodes = []
names = ["1. Choose a topic\nand a paper", "2. Idea pitch\n(approved)", "3. Baseline", "4. Extension", "5. Report\nand slides", "6. Defense\nModule 6"]
kinds = ["user", "code", "tool", "model", "data", "user"]
for i, (n, k) in enumerate(zip(names, kinds)):
    nodes.append(N("n%d" % i, n, k, 130 + 240 * i, 100, 200, 96))
edges = [E("e%d" % i, "n%d" % i, "n%d" % (i + 1)) for i in range(5)]
steps = []
for i in range(6):
    show = ["n%d" % i] + (["e%d" % (i - 1)] if i else [])
    steps.append(S(show, ["e%d" % (i - 1)] if i else [], {("n%d" % i): "active"} | ({("n%d" % (i - 1)): "idle"} if i else {})))
sp = spec(1448, 200, nodes, edges, steps)
slides.append(slide(
    "The project in one picture", SEC, 3, "Start here",
    "Choose a paper, reproduce it, add your own idea, defend it",
    flow_walk("The project in one picture", sp, [
        ("Choose", "You form a team of two or three and choose one of five topics and one research paper."),
        ("Pitch", "You write a short <b>idea pitch</b> about your own idea. The instructor approves it before real work starts."),
        ("Baseline", "The <b>baseline</b> is the paper's own method, running on your computer, with at least one of its results reproduced."),
        ("Extension", "The <b>extension</b> is your own new idea, built on top of the baseline and compared with it."),
        ("Hand in", "You write a short report and prepare slides. Your code, report and slides are handed in before Module 6."),
        ("Defend", "At the defense you present for 12 minutes and answer questions for 12 minutes."),
    ]) + callout("Definitions", "<b>Baseline</b>: the starting point you reproduce. <b>Extension</b>: your own improvement or test on top of it. <b>Defense</b>: the session (Module 6) where each team presents and answers questions."),
    '''<p>Three minutes. Walk the six steps left to right. Stress the order: the extension cannot be trusted without the baseline, because you need a number to compare against. There is no shared agent for the whole class any more: each team extends one paper.</p>'''))

# ============================================================== 3 baseline and extension example
bn = [
    N("paper", "The paper\n(for example Gorilla)", "data", 185, 70, 300, 84),
    N("base", "Baseline\nthe authors' method", "code", 560, 70, 290, 84),
    N("a", "Your number A,\nnext to the paper's", "data", 960, 70, 300, 84),
    N("ext", "Extension\nyour own idea", "model", 560, 215, 290, 84),
    N("b", "Your number B", "data", 960, 215, 300, 70),
    N("cmp", "Comparison:\nis B better than A?", "tool", 1310, 140, 250, 90),
]
be = [E("e1", "paper", "base"), E("e2", "base", "a"), E("e3", "base", "ext", "builds on"), E("e4", "ext", "b"), E("e5", "a", "cmp"), E("e6", "b", "cmp")]
sp = static_spec(1448, 290, bn, be)
slides.append(slide(
    "Baseline and extension, with an example", SEC, 3, "What you actually produce",
    "First reproduce the paper's number, then try to improve on it",
    flow_static(sp) + callout("An example from the paper list", "For the Gorilla paper, a team could run the authors' released model on part of the test set (the baseline, number A). Then it could try an idea the paper leaves open, such as a new kind of API that the test set does not cover (the extension, number B). The comparison of B with A is the heart of the project. <b>Smoke test</b>: a small run that stands in for a full run. It is allowed if you can explain what a full run would need."),
    '''<p>Three minutes. The Gorilla example comes from the paper menu, whose entry lists three open ideas: a new API category APIBench does not cover, an ablation on retriever quality, or a tighter hallucination check than AST matching alone. Teams are not limited to those.</p>
    <p>Explain smoke test here, it comes up again on the rules and grading slides.</p>'''))

# ============================================================== 4 five topics
slides.append(slide(
    "The five topics", SEC, 3, "One topic per team",
    "Pick one of five topics. Each matches one module.",
    table(["Topic", "Module", "What it studies", "Papers taught in that module"],
          [["<b>Extraction</b>", "1", "Turning a sentence into structured data: intent, entities, function calling", "Gorilla"],
           ["<b>Dialogue</b>", "2", "Agents over many turns: state, routing, escalation", "Helping Customers in Distress"],
           ["<b>Grounding</b>", "3", "Answers based on real sources: retrieval, citation, refusal", "Cache-augmented generation (\"Don't Do RAG\")"],
           ["<b>Memory</b>", "4", "What an agent remembers within and across sessions", "Mem0, Zep, SeCom"],
           ["<b>Evaluation</b>", "5", "Testing agents over whole conversations, bias and privacy checks", "tau-bench, tau2-bench"]])
    + '<p class="lu-caption" style="margin-top:var(--lu-s3)">You are not limited to the taught papers. A paper taught in a module is a valid choice, and it may make your pitch easier to approve because the instructor already knows it.</p>',
    '''<p>Three minutes. Each team picks one topic and goes deep. You do not owe the course a working version of all five.</p>
    <p>Source: PROJECT-REDESIGN.md and the syllabus Section 9.</p>''',
    tint=True))

# ============================================================== 5-8 the paper menu (four slides)
def menu_table(rows):
    return table(["Paper", "What you would run", "Cost and effort"], rows)
MENU_CAP = '<p class="lu-caption" style="margin-top:var(--lu-s3)">14 papers on the menu, 13 with public code. Checked against arXiv and each repository on 17 September 2026. Full menu with code links: ' + a(MENU, "research/PROJECT-PAPER-MENU.md") + '. You may also propose your own paper.</p>'
slides.append(slide(
    "The paper menu: extraction and grounding", SEC, 2, "The paper menu · 1 of 4",
    "Extraction and grounding papers",
    menu_table([
        ["<b>Extraction.</b> Gorilla, Patil et al., 2023, arXiv:2305.15334", "The authors' released model on part of the test set (APIBench)", "A laptop GPU or a free hosted notebook. No training."],
        ["<b>Extraction.</b> ToolLLM / ToolBench, Qin et al., 2023, arXiv:2307.16789", "A small subset of the queries, not the whole suite", "Keep any GPT comparison under the cost limit."],
        ["<b>Grounding.</b> Cache-augmented generation, Chan et al., 2024, arXiv:2412.15605", "Preload a knowledge source into an open model", "The cheapest on the menu. A personal computer."],
        ["<b>Grounding.</b> Self-RAG, Asai et al., 2023, arXiv:2310.11511", "The released 7B or 13B models", "A 7B model on a consumer GPU or a free hosted notebook."],
    ]) + MENU_CAP,
    '''<p>Two minutes. Read the bold topic word and one line per paper. Gorilla and the cache-augmented generation paper are taught in Modules 1 and 3. ToolLLM and Self-RAG are not taught, so a team choosing them is choosing a road the lectures do not cover.</p>
    <p>Re-check a paper's repository before a team commits to it: the menu was checked on 17 September 2026 and projects change. The menu has 14 entries; 13 have public code.</p>'''))
slides.append(slide(
    "The paper menu: dialogue", SEC, 2, "The paper menu · 2 of 4",
    "Dialogue papers",
    menu_table([
        ["<b>Dialogue.</b> Helping Customers in Distress, Atreya et al., 2026, arXiv:2605.16268", "<b>No public code.</b> You build the baseline from the paper's own description", "More work at the start."],
        ["<b>Dialogue.</b> MultiWOZ, Budzianowski et al., 2018, arXiv:1810.00278", "The dialogue-state tracking baseline", "A laptop CPU. No API cost."],
        ["<b>Dialogue.</b> ABCD, Chen et al., 2021, arXiv:2104.00783", "An agent that follows company policy in a dialogue", "A laptop or one modest GPU. No API cost."],
    ]) + callout("Why the first one is marked", "It describes a real system at a bank, not an open-source release, and no code was found. It is still a valid choice, and it is the one taught in Module 2, but you would build the baseline yourself. The other two come with code.", concept=False),
    '''<p>Two minutes. "Helping Customers in Distress" is the only entry on the menu without public code. The menu file explains the search that found none.</p>''',
    tint=True))
slides.append(slide(
    "The paper menu: memory", SEC, 2, "The paper menu · 3 of 4",
    "Memory papers",
    menu_table([
        ["<b>Memory.</b> Mem0, Chhikara et al., 2025, arXiv:2504.19413", "The library plus an LLM key", "A laptop. Cheap."],
        ["<b>Memory.</b> Zep / Graphiti, Rasmussen et al., 2025, arXiv:2501.13956", "A small memory graph, self-hosted with Docker", "A personal computer and an LLM key."],
        ["<b>Memory.</b> SeCom, Pan et al., 2025, arXiv:2502.05589", "A subset of the LOCOMO or Long-MT-Bench+ tests", "Embeddings and a modest number of LLM calls."],
        ["<b>Memory.</b> MemGPT / Letta, Packer et al., 2023, arXiv:2310.08560", "A self-hosted agent that manages its own memory. Not taught in class", "An LLM key covers it."],
    ]) + MENU_CAP,
    '''<p>Two minutes. Mem0, Zep and SeCom are the three papers taught in Module 4. MemGPT is included on purpose because it uses a different idea from all three.</p>'''))
slides.append(slide(
    "The paper menu: evaluation", SEC, 2, "The paper menu · 4 of 4",
    "Evaluation papers",
    menu_table([
        ["<b>Evaluation.</b> tau-bench, Yao et al., 2024, arXiv:2406.12045", "A handful of tasks in one domain, with a cheaper model", "Well under $20."],
        ["<b>Evaluation.</b> tau2-bench, Barres et al., 2025, arXiv:2506.07982", "The same idea, where the user can act too", "Well under $20."],
        ["<b>Evaluation.</b> AgentBench, Liu et al., 2023, arXiv:2308.03688", "One lightweight environment of the eight", "Avoid the heavy environments."],
    ]) + callout("Naming a paper is not an approved pitch", "The pitch step still applies to every team, whichever paper you choose. A paper with working code only means less of your time goes to setting up the baseline, so more goes to the part that is yours.", concept=True),
    '''<p>Two minutes. tau-bench and tau2-bench are the two papers taught in Module 5. AgentBench is the broader alternative.</p>''',
    tint=True))

# ============================================================== 7 choosing rules
slides.append(slide(
    "Choosing a paper: the rules", SEC, 3, "What is allowed, and the cost limit",
    "Five rules for choosing your paper",
    '''<div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ol class="lu-list lu-list--num">
      <li><b>Team size:</b> two or three people.</li>
      <li><b>One topic and one paper</b> for the whole project.</li>
      <li><b>Cost limit:</b> it must run on a personal computer, or cost at most <b>$20</b> in API fees in total.</li>
      <li><b>A smoke test is fine</b> instead of a full run, if you can explain what a full run would need.</li>
      <li><b>Any paper on the menu, or your own,</b> with the instructor's approval of your pitch.</li>
    </ol>''' + callout("Two things that are not a problem", "Another team chooses the same paper. You choose a paper that was taught in a module. Neither is restricted or penalized. What counts is the extension you add.") + '''
  </div>''',
    '''<p>Three minutes. The cost limit is a hard number on purpose, so a self-proposed paper can be checked with one question: does it fit this box, yes or no. Say the two things that are not a problem out loud, they come up every time.</p>'''))

# ============================================================== 8 idea pitch
slides.append(slide(
    "The idea pitch", SEC, 4, "Issue 1: one short piece of writing, approved before real work starts",
    "The idea pitch: what to write",
    table(["Part", "What to write", "Example (invented for teaching)"],
          [["<b>Topic and paper</b>", "Topic, paper (title, authors, year, link), and the code for the baseline", "Extraction. Gorilla (2023). The authors' code."],
           ["<b>The limitation</b>", "One specific weakness of the paper that you will target. Not \"make it better\"", "The test set has only machine learning APIs."],
           ["<b>Your idea</b>", "What you will build or change, and why it addresses that weakness", "Test the model on a new kind of API and compare."],
           ["<b>Related work</b>", "Did you look for a published follow-up? List what you found, even \"nothing\"", "Searched: one related paper, it uses a different test set."],
           ["<b>Cost check</b>", "Does it fit a personal computer or $20? Say now if a smoke test will be used", "Smoke test on 50 requests. A full run needs more compute."]])
    + '<p class="lu-caption" style="margin-top:var(--lu-s2)">Do not start real work until the instructor approves the pitch.</p>',
    '''<p>Four minutes. The instructor sets the deadline: decide and say it aloud, nothing in the course documents fixes one yet. The five parts come from the idea-pitch issue template in the team repository. The right-hand column is invented to show the level of detail, it is not an approved pitch.</p>
    <p>Decide and say the pitch deadline aloud. Nothing in the course documents fixes one yet.</p>'''))

# ============================================================== 9 guardrails
slides.append(slide(
    "Two guardrails", SEC, 2, "Why the pitch and the report ask for honesty",
    "Two checks that keep the project honest",
    '''<div class="lu-split" style="margin-top:var(--lu-s3)">
    <div class="lu-card"><span class="lu-card__label">Before the work: the pitch approval</span>
      <p class="lu-sub">The instructor reads your pitch to catch one thing: an idea that already exists as someone else's published follow-up paper. Finding that out after weeks of work is the worst time.</p></div>
    <div class="lu-card"><span class="lu-card__label">After the work: related-work honesty</span>
      <p class="lu-sub">Your report must list related follow-up work on the same paper and say how your extension is different. Saying nothing about it counts against you. If you found none, say so.</p></div>
  </div>''',
    '''<p>Two minutes. Both checks exist because an extension idea cannot simply be copied the way code can, but it can still turn out to be someone else's published idea.</p>''',
    tint=True))

# ============================================================== 10 repository flow
rn = []
rl = ["1. Use the\ntemplate", "2. Add your\ninstructor", "3. Protect the\nmain branch", "4. Add your\nkey (.env)", "5. Run\nverify_setup"]
for i, l in enumerate(rl):
    rn.append(N("r%d" % i, l, "code" if i in (0, 2) else "tool", 145 + 290 * i, 95, 240, 96))
re_ = [E("x%d" % i, "r%d" % i, "r%d" % (i + 1)) for i in range(4)]
rsteps = []
for i in range(5):
    show = ["r%d" % i] + (["x%d" % (i - 1)] if i else [])
    rsteps.append(S(show, ["x%d" % (i - 1)] if i else [], {("r%d" % i): "active"} | ({("r%d" % (i - 1)): "idle"} if i else {})))
sp = spec(1448, 190, rn, re_, rsteps)
slides.append(slide(
    "Your repository: five setup steps", SEC, 4, "Every team starts from the same template",
    "Create your team repository from the course template",
    flow_walk("Your repository", sp, [
        ("Use the template", "On the template page on GitHub, click <b>Use this template</b> (not fork, not clone) and create a <b>private</b> repository for your team, for example team-alpha-gorilla-extension. Then clone it."),
        ("Add your instructor", "Add your instructor as a collaborator on the new repository, so your work can be reviewed and graded."),
        ("Protect the main branch", "In the repository settings turn on branch protection for <b>main</b>: a pull request is required, with at least one approval. This setting does not come with the template, so do it now."),
        ("Add your key", "Copy <code>.env.example</code> to <code>.env</code> and add the API key your paper's baseline needs. Never commit <code>.env</code>."),
        ("Check the setup", "Run <code>pip install -r requirements.txt</code>, then <code>python scripts/verify_setup.py</code>. Fix every FAIL before real work."),
    ]) + callout("Yes, every team uses the template", "Each team works in <b>one private repository created from the course template</b>: " + a(TEMPLATE, "github.com/ahmabboud/dsca-team-template") + ". It already has the folders, the four issue templates and the team rules. <b>Template</b>: a repository you copy as a starting point, with its own separate history."),
    '''<p>Four minutes. Yes, the template is required, it is the workflow in syllabus Section 11. Show the GitHub page and the green "Use this template" button. The template repository is public, the repositories teams create from it should be private.</p>
    <p>Do this on your own time after choosing a paper, not in class. The instructor's demonstrations need no setup from students.</p>'''))

# ============================================================== 11 inside the repo
slides.append(slide(
    "What is inside your repository", SEC, 2, "One folder for each part of the project",
    "Where each part of your project goes",
    table(["Folder or file", "What goes there"],
          [["<code>baseline/</code>", "Your reproduction of the paper's method, with the exact commands to run it"],
           ["<code>extension/</code>", "Your own idea's code, kept clearly apart from the baseline"],
           ["<code>report/REPORT.md</code>", "The paper-style report, from the template"],
           ["<code>slides/</code>", "Your defense slides, as an exported file or a link"],
           ["<code>data/</code>", "Your own data, or notes on where it comes from"],
           ["<code>tests/</code> and <code>scripts/verify_setup.py</code>", "Checks that the setup works. Add real tests as you build"],
           ["<code>.github/ISSUE_TEMPLATE/</code> and <code>CONTRIBUTING.md</code>", "The four issues and the team rules"]]),
    '''<p>Two minutes. Keeping the baseline and the extension in separate folders makes it obvious what is the paper's work and what is yours, which is exactly what the graders need to see.</p>'''))

# ============================================================== 12 team rules
slides.append(slide(
    "How the team works together: three rules", SEC, 3, "Each rule solves a different problem",
    "Three team rules, and the problem each one solves",
    table(["Rule", "What it means", "The problem it solves"],
          [["<b>1. One branch and one pull request per person</b>", "Work on your own branch (for example alice/baseline-eval-loop). When ready, open a <b>pull request</b> into main yourself. Never commit straight to main.", "Two people editing the same file at the same time."],
           ["<b>2. Every pull request needs a teammate's approval</b>", "Another teammate reads the changes, runs them and asks questions before merging. A quick \"looks good\" is not a review.", "Knowing who wrote what, for learning and for grading."],
           ["<b>3. Always commit under your own GitHub account</b>", "Never share a login and never commit for someone else. If you worked as a pair, both of you push from your own branch.", "Making rules 1 and 2 mean something."]])
    + callout("Definitions", "<b>Branch</b>: your own copy of the work inside the repository. <b>Pull request</b>: a request to merge your branch into main, which a teammate can review.", concept=False),
    '''<p>Three minutes. These are the three rules in the team repository's CONTRIBUTING.md. The instructor can see every pull request's author and every review, and will use that history in the defense to ask each of you about a part a teammate built.</p>''',
    tint=True))

# ============================================================== 13 four issues
slides.append(slide(
    "The four issues", SEC, 4, "Four checkpoints in your repository, in order",
    "Four GitHub issues, four checkpoints",
    table(["Issue", "It is done when..."],
          [["<b>1. Idea pitch</b>", "The instructor has approved it (a checkbox in the issue)."],
           ["<b>2. Baseline reproduction</b>", "The baseline runs end to end and the commands are in <code>baseline/README.md</code>. At least one of the paper's numbers is reproduced, with your number beside the paper's. A smoke test is explained. The cost limit is respected."],
           ["<b>3. Extension</b>", "The extension runs end to end and is compared directly with the baseline. Results are credible, or a smoke test is stated plainly. The numbers are ready for the report. The cost limit is respected."],
           ["<b>4. Report and slides</b>", "The report is complete, related work is cited, and any smoke test is stated. The slides follow the required structure. Both are handed in before Module 6."]])
    + '<p class="lu-caption" style="margin-top:var(--lu-s3)">For each issue: assign it to the teammates who will work on it, write who does which part in its checklist, and link your pull requests to it (<code>Closes #number</code>).</p>',
    '''<p>Four minutes. The four issue templates are in the team repository under .github/ISSUE_TEMPLATE. The third acceptance item of the baseline issue and the last one of the report issue both ask for honesty about smoke tests.</p>'''))

# ============================================================== 14 report
slides.append(slide(
    "The report", SEC, 3, "A short paper about your own work",
    "The report has five sections",
    table(["Section", "What goes there"],
          [["<b>Abstract</b>", "3 to 5 sentences: what the paper does, what limitation you targeted, what you built, the main result. Write it last."],
           ["<b>1. The baseline paper</b>", "Its problem, its method (the real mechanism, not only its name) and its results with numbers."],
           ["<b>2. Your extension</b>", "Why (the limitation), what you built (enough to reproduce it) and notes on running your code."],
           ["<b>3. Results</b>", "Your reproduction next to the paper's numbers, your extension against the baseline, and an honest assessment of what worked and what did not."],
           ["<b>4. Related work</b>", "Published follow-up work on the same paper, and how your extension differs. If none, say so."],
           ["<b>5. Limits and full validation</b>", "If you used a smoke test, exactly what a full run would need: data, compute, time or cost."]]),
    '''<p>Three minutes. The sections are the ones in report/REPORT.md in the team template. Section 3.3 (honest assessment) exists so that a team does not show only the numbers that look good. Section 5 is not a penalty as long as it is honest.</p>'''))

# ============================================================== 15 slides
sl_nodes = [
    N("s0", "Cover", "user", 130, 90, 190, 76),
    N("s1", "1. Paper:\nthe problem", "data", 380, 90, 190, 76),
    N("s2", "2. Paper:\nthe solution", "data", 630, 90, 190, 76),
    N("s3", "3. Paper:\nthe results", "data", 880, 90, 190, 76),
    N("s4", "4. Your\nidea", "model", 1130, 90, 190, 76),
    N("s5", "5. Your\nresults", "model", 1380, 90, 190, 76),
]
sl_edges = [E("t%d" % i, "s%d" % i, "s%d" % (i + 1)) for i in range(5)]
sp = static_spec(1448, 180, sl_nodes, sl_edges)
slides.append(slide(
    "The defense slides", SEC, 2, "A hard limit, not a suggestion",
    "At most 8 slides: a cover, up to 6 content slides, and references",
    flow_static(sp) + '''<ul class="lu-list" style="margin-top:var(--lu-s4)">
    <li><b>Cover:</b> team name, paper, topic. <b>Content (no more than 6):</b> the baseline paper's problem, solution and results, then your extension's idea and results, in that order.</li>
    <li><b>References:</b> full citations for the paper and any related work in your report.</li>
    <li>Numbers from your comparison belong on the slides. Long method text does not.</li>
  </ul>''',
    '''<p>Two minutes. The limit comes from the rubric and from slides/README.md in the team template. Fewer content slides is fine if the material fits. More is not allowed.</p>'''))

# ============================================================== 16 hand in
slides.append(slide(
    "What to hand in, and when", SEC, 2, "Everything is handed in before the defense",
    "What to hand in, and when",
    table(["What", "When", "Counts for"],
          [["Approved idea pitch", "Early, before real work begins", "A required step, no points of its own"],
           ["Working repository: the baseline and your extension", "Before Module 6", "Part A of the grade"],
           ["Paper-style report", "Before Module 6", "Part A of the grade"],
           ["Defense slides (at most 8)", "Before Module 6", "Part A of the grade"],
           ["The defense: 12 minutes presenting, 12 minutes of questions", "Module 6", "Part A of the grade"],
           ["Being there and taking part", "Every session", "Part B of the grade"]])
    + '<p class="lu-caption" style="margin-top:var(--lu-s3)">Everything is handed in <b>before</b> Module 6, not brought on the day, so the instructor can read it and ask targeted questions. Your instructor will tell you how to submit (a link or a file).</p>',
    '''<p>Two minutes. Stress "not brought on the day". The defense-day scoring relies on the instructor having read the repository, report and slides beforehand.</p>''',
    tint=True))

# ============================================================== 17 defense
dn = [
    N("d0", "Before Module 6:\nrepository, report\nand slides handed in", "data", 185, 105, 290, 120),
    N("d1", "12 minutes:\nyou present", "user", 600, 105, 230, 96),
    N("d2", "12 minutes:\nquestions", "tool", 930, 105, 230, 96),
    N("d3", "Scores and\nfeedback returned", "code", 1270, 105, 250, 96),
]
de = [E("y0", "d0", "d1"), E("y1", "d1", "d2"), E("y2", "d2", "d3")]
dst = [S(["d0"], [], {"d0": "active"}), S(["d1", "y0"], ["y0"], {"d0": "idle", "d1": "active"}),
       S(["d2", "y1"], ["y1"], {"d1": "idle", "d2": "active"}), S(["d3", "y2"], ["y2"], {"d2": "idle", "d3": "active"})]
sp = spec(1448, 220, dn, de, dst)
slides.append(slide(
    "Defense day", SEC, 3, "Module 6",
    "The defense: 12 minutes to present, 12 minutes of questions",
    flow_walk("Defense day", sp, [
        ("Before", "The instructor has already read your repository, report and slides. Nothing new is handed in on the day."),
        ("You present", "You present for 12 minutes: the paper's problem, solution and results, then your extension's idea and results."),
        ("Questions", "Then 12 minutes of questions. <b>Any teammate can be asked about any part</b>: the paper, the extension or the code."),
        ("Scores", "The instructor scores each team against the rubric. Scores and feedback are returned at the end of the session."),
    ]) + callout("Good to know", "Module 6 is 180 minutes, and the instructor may extend it by up to one hour if there are many teams. No team's time is shortened to fit. If you plan a live demo, check that it already works before your slot."),
    '''<p>Three minutes. The format comes from the syllabus Module 6 entry. The instructor's own schedule sheet and scoring sheet are not shared with students, so do not promise specific slot times here: say they will be announced.</p>'''))

# ============================================================== 18-19 grading
slides.append(slide(
    "How you are graded, part A: the defense", SEC, 2, "85 of the 100 points",
    "Part A: what each line of the project rubric asks",
    '<table class="lu-table"><thead><tr><th>Criterion</th><th>Score</th><th>The question the graders ask</th><th>Full marks look like</th></tr></thead><tbody><tr><td><b>Code and reproduction quality</b></td><td>25</td><td>Does it run, and is it correct?</td><td>The paper\'s method runs on your computer, and your own extension is really built and works.</td></tr><tr><td><b>Understanding of the research</b></td><td>25</td><td>Do you understand the paper?</td><td>You explain the paper\'s problem, method and results, and answer questions about all of it, not only your own part.</td></tr><tr><td><b>Motivation and value</b></td><td>25</td><td>Why is your idea worth doing?</td><td>It fixes a real, specific weakness of the paper and is useful, not new only for the sake of being new.</td></tr><tr><td><b>Result quality</b></td><td>25</td><td>Did it actually work?</td><td>A real comparison with the baseline and believable results. A small test run is fine if you say what a full run would need.</td></tr></tbody></table>'
    + '<p class="lu-caption" style="margin-top:var(--lu-s3)">Each line is scored out of 25 (100 in all). The total is multiplied by <b>0.85</b>, which gives the 85 points of Part A. The defense score belongs to the team.</p>',
    '''<p>Two minutes. Same content as the rubric slide in Module 1 and the syllabus Section 9.</p>'''))
slides.append(slide(
    "How you are graded, part B: attendance and participation", SEC, 2, "15 of the 100 points",
    "Part B: 2.5 points for each of the 6 sessions",
    '<table class="lu-table"><thead><tr><th>What</th><th>Points</th><th>How it is scored</th></tr></thead><tbody><tr><td><b>Attendance</b></td><td>1.5 a session</td><td>You are there and you stay for the session.</td></tr><tr><td><b>Participation</b></td><td>1.0 a session</td><td>1 = you asked a question, answered one, or joined the discussion at least once. 0.5 = you joined only when asked directly. 0 = no contribution.</td></tr><tr><td><b>One excused absence</b></td><td>No loss</td><td>You may miss one module. It keeps its 2.5 points if you finish the missed project work before the next module. Any other absence loses that session\'s points.</td></tr></tbody></table>'
    + '<p class="lu-caption" style="margin-top:var(--lu-s3)">Labs are demonstrations run by the instructor, so participation means taking part in the demonstration and the discussion. <b>Final grade = 0.85 x defense score + Part B points.</b> Example: 88 at the defense and 13 for Part B gives 74.8 + 13 = 87.8. Part B is yours alone, not the team\'s.</p>',
    '''<p>Two minutes. Same content as the Part B slide in Module 1 and the syllabus Sections 9 to 11.</p>''',
    tint=True))

# ============================================================== 20 questions to expect
slides.append(slide(
    "Questions you can expect", SEC, 3, "Prepare every teammate for every part",
    "Any teammate can be asked about any part",
    table(["About...", "Examples of questions (invented to show the style)"],
          [["<b>The paper</b>", "What problem does the paper solve? How does its method work, step by step? What do its results show, and what do they not show?"],
           ["<b>Your extension</b>", "Which weakness of the paper does it target? Why is that worth fixing? What did you change, and why that?"],
           ["<b>The code</b>", "Show me where in the code this step happens. What happens if this input is empty? How did you get this number?"],
           ["<b>Your results</b>", "How did you compare with the baseline? Was it a full run or a smoke test? What would change at full size?"]])
    + callout("How to prepare", "Do not split the project into \"my part\" and \"your part\". Each of you should be able to explain the paper, the extension and the code. Practice by asking each other these questions, and read each other's pull requests properly.", concept=True),
    '''<p>Three minutes. The questions are examples written for this guide, not a list the instructor will use. They follow the four rubric lines. The instructor can see every pull request and review, so a teammate may be asked about a part someone else built.</p>'''))

# ============================================================== 21 checklist
slides.append(slide(
    "A checklist before Module 6", SEC, 2, "Tick every line before you hand in",
    "Checklist: are you ready to defend?",
    '''<div class="lu-split" style="margin-top:var(--lu-s3)">
    <ul class="lu-list lu-list--check">
      <li>The pitch is approved, and the report says if the idea changed.</li>
      <li>The baseline runs, with the commands in <code>baseline/README.md</code>.</li>
      <li>Your number is next to the paper's number.</li>
      <li>The extension runs and is compared with the baseline.</li>
      <li>Any smoke test is stated, with what a full run would need.</li>
    </ul>
    <ul class="lu-list lu-list--check">
      <li>The report is complete and cites related work.</li>
      <li>The slides: a cover, at most 6 content slides, references.</li>
      <li>The cost stayed under $20, or it ran on a personal computer.</li>
      <li>Everything is handed in before Module 6.</li>
      <li>Each teammate can answer about the paper, the extension and the code.</li>
    </ul>
  </div>''',
    '''<p>Two minutes. Every line maps to an acceptance item of one of the four issues or to a rubric line.</p>''',
    tint=True))

# ============================================================== 22 where to find things
slides.append(slide(
    "Where to find everything", SEC, 1, "Links",
    "Where to find everything",
    '''<div class="lu-split lu-split--wide-left" style="margin-top:var(--lu-s3)">
    <ul class="lu-list">
      <li>The team template: ''' + a(TEMPLATE, "github.com/ahmabboud/dsca-team-template") + '''</li>
      <li>The paper menu with code links: ''' + a(MENU, "research/PROJECT-PAPER-MENU.md") + '''</li>
      <li>The team rules: <code>CONTRIBUTING.md</code> in your repository</li>
      <li>The setup steps: <code>README.md</code> in your repository</li>
      <li>The four issues: <b>Issues, New issue</b> in your repository</li>
      <li>The report and slides templates: <code>report/REPORT.md</code> and <code>slides/README.md</code></li>
    </ul>''' + callout("Stuck?", "Say so early, in your team channel or at the start of the next session. Do not wait until the week of the defense.") + '''
  </div>''',
    '''<p>One minute.</p>'''))

# ============================================================== 23 glossary
g1 = [["Baseline", "The paper's own method, reproduced by you"], ["Extension", "Your own idea, built on the baseline"], ["Smoke test", "A small run that stands in for a full run"],
      ["Benchmark", "A fixed test many methods can take"], ["Preprint", "A paper shared before formal review"]]
g2 = [["Related work", "Other papers on the same topic"], ["Template", "A repository you copy as a start"], ["Branch", "Your own copy of the work"],
      ["Pull request", "A request to merge, with a review"], ["Defense", "The Module 6 presentation and questions"]]
slides.append(slide(
    "Words used in the project", SEC, 2, "A reminder of the project words",
    "Words used in the project",
    '<div class="lu-split">' + table(["Word", "Meaning"], g1) + table(["Word", "Meaning"], g2) + '</div>',
    '''<p>Two minutes. Ask two students to explain one word each in their own words.</p>'''))

# ============================================================== 24 self-check
slides.append(slide(
    "Self-check", SEC, 2, "Self-check",
    None,
    '''<div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <div class="lu-mcq" data-qid="proj-q1" data-answer="b"
           data-label="The cost limit for the project"
           data-fb-correct=" A personal computer, or $20 in API fees in total."
           data-fb-wrong=" The limit is a personal computer, or $20 in total.">
        <p class="lu-mcq__q">What is the cost limit for the project?</p>
        <div class="lu-mcq__opts">
          <button class="lu-mcq__opt" type="button" data-key="a">No limit if the results are good<span class="lu-mcq__why" hidden>There is a fixed limit.</span></button>
          <button class="lu-mcq__opt" type="button" data-key="b">A personal computer, or $20 in API fees in total<span class="lu-mcq__why" hidden>Yes. A smoke test is fine if you explain a full run.</span></button>
          <button class="lu-mcq__opt" type="button" data-key="c">$20 per teammate per module<span class="lu-mcq__why" hidden>It is $20 in total for the project.</span></button>
        </div>
        <div class="lu-mcq__fb" hidden></div>
      </div>
    </div>
    <div class="lu-stack"><div data-score></div>
      <p class="lu-caption">Press <kbd>S</kbd> for study mode. Your answers stay in this browser only.</p></div>
  </div>''',
    '''<p>Two minutes. One question is enough for a reference deck. Add more of your own if you use it in class.</p>'''))

# ============================================================== assemble
mod = open(OUT.replace('dsca-project-guide', 'dsca-module-01')).read()
head = mod[:re.search(r'<!-- =+ 01 -->', mod).start()]
foot = mod[mod.index('</div><!-- /stage -->'):]
total = sum(int(m) for m in re.findall(r'data-minutes="(\d+)"', "".join(slides)))
head = head.replace('Foundations and Modern Understanding · Data Science for Conversational AI, Module 1', 'The Team Project: a guide · Data Science for Conversational AI')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Student guide to the team project of Data Science for Conversational AI, MSc, Lebanese University: topics, choosing a paper, the repository, what to hand in, the defense, and the grading.">', head)
head = head.replace('data-deck-id="dsca-m01"', 'data-deck-id="dsca-project"').replace('data-session="Module 1 of 6"', 'data-session="Team project"').replace('data-duration="180"', 'data-duration="%d"' % total)
out = []
for i, s in enumerate(slides, 1):
    out.append('<!-- %s %02d -->\n%s' % ('=' * 66, i, s))
open(OUT, 'w').write(head + "\n".join(out) + "\n" + foot)
import collections
c = collections.OrderedDict()
for k, m in re.findall(r'data-section="([^"]+)" data-minutes="(\d+)"', "".join(slides)): c[k] = c.get(k, 0) + int(m)
print(dict(c), total, 'slides', len(slides))
