# Measuring contrast correctly

Muted text is usually alpha-blended (`opacity`, `rgb(var(--color-foreground-rgb) / X%)`, `color-mix(...)`) over a scheme background that varies. The opacity number in CSS says nothing about rendered contrast.

1. Take the report's `explanation` values (for example `contrast of 2.34 (foreground #918e88, background #e0dacf)`) to sanity-check your model. The element's font size and weight tell you whether 4.5:1 (normal text) or 3:1 (large text: 24px and up, or 18.5px and up if bold) applies.
2. Composite the foreground over the background at rising opacity until the relative-luminance contrast clears the threshold with headroom. First check whether the theme already uses a "muted but legible" opacity elsewhere and reuse it before inventing a value.
3. After editing, verify on the live page by walking the ancestor chain: composite each ancestor's `background-color` (including alpha) down to the element, then compute contrast against the resolved foreground. `getComputedStyle` may return `rgb()`, `rgba()` or `color(srgb r g b)` (common for `color-mix`), so the parser must handle all three.

```js
const lin = c => (c/=255) <= 0.03928 ? c/12.92 : ((c+0.055)/1.055) ** 2.4;
const L = ([r,g,b]) => 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b);
const ratio = (a,b) => { const [x,y] = [L(a),L(b)].sort((p,q)=>q-p); return (x+0.05)/(y+0.05); };
const blend = (fg,a,bg) => fg.map((v,i)=>v*a + bg[i]*(1-a));
```

4. Check every colour scheme the component can render in. A pass on a light scheme can fail on a mid-tone one.
5. Never accept "the value looks reasonable".
