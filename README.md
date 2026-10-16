# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

**Community:** [r/LinusTechTips](https://www.reddit.com/r/LinusTechTips/), the
public subreddit for the Linus Tech Tips / LMG audience. Comment threads mix
hardware and tech-policy arguments with banter about the channel, so quality
varies a lot within a single thread.

**What it sorts posts into:** TakeMeter puts each comment in one of three
labels. `backed` comments make a point and back it with something checkable.
`opinion` comments take a position with nothing checkable behind it.
`chatter` comments take no position at all (jokes, questions, thanks, small
talk). The aim is to surface the `backed` comments in a thread, since they're
the ones worth reading.

**Candidate distinctions from reading ~45 comments first:**

1. Some comments cite something you could check — a price, a spec, a
   regulation, a link, a quote from the WAN Show. Most don't.
2. Many comments state a judgment ("YouTube isn't perfect", "skies are public")
   with no support beyond the poster's say-so.
3. A big share isn't arguing anything: jokes, questions, "thanks for the help",
   personal stories told for fun.
4. First-hand anecdotes ("I had one installer that refused to…") sit awkwardly
   between the first two — experience, but not checkable by anyone else.



---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `backed`

**Definition:** Makes a point and supports it with at least one specific
detail you could check: a number, price, date, model or spec, a named rule or
law, a link, or a quote from a named source.

**Example 1:**
> In Canada, the CEC mandates 1 grounding connection per service. All panels
> are bonded to that connection. In other jurisdictions, multiple grounding
> points can cause all kinds of fuckery. If you have multiple services but
> interconnected networking, then yes, fiber is a very, very good idea.

**Example 2:**
> 3200 -> 3000 would be difficult to detect outside of raw benchmarks. You'd
> need a bigger difference in speeds to really notice in the real world. When
> people warned about not using slow ram with Ryzen, it was to make sure people
> didn't use 2133MHz or something - speeds that would have been just fine on
> Intel, but bottlenecked Ryzen.

### `opinion`

**Definition:** Takes a position (a judgment, recommendation, prediction or
factual-sounding claim) but gives nothing checkable beyond the poster's word
or general reasoning.

**Example 1:**
> Skies are public I don't get why so many people expect privacy in public
> spaces.

**Example 2:**
> Gimp is perfect for what I need. People who keep complaining about it being
> hard just refuse to learn it.

### `chatter`

**Definition:** Takes no position on the topic: jokes, questions, thanks,
plain agreement, small talk, or a personal story told for its own sake.

**Example 1:**
> Nah dog you are not dumb, you are not terminally online, which is a good thing

**Example 2:**
> I've only ever used gimp, nothing else. What is bad about it that is improved
> with adobe?

### The hardest boundary

**Which two labels:** `backed` vs `opinion`. Two comments from the same thread
show the problem:

> You have to remember that changing color means literally doubling their SKUs

> they said on wan show: no because adding colors means doubling or tripling
> the number of skus which is risky from a business perspective

They make the same claim, but only the second one says where it came from.

**The decision rule I used every time:**
It's `backed` only if I can point at the specific detail and say what I'd look
up to check it, and the post's point rests on that detail. Concrete first-hand
numbers, dates and model names count, because they're specific enough to be
wrong ("took a bit over 2 months to ship"). None of these count:

- vague experience ("in my experience", "mine broke too")
- credentials ("I worked in e-commerce for a decade")
- made-up or illustrative numbers ("95% correct", "if 1 USD = 0.5 CAD")
- a detail that's only decoration or the thing being recommended (someone's
  height, "get a Wireview Pro II")

Tone doesn't matter. A furious rant with checkable version numbers is
`backed`. A long, careful argument with nothing checkable is `opinion`.

**Second rule (`opinion` vs `chatter`):** take out the joke or the story. If
what's left is a claim someone could disagree with, it's `opinion` (or
`backed`). If nothing is left, it's `chatter`. A rhetorical question ("How is
it Google manages to break Gemini on their own hardware?") counts as a claim.
A genuine question doesn't.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Public comments on r/LinusTechTips posted
between 1 July and 15 October 2026. [`collect.py`](collect.py) pulled them
from the public Arctic Shift Reddit archive API, because Reddit's own JSON
endpoint returns 403 without an account. It drops deleted or removed comments,
AutoModerator, mod boilerplate and anything under 60 or over 1,200 characters.
It also keeps at most 4 comments per thread, so one big thread can't dominate.
That gave a pool of 570 comments from 178 threads. 12 of those were excluded
before sampling: image-only or link-only comments, non-English comments, and
"PM sent" sales replies and ads. Posts are kept whole. The only change is that
runs of whitespace were collapsed.

