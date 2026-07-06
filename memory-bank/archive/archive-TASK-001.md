# Archive: TASK-001 - Credit Warning Knowledge-Archaeology Audit

## Metadata
- **Task ID**: TASK-001
- **Complexity**: Level 1
- **Branch**: task/001-credit-warning-archaeology-audit
- **Completed**: 2026-07-06

## Summary

A knowledge-archaeology audit of the Odoo 18.0 credit warning pipeline spanning two functions:
- `_compute_partner_credit_warning` — `addons/sale/models/sale_order.py:770-781`
- `_build_credit_warning_message` — `addons/account/models/account_move.py:1846-1891`

The audit surfaced 14 named invariants, 6 false invariants (calibration section), and recommended `systemPatterns.md` ENFORCED entries. No code was modified.

## Key Findings

### Actionable Bugs in Upstream Odoo 18.0

| ID | Description | Impact | File:Line |
|----|-------------|--------|-----------|
| INV-001 | `with_company()` return discarded — no-op in both callers | Wrong credit data in multi-company setups | `sale_order.py:773`, `account_move.py:1827` |
| INV-006 | `@api.depends` missing `state` and `currency_id` | Stale cached warning within ORM session after state/currency change | `sale_order.py:770` |

### Critical Invariants (must not be broken in any refactor)

| ID | Invariant | Risk if Dropped |
|----|-----------|-----------------|
| INV-002 | `order.sudo()` required — `credit`/`credit_limit`/`credit_to_invoice` are group-restricted | `AccessError` for all sales users |
| INV-003 | All credit arithmetic on `commercial_partner_id`, never child contacts | Silent false-negatives on credit checks |
| INV-004 | `current_amount` must be in company currency | Cross-currency sum → wrong threshold comparison |
| INV-007 | State-machine gates (`draft`/`sent` for SO; `draft`+`out_invoice` for AM) | Warning spam on confirmed documents; NoneType crash |
| INV-008 | `_build_credit_warning_message` is a model-level utility — never add `ensure_one()` | `ValueError` on every sale order credit check |
| INV-010 | `credit_limit = 0.0` means unlimited, not zero-dollar block | Inverting check blocks all partners without limits |

## Files Examined (no changes made)

- `addons/sale/models/sale_order.py` — primary audit target
- `addons/account/models/account_move.py` — primary audit target
- `addons/account/models/partner.py` — `credit`, `credit_to_invoice`, `credit_limit` field definitions
- `addons/sale/models/res_partner.py` — `_compute_credit_to_invoice` override
- `addons/sale/models/account_move.py` — `_get_partner_credit_warning_exclude_amount` override

## Recommended Follow-Up

1. **Apply systemPatterns.md ENFORCED entries** from the audit (see reflection document)
2. **Fix INV-001**: `order_sudo = order.with_company(order.company_id).sudo()` in `sale_order.py:779`
3. **Fix INV-006**: Add `state`, `currency_id` to `@api.depends` at `sale_order.py:770`

## Notes

The `_get_partner_credit_warning_exclude_amount` override chain (`account → sale`) is a critical part of the pipeline not mentioned in the original spec but audited for completeness (INV-014).

## References

- Reflection: `memory-bank/reflection/reflection-TASK-001.md`
- Learned rules: `memory-bank/agent-rules/_learned/odoo-patterns.md`
