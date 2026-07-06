---
name: "Learned: Odoo Patterns"
globs: ["addons/**/*.py"]
topics: ["odoo", "orm", "multi-company", "access-control"]
priority: low
evidence_count: 2
last_updated: 2026-07-06
auto_generated: true
---

# Odoo Patterns

- When auditing Odoo computed fields, always check whether `with_company()` return values are discarded — this is a recurring latent multi-company bug pattern in Odoo core.
- `credit`, `credit_limit`, and `credit_to_invoice` on `res.partner` are group-restricted (`account.group_account_invoice`) — any method accessing these on behalf of a sales user MUST use `sudo()` or the caller must hold that group.

## Evidence

| Learning | Source | Date |
|----------|--------|------|
| with_company discard pattern | [reflection-TASK-001.md](../reflection/reflection-TASK-001.md) | 2026-07-06 |
| credit fields access-control | [reflection-TASK-001.md](../reflection/reflection-TASK-001.md) | 2026-07-06 |