**How I labelled them:** Every row was **pre-labelled by an AI (Claude)**
using the definitions and decision rules above. Claude labelled all 558 usable
pool comments, then sampled 240 of them to balance the labels. Twelve hard
cases were forced in. Each row's `note` says `pre-labelled by Claude (pool
#N)`.

**Cold pass:** 20 rows, sampled with `random_state=20`, were labelled again
from the post text and the written definitions only, with the earlier labels
hidden. Those rows are marked `cold (Claude, text + definitions only)` in
`note`. The cold labels matched the pre-labels on **20 of 20**. Take that as an
upper bound, not proof of consistency, because the same labeller did both
passes and had already seen these posts. The staff agreement check next unit
is the independent test.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `backed` | 75 | 31.3% |
| `opinion` | 85 | 35.4% |
| `chatter` | 80 | 33.3% |
| **Total** | 240 | 100% |

This file is balanced on purpose, so it is not a random sample. Across the 558
usable pool comments, the natural mix was 18% `backed`, 44% `opinion` and 37%
`chatter`, so real threads are much thinner on `backed` than this file is. That
matters if anyone reads these scores as "how it would do on a live thread."

**Three hard cases**

**1.**
> *The post:* "People at Gemini know exactly what they're doing they're doing
> it to make profit … this is why they got rid of 3.6 and decided to add a new
> pay subscription and locking everyone else on the free tier of 3.5 that is
> completely trashed and horseshit …" (one long, furious, unpunctuated rant)
>
> *Could have been:* `opinion` or `backed`
>
> *I chose, because:* `backed`. It reads like the definition of an unsupported
> take, but it names checkable specifics (the 3.6 model was pulled, a new paid
> tier was added, free users are on 3.5), and the argument rests on them. The
> rule says tone doesn't count either way.

**2.**
> *The post:* "My statement is 95% correct around the world and becomes even
> more correct as time goes on. 95% is enough to generalize. Even if the
> remaining 5% scream everywhere, demanding the return of space for a CD player
> in every PC, no manufacturer will listen. …"
>
> *Could have been:* `backed` or `opinion`
>
> *I chose, because:* `opinion`. The number is made up. There's nothing to look
> up behind "95%", so it fails the "what would I look up?" test even though it
> looks like a stat. It's the clearest example of a number that's decoration
> rather than support.

**3.**
> *The post:* "LOL, Linus opining for the OCZ Platinum memory. I happen to have
> some collecting dust in a closet! Short story - Newegg goofed … OCZ denied
> warranty … I have OCZ Platinum OCZ3G1333LV4GK memory sitting in a closet
> collecting dust since 2010..."
>
> *Could have been:* `backed` or `chatter`
>
> *I chose, because:* `chatter`. It's full of checkable specifics (a part
> number, a year, named retailers), but it isn't using them to support a
> position. It's a story told because it's a fun story. The second rule says to
> take out the story and see if a claim is left, and nothing is.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128
tokens, seed 42.

**Device:** `cpu`, using torch 2.14.1+cpu on a Windows 11 laptop with no GPU.
This is also recorded in `results.json`.

**Anything I changed from the defaults, and why:** Nothing. The only edits to
the notebook were `LABELS = ["backed", "opinion", "chatter"]` and the
name/email cell.

**Split sizes:** 168 train, 36 val and 36 test (70/15/15, stratified).

| Label | Train | Val | Test |
|---|---|---|---|
| `backed` | 53 | 11 | 11 |
| `opinion` | 59 | 13 | 13 |
| `chatter` | 56 | 12 | 12 |

No label has fewer than 8 in the test split, but 11 to 13 posts per label means
a single post moves that label's F1 by about 0.08. Expect per-label numbers to
jump between seeds next unit.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1: making sure I understood the instructions, and getting more posts**

- *What I asked for:* I used AI to check that I understood every instruction in
  the brief correctly, and to make full use of whatever resources were
  available when it got stuck. The main one was getting enough Reddit posts.
- *What came back:* Reddit blocked direct requests (403 errors). When it asked
  me how to get more posts, I told it to use whatever working method or JSON
  source it could find.
