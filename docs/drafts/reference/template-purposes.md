# Template purposes reference

A **purpose** is a template's job. The system uses purposes to pick the right layout automatically — at bind time, when a sale starts, when an order is being picked. You set a template's purpose with the pill on the console's Templates page — see [Put templates to work](../owners/templates/c12-sale-layouts-and-defaults.md).

## The purposes

| Purpose | What it's for | When it appears on a tag |
|---|---|---|
| **Normal price** | The everyday product layout | Whenever a bound product is not on sale |
| **On-sale** | The sale layout | Swaps in automatically while the product's sale window (from your POS) is active, then swaps back — including changes at midnight. Requires being paired with a Normal default |
| **Pick-by-Light — idle** | The resting look for tags used in order picking | When no pick is running |
| **Pick-by-Light — active** | The flashing-pick layout, typically showing quantity and order number readable across an aisle | While that tag's line is being picked |
| **Will-call — idle** | The empty pickup-bin sign | While the bin has no order |
| **Will-call — active** | The occupied sign showing the pickup code and customer | While an order is assigned to the bin |
| **Weather** | The everyday weather display | On tags set up as weather displays |
| **Weather alert** | The layout that takes over during a warning | While a weather alert is active for your city |

## How the system picks a template

1. **An explicit choice wins.** A template picked by hand — on the console's bind form, or via Edit on a handheld — is always used.
2. **Otherwise, the store default applies.** For each tag size and purpose, the default set on the Templates page's Defaults card is used. This is what handheld binds rely on.
3. **If several same-size templates share a purpose,** the automatic pick is the alphabetically-first active one. Rename templates to control which wins, or pick explicitly.

## Good to know

- Only **active** templates with the **right purpose** appear in the Defaults dropdowns. If a template is missing from a dropdown, check its purpose pill first.
- Downloaded and imported templates often arrive with the wrong purpose — fix the pill before setting defaults.
- When a store feature is turned off (on the console's System page), its purpose also disappears from the handhelds' options.
