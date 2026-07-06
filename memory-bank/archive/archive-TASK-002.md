# Archive: Characterization Tests for _compute_partner_credit_warning

## Metadata
- **Task ID**: TASK-002
- **Complexity**: Level 1
- **Branch**: task/002-characterization-tests-credit-warning
- **Completed**: 2026-07-06
- **Reflection**: memory-bank/reflection/reflection-TASK-002.md

## Summary

Authored a complete characterization test suite for `sale.order._compute_partner_credit_warning` in a new `banyan_sale_safety` addon. All 11 tests pass, covering every behavioral branch identified in the TASK-001 audit plus two additional boundary/state tests.

The suite captures the method's current output byte-for-byte using `self.assertEqual` on full strings, with language locked to `en_US`. This gives the team a regression net: any future refactor that silently changes warning message text, threshold logic, or state-gate behavior will break a specific, named test.

## Solution

Created the `banyan_sale_safety` addon as a test-only module depending on `sale` and `account`. The test class extends `TestSaleCommon` (which provides `partner_a`, `company_data`, and the full sales/accounting test infrastructure). Three helpers set up test state:

- `_draft_order(amount)` — creates a draft SO for `partner_a`
- `_confirmed_order(amount)` — confirms a SO to drive `credit_to_invoice` upward
- `_post_invoice(amount)` — posts a customer invoice to drive `partner.credit` upward

Language is locked per-test in `setUp` via `self.env = self.env(context=dict(self.env.context, lang='en_US'))` (immutable reassignment — not dict mutation).

## Behavioral Branches Covered

| Test | Branch | Expected |
|------|--------|----------|
| `test_branch_feature_disabled` | `account_use_credit_limit = False` | `''` |
| `test_branch_state_draft_does_not_suppress` | `state='draft'`, over limit | warning |
| `test_branch_state_sent_does_not_suppress` | `state='sent'` via `action_lock()`, over limit | warning |
| `test_branch_state_sale_suppresses` | `state='sale'` (confirmed) | `''` |
| `test_branch_under_limit` | `total < limit` | `''` |
| `test_branch_exactly_at_limit` | `total == limit` | `''` (≤ boundary) |
| `test_branch_zero_credit_limit_means_unlimited` | `credit_limit = 0` | `''` |
| `test_branch_both_credit_to_invoice_and_current_amount` | both > 0 | "including sales orders and this document" |
| `test_branch_credit_to_invoice_only` | only `credit_to_invoice > 0` | "including sales orders" |
| `test_branch_current_amount_only` | only `current_amount > 0` | "including this document" |
| `test_branch_existing_credit_only` | only posted invoice credit | "Total amount due" |

## Files Changed

- `addons/banyan_sale_safety/__manifest__.py` — new addon manifest
- `addons/banyan_sale_safety/__init__.py` — empty init
- `addons/banyan_sale_safety/tests/__init__.py` — test package init
- `addons/banyan_sale_safety/tests/test_characterize_credit_warning.py` — 11 characterization tests
- `memory-bank/tasks/TASK-002.md` — task tracking
- `memory-bank/reflection/reflection-TASK-002.md` — reflection document
- `memory-bank/agent-rules/_learned/testing-patterns.md` — 2 extracted Odoo test idioms
- `memory-bank/learning-log.md` — learning event log
- `memory-bank/learning-metrics.md` — metrics tracking

## Test Results

```
banyan_sale_safety: 13 tests  6.58s  3827 queries
11/11 test methods PASS
Suite-wide: 2 failed, 2 errors of 1594 (all pre-existing in unrelated modules)
```

## Notes

- `action_lock()` confirmed as the correct Odoo 18 method for `state='sent'` transition
- `@tagged('post_install', '-at_install')` is correct for tests that depend on full account infrastructure
- `invalidate_recordset(['credit', 'credit_to_invoice'])` is load-bearing after SO confirmation or invoice posting — without it, ORM cache masks the compute trigger
- Pre-existing suite failures in `sales_team` and `account_edi_ubl_cii` are unrelated to this task and should be investigated separately