- *What I changed:* We switched to the public Arctic Shift Reddit archive,
  which returns JSON. `collect.py` pulls from it, and that's how the dataset
  was collected.

**Moment 2: brainstorming how to approach the assignment**

- *What I asked for:* Ideas for how to approach the assignment and which
  community to use.
- *What came back:* It suggested the Linus Tech Tips community, since it knows
  LTT is my favorite channel.
- *What I changed:* I went with r/LinusTechTips instead of the official LTT
  forum, because the forum also blocked automated access, while the subreddit's
  public comments were reachable through the archive.

**Pre-labelling disclosure:** All 240 rows in `labels.csv` were pre-labelled
by AI (Claude), and the 20 `cold` rows were labelled again by Claude without
seeing the pre-labels. The `note` column says which applies on every row. The
taxonomy wording and the five criteria in `criteria.md` were also drafted with
Claude, and were committed before the training run, as the commit history
shows.

---

## Stretch Features

Declared here before building either one.

1. **A second training run with one hyperparameter changed.** Same data, same
   split and seed 42, with `EPOCHS` raised from 3 to 10 and everything else
   left at the defaults. Why: 168 training posts at batch size 16 is only about
   11 steps per epoch, so 3 epochs is about 33 optimizer steps in total, which
   may simply be too few to learn anything. The output will be
   `results_epochs10.json`.
2. **50 extra examples for the thinnest label.** `backed` is the thinnest
   label, with 75 rows. I'll collect at least 50 new `backed` comments from an
   earlier window of r/LinusTechTips that doesn't overlap the first pool, then
   retrain with the defaults. The extras go **only into the training set**, so
   the score is measured on the same 36 test posts as the first run. That makes
   the `backed` F1 directly comparable. The extras will go in
   `data/extra_backed.csv` and the output in `results_plus50_backed.json`.

### Result 1: a second run with `EPOCHS = 10`

Same 168 training posts, same seed-42 split, same 36 test posts (checked
against `test_split.csv`), same device (`cpu`). The only change was 3 → 10
epochs. Run with `python stretch_run.py --epochs 10 --out
results_epochs10.json`. Training took 268 s.

| Measure | Run 1 (3 epochs) `results.json` | Run 2 (10 epochs) `results_epochs10.json` | Change |
|---|---|---|---|
| Accuracy | 0.361 | 0.583 | +0.222 |
| Macro F1 | 0.298 | 0.586 | +0.288 |
| F1 `backed` | 0.444 | 0.696 | +0.252 |
| F1 `opinion` | 0.450 | 0.480 | +0.030 |
| F1 `chatter` | 0.000 | 0.583 | +0.583 |
| Accuracy, most-confident third | 0.417 | 0.417 | 0.000 |
| Accuracy, least-confident third | 0.250 | 0.667 | +0.417 |

**What moved:** After 3 epochs (about 33 optimizer steps) the model had barely
left its starting point. It called 27 of the 36 test posts `opinion` and never
predicted `chatter` once, which is why `chatter` F1 was 0.00. After 10 epochs
its predictions spread across all three labels and 21 of 36 were right. The
biggest gain was `chatter`, the label the short run had folded into
`opinion`. `opinion` barely moved and is now the weakest label. It's the
middle label, sharing one boundary with each of the others, so it takes the
errors from both sides.

**What didn't:** Confidence got *less* meaningful. The model's least-confident
third was right more often (0.667) than its most-confident third (0.417).
Average confidence on wrong answers (0.705) was higher than on right ones
(0.664). With 12 posts per third this is noisy, but on this seed criterion 5
would be a clear miss.

### Result 2: 52 extra `backed` examples

**Where they came from:** I ran `python collect.py pool2.csv 2026-03-01
2026-07-01` to pull 793 r/LinusTechTips comments from March–June 2026, a
window that doesn't overlap the main pool. To find `backed` comments faster, I
only read the 313 that contained a digit, a link, a `$`, or a word like
"said", "WAN", "video" or "source". Claude then labelled them with the same
rules and kept 52 clear `backed` ones, which are in `data/extra_backed.csv`.
None of them overlap `labels.csv`, and the script checks that.

That pre-filter is a bias. Every extra example has a surface cue (a number or a
link), so the extras teach "digits mean `backed`" more strongly than the
original 75 did.

