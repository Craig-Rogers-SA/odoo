# TASK-001: Credit Warning Knowledge-Archaeology Audit

**Complexity**: Level 1
**Status**: COMPLETE
**Archived**: memory-bank/archive/archive-TASK-001.md
**Completed**: 2026-07-06
**PR URL**: https://github.com/DaKaZ/odoo/pull/2
**Roadmap**: N/A
**Branch**: task/001-credit-warning-archaeology-audit
**Worktree**: N/A
**Reflection**: memory-bank/reflection/reflection-TASK-001.md

## Task Description

Run a knowledge-archaeology audit on `_compute_partner_credit_warning` at
`addons/sale/models/sale_order.py:770-781` AND its callee
`_build_credit_warning_message` at `addons/account/models/account_move.py:1846-1891`.

Surface every implicit invariant a naive refactor might silently break.
For each: name, file:line, what would break if dropped, confidence (HIGH/MED/LOW).

Include a 'Looks Like an Invariant But Isn't' calibration section.

Look for: sudo, with_company, with_context, @api.depends ordering, discarded-return
idioms, multi-record vs singleton contracts, currency assumptions, state-machine
gates, boundary conditions, field rollups (commercial_partner_id), translation
idioms (_()),  access-control side effects.

Do NOT refactor. Audience: senior Odoo developer. Aim for completeness over brevity.

Also include 'Recommended systemPatterns.md ENFORCED Entries' section.

## Execution State

**Build Status**: IDLE
**Current Phase**: COMPLETE
**Can Resume**: NO

### Completed Steps
- [x] Task created
- [x] Branch created: task/001-credit-warning-archaeology-audit
- [x] Audit delivered inline (14 invariants, 6 false invariants, systemPatterns recommendations)
- [x] Reflection document created: memory-bank/reflection/reflection-TASK-001.md
- [x] Learned rules extracted: memory-bank/agent-rules/_learned/odoo-patterns.md
