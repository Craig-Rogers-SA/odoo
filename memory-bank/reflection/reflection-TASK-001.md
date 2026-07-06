# Reflection: TASK-001 - Credit Warning Knowledge-Archaeology Audit

**Date**: 2026-07-06
**Task Complexity**: Level 1
**Total Phases**: 1 (inline analysis)
**Duration**: Single session

---

## Executive Summary

TASK-001 was a knowledge-archaeology audit of the credit warning pipeline spanning `addons/sale/models/sale_order.py:770-781` and `addons/account/models/account_move.py:1846-1891`. The task produced 14 named invariants, a calibration section of 6 false invariants, and a set of recommended `systemPatterns.md` ENFORCED entries — all without making any code changes.

The audit surfaced two actionable bugs in production Odoo 18.0 code: a discarded `with_company` return (INV-001) that silently produces wrong credit data in multi-company environments, and a missing `state`/`currency_id` from `@api.depends` (INV-006) that can leave stale cached values within an ORM session. These were not introduced by this task — they exist in upstream Odoo.

The task was well-scoped for Level 1 and executed cleanly. The primary workflow friction was that `/banyan-task` is semantically designed for code-change tasks, but this was a research/analysis task — the "build" was the audit itself delivered inline rather than via `/banyan-build`.

---

## Dimension 1: Task Implementation Quality

### Requirements Achievement

**Status**: ✅ All Met

| Requirement | Status |
|---|---|
| Audit `_compute_partner_credit_warning` | ✅ |
| Audit `_build_credit_warning_message` | ✅ |
| Surface implicit invariants with file:line | ✅ 14 invariants |
| Confidence ratings (HIGH/MED/LOW) | ✅ All rated |
| 'Looks Like an Invariant But Isn't' section | ✅ 6 entries |
| Cover: sudo, with_company, @api.depends ordering | ✅ |
| Cover: discarded-return idioms | ✅ INV-001 |
| Cover: multi-record vs singleton contracts | ✅ INV-008, INV-014 |
| Cover: currency assumptions | ✅ INV-004, INV-005, INV-012 |
| Cover: state-machine gates | ✅ INV-007 |
| Cover: commercial_partner_id rollups | ✅ INV-003 |
| Cover: translation idioms | ✅ INV-013 |
| Cover: access-control side effects | ✅ INV-002 |
| Recommended systemPatterns.md ENFORCED entries | ✅ |
| No refactoring | ✅ No code changed |

### Code Quality Assessment

**Overall Rating**: Excellent (for an analysis artifact)

- **Completeness**: All requested categories covered; cross-file context (partner.py, sale/res_partner.py, sale/account_move.py) pulled in to substantiate claims
- **Evidence quality**: Each invariant anchored to a specific file:line with the exact code quoted
- **Calibration section**: False invariants were genuinely non-obvious; the `with_company` discard (FAKE-A) and `sudo()` company confusion (FAKE-D) are the kind of mistakes experienced Odoo developers make
- **Audience calibration**: Appropriate depth for a senior Odoo developer — no padding, no over-explanation of basic ORM concepts

### Technical Decisions

1. **Read partner.py and sale/res_partner.py in addition to the two target files** — necessary to substantiate INV-003 (`commercial_partner_id` rollup) and INV-009 (`credit_to_invoice` company-context sensitivity). Without these, those invariants would be assertions without evidence.

2. **Included `_get_partner_credit_warning_exclude_amount` override in sale/account_move.py** — this was not in the original spec but is a direct callee of `_build_credit_warning_message`'s call site. Omitting it would have missed INV-014.

3. **Framed INV-001 as a latent bug rather than a false invariant** — the discarded `with_company` is in both files. It's clearly intentional code that doesn't work as intended, not a placeholder. Calling it a bug (HIGH confidence) rather than "unclear intent" is the correct honest assessment.

### What Went Well

1. The bottom-up read strategy (target files → callees → field definitions → override chain) surfaced the full dependency graph without missing anything material
2. The calibration section prevented INV-001 from being incorrectly classified as "working as intended"
3. Currency invariants (INV-004, INV-005, INV-012) were kept distinct — easy to conflate but serve different purposes

### Challenges Encountered

1. **`res_partner.py` path** — initial attempt to read `addons/account/models/res_partner.py` failed (file is `addons/account/models/partner.py`). Resolved by using Grep to find the right filename.
2. **Scope of `_get_partner_credit_warning_exclude_amount`** — not in the original spec; had to make a judgment call to include it. Correct decision but added read overhead.

### Technical Debt & Future Work

- **INV-001 fix**: The `with_company` discard is a latent multi-company bug in upstream Odoo. Worth filing as an upstream bug report or patching in a local override.
- **INV-006 fix**: Adding `state` and `currency_id` to the `@api.depends` on `sale_order._compute_partner_credit_warning` is a one-line safe change.
- **systemPatterns.md**: The recommended ENFORCED entries should be merged into `memory-bank/systemPatterns.md` before any future credit-warning refactoring tasks.

