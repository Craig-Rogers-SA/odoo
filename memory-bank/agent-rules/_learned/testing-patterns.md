---
name: "Learned: Odoo Testing Patterns"
globs: ["addons/*/tests/*.py"]
topics: ["testing-patterns", "odoo"]
priority: low
evidence_count: 2
last_updated: 2026-07-06
auto_generated: true
---

# Odoo Testing Patterns

- Lock translation in `setUp` with `self.env = self.env(context=dict(self.env.context, lang='en_US'))` — not dict mutation — so characterization test strings are stable across locale changes.
- Call `partner.invalidate_recordset(['credit', 'credit_to_invoice'])` after confirming a sale order or posting an invoice to prevent stale ORM cache from masking the compute trigger under test.

## Evidence

| Learning | Source | Date |
|----------|--------|------|
| env language locking idiom | [reflection-TASK-002.md](../reflection/reflection-TASK-002.md) | 2026-07-06 |
| invalidate_recordset after state transitions | [reflection-TASK-002.md](../reflection/reflection-TASK-002.md) | 2026-07-06 |
