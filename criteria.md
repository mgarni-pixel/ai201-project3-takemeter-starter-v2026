# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

All five are measured on the held-out test split. Each one has to hold on
**every one of the three seeds** (42, 7, 2024) in unit 6, not on average.

Context for the numbers: `labels.csv` has 240 r/LinusTechTips comments split
75 `backed`, 85 `opinion` and 80 `chatter`. A 15% test split is 36 posts, about
11 / 13 / 12 per label, so each test post is worth about 2.8 points of
accuracy. Always guessing the biggest label (`opinion`) scores 0.35.

## 1. Overall accuracy is at least 0.60 on every seed.

**Why this target:** Guessing the majority label gets 0.35, so 0.60 means the
model is right on about 22 of 36 posts, which is far enough above guessing that
I'd trust it as a rough first pass over a thread. I didn't go higher because
`backed` vs `opinion` depends on whether a detail is load-bearing, which isn't
something a surface cue can settle, and a lot of my own labels were judgment
calls on exactly that line.

## 2. `backed` has an F1 of at least 0.55 on every seed.

**Why this target:** `backed` is the label TakeMeter exists for, because it
marks the comments worth reading. It's also my smallest label, with about 11
test posts, so one or two misses move its F1 by around 0.1. I set it below
criterion 1 for that reason. It also can't be met by flagging every post with a
digit or a link, because my decision rule labels decoration numbers ("6'4", 310
lbs", "95% correct") as not `backed`.

## 3. No label has an F1 below 0.45 on any seed.

**Why this target:** This is the floor for the weakest label, whichever one it
is. With three roughly equal labels, a model that collapses one of them into
another can still reach 0.60 accuracy, and this catches that. 0.45 is about 15
points under criterion 1 because roughly 12 test posts per label makes a single
label's F1 jumpy.

## 4. On the 30-post staff set, my labels agree with staff on at least 21 of 30 (70%).

**Why this target:** This is the consistency check. The staff taxonomy
(`analysis` / `hot_take` / `reaction`) uses the same load-bearing-fact test as
my `backed` vs `opinion` rule, so I should mostly apply it the way they did. I
didn't set 90%, because the brief says several of the 30 were picked for being
ambiguous. Their `reaction` label is also narrower than my `chatter`, which
covers jokes and questions too, and I expect that mismatch to cost me some
posts.

## 5. Accuracy on the model's most-confident third is at least 0.15 higher than on its least-confident third, on every seed.

**Why this target:** A real TakeMeter would only auto-tag comments it's sure
about and leave the rest alone, which only works if confidence means
something. `results.json` reports both thirds, and with 36 test posts each third
is 12 posts, so 0.15 is about 2 more correct posts. A gap smaller than that
could come from a single lucky split.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