---

## Dimension 2: Claude Code Ecosystem Effectiveness

### Build Session Analysis

**Build Sessions**: 1 (inline, no `/banyan-build` invoked)
**Sub-Agents Spawned**: 0
**Tool Calls (estimated)**: ~18 (Read ×8, Grep ×6, Bash ×2, Glob ×2)
**Errors Recovered**: 1 (wrong path for res_partner.py — self-corrected via Glob)

#### Tool Utilization

| Tool | Count | Notes |
|------|-------|-------|
| Read | ~8 | Target files + partner.py + sale/res_partner.py + sale/account_move.py |
| Grep | ~6 | Field definitions, method cross-references, override chain |
| Bash | ~2 | git branch, directory creation |
| Glob | ~2 | File discovery when path unknown |
| Write | 2 | Task file + this reflection |
| Edit | 1 | tasks.md registry |

### Command Workflow Evaluation

**Commands Used**: `/banyan-task` (×2 — duplicate invocation by user)

**Workflow Efficiency**: Good with one structural note

**Assessment**:
- `/banyan-task` handled the analysis task correctly as Level 1
- The command was invoked twice with identical arguments — the second invocation was correctly detected as a duplicate and no new task was created. This is good defensive behavior.
- **Gap**: `/banyan-task` is semantically framed around code changes (bug fixes, typos, config). A pure analysis/research task doesn't have a natural "build" step — the output is a report delivered inline, not a commit. The workflow has no explicit "research task" primitive. The `/banyan-reflect` step ended up reflecting on an audit rather than a code change, which required light reinterpretation of the Level 1 reflection template.

### Context File Effectiveness

**Files Loaded**: `level1-reflection.md`, `reflection-agent.md`, `persistent-context-line.md`

**Assessment**:
- `reflection-agent.md`: Comprehensive template; worked well even for a non-code task with minor adaptation
- `level1-reflection.md`: Minimal and appropriate for Level 1; the "Completed Bug Fixes" template section didn't quite fit an audit task but was easy to adapt
- **Gap**: No context file for "research/analysis" task type — these are common in brownfield archaeology work

### Memory Bank Organization

**Assessment**:
- **Structure**: Clean; `tasks/`, `reflection/`, `agent-rules/_learned/` directories are logical
- **Navigation**: Straightforward for a single active task
- **Missing**: No `systemPatterns.md` ENFORCED section yet — the audit produced concrete recommendations that should be merged there as a follow-up

### Suggested Improvements to Claude Code System

**Medium Priority**:
1. **Research task type in /banyan-task** — Add a "research/analysis" branch that doesn't expect a git diff, produces a report artifact instead of code changes, and skips the `/banyan-build` step. Current workaround (inline delivery) works but feels like the workflow fighting its own grain.
2. **Duplicate command detection** — The second `/banyan-task` invocation with identical args was handled correctly but silently. A brief "TASK-001 already exists with this description — skipping creation" message would reduce user uncertainty.

**Low Priority / Nice to Have**:
1. **systemPatterns.md auto-merge prompt** — When an audit produces recommended ENFORCED entries, `/banyan-reflect` could prompt: "Apply recommended systemPatterns.md entries? (y/n)" rather than leaving them in the audit output.

---

## Key Learnings

### Extractable Learnings (for Continuous Learning)

1. **odoo-patterns** (`addons/**/*.py`): When auditing Odoo computed fields, always check whether `with_company()` return values are discarded — this is a recurring latent multi-company bug pattern in Odoo core.
2. **odoo-patterns** (`addons/**/*.py`): `credit`, `credit_limit`, and `credit_to_invoice` on `res.partner` are group-restricted (`account.group_account_invoice`) — any method accessing these on behalf of a sales user MUST use `sudo()` or the caller must hold that group.

### Learned Rules Applied

- No learned rules available (first task in this project)

### For Claude Code Workflow

1. **Analysis tasks need a first-class primitive** — Research/audit tasks are common in brownfield Odoo work; the current `/banyan-task` → `/banyan-build` flow assumes a code output. A `/banyan-task --research` flag or a dedicated task type would fit more naturally.
2. **Duplicate invocation detection worked** — The second identical `/banyan-task` call was cleanly handled; this is good defensive behavior worth preserving.

---

## Conclusion

TASK-001 delivered a complete, evidence-based invariant map of the Odoo 18.0 credit warning pipeline. All 15 requested categories were covered, two latent bugs were identified (INV-001 multi-company discard, INV-006 missing depends), and the false-invariant calibration section adds genuine value for refactoring safety. The workflow adapted cleanly to a research task despite `/banyan-task` being primarily designed for code changes.

**Overall Task Success**: ✅ Success

**Overall Workflow Effectiveness**: ✅ Highly Effective (with minor friction on research-task semantics)

**Recommendation**: Ready to archive. Before closing, consider merging the recommended `systemPatterns.md` ENFORCED entries from the audit output as a follow-up.
