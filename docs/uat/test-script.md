---
search:
  exclude: true
---

# Sosh UAT Test Script

52 cases across 12 categories. Click any column header in the index
below to sort. Click a case ID to jump to its details. Skip cases for
tiers you don't have — mark them `N-A` in
[result-template.md](result-template.md).

## Index

| ID                          | Tier   | Category               | Case                                         |
| --------------------------- | ------ | ---------------------- | -------------------------------------------- |
| [UAT-CLD-01](#uat-cld-01)   | CLOUD  | Account & Access       | Operator can log into admin console          |
| [UAT-CLD-02](#uat-cld-02)   | CLOUD  | Account & Access       | Wrong password is rejected clearly           |
| [UAT-CLD-03](#uat-cld-03)   | CLOUD  | Account & Access       | Change-password flow works                   |
| [UAT-CLD-04](#uat-cld-04)   | CLOUD  | Account & Access       | Logout actually logs you out                 |
| [UAT-CLD-05](#uat-cld-05)   | CLOUD  | Storefront             | Browse and find product info                 |
| [UAT-CLD-06](#uat-cld-06)   | CLOUD  | Storefront             | Add to cart and view cart                    |
| [UAT-CLD-07](#uat-cld-07)   | CLOUD  | Storefront             | Reach checkout (do NOT pay)                  |
| [UAT-CLD-08](#uat-cld-08)   | CLOUD  | Stores & Users         | Customers/orgs page lists your org           |
| [UAT-CLD-09](#uat-cld-09)   | CLOUD  | Stores & Users         | Edit your store's name                       |
| [UAT-CLD-10](#uat-cld-10)   | CLOUD  | Stores & Users         | Create a new user                            |
| [UAT-CLD-11](#uat-cld-11)   | CLOUD  | Stores & Users         | Reset that user's password                   |
| [UAT-CLD-12](#uat-cld-12)   | CLOUD  | Stores & Users         | API token lifecycle                          |
| [UAT-CLD-13](#uat-cld-13)   | CLOUD  | Tag Lifecycle          | See the tag inventory                        |
| [UAT-CLD-14](#uat-cld-14)   | CLOUD  | Tag Lifecycle          | Drill into one tag's detail                  |
| [UAT-CLD-15](#uat-cld-15)   | CLOUD  | Tag Lifecycle          | Bind a tag to a different product            |
| [UAT-CLD-16](#uat-cld-16)   | CLOUD  | Tag Lifecycle          | Unbind that tag                              |
| [UAT-CLD-17](#uat-cld-17)   | CLOUD  | Tag Lifecycle          | Trigger a flash (LED test)                   |
| [UAT-CLD-18](#uat-cld-18)   | CLOUD  | Tag Lifecycle          | Bulk bind via CSV                            |
| [UAT-CLD-19](#uat-cld-19)   | CLOUD  | Designer               | Open the designer                            |
| [UAT-CLD-20](#uat-cld-20)   | CLOUD  | Designer               | Browse existing templates                    |
| [UAT-CLD-21](#uat-cld-21)   | CLOUD  | Designer               | Create a new blank template                  |
| [UAT-CLD-22](#uat-cld-22)   | CLOUD  | Designer               | Add and edit a text element                  |
| [UAT-CLD-23](#uat-cld-23)   | CLOUD  | Designer               | Add an icon from the icon picker             |
| [UAT-CLD-24](#uat-cld-24)   | CLOUD  | Designer               | Add a barcode/QR element                     |
| [UAT-CLD-25](#uat-cld-25)   | CLOUD  | Designer               | Upload an image asset                        |
| [UAT-CLD-26](#uat-cld-26)   | CLOUD  | Designer               | Save and reopen the template                 |
| [UAT-CLD-27](#uat-cld-27)   | CLOUD  | Templates → Tag        | Change a product price; tag updates          |
| [UAT-CLD-28](#uat-cld-28)   | CLOUD  | Templates → Tag        | Edit template; bound tags queue              |
| [UAT-CLD-29](#uat-cld-29)   | CLOUD  | Templates → Tag        | Bulk import prices via CSV                   |
| [UAT-CLD-30](#uat-cld-30)   | CLOUD  | Templates → Tag        | Weather widget renders                       |
| [UAT-KIT-01](#uat-kit-01)   | KIT    | POS Sync               | Open the POS config page                     |
| [UAT-KIT-02](#uat-kit-02)   | KIT    | POS Sync               | Test connection with bad creds               |
| [UAT-KIT-03](#uat-kit-03)   | KIT    | POS Sync               | Test connection with real creds              |
| [UAT-KIT-04](#uat-kit-04)   | KIT    | POS Sync               | Run sync; tags update                        |
| [UAT-MOB-01](#uat-mob-01)   | MOBILE | Mobile App             | Install and open the APK                     |
| [UAT-MOB-02](#uat-mob-02)   | MOBILE | Mobile App             | Scan the binding QR                          |
| [UAT-MOB-03](#uat-mob-03)   | MOBILE | Mobile App             | Picker role: home screen                     |
| [UAT-MOB-04](#uat-mob-04)   | MOBILE | Mobile App             | Signage role display                         |
| [UAT-MOB-05](#uat-mob-05)   | MOBILE | Mobile App             | Staff role: navigate tabs                    |
| [UAT-KIT-05](#uat-kit-05)   | KIT    | Pick-by-Light          | Operator creates pick session                |
| [UAT-KIT-06](#uat-kit-06)   | KIT    | Pick-by-Light          | Picker scans session; tag lights             |
| [UAT-KIT-07](#uat-kit-07)   | KIT    | Pick-by-Light          | Confirm pick; LED clears                     |
| [UAT-KIT-08](#uat-kit-08)   | KIT    | Commander :8080        | Reach the dashboard                          |
| [UAT-KIT-09](#uat-kit-09)   | KIT    | Commander :8080        | View fleet/assignments                       |
| [UAT-KIT-10](#uat-kit-10)   | KIT    | Commander :8080        | Configure weather                            |
| [UAT-KIT-11](#uat-kit-11)   | KIT    | Commander :8080        | Beacon shows online                          |
| [UAT-KIT-12](#uat-kit-12)   | KIT    | Commander TUI          | TUI PIN login                                |
| [UAT-KIT-13](#uat-kit-13)   | KIT    | Commander TUI          | Push from TUI screen 4                       |
| [UAT-KIT-14](#uat-kit-14)   | KIT    | Commander TUI          | Mobile binding from TUI screen 8             |
| [UAT-CLD-31](#uat-cld-31)   | CLOUD  | Reports                | Fleet summary report                         |
| [UAT-CLD-32](#uat-cld-32)   | CLOUD  | Reports                | Activity log                                 |
| [UAT-CLD-33](#uat-cld-33)   | CLOUD  | Reports                | CSV export                                   |

!!! tip "Sorting"
    Click any column header above to sort. Click again to reverse.
    Sort by **Tier** to group all your cases together.

---

## Cases

### UAT-CLD-01 — Operator can log into admin console { #uat-cld-01 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                                    |
| Category | Account & Access                                                                             |
| Pre      | Tester has UAT username + password.                                                          |
| Steps    | 1. Open `https://sovereignshelf.net/admin/login`<br>2. Enter username + password<br>3. Click Sign In |
| Expected | Within 5 seconds you land on the admin dashboard and see your name (or username) on the page, plus a list/summary of stores/tags. |

### UAT-CLD-02 — Wrong password is rejected clearly { #uat-cld-02 }

| Field    | Value                                                                              |
| -------- | ---------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                          |
| Category | Account & Access                                                                   |
| Pre      | UAT-CLD-01 passed.                                                                 |
| Steps    | 1. Log out (top-right menu, or `/admin/logout`)<br>2. Try to log in with username + password `wrong` |
| Expected | You stay on the login page. A clear error message tells you the credentials were wrong. The page does not crash, redirect to a stack trace, or hang. |

### UAT-CLD-03 — Change-password flow works { #uat-cld-03 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                                    |
| Category | Account & Access                                                                             |
| Pre      | Logged in as UAT user.                                                                       |
| Steps    | 1. Visit `/admin/change-password`<br>2. Enter current password<br>3. Enter new password<br>4. Confirm and submit<br>5. Log out, log back in with the new password<br>6. Change it back to the original |
| Expected | Each step succeeds with a clear confirmation. The new password works on next login. Reverting works the same way. |

### UAT-CLD-04 — Logout actually logs you out { #uat-cld-04 }

| Field    | Value                                                                              |
| -------- | ---------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                          |
| Category | Account & Access                                                                   |
| Pre      | Logged in.                                                                         |
| Steps    | 1. Click Sign Out<br>2. With the browser back button, try to return to the admin dashboard |
| Expected | You are sent back to the login page, not shown cached admin content. The back button does not let you bypass authentication. |

### UAT-CLD-05 — Browse the storefront and find product info { #uat-cld-05 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                                    |
| Category | Storefront                                                                                   |
| Pre      | None.                                                                                        |
| Steps    | 1. Open `https://sovereignshelf.com`<br>2. Browse to a hardware product (e.g. Sentinel or Guardian)<br>3. Read the product page |
| Expected | Page loads in under 5 seconds. Product details are legible. Images render. Nothing obviously broken. |

### UAT-CLD-06 — Add to cart and view cart { #uat-cld-06 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Storefront                                                             |
| Pre      | UAT-CLD-05 passed.                                                     |
| Steps    | 1. Click Add to Cart<br>2. Open the cart<br>3. Change quantity to 2<br>4. Remove the item |
| Expected | Each action updates the cart immediately. Totals recompute. Removing leaves a clear empty-cart state. |

### UAT-CLD-07 — Reach checkout (do NOT pay) { #uat-cld-07 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                                    |
| Category | Storefront                                                                                   |
| Pre      | Cart has at least one item.                                                                  |
| Steps    | 1. Click Checkout<br>2. Fill in a fake shipping address (`123 Test St, Anytown` — not real)<br>3. Proceed to payment step<br>4. **Stop.** Do not enter payment details. |
| Expected | You can move through the address step without errors. Shipping rate options appear. The payment step loads but does not charge until you submit. |

### UAT-CLD-08 — Customers/orgs page lists your org { #uat-cld-08 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Stores & Users                                                         |
| Pre      | Logged in.                                                             |
| Steps    | 1. Visit `/admin/customers`                                            |
| Expected | You see your UAT org listed, with at least one store under it. The page does not throw an error. |

### UAT-CLD-09 — Edit your store's name { #uat-cld-09 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Stores & Users                                                         |
| Pre      | UAT-CLD-08 passed.                                                     |
| Steps    | 1. From `/admin/customers` find your store<br>2. Edit its name (e.g. append `-edited`)<br>3. Save<br>4. Refresh the page |
| Expected | The new name persists after refresh. No error message.                 |

### UAT-CLD-10 — Create a new user under your org { #uat-cld-10 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Stores & Users                                                         |
| Pre      | Logged in.                                                             |
| Steps    | 1. Visit `/admin/users`<br>2. Click New (or equivalent)<br>3. Fill in fake user (`tester-bob` / `bob@example.test`)<br>4. Save |
| Expected | The new user appears in the list. You can click into their detail page. |

### UAT-CLD-11 — Reset that user's password { #uat-cld-11 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Stores & Users                                                         |
| Pre      | UAT-CLD-10 passed.                                                     |
| Steps    | 1. From the user's detail page, click Reset Password<br>2. Confirm    |
| Expected | A new temporary password is shown or emailed. The flow makes it clear how the user receives it. |

### UAT-CLD-12 — Personal access token lifecycle { #uat-cld-12 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                                    |
| Category | Stores & Users                                                                               |
| Pre      | Logged in.                                                                                   |
| Steps    | 1. Visit `/admin/tokens`<br>2. Create a new token (give it a name)<br>3. Copy the token shown<br>4. Revoke the same token |
| Expected | Token created with a clear "shown only once" warning. Revoking removes it from the list.     |

### UAT-CLD-13 — See the tag inventory { #uat-cld-13 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Tag Lifecycle                                                          |
| Pre      | Logged in. UAT store has ≥3 demo tags pre-bound.                       |
| Steps    | 1. Visit `/admin/tags`                                                 |
| Expected | List of tags with ESL codes, last-seen, bound product. Loads in <5s.   |

### UAT-CLD-14 — Drill into one tag's detail { #uat-cld-14 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Tag Lifecycle                                                          |
| Pre      | UAT-CLD-13 passed.                                                     |
| Steps    | 1. Click on one tag's ESL code                                         |
| Expected | Detail page shows bound product, template, last push, battery (if reported), recent activity. |

### UAT-CLD-15 — Bind a tag to a different product { #uat-cld-15 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Tag Lifecycle                                                          |
| Pre      | Detail page open from UAT-CLD-14.                                      |
| Steps    | 1. Click Bind (or Re-bind)<br>2. Pick a different product from the catalog<br>3. Confirm |
| Expected | Tag's bound product updates. Detail page now shows new product. A push is queued (status like "queued" or "pending"). |

### UAT-CLD-16 — Unbind that tag { #uat-cld-16 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Tag Lifecycle                                                          |
| Pre      | UAT-CLD-15 passed.                                                     |
| Steps    | 1. From the same detail page, click Unbind<br>2. Confirm              |
| Expected | Tag now shows as unbound. Product name no longer appears.              |

### UAT-CLD-17 — Trigger a flash (LED test) { #uat-cld-17 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                                    |
| Category | Tag Lifecycle                                                                                |
| Pre      | A tag detail page is open.                                                                   |
| Steps    | 1. Click Flash (or Locate)                                                                   |
| Expected | UI confirms the flash was sent. **`[KIT]` testers**: the physical LED actually flashes within ~5 seconds. |

### UAT-CLD-18 — Bulk bind via CSV { #uat-cld-18 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                                    |
| Category | Tag Lifecycle                                                                                |
| Pre      | Logged in. UAT store has demo products.                                                      |
| Steps    | 1. Visit `/admin/tags`<br>2. Find Bulk bind / CSV upload<br>3. Download the CSV template<br>4. Edit it with 2 rows mapping ESL codes to product SKUs<br>5. Upload it |
| Expected | Upload reports rows succeeded/failed. The 2 tags now show as bound to the SKUs you specified. |

### UAT-CLD-19 — Open the designer { #uat-cld-19 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                                    |
| Category | Designer                                                                                     |
| Pre      | Logged in.                                                                                   |
| Steps    | 1. Visit `https://sovereignshelf.net/design`                                                 |
| Expected | A graphical canvas-based editor loads. No JS errors in the browser console (skip this if you don't know how to open DevTools — just confirm the UI looks intact). |

### UAT-CLD-20 — Browse existing templates { #uat-cld-20 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Designer                                                               |
| Pre      | Designer open.                                                         |
| Steps    | 1. Find the templates list/library                                     |
| Expected | The 2-3 demo templates pre-seeded for the UAT org are listed. You can preview each. |

### UAT-CLD-21 — Create a new blank template { #uat-cld-21 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Designer                                                               |
| Pre      | Designer open.                                                         |
| Steps    | 1. Click New Template<br>2. Pick any tag size (e.g. TAG21)<br>3. Name it `uat-<your-name>-1` |
| Expected | A blank canvas appears, sized to the tag profile you picked.           |

### UAT-CLD-22 — Add and edit a text element { #uat-cld-22 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Designer                                                               |
| Pre      | Blank template open.                                                   |
| Steps    | 1. Add a text element<br>2. Type your name<br>3. Move it<br>4. Resize it |
| Expected | Text appears, can be moved, can be resized, font scales sensibly without clipping. |

### UAT-CLD-23 — Add an icon from the icon picker { #uat-cld-23 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Designer                                                               |
| Pre      | Template open.                                                         |
| Steps    | 1. Add an icon element<br>2. Search the icon picker (e.g. `star` or `cart`)<br>3. Pick one |
| Expected | Picker has hundreds of options. Chosen icon appears on the canvas.     |

### UAT-CLD-24 — Add a barcode/QR element { #uat-cld-24 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Designer                                                               |
| Pre      | Template open.                                                         |
| Steps    | 1. Add a barcode or QR element<br>2. Bind it to a product field (SKU is a typical default) |
| Expected | A barcode/QR renders on the canvas. The data binding is visible in the property panel. |

### UAT-CLD-25 — Upload an image asset { #uat-cld-25 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                                    |
| Category | Designer                                                                                     |
| Pre      | Template open.                                                                               |
| Steps    | 1. Find the asset upload control<br>2. Upload any small PNG or JPG<br>3. Drag the uploaded image onto the canvas |
| Expected | Upload succeeds. Image appears in your asset library and on the canvas. (It will be quantised to black/white/red — expected, don't flag.) |

### UAT-CLD-26 — Save and reopen the template { #uat-cld-26 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Designer                                                               |
| Pre      | A template with at least one element.                                  |
| Steps    | 1. Save<br>2. Close and reopen the template from the list             |
| Expected | Template reopens with everything you placed, exactly as you left it.   |

### UAT-CLD-27 — Change a product price; bound tag updates { #uat-cld-27 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]` (full effect on `[KIT]`)                                                           |
| Category | Templates → Tag                                                                              |
| Pre      | A demo tag is bound to a demo product (visible on `/admin/tags`).                            |
| Steps    | 1. Visit products section of the admin<br>2. Edit the price of the product bound to your test tag<br>3. Save<br>4. Watch the tag's detail page for ~30 seconds |
| Expected | Tag enters "queued / pushing" state then shows new push completed. **`[KIT]` testers**: physical tag display updates within ~3 minutes. |

### UAT-CLD-28 — Edit a template; all tags using it queue a push { #uat-cld-28 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                                    |
| Category | Templates → Tag                                                                              |
| Pre      | A template is in use by ≥1 tag.                                                              |
| Steps    | 1. Open that template in the designer<br>2. Move an element a noticeable amount<br>3. Save<br>4. Visit `/admin/tags` and look at tags using this template |
| Expected | Each affected tag is marked for push (queued) without you having to click anything else.     |

### UAT-CLD-29 — Bulk import product prices via CSV { #uat-cld-29 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                                    |
| Category | Templates → Tag                                                                              |
| Pre      | Logged in.                                                                                   |
| Steps    | 1. Find products bulk import (CSV template)<br>2. Download template<br>3. Edit 2-3 rows with new prices<br>4. Upload |
| Expected | Import reports rows succeeded/failed. Affected bound tags queue a push automatically.        |

### UAT-CLD-30 — Weather widget renders { #uat-cld-30 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                                                    |
| Category | Templates → Tag                                                                              |
| Pre      | A template in the designer.                                                                  |
| Steps    | 1. Add a weather widget to a template<br>2. Set a city in the property panel (e.g. `Toronto`)<br>3. Preview the template |
| Expected | Current weather icon and temperature appear in the preview. Data is plausible (not 999°). If no city options appear, mark Fail. |

### UAT-KIT-01 — Open the POS config page { #uat-kit-01 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                                      |
| Category | POS Sync                                                                                     |
| Pre      | Commander reachable on the local network. Tester knows the Commander LAN IP.                 |
| Steps    | 1. From a laptop on the same LAN, open `http://<commander-ip>:8080/admin/pos-config`<br>2. Log in if prompted |
| Expected | A POS configuration page loads. Fields for SQL host, port, database, username, password.     |

### UAT-KIT-02 — Test connection with bad creds { #uat-kit-02 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                                      |
| Category | POS Sync                                                                                     |
| Pre      | UAT-KIT-01 passed.                                                                           |
| Steps    | 1. Enter bogus SQL details (host `1.2.3.4`)<br>2. Click Test Connection                      |
| Expected | A clear "could not connect" error within ~30 seconds. Page does not hang or crash.           |

### UAT-KIT-03 — Test connection with the real creds { #uat-kit-03 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                |
| Category | POS Sync                                                               |
| Pre      | Real test-POS creds provided by author.                                |
| Steps    | 1. Enter provided host, port, database, username, password<br>2. Click Test Connection |
| Expected | "Connection successful" or equivalent.                                 |

### UAT-KIT-04 — Run a sync; tags update { #uat-kit-04 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                                      |
| Category | POS Sync                                                                                     |
| Pre      | UAT-KIT-03 passed; ≥1 tag is bound to a product whose price exists in the test POS.          |
| Steps    | 1. Click Run Sync Now<br>2. Wait for it to finish<br>3. Check the bound tag's display       |
| Expected | Sync reports rows processed. Within ~3 minutes, the physical tag shows the price from the POS. |

### UAT-MOB-01 — Install and open the APK { #uat-mob-01 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[MOBILE]`                                                                                   |
| Category | Mobile App                                                                                   |
| Pre      | APK file from the author on your phone.                                                      |
| Steps    | 1. Tap the APK to install (allow from this source if prompted)<br>2. Open the app           |
| Expected | App installs without error. First screen prompts you to scan a binding QR or begin onboarding. |

### UAT-MOB-02 — Scan the binding QR { #uat-mob-02 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[MOBILE]`                                                                                   |
| Category | Mobile App                                                                                   |
| Pre      | Author has provided a binding QR (printed or as an image).                                   |
| Steps    | 1. From the first-boot screen, tap Scan QR<br>2. Point camera at the QR                     |
| Expected | Phone reads the QR within ~5 seconds and proceeds to PIN/login. Store name shown matches the UAT store. |

### UAT-MOB-03 — Log in as Picker { #uat-mob-03 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[MOBILE]`                                                             |
| Category | Mobile App                                                             |
| Pre      | UAT-MOB-02 passed; you've been told to log in as Picker.               |
| Steps    | 1. Enter your PIN<br>2. Look around the home screen                   |
| Expected | Home shows pickable sessions/orders. Tapping into one shows tasks/items. UI looks made for a phone. |

### UAT-MOB-04 — Switch to Signage role { #uat-mob-04 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[MOBILE]`                                                             |
| Category | Mobile App                                                             |
| Pre      | Author has told you how to switch roles.                               |
| Steps    | 1. Switch to the Signage role per the author's instructions            |
| Expected | Phone goes into a passive full-screen display showing store graphics. No interactive controls (correct). |

### UAT-MOB-05 — Switch to Staff role; navigate the tabs { #uat-mob-05 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[MOBILE]`                                                             |
| Category | Mobile App                                                             |
| Pre      | Switch to Staff role.                                                  |
| Steps    | 1. Tap each of the bottom tabs (Dashboard / Tags / Stock / More)       |
| Expected | Each tab loads without error. Each shows content relevant to its name. |

### UAT-KIT-05 — Operator creates a pick session { #uat-kit-05 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                |
| Category | Pick-by-Light                                                          |
| Pre      | Commander reachable; pick-by-light feature enabled.                    |
| Steps    | 1. Open `http://<commander-ip>:8080/`<br>2. Find pick sessions section<br>3. Create a new session with 2-3 items |
| Expected | Session is created with a session ID or QR. Operator-side UI shows the session as ready. |

### UAT-KIT-06 — Picker scans the session and sees the lit tag { #uat-kit-06 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                                      |
| Category | Pick-by-Light                                                                                |
| Pre      | UAT-KIT-05 passed; phone is in Picker role; tags are physically present.                     |
| Steps    | 1. On the phone, scan the session QR (or enter the ID)<br>2. Look at the shelf              |
| Expected | First tag in the session has its LED lit. Phone shows item name and quantity to pick.        |

### UAT-KIT-07 — Confirm a pick; LED clears, next lights { #uat-kit-07 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                                      |
| Category | Pick-by-Light                                                                                |
| Pre      | UAT-KIT-06 passed.                                                                           |
| Steps    | 1. Scan the item's barcode (or tap Confirm if no scanner)                                    |
| Expected | Within ~3s the lit tag goes dark and the next tag lights. After last item the phone shows session-complete. |

### UAT-KIT-08 — Reach the dashboard { #uat-kit-08 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                                      |
| Category | Commander :8080                                                                              |
| Pre      | Commander on the LAN.                                                                        |
| Steps    | 1. Open `http://<commander-ip>:8080/`<br>2. Log in (`sovereign` / `shelf` unless rotated)   |
| Expected | Dashboard shows tag count, beacon count, service health.                                     |

### UAT-KIT-09 — View fleet/assignments { #uat-kit-09 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                |
| Category | Commander :8080                                                        |
| Pre      | Logged into local admin.                                               |
| Steps    | 1. Visit the Assignments page                                          |
| Expected | A list of `(tag, template, SKU)` rows. You can edit one assignment.    |

### UAT-KIT-10 — Configure weather { #uat-kit-10 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                                      |
| Category | Commander :8080                                                                              |
| Pre      | Logged in.                                                                                   |
| Steps    | 1. Visit weather settings page<br>2. Set a city (e.g. `Calgary`)<br>3. Save<br>4. Click Refresh / Test |
| Expected | Within ~30s the dashboard shows a successful weather pull. Tags configured for weather mode queue a push. |

### UAT-KIT-11 — Beacon shows online { #uat-kit-11 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                                      |
| Category | Commander :8080                                                                              |
| Pre      | Beacon plugged into a Commander LAN port and powered.                                        |
| Steps    | 1. Visit the APs / Beacons page                                                              |
| Expected | Beacon's MAC is listed and shows Online within ~60s of being plugged in. No manual configuration. |

### UAT-KIT-12 — TUI PIN login { #uat-kit-12 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                |
| Category | Commander TUI                                                          |
| Pre      | HDMI display + USB keyboard plugged into Commander.                    |
| Steps    | 1. Look at the screen<br>2. Enter the PIN provided by the author      |
| Expected | TUI dashboard loads. You can see at least the fleet count and the time. |

### UAT-KIT-13 — Push from TUI { #uat-kit-13 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                |
| Category | Commander TUI                                                          |
| Pre      | TUI logged in.                                                         |
| Steps    | 1. Navigate to screen 4 (Push)<br>2. Trigger "push changed"           |
| Expected | A live progress bar shows current/total/failed. Completes within a few minutes. |

### UAT-KIT-14 — Mobile binding from TUI screen 8 { #uat-kit-14 }

| Field    | Value                                                                                        |
| -------- | -------------------------------------------------------------------------------------------- |
| Tier     | `[KIT]`                                                                                      |
| Category | Commander TUI                                                                                |
| Pre      | TUI logged in.                                                                               |
| Steps    | 1. Navigate to screen 8 (Mobile)<br>2. Generate a binding QR                                |
| Expected | A QR code appears on the screen. Scanning it from a fresh phone produces the same outcome as UAT-MOB-02. |

### UAT-CLD-31 — Fleet summary report { #uat-cld-31 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Reports                                                                |
| Pre      | Logged in.                                                             |
| Steps    | 1. Visit `/admin/reports`                                              |
| Expected | A summary view shows tag count, online %, last push status. Numbers are plausible. |

### UAT-CLD-32 — Activity log { #uat-cld-32 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Reports                                                                |
| Pre      | Logged in. You've performed several actions in earlier cases.          |
| Steps    | 1. Visit `/admin/reports/activity`                                     |
| Expected | Chronological log of actions. Recent things you did (binds, pushes) appear within ~1 minute. |

### UAT-CLD-33 — CSV export { #uat-cld-33 }

| Field    | Value                                                                  |
| -------- | ---------------------------------------------------------------------- |
| Tier     | `[CLOUD]`                                                              |
| Category | Reports                                                                |
| Pre      | A reports page that offers CSV export.                                 |
| Steps    | 1. Click Export CSV                                                    |
| Expected | A CSV downloads. Opening it in any spreadsheet shows sensible column headers and rows. |

---

## End

Total: 33 cloud + 5 mobile + 14 kit = **52** cases. Save your filled
[result-template.md](result-template.md) and send it back when done.
