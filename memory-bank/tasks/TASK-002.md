# TASK-002: Characterization Tests for _compute_partner_credit_warning

**Complexity**: Level 1
**Status**: COMPLETE
**Reflection**: memory-bank/reflection/reflection-TASK-002.md
**Archived**: memory-bank/archive/archive-TASK-002.md
**Completed**: 2026-07-06
**PR URL**: https://github.com/Craig-Rogers-SA/odoo/pull/1
**Roadmap**: N/A
**Branch**: task/002-characterization-tests-credit-warning
**Worktree**: N/A (Level 1 uses direct branch, not worktree)

## Task Description

Author CHARACTERIZATION tests for `sale.order._compute_partner_credit_warning`
in `addons/banyan_sale_safety/tests/`.

These are NOT unit tests. Read the method to discover its behavioral branches,
then capture what it currently returns for each one — byte-for-byte. Do NOT
assert what it SHOULD return. Use `self.assertEqual` on the full string (no
`assertIn`, no `assertRegex`). Lock language with
`self.env.context = {'lang': 'en_US'}`.

## Implementation Notes

- Target method: `sale_order.py:770-781`
- Behavioral branches identified in TASK-001 audit:
  1. `account_use_credit_limit` disabled → always empty string
  2. `state` not in `('draft', 'sent')` → always empty string
  3. credit limit not exceeded → empty string
  4. limit exceeded, `credit_to_invoice > 0` and `current_amount > 0` → "including sales orders and this document"
  5. limit exceeded, `credit_to_invoice > 0` only → "including sales orders"
  6. limit exceeded, `current_amount > 0` only → "including this document"
  7. limit exceeded, neither → base message only
- Addon structure needed: `__manifest__.py`, `__init__.py`, `tests/__init__.py`
- Language must be pinned to `en_US` to lock translation output

---

## Execution State

**Build Status**: IDLE
**Current Phase**: COMPLETE
**Can Resume**: NO

### Active Sub-Agents
- Reflection Agent: COMPLETE (2026-07-06) - Output: memory-bank/reflection/reflection-TASK-002.md

### Completed Steps
- [x] Branch created: task/002-characterization-tests-credit-warning
- [x] Addon scaffolded: addons/banyan_sale_safety/{__manifest__.py, __init__.py}
- [x] Tests written: addons/banyan_sale_safety/tests/test_characterize_credit_warning.py
  - 11 tests covering all 7 behavioral branches + boundary + state variants
- [x] Tests run: 11/11 PASS (2026-07-06, odootest DB, 6.58s, 3827 queries)
