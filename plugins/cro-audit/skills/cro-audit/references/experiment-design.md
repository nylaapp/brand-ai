# Experiment design

For items in the **Test** bucket. The skill writes the plan and checks the maths; the experiment is
run in the person's testing tool or by their developer.

## 1. Write the hypothesis

> Because we saw **[evidence]**, we believe that **[change]** for **[segment]** will **[effect]**,
> measured by **[primary metric]**.

Example shape: "Because 9 of 24 mobile recordings show visitors tapping the announcement bar to book
and the funnel shows 40% fewer booking starts on mobile, adding a Book button to the phone header for
mobile visitors will increase booking starts per session." Every hypothesis names its evidence.

## 2. Choose metrics

- **One primary metric** closest to the change and to money (booking starts, add-to-cart rate,
  completed purchases). Decide it before the test; don't pick the winner afterwards.
- **Guardrail metrics** that must not get worse (revenue per visitor, bounce, errors, page speed,
  cancellations or refunds).
- Optional secondary metrics for learning, not for deciding.

## 3. Size and duration

Run `scripts/sample_size.py --baseline <current rate> --mde <smallest worthwhile relative change>
--daily-visitors <visitors to the tested page per day>`.

- If the answer is more than about eight weeks, the test isn't feasible as designed. Test a bigger
  change, test where there is more traffic, use a metric closer to the click, or don't test (use
  qualitative checks and a careful before/after with the limits stated).
- Run **whole weeks**, at least two, so weekday and weekend behaviour is covered. Avoid major
  promotions, launches and holidays unless they are the point.
- Split traffic evenly unless there is a reason; randomise per visitor, and keep a visitor in the same
  arm for the whole test.

## 4. Run it cleanly

- **Don't peek and stop early.** Looking daily and stopping when it "looks significant" inflates false
  wins. Decide the sample size up front and read once. (Sequential testing methods exist; use them only
  if the tool provides them and you understand them.)
- **Check the split** (`scripts/ab_result.py` reports a sample ratio mismatch). A mismatch means a bug;
  discard the result.
- **QA first**: test the variant on the real devices and browsers before sending traffic, and confirm
  the events fire in both arms.
- **One change at a time** where you can. If you combine changes, you can learn that the bundle worked,
  not which part.
- **More variants need more traffic**: each extra arm adds a comparison; `sample_size.py --variants`
  applies a conservative correction.

## 5. Read it

Use `scripts/ab_result.py --control visitors,conversions --variant visitors,conversions`. Read the
interval, not just the p-value: a wide interval that touches zero means "not enough information", not
"no effect". Check guardrails. Look at device and new vs returning only as leads for the next test; don't
declare winners in slices you didn't plan.

## 6. Record it

Whatever the result, write down the hypothesis, the evidence, the dates, the sample, the result with its
interval, what was learned, and the next step. A flat or losing test that teaches why is worth keeping.

## Low traffic

If the page can't support a test: ship the "Just do it" fixes, make larger changes, run user tests and
surveys for the why, and measure before and after with the limits stated (seasonality and other changes
can't be ruled out). Say plainly that this is weaker evidence than a controlled test.
