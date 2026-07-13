# Show live product data

**You'll learn:** how to bind an object to a data field so one template can print the real name, price, or barcode of every product in your store.

**Before you start:**

- The Designer is open — see [the Designer tour lesson](c02-designer-tour.md).
- You have at least one text object on the canvas — see [Add text and paragraphs](c03-text-and-paragraphs.md).
- You're on a desktop computer — the Designer does not run on phones or tablets.

!!! video "Watch: Show live product data (~5 min)"
    Video coming soon — the written steps below cover everything.

This lesson is the core skill of the whole module. Here is the idea in two sentences: an object on your canvas shows sample text — whatever you typed when you made it. **Binding** that object to a data field tells the Designer to replace the sample with the real product's value when the label prints, so one template serves every product in your store.

## Bind an object to a data field

1. Click a text object on the canvas to select it. Binding works the same way on paragraphs, barcodes, QR codes, icons, and pictures.
2. In the Properties panel on the right, find the **Data Binding** section.
3. Keep the mode toggle on **Single Product**. The other mode is for large labels that show several products at once — that's covered in the multi-product templates lesson (coming soon).
4. If you see a Product / Order / Weather choice, leave it on **Product**. That's the one for price labels.
5. Open the **Field** dropdown. Fields come in groups so they're easy to find: Product (names and descriptions), Pricing, Identifiers (SKU and barcode), Inventory, Details, Supplier, Price Levels, your point-of-sale system's (POS) custom fields, and more. The full catalogue is in the [data fields reference](../../reference/data-fields.md).
6. Pick a field — for example, the product's name. That's it. Your sample text stays on the canvas as a stand-in, but at print time the product's real value appears in its place.

!!! screenshot "Screenshot: Properties panel with the Data Binding section open and the Field dropdown expanded, showing the grouped field list; highlight the Field dropdown"
    To capture: assets/designer/data-binding-field-dropdown.png

## Dress up the value

The Data Binding section also has a few finishing touches. All of them wrap around or reshape the value — the field itself never changes.

- **Prefix** and **Postfix** add text before and after the value. Currency is simply a `$` typed into the Prefix box — there is no separate currency setting. A Postfix of `/ea` turns `4.99` into `$4.99/ea`.
- **Number Format** groups big numbers with commas, so `1234.56` prints as `1,234.56`.
- **Superscript ¢** raises the cents above the dollars for that classic price-tag look.

!!! tip
    Hover the small ⓘ next to these options to see a worked example before you commit.

!!! screenshot "Screenshot: a selected price text object with Prefix set to $ and Superscript ¢ checked, plus the canvas showing the styled price; highlight the Prefix box and the Superscript ¢ checkbox"
    To capture: assets/designer/price-prefix-superscript.png

## When a product doesn't have the field

Not every product has every field, and each object type handles that differently:

- A bound **text object** prints **blank** — the sample text disappears. If you bind a line to the sale price and the product isn't on sale, that line simply doesn't print. That's often exactly what you want, but check it by [previewing with a real product](c10-preview-with-real-products.md).
- **Barcodes and QR codes** fall back to their **Static Data** value instead of going blank.
- **Icons and pictures** keep whatever you drew.

??? note "An older shortcut: #field_name inside plain text"
    Plain text that contains a field name with a `#` in front — like `#sku` — also gets swapped for the real value at print time. It's an older shortcut you may spot in templates downloaded from the library. It still works, but use the Field dropdown for your own designs — it's easier to read and harder to mistype.

## Check your work

- Preview with a real product ([lesson 10 shows how](c10-preview-with-real-products.md)) — the preview shows that product's actual name and price in your layout, not your sample text.
- Your price shows the `$` and the cents styled the way you chose.
- Click each bound object and confirm the Field dropdown shows the field you meant.

## If something looks wrong

- **The preview still shows my sample text** — the object isn't bound yet. Select it and pick a field in Properties > Data Binding.
- **The value prints blank** — that product doesn't have the field. Preview with a product that does, or accept the blank if that's the design (common for sale prices).
- **My price has no dollar sign** — type `$` into the Prefix box. The field carries only the number.
- **A big number has no commas** — turn on **Number Format** in the Data Binding section.

**Next:** [Add shapes, lines, and colours](c05-shapes-lines-and-colours.md).
