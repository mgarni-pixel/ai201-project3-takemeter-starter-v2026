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

**AI use this unit:** I used Claude to run the scripts and draft the
write-up, and to group my model's errors, which is where the "surface cues
vs. function" finding came from. My staff-set labels were also done with
Claude.

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

**What the definitions were worth, measured:** I ran the baseline a second
time with bare label names instead of `label_definitions.txt` (`python
baseline.py --definitions no_definitions.txt --out
baseline_bare_names.json`), on the same 36 posts.

| Measure | Bare label names | With my definitions | Definitions added |
|---|---|---|---|
| Overall accuracy | 0.389 | 0.361 | −0.028 |
| Macro F1 | 0.392 | 0.249 | −0.143 |
| F1 — `backed` | 0.370 | 0.512 | +0.142 |
| F1 — `chatter` | 0.421 | 0.000 | −0.421 |
| F1 — `opinion` | 0.385 | 0.235 | −0.150 |

**My definitions made the zero-shot model worse overall.** The `backed`
definition lists "a number, price, date, model or spec, named rule or law,
link, or quote". Almost every r/LinusTechTips comment names *some* product or
number, so the entailment model matched it on 32 of 36 posts. The `chatter`
definition is mostly a list of what the post *doesn't* do ("takes no
position"), which an entailment model can't match, so it fell from 0.421 to
0.000. The bare names spread the guesses more evenly. The baseline reported
in the table above is the with-definitions run, as the brief asks.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

