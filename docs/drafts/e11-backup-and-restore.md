# Back up and restore your Commander

**You'll learn:** what your Commander saves for you every night, how to keep your own copy, how to put a backup back if something goes wrong — and the one thing you must store somewhere safe today.

**Before you start:**

- You're signed in to the Guardian console ([Sign in](../getting-started/a3-sign-in.md)).
- You have somewhere safe and *offline* to keep a recovery key — a locked drawer, a safe, a password manager. Not a sticky note on the Commander.

Your Commander already backs itself up every night. This lesson is about the other half: knowing it's working, keeping a copy you control, and being able to put things back on a bad day.

## What's in a backup (and what isn't)

A backup saves **your setup, not your products**:

| Saved | Not saved |
|---|---|
| Which product is on which tag | Your product catalog and prices |
| Your label designs | Your customer orders |
| Store settings, staff, weather setup | |
| Your product name changes and photos | |

That split is deliberate. Your POS is the master copy of products, prices and orders — after a restore the Commander simply re-syncs them, usually within a few minutes. There's no point carrying a second copy of data you already own somewhere else.

One exception worth knowing: **product renames and photos you added yourself are saved**, because they exist nowhere but on your Commander.

## Your recovery key — do this once, today

Every backup is **encrypted with your 16-digit recovery key**. That is the whole point: a backup file is useless to anyone who finds it. It also means that without the key, *nobody* can open your backups — not your staff, not us.

Your key was issued when your Commander was set up. **Write it down and put it somewhere offline, away from the Commander itself.** If the Commander's disk ever fails, the key is what turns a saved backup back into a working store.

!!! warning "If you don't know where your recovery key is"
    Ask your installer or contact support *before* you need it. A missing key is only a problem on the worst day of the year, which is exactly the wrong time to find out.

## Check your nightly backup is healthy

1. In the Guardian console, click **System** in the left menu and find the **Backup** card.

2. Read the line under the description. It tells you one of three things:

    - **Last backup: today** (or a day or two ago) — nothing to do.
    - **No successful backup in N days** — worth a look. The most common cause is the Commander having been offline; see *If something looks wrong* below.
    - **No successful backup on record** — this one needs sorting out. Contact support.

    !!! screenshot "Screenshot: the System page Backup card, with the freshness line and the target/profile dropdowns highlighted"
        To capture: assets/console/system-backup-card.png

3. Under **Recent backups** you'll see the last several nights listed. Your Commander keeps roughly the last five, and anything from the past 30 days.

That's the whole routine. Glance at it once a month — say, when you check your license — and you'll never be surprised.

## Keep your own copy

The nightly backup is automatic and hands-off. A copy you hold yourself is worth taking before anything big: a POS changeover, a store remodel, a large re-tagging job.

4. On the **Backup** card, set the first dropdown to **Download to this computer**.

5. Leave the second dropdown on **Settings only** — that's the same content as the nightly backup, and it's small.

6. Click **Back up now** and wait. When it finishes, a **Download** button appears. Click it and save the file somewhere you'll find it again.

    !!! screenshot "Screenshot: the Backup card after a download-target backup completes, with the green Download button visible"
        To capture: assets/console/system-backup-download-ready.png

7. Store the file and your recovery key **in different places**. Together they restore your store; separately, neither is worth anything to anyone.

??? note "The bigger option: Full snapshot"
    The second dropdown also offers **Full snapshot**. That adds your entire product list, every product photo, and the phone apps — everything, not just settings. It's much larger, and it deliberately never leaves your building: you can save it to this computer or to a USB stick, but it is never uploaded anywhere.

    Most stores never need it. It's there for moving to replacement hardware without waiting on a POS re-sync, and for stores that keep photos the POS doesn't have.

## Put a backup back

Restoring is the emergency button, not a routine. **It overwrites what's on the Commander right now** — bindings, designs and settings — and restarts the device. Your tags re-render afterwards, and you'll need to type your POS password in again.

8. On the **System** page, find the **Restore** card and choose where the backup is coming from:

    - **From cloud** — pick a night from the list. This is the usual choice.
    - **From a file on this computer** — choose a file you downloaded earlier, then click **Inspect**. The console tells you what's in it and when it was taken *before* anything is overwritten. Always inspect first.
    - **From USB** — insert the stick, click **Scan USB**, and pick a backup from the list.

    !!! screenshot "Screenshot: the System page Restore card showing the cloud list, the file picker with Inspect, and the typed-confirmation box"
        To capture: assets/console/system-restore-card.png

9. Type `RESTORE` in the confirmation box and tick **device will restart**. The restore buttons stay greyed out until you do both — that's on purpose.

10. Click the restore button for your chosen source, then leave the Commander alone. It will restart and come back on its own.

11. When it's back: sign in, go to the **POS** page and re-enter your POS password, then click **Run sync now**. Your catalog and orders flow back in.

## Check your work

- The **Backup** card shows a recent date, and **Recent backups** lists several nights.
- Your recovery key is written down somewhere offline, away from the Commander.
- You've downloaded one copy of your own and know where it is.
- After a restore: tags show the right products, your designs are intact, and the Products page has filled back in from your POS.

## If something looks wrong

**"No successful backup in N days"** — nearly always means the Commander lost its internet connection for a while. Check the Dashboard: if it's back online, the next night's backup will catch up on its own. Still stuck after two nights? Contact support.

**"No successful backup on record"** — the Commander has never managed one. This needs support; don't wait for it to fix itself.

**Inspect says the file can't be opened** — either it isn't a Sovereign Shelf backup file, or it came from a *different* Commander. A backup can only be opened by the store it was taken from.

**The restore buttons won't light up** — you've typed `RESTORE` but not ticked the restart box, or the other way around. Both are required.

**Prices and products are missing after a restore** — expected for a few minutes. They come from your POS, not the backup. Re-enter your POS password on the **POS** page and click **Run sync now**.

??? note "Secrets Vault — for replacing the hardware"
    Some installations also have a **Secrets Vault** card on the System page. It's a different job from a backup: it captures everything that makes this box *your store's* Commander — the keys and passwords it uses to talk to the cloud and to your POS — onto a USB stick, so a blank replacement unit can become this Commander without an internet connection.

    It never goes to the cloud, and it's protected by a passphrase **you** choose. **If you lose that passphrase the stick is unrecoverable** — there's no reset. Keep the stick and the passphrase in separate places.

    If you don't see this card, your installation doesn't have it switched on. That's the normal setting; ask your installer if you need it.

**Next:** back to [Running the store](../owners/operations/index.md) for the rest of the day-to-day lessons.
