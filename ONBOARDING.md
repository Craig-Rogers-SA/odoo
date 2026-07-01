# Odoo Developer Field Guide

Operational knowledge that lives outside the source code — the tribal rules every developer needs before they lose a database, send a real email from a test environment, or spend two hours on a stale asset cache.

---

## Database Management

### Demo data is a one-way door

When creating a database at `/web/database/manager`, the "Load demo data" checkbox cannot be undone without dropping and recreating the database entirely. Never check it for a database you intend to use for realistic testing or production-like workflows.

### Neutralize a production dump before using it

Before loading a production database copy into your dev environment, manually disable the following — or you will send real emails and trigger real scheduled actions against live data:

| Model | What to disable | Where to find it |
|-------|----------------|-----------------|
| `ir.mail_server` | All outgoing mail servers | Settings → Technical → Email → Outgoing Mail Servers |
| `ir.cron` | All active scheduled actions | Settings → Technical → Automation → Scheduled Actions |
| `payment.provider` | All live payment credentials | Website → Configuration → Payment Providers |

> **Trap: `docker-compose down -v` destroys your database.** The `-v` flag removes named volumes including `pg-data`. Use plain `docker-compose down` to stop containers while keeping data intact.

---

## Install vs. Upgrade

### `-i` and `-u` are not interchangeable

`-i module` runs only on first install — if the module is already installed, it does nothing. `-u module` re-runs all data files, recomputes stored fields, and applies schema changes. When in doubt, use `-u`.

> **Trap: New stored computed fields leave existing rows NULL.** When you add `store=True` to a compute field, all records created before the upgrade have no value. Run `-u your_module` to trigger recomputation. Reports and filters on that field silently return nothing until this is done.

### File load order in the manifest is execution order

Files listed under `data:` in `__manifest__.py` load in the order they appear. `security/ir.model.access.csv` must come before any XML that references groups defined within it — otherwise you get a confusing reference error at install time that doesn't explain the real cause.

---

## When to Restart vs. Reload

New developers either restart for every change (slow) or assume reload covers everything (broken). The rule is precise: Python requires a restart; XML and access records do not.

| Change type | What's required |
|-------------|----------------|
| Python model / controller | Full server restart |
| `__manifest__.py` | Full restart + `-u module` |
| XML views | Use `--dev=xml` for auto-reload, or restart. No `-u` needed. |
| JS / CSS static assets | Clear Odoo asset bundle cache + browser cache (see Debug Mode) |
| `ir.model.access.csv` | Run `-u module` — no restart needed |
| `ir.rule` records | Run `-u module` — no restart needed |

---

## Debug Mode

Debug mode is the primary tool for diagnosing permission errors, broken views, and field issues — and it is mentioned nowhere in the codebase. Activate it by appending `?debug=1` to any URL, or via **Settings → (scroll to bottom) → Activate developer mode**.

| Mode | URL parameter | Unlocks |
|------|--------------|---------|
| Standard debug | `?debug=1` | Technical menu, field metadata on hover, view IDs, access rights inspector |
| Assets debug | `?debug=assets` | Unminified JS and CSS — required for readable stack traces |
| Test debug | `?debug=tests` | Runs the JS test suite in the browser |

### The asset cache has two layers

When JS or CSS changes don't appear after clearing the browser cache, Odoo has a second cache layer. In debug mode: **Settings → Technical → User Interface → Views**, then delete the asset bundle records. This step is not documented anywhere in the UI.

---

## ORM Gotchas

### The N+1 query trap

Accessing a relational field inside a Python loop triggers one SQL query per record. The ORM makes this easy to write wrong and impossible to notice until load testing.

```python
# Triggers one SQL query per order — silent performance killer
for order in orders:
    print(order.partner_id.name)

# Correct — ORM prefetches in a single batched query
orders.mapped('partner_id.name')
```

### `sudo()` is not full access

`sudo()` bypasses record-level `ir.rule` filters, but **does not bypass `ir.model.access`** (model-level ACL). Developers use it expecting total access and still receive `AccessError` on models the sudo user cannot read at the model level.

### Shell sessions don't persist without an explicit commit

In `odoo-bin shell`, all changes are inside a transaction that rolls back on exit.

```python
env['res.partner'].create({'name': 'Test Partner'})
env.cr.commit()  # Required — or everything rolls back on exit
```

---

## Extension Pitfalls

### Always call `super()` in overridden methods

Skipping `super()` in `create`, `write`, `unlink`, or any `action_*` method silently drops all other modules' hooks on that method — chatter entries, workflow transitions, downstream computed field updates. There is no error; business logic simply stops happening.

### `_name` + `_inherit` together creates a fork, not an extension

Defining both `_name = 'my.model'` and `_inherit = 'sale.order'` copies fields into a new independent model — it does not extend `sale.order`. The original model is unchanged. No error is raised.

> **Trap: Never patch core files.** Any change outside `addons/` will be overwritten by the next upstream merge. Keep all customizations as addon modules.

### Missing manifest dependency looks like a Python error

If module B inherits a model from module A but A is missing from B's `depends`, the failure at load time surfaces as a Python `AttributeError` or `KeyError` in the ORM registry — not a dependency error. The fix is adding A to `depends` in `__manifest__.py`, but the error message gives no indication of this.

---

*Odoo 18.0 · Last updated 2026-07-01*
