# C4 Manifest

<!--
  This file is the source of truth for /banyan-c4 idempotency. It tracks every
  source directory the c4-code agent has walked, along with a content hash and
  a pointer to its generated doc. The orchestrator reads this file on every run
  to decide which subtrees to re-walk.
-->

## Run Metadata

- **Plugin Version**: 1.8.0
- **Last Run ID**: banyan-c4-20260701-init
- **Last Run At**: 2026-07-01T00:00:00Z
- **Hash Strategy**: git-tree
- **Scope**: full (odoo/ core leaf dirs + addons/ top-level module dirs)
- **Levels Built**: code (in-progress)
- **IaC Adapters Used**: dockerfile, docker-compose

## Counters

| Metric | Value |
|--------|-------|
| Directories walked this run | 0 |
| Directories reused from prior run | 0 |
| Directories archived this run | 0 |
| c4-code docs total | 0 |
| Components | 0 |
| Containers | 0 |
| IaC compute resources | 0 |
| IaC stateful resources | 0 |
| IaC messaging resources | 0 |
| IaC inferred containers (no backing) | 0 |
| Boundary resource types | 0 |
| Image-trace: traced | 0 |
| Image-trace: external | 0 |
| Image-trace: untraceable | 0 |

## Excluded Patterns

```
node_modules/
.git/
.venv/
venv/
__pycache__/
build/
dist/
out/
target/
.next/
.nuxt/
coverage/
.cache/
vendor/
static/lib/
static/src/lib/
```

## Walk Strategy Notes

This manifest covers a "practical walk" scoped at init time:
- `odoo/` core: all Python leaf directories (82 dirs, exhaustive)
- `addons/`: top-level module directories only (621 dirs, one per addon)
  - Sub-directories within each addon are NOT walked in this pass
  - Run `/banyan-c4 --scope addons/<module>` to deepen any individual addon

## Code-Level Entries

<!-- AUTO-MANAGED: code-entries -->

| Directory | Hash Strategy | Content Hash | Last Walked | Status | Doc |
|-----------|--------------|--------------|-------------|--------|-----|
| (no entries yet) | | | | | |

<!-- /AUTO-MANAGED: code-entries -->

## Component-Level Entries

<!-- AUTO-MANAGED: component-entries -->

| Component | Constituent Code Docs | Last Synthesized | Status | Doc |
|-----------|----------------------|------------------|--------|-----|
| (no entries yet) | | | | |

<!-- /AUTO-MANAGED: component-entries -->

## Container-Level Entries

<!-- AUTO-MANAGED: container-entries -->

| Container | Class | Primary IaC Resource | Image Trace | Components | Last Synthesized | Status | Doc |
|-----------|-------|---------------------|-------------|------------|------------------|--------|-----|
| (no entries yet) | | | | | | | |

<!-- /AUTO-MANAGED: container-entries -->

## Infrastructure Resources (IaC Inventory)

<!-- AUTO-MANAGED: iac-inventory -->

| Resource ID | Type | Class | IaC Source | Image / Runtime | Maps to Container | Status |
|-------------|------|-------|-----------|-----------------|-------------------|--------|
| (no entries yet) | | | | | | |

<!-- /AUTO-MANAGED: iac-inventory -->

## Pending Approvals

<!-- AUTO-MANAGED: pending-approvals -->

| File | Proposed Content | Diff Report | Removals | Material Alterations | Reason |
|------|-----------------|-------------|---------:|---------------------:|--------|
| (none yet) | | | | | |

<!-- /AUTO-MANAGED: pending-approvals -->

## Boundary Infrastructure

<!-- AUTO-MANAGED: boundary-infra -->

| Resource Type | Count | IaC Sources | Note |
|---------------|-------|-------------|------|
| (no entries yet) | | | |

<!-- /AUTO-MANAGED: boundary-infra -->

## Context Entry

<!-- AUTO-MANAGED: context-entry -->

| Last Synthesized | Status | Doc |
|------------------|--------|-----|
| (not yet synthesized) | | |

<!-- /AUTO-MANAGED: context-entry -->

## Inputs Tracked for Higher-Level Refresh

| Input | Affects | Reason |
|-------|---------|--------|
| `memory-bank/productBrief.md` | Context | Personas drive context-level diagrams |
| `docker-compose.yml` | Container + IaC Inventory | Container topology |
| `Dockerfile` | Container | Image definition |
| `memory-bank/techContext.md` | Container | Tech-stack mapping |
| Any constituent code-level entry | Component | Component is a synthesis of its code docs |
| Any constituent component | Container | Container groups components |
