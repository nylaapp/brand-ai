# Motion

Many brands use none. Find out, and record the answer either way.

## Measure
On the reference store or the live site, at desktop (hover states need a real hover):
- **Transitions** on buttons, links, cards and images: read `transition-property`, `transition-duration`
  and `transition-timing-function` from computed styles, in the default state and after hover.
- **Hover effects:** card lift, image zoom, underline, colour change.
- **Page transitions and scroll reveals:** watch a page load and a slow scroll for any fade or slide.
- **Feedback:** what happens on add to cart.
- **Reduced motion:** whether the site honours the user's reduced-motion setting.

## Decide what the brand does
A short table: effect, where, duration and easing, source (measured or stated). If nothing animates, write
"No animation" in `design.md`, as with shadows, so nobody adds it later by default.

## Map into the theme
- Use the theme's own settings first (Horizon: page transition, transition to main product, add-to-cart
  animation, card hover effect). A brand with no animation turns these off.
- A motion the settings can't express (a custom duration or easing) goes in the repo's scoped stylesheet
  as a token, following the repo's cascade rules. Note it in `design.md`.
- Always honour `prefers-reduced-motion`: remove or reduce motion for those users. Keep durations short
  and never block interaction while something animates.

## Verify
On the chosen theme's preview, hover and click through each effect at desktop, check that nothing shifts layout, and
check with reduced motion switched on that the motion stops. Record "measured" or "stated" for each.
