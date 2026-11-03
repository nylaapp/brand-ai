# Mobile pass (375 x 812)

Measure where you can; mark measured rows `[Measured]` and judged rows `[Heuristic]`.

| # | Check | How |
|---|---|---|
| M1 | Tap targets at least 44 x 44 CSS px (the practical target; WCAG 2.2 minimum is 24 x 24) with space between neighbours | Measure bounding boxes of buttons, links, icons, form controls |
| M2 | No horizontal scroll: document width equals viewport width | Compare scrollWidth and innerWidth |
| M3 | Text is at least 16 CSS px for body copy and inputs (smaller input text makes iOS zoom in) | Computed font size |
| M4 | No text truncated so the meaning is lost (prices, names, button labels) | Look; list the elements |
| M5 | The primary action is visible in the first screen, or a sticky action stays reachable | Screenshot at scroll 0 and mid-page |
| M6 | A sticky bar, banner or chat bubble does not cover content or the primary action | Look while scrolling |
| M7 | Popups and cookie banners can be closed with a thumb and do not hide the page for long | Look on load |
| M8 | Carousels and galleries swipe, show position, and do not trap vertical scroll | Look; do not interact beyond swiping |
| M9 | Form fields use the right keyboard (email, tel, number) and labels stay visible | Inspect input types |
| M10 | Images are sized for the screen (no huge files scaled down) and do not shift the layout | Check dimensions and layout shift |
| M11 | Menu opens, shows where you are and closes without losing place | Look |
| M12 | Reaching the primary action from the top of a long page takes one obvious step | Judge |

If the browser cannot emulate a phone viewport, say so and mark this stream partial.