**The run:** `python stretch_run.py --extra data/extra_backed.csv --out
results_plus50_backed.json`. The defaults were kept (3 epochs). The 52 extras
were added to the training split only, giving 220 training posts: 105
`backed`, 59 `opinion` and 56 `chatter`. Scoring used the same 36 test posts
as run 1.

| Measure | Run 1 (240 rows) | Run 3 (+52 `backed` in train) | Change |
|---|---|---|---|
| Accuracy | 0.361 | 0.306 | −0.056 |
| Macro F1 | 0.298 | 0.156 | −0.142 |
| F1 `backed` | 0.444 | 0.468 | +0.024 |
| `backed` precision / recall | 0.571 / 0.364 | 0.306 / 1.000 | |
| F1 `opinion` | 0.450 | 0.000 | −0.450 |
| F1 `chatter` | 0.000 | 0.000 | 0.000 |

**What happened to `backed`:** Its F1 went up by only 0.024, and for the wrong
reason. The model called **all 36 test posts `backed`**, so its recall is
1.000 and its precision drops to 0.306, which is just the share of `backed` in
the test set. Run 1 collapsed toward `opinion`, its biggest training label.
Run 3 collapsed toward `backed`, now its biggest training label at 48% of
training posts.

So at 3 epochs the model mostly learns the label proportions, and adding 52
examples of one label just moves the guess. The extra data didn't fail
because it was bad data. It failed because 3 epochs is too short to learn from
any of it, which is what Result 1 showed. The obvious next test is the extras
*and* 10 epochs together, but that would be two changes at once, so I've left
it for unit 6's improvement step.

Not attempted: **a fourth label**. Nothing in the 570-comment pool needed one.
Tech-support questions and answers already split cleanly into `chatter`,
`opinion` and `backed` under the existing rules.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

**Unit 6 note on AI use:** As in unit 5, I directed Claude (in Claude Code) to
carry out this unit's steps. It labelled the 30 staff posts, ran the baseline,
the three-seed runs and the improvement, and drafted these sections. All
numbers below come from the committed JSON files.

**Unit 6 stretch features, declared before building:**

1. **A confidence check.** Report whether the model's confident predictions are
   right more often than its unsure ones, using the per-seed confidence numbers
   in `results_three_seeds_*.json`.
2. **A per-label error write-up.** For whichever label the confusion matrix
   says is worst: which label it gets confused with, and what those posts have
   in common.
3. **A second measured improvement.** If the first improvement is a training
   change, the second will be a data change, logged in the same three-seed
   table.

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

Output of `python baseline.py --trained results.json`. Both columns are scored
on the same 36 held-out posts in `test_split.csv`. The baseline is
`facebook/bart-large-mnli`, zero-shot, prompted with the definitions in
`label_definitions.txt`, on `cpu`. "Trained" is the unit 5 run in
`results.json` (seed 42, 3 epochs).

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.361 | 0.361 | +0.000 |
| Macro F1 | 0.249 | 0.298 | +0.049 |
| F1 — `backed` | 0.512 | 0.444 | -0.067 |
| F1 — `chatter` | 0.000 | 0.000 | +0.000 |
| F1 — `opinion` | 0.235 | 0.450 | +0.215 |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->
Written and committed before running `baseline.py`. I'd already seen the
trained run from unit 5 (0.361 accuracy, close to guessing). I predict the
zero-shot baseline will **match or beat it, landing around 0.40 accuracy**. It
should do best on `backed`, since "a number, price, link or quote" is the kind
of surface feature an entailment model can match. It should do worst on
`chatter`, because "takes no position" is a negative definition and those are
hard to match zero-shot. If that's right, the unit 5 fine-tune added nothing
over reading the definitions.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->
**The unit 5 fine-tune added nothing over the baseline in accuracy. Both got
13 of 36 right.** The prediction was right on two of its three calls. The
baseline matched the trained model rather than beating it, did best on
`backed` (0.512) and scored 0.000 on `chatter`.

The two models fail in different directions. In `baseline_results.json` the
zero-shot model calls **32 of 36 posts `backed`**. It reads almost any concrete
noun as "a specific detail" and never predicts `chatter`. The trained model
calls 27 of 36 posts `opinion`. Each one collapses onto a single label, and
they just picked different ones. The only real edge the fine-tune has is
`opinion` F1 (+0.215), and that comes from predicting `opinion` nearly every
time.

So 3 epochs of fine-tuning on 168 posts is not enough to beat reading the
definitions. The three-seed runs below check whether that holds beyond seed
42.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