Notebook section 6, `RUN_LABEL = "before"`, the unit 5 defaults (3 epochs,
lr 2e-5, batch 16), on **`cpu`** (torch 2.14.1+cpu). The source file is
`results_three_seeds_before.json`. Seed 42 reproduced the unit 5 run exactly
(0.361).

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 every seed | 0.361 | 0.500 | 0.500 | MISSED |
| 2. F1 `backed` | ≥ 0.55 every seed | 0.444 | 0.167 | 0.636 | MISSED |
| 3. Lowest label F1 | ≥ 0.45 every seed | 0.000 (`chatter`) | 0.167 (`backed`) | 0.333 (`opinion`) | MISSED |
| 4. Agreement with staff set | ≥ 21/30 | 30/30 | 30/30 | 30/30 | MET (one 30-post check; it doesn't vary by seed) |
| 5. Confidence gap (most-sure third − least-sure third) | ≥ 0.15 every seed | 0.167 (0.417 − 0.250) | 0.417 (0.667 − 0.250) | 0.417 (0.750 − 0.333) | MET |

The spread table from section 6, pasted as printed:

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.361 | 0.500 | 0.500 | 0.139 |
| Macro F1 | 0.298 | 0.419 | 0.503 | 0.205 |
| F1 — `backed` | 0.444 | 0.167 | 0.636 | 0.470 |
| F1 — `opinion` | 0.450 | 0.591 | 0.333 | 0.258 |
| F1 — `chatter` | 0.000 | 0.500 | 0.538 | 0.538 |

> Accuracy moved 0.139 across seeds — more than 10 points. Your dataset is too
> small or too lopsided for a stable measure. That IS a diagnosis. Write it down.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42, from section 7 (device `cpu`):

| true \ predicted | backed | opinion | chatter |
|---|---|---|---|
| **backed** | 4 | 7 | 0 |
| **opinion** | 2 | 9 | 2 |
| **chatter** | 1 | 11 | 0 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

**11 real `chatter` posts were called `opinion`, and only 2 went the other
way.** The model never learned the `opinion`/`chatter` boundary. Every
`chatter` post that wasn't called `backed` went to `opinion`, and the
`opinion` column takes 27 of the 36 predictions. This isn't a confusion
between two labels so much as a model that defaults to `opinion`. Seed 7 is
the same but worse (31 of 36 predicted `opinion`, including 10 of 11 real
`backed` posts). The direction isn't stable either: on seed 2024, where
predictions spread out, the biggest cell flips to 6 real `opinion` posts
called `chatter`.

---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.60 on every seed | MISSED | Best seed is 0.500; none of the three reach 0.60. |
| 2 | F1 `backed` | ≥ 0.55 on every seed | MISSED | Seed 2024 clears it (0.636), but seed 42 (0.444) and seed 7 (0.167) don't, and the target has to hold on all three. |
| 3 | No label F1 below 0.45 | ≥ 0.45 on every seed | MISSED | The weakest label is below 0.45 on every seed: 0.000, 0.167, 0.333. |
| 4 | Staff agreement | ≥ 21 / 30 | MET | `agreement.py`: 30 of 30, well clear of 21. |
| 5 | Confidence gap | ≥ 0.15 on every seed | MET | Gaps are 0.167, 0.417 and 0.417, so all three clear 0.15. Seed 42 clears it by only 2 posts in 12 (5 right vs 3 right). |

No criteria were revised.

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**Misses 1, 2 and 3 have one shared cause: the task can't be reached from
this much data in this much training. Too few optimizer steps, not
inconsistent labels.**

The evidence:

1. **The model collapses onto one label.** On seed 42 it predicts `opinion`
   27 of 36 times, and on seed 7 it does so 31 of 36 times. A model that has
   learned a boundary doesn't send 10 of 11 real `backed` posts (seed 7) to
   the same column as the jokes.
2. **It's barely more confident than a random guess.** Average top-class
   confidence is 0.38–0.41 on every seed, where guessing among three labels
   gives 0.33. The classifier head has hardly moved from where it started.
3. **The arithmetic says so too.** 168 training posts ÷ batch 16 ≈ 11 steps
   per epoch × 3 epochs = **about 33 optimizer steps**, at a learning rate of
   2e-5.
4. **The same labels can be learned.** In unit 5's stretch run, seed 42 with
   identical labels and 10 epochs scored 0.583 accuracy and `chatter` F1 0.583
   (up from 0.000). Nothing about the labels changed. If the labels were the
   problem, more training on them wouldn't have fixed `chatter`.
5. **The direction of the errors flips between seeds.** `chatter` → `opinion`
   is 11 vs 2 on seed 42, but on seed 2024 the largest cell is `opinion` →
   `chatter` (6). A labelling inconsistency, where I applied the
   `opinion`/`chatter` rule two different ways, would push errors the *same*
   way on every seed.

**What the agreement report can and can't add here.** It's the instrument for
telling a labelling problem from a model problem. **I agreed with staff on
30 of 30, including all 8 posts staff marked HARD.** Rule 1 there ("is the
fact load-bearing?") is the same test as my `backed`/`opinion` rule, so the
labeller applies that kind of rule consistently. Together with point 5
(errors flipping direction between seeds) and point 4 (the same labels became
learnable with more training), the evidence points to the **model and
training**, not to my labels. One limit: the staff set has no equivalent of my
`opinion`/`chatter` "about the poster vs about the topic" line, so it can't
clear that boundary. The unit 5 cold pass (20/20, same labeller) is the only
check on it.

**Contributing, for criterion 2 in particular:** `backed` is the smallest
label (53 training posts, 11 test posts). One test post moves its F1 by about
0.08, which is why it ranges from 0.167 to 0.636. That's the "too few examples
for a label" cause, and it's why the second improvement below targets
`backed` data.

**Instability across seeds:** accuracy moves 0.139. With 36 test posts that's
5 posts, so even a fixed model can't be called against a target to better than
about ±0.07 on one seed.

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** **30 / 30 = 100%** (`python agreement.py`, written to
`agreement_results.json`). `my_staff_labels.csv` was saved before
`data/staff_labels.csv` was opened.

**Disagreements:** none, so there is nothing to adjudicate. Agreement still
tells me something, because staff marked 8 posts as HARD and I matched all
eight. Four of them are the posts I flagged as likely disputes before seeing
the key:

| Post | Staff (HARD) | Me | Rule that settled it |
|---|---|---|---|
| sp_005 "Carbon plates aren't the whole story… 2%… another 2%… 35 to 50 miles" | analysis | analysis | Rule 1: the two drops carry the argument |
| sp_010 "Three of us ran the same session… within 10 seconds" | analysis | analysis | Rule 1: hedged, but the observation is what the claim rests on |
| sp_014 "Times are down about 3%… so obviously the shoes" | hot_take | hot_take | Rule 1: the 3% is decoration ("so obviously" does the work) |
| sp_019 "Nobody actually enjoys the long run…" | hot_take | hot_take | Rule 2: a general claim, not the writer's own morning |
| sp_020 "Every injury thread… is the same injury" | hot_take | hot_take | Checkable in principle, but no count is given |
| sp_028 "Third DNF this year…" | reaction | reaction | Rule 3: the count isn't load-bearing |
| sp_029 "…the shoes I set every PB in… wrong size" | reaction | reaction | Rule 2: the writer's own realisation, now |
| sp_021 "Four minutes off. FOUR." (not marked HARD; I flagged it) | reaction | reaction | Staff: "the number is the news, not an argument" |

**What the pattern tells me:** the set is not easy, since 8 of 30 posts are
marked HARD, so 100% means the "is the number load-bearing?" test is
applied tightly. That's the same test as my own `backed`/`opinion` rule.
This is evidence *against* a labelling problem on that boundary. Two
caveats. First, Claude labelled both this set and my 240, so this measures
how consistently that labeller applies a written rule, not my unaided
judgement. Second, staff's `reaction` is narrower than my `chatter`, so this
check doesn't test my `opinion`/`chatter` boundary at all. That boundary is
where my errors cluster (see the error write-up).

---

## The Improvement

**What I changed:** One hyperparameter. `EPOCHS` went from 3 to 10 in
section 2 of the notebook. Everything else stayed the same:
`labels.csv`, lr 2e-5, batch 16, max length 128, the same three seeds and
splits, and `cpu`. The section 6 rerun used `RUN_LABEL = "after"`, so the
before file wasn't overwritten.

**Which diagnosis pointed at it:** The shared diagnosis for misses 1–3: about
33 optimizer steps isn't enough. The evidence was the collapse onto `opinion`
(27/36 and 31/36 predicted), top-class confidence of 0.38–0.41 against a
0.33 random-guess level, and unit 5's single-seed 10-epoch run fixing
`chatter` with the same labels. Ten epochs is about 110 steps. If the
diagnosis is right, predictions should spread across all three labels on
every seed and the per-label floor (criterion 3) should rise most.

### Run Log — After

Notebook section 6 with `EPOCHS = 10`, `RUN_LABEL = "after"`, the same seeds
and splits, on **`cpu`**. The source file is `results_three_seeds_after.json`.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 every seed | 0.583 | 0.639 | 0.556 | MISSED |
| 2. F1 `backed` | ≥ 0.55 every seed | 0.696 | 0.700 | 0.667 | MET |
| 3. Lowest label F1 | ≥ 0.45 every seed | 0.480 (`opinion`) | 0.519 (`opinion`) | 0.480 (`chatter`) | MET |
| 4. Agreement with staff set | ≥ 21/30 | 30/30 | 30/30 | 30/30 | MET (one 30-post check; it doesn't vary by seed) |
| 5. Confidence gap (most-sure third − least-sure third) | ≥ 0.15 every seed | −0.250 (0.417 − 0.667) | 0.750 (1.000 − 0.250) | 0.417 (0.750 − 0.333) | MISSED |

Before and after, side by side (same seeds, same test posts):

| Measure | Before: 42 / 7 / 2024 | After: 42 / 7 / 2024 |
|---|---|---|
| Overall accuracy | 0.361 / 0.500 / 0.500 | 0.583 / 0.639 / 0.556 |
| Macro F1 | 0.298 / 0.419 / 0.503 | 0.586 / 0.646 / 0.562 |
| F1 `backed` | 0.444 / 0.167 / 0.636 | 0.696 / 0.700 / 0.667 |
| F1 `opinion` | 0.450 / 0.591 / 0.333 | 0.480 / 0.519 / 0.538 |
| F1 `chatter` | 0.000 / 0.500 / 0.538 | 0.583 / 0.720 / 0.480 |
| Accuracy spread across seeds | 0.139 | 0.083 |

Seed-42 confusion matrix after the change (section 7):

| true \ predicted | backed | opinion | chatter |
|---|---|---|---|
| **backed** | 8 | 2 | 1 |
| **opinion** | 3 | 6 | 4 |
| **chatter** | 1 | 4 | 7 |

**Did it help, and how do I know:** **Yes, on what the diagnosis predicted,
but not enough to hit criterion 1, and it broke criterion 5.**

- **What improved:** Accuracy rose on all three seeds (+0.222, +0.139,
  +0.056). Two criteria flipped from MISSED to MET: `backed` F1 (2) and the
  per-label floor (3). The diagnosis predicted the predictions would spread
  out. Seed 42 now predicts exactly 12 / 12 / 12 against 7 / 27 / 2 before,
  and no seed sends more than 14 of 36 to any one label. Accuracy also became
  steadier, with the spread across seeds falling from 0.139 to 0.083.
- **What didn't:** Criterion 1 is still missed. Only seed 7 clears 0.60, and
  0.556 to 0.639 sits inside a band the notebook says "can't really be called
  either way".
- **What got worse:** Criterion 5 went from MET to MISSED. On seed 42 the
  model's most-confident third is now *less* accurate than its least-confident
  third (0.417 vs 0.667). See the confidence check below.



### Stretch: confidence check

Declared at the top of unit 6 before building. The question: are the model's
confident predictions right more often than its unsure ones? The numbers are
the `confidence` block in each seed's entry, with 12 test posts per third.

| Run | Seed | Accuracy, most-confident third | Accuracy, least-confident third | Avg. confidence when right / wrong |
|---|---|---|---|---|
| Before (3 epochs) | 42 | 0.417 | 0.250 | 0.410 / 0.405 |
| Before | 7 | 0.667 | 0.250 | 0.384 / 0.373 |
| Before | 2024 | 0.750 | 0.333 | 0.393 / 0.379 |
| After (10 epochs) | 42 | 0.417 | 0.667 | 0.664 / 0.705 |
| After | 7 | 1.000 | 0.250 | 0.650 / 0.487 |
| After | 2024 | 0.750 | 0.333 | 0.678 / 0.566 |

**Answer: mostly yes, but not reliably.** On 5 of 6 seed-runs the confident
third beats the unsure third. After the change, seed 7's most-confident 12
posts were all correct.

Two things undercut that:

1. **Before the change, the "confidence" barely existed.** Right and wrong
   answers averaged 0.38–0.41, about the 0.33 a random guess among three
   labels gets. So the before-run gaps that met criterion 5 come from tiny
   differences between near-identical scores.
2. **After the change, seed 42 inverts.** It was *more* confident when wrong
   (0.705) than when right (0.664).

So longer training made the model confident, but on seed 42 that confidence
landed on its mistakes. A threshold like "auto-tag only when confidence is in
the top third" would work on seed 7 and backfire on seed 42.

### Stretch: per-label error write-up (`opinion`)

Declared at the top of unit 6 before building. After the change, `opinion` is
the worst label on two of three seeds (0.480, 0.519, 0.538). In the seed-42
matrix only 6 of 13 real `opinion` posts are right: **4 go to `chatter` and 3
to `backed`**. Another 4 real `chatter` posts are called `opinion`. These are
the actual posts, from the seed-42 predictions.

- **`opinion` → `backed` (3): a link, a product list or a percentage that's
  only decoration.** "They should of started with Onenote, the rest of the apps
  all have alternatives that work 99% fine.. Joplin / Trillium / Obsidian…".
  Another post is a screenshot link plus "he's very salty… Justified." Another
  quotes a subreddit name. Under my rule all three are `opinion`, because the
  names and the 99% decorate the claim rather than support it. The model
  learned the surface cue (named products, links, numbers mean `backed`) and
  not the "is it load-bearing?" test.
- **`opinion` → `chatter` (4): claims dressed as questions or hedges.** "Why
  fiddle with ocr when you can grab the text from the page source?", "…2 or 3
  seconds is fair use, surely?", "I'm pretty sure I heard the little Lord
  mention he got to ASML…". My second rule says a rhetorical question counts as
  a claim. The model treats question marks and "pretty sure" as no position.
- **`chatter` → `opinion` (4): first-person habits with strong wording.**
  "Never have and never will. I don't want to talk to a computer…", "I've long
  since accepted that evil is better than good in this world." This is the
  boundary I settled late while labelling in unit 5. "Never have and never
  will" is the exact post I moved from `opinion` to `chatter` partway through.
  The model reads the strong wording as a stance.

**What they have in common:** in every case the deciding feature is something
my rules define by *function* (is the number load-bearing, is the question
rhetorical, is it about the poster or the topic). The model only sees
*surface* (digits and names, question marks, "I" and strong words). `opinion`
sits between the other two labels, so it loses posts in both directions.

### Stretch: second improvement (30 more `opinion` posts)

Declared at the top of unit 6 ("the second will be a data change"). After the
first improvement, `opinion` was the worst label (F1 0.480 / 0.519 / 0.538).
The brief's matching fix is "thirty more posts of the label with the worst
F1". I took 30 `opinion` posts at random (`random.Random(6)`) from the 163
that were labelled in unit 5's pool but never used. They're in
`data/extra_opinion.csv`. They were added to each seed's **training split
only**. `labels.csv`, the test posts and `EPOCHS = 10` didn't change, so the
only change against the after run is these 30 posts. The source file is
`results_three_seeds_after2.json`, on `cpu`.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 every seed | 0.528 | 0.694 | 0.611 | MISSED |
| 2. F1 `backed` | ≥ 0.55 every seed | 0.696 | 0.737 | 0.667 | MET |
| 3. Lowest label F1 | ≥ 0.45 every seed | 0.421 (`chatter`) | 0.667 (`chatter`) | 0.500 (`chatter`) | MISSED |
| 4. Agreement with staff set | ≥ 21/30 | 30/30 | 30/30 | 30/30 | MET |
| 5. Confidence gap | ≥ 0.15 every seed | 0.000 (0.417 − 0.417) | 0.750 (1.000 − 0.250) | 0.250 (0.750 − 0.500) | MISSED |

| Measure | After (10 epochs): 42 / 7 / 2024 | After 2 (+30 `opinion`): 42 / 7 / 2024 |
|---|---|---|
| Overall accuracy | 0.583 / 0.639 / 0.556 | 0.528 / 0.694 / 0.611 |
| F1 `opinion` | 0.480 / 0.519 / 0.538 | 0.467 / 0.690 / 0.645 |
| F1 `chatter` | 0.583 / 0.720 / 0.480 | 0.421 / 0.667 / 0.500 |
| Accuracy spread | 0.083 | 0.167 |

**Did it help?** **Not reliably.** It helped on two seeds and hurt on one.

- **Where it helped:** `opinion` F1 rose on seeds 7 and 2024 (+0.171,
  +0.107), and the mean accuracy across seeds edged up from 0.593 to 0.611.
- **Where it hurt:** On seed 42 accuracy fell (0.583 → 0.528) and `chatter`
  dropped to 0.421. That pushes criterion 3 from MET back to MISSED. In the
  seed-42 matrix, 7 real `chatter` posts are now called `opinion` (it was 4),
  so the extra `opinion` examples pulled the shared boundary toward `opinion`.
- **Stability got worse:** the accuracy spread doubled to 0.167. One version
  passes on two seeds and fails on the third, and that's the instability the
  three-seed rule is there to catch.

I'm keeping the first improvement (10 epochs, `labels.csv` only) as the
reported model.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

These are measured against the reported model, the first improvement (10
epochs).

- **Criterion 1, accuracy ≥ 0.60 (missed: 0.583 / 0.639 / 0.556).**
  - *What I'd do:* make the `opinion`/`chatter` line learnable rather than
    adding more examples of one side. That means relabelling only the
    "first-person habit vs stance" posts under one written rule, since that
    is the boundary where the errors sit, then rerunning the same three seeds.
  - *Why I stopped:* the brief allows one change. The second, data-only change
    (30 `opinion` posts) showed that leaning on one side of that boundary
    just moves the errors to the other side.
- **Criterion 5, confidence gap ≥ 0.15 (missed on seed 42: −0.250).**
  - *What I'd do:* check the gap on a larger test set before trusting it.
    Twelve posts per third means one post is 0.083, so I'd pool predictions
    across all three seeds (108 posts) and report the gap on that.
  - *Why I stopped:* pooling changes how the criterion is measured, and
    changing a criterion's measurement after seeing results is the revision
    the brief rules out.



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->

I meant the labels to capture what a comment *does*: whether a number
carries an argument, whether a question is really a claim, whether a post is
about the topic or about the poster. In the seed-42 matrix, 3 real `opinion`
posts land in `backed` and 4 in `chatter`, so the model learned what a comment
*looks like* (digits and product names mean `backed`; question marks and
"I…" mean `chatter`), which gets `backed` right (F1 ≈ 0.69) and leaves
`opinion` and `chatter` confused in both directions (4 and 4).



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
