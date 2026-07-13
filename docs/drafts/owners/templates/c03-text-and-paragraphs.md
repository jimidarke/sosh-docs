# Add text

**You'll learn:** how to put single-line text and wrapping paragraphs on a label, and when to reach for each one.

**Before you start:**

- The Designer is open — see [Tour the Designer](c02-designer-tour.md).
- You're on a desktop computer — the Designer does not run on phones or tablets.

!!! video "Watch: Add text (~4 min)"
    Video coming soon — the written steps below cover everything.

The Designer gives you two kinds of text, and they behave very differently. **Text** holds exactly one line — perfect for a price or a SKU. **Paragraph** holds text that *wraps*: when a line reaches the edge of its box, it continues on a new line below, like the words in a book. Picking the right one saves a lot of head-scratching, so this lesson covers both.

## Add single-line text

1. Click the **T** (Text — Single Line) button on the left tool strip. A text box appears on the label.
2. Type your words. Either double-click the box and type right on the label, or keep it selected and edit the **Content** box in the Properties panel on the right, under **Text**.
3. Style it in **Properties > Text**:
    - **Font** — pick a typeface from the dropdown. A live sample underneath shows what each one really looks like, so choose by eye.
    - **Size** — how tall the letters are.
    - **Weight** — normal or bold.
    - **Style** — normal or italic.
    - **Align** — sit the words at the left, middle, or right of the box.
    - The colour swatches — **Color** (the letters), **Bg** (the fill behind them), and **Border** — each offer only **White**, **Black**, **Red**, or **None**. That's not a limitation of the Designer; those are the only colours a tag can display.
4. Resize the box by dragging the handles on its **left and right sides** — those are the only handles it has. The height is locked to the font size, so to make the text taller, raise the **Size** number instead.

!!! screenshot "Screenshot: a selected single-line Text object with Properties > Text open on the right; highlight the left/right resize handles and the Content box"
    To capture: assets/designer/text-properties-panel.png

Here's the rule to remember: **single-line text never wraps.** If the words grow wider than the box, the extra is simply cut off at the edge. And if you press Enter while typing, the line break turns into a space — one line means one line.

## Add a paragraph (text that wraps)

For anything longer than a line — a product name that might run long, a short description — use a Paragraph.

1. Click the **P** (Paragraph — Multi-Line) button on the left tool strip.
2. Set the box **width** by dragging its side handles. Width is the only size you choose: text wraps at that width, and the box grows downward on its own as lines are added. That's why the **Height** field in Properties is greyed out — the Designer manages it for you.
3. In **Properties > Paragraph**, the **Word Wrap** checkbox controls *where* lines break. Checked, lines break between whole words. Unchecked, a line can break anywhere — even in the middle of a word — which fits more in but reads worse.

<!-- REVIEW: confirm which state of the Word Wrap checkbox is the default for new paragraph objects -->

4. To stop a paragraph from growing forever, check **Limit Lines** and set **Max Lines** to the most lines you'll allow.

!!! screenshot "Screenshot: a selected Paragraph with wrapped text on the canvas; highlight the Word Wrap and Limit Lines checkboxes and the greyed-out Height field"
    To capture: assets/designer/paragraph-wrap-properties.png

!!! warning "Limit Lines drops text silently"
    When a paragraph runs past its Max Lines, the extra lines are simply not drawn — there's no "..." to warn you. Leave a line of headroom for your longest product names, then check the tricky ones in preview ([Preview with real products](c10-preview-with-real-products.md)).

!!! tip "Text or Paragraph?"
    Need one short line — a price, a SKU, a heading? Use **Text**. Need anything that might wrap — a product name, a description? Use **Paragraph**. You cannot make a Text box taller, so if you're ever fighting a Text box for a second line, you picked the wrong tool.

## Check your work

- You can type into a Text object two ways: double-click it, or edit **Content** in the Properties panel.
- You changed the font and watched the live sample under the dropdown update.
- Your paragraph re-wraps when you drag its side handles, and the box grows downward on its own.
- You can say which tool you'd use for a price (Text) and for a product name (Paragraph) — and why.

## If something looks wrong

**Words are cut off at the right edge** — that's a single-line Text object doing exactly what it does. Replace it with a Paragraph, which wraps instead of clipping.

**The end of your paragraph is missing** — **Limit Lines** is set too low. Raise **Max Lines**, or uncheck it while you experiment.

**You can't drag a Text box taller** — by design. A Text box's height comes from its font size; raise **Size** instead.

**You pressed Enter but everything stayed on one line** — single-line Text turns line breaks into spaces. Use a Paragraph for multiple lines.

**Next:** [Show live product data](c04-show-live-product-data.md)
