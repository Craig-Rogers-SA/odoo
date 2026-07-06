# Project Brief

## Project Overview

**Project**: Odoo 18.0
**Description**: Local development environment for Odoo — an open-source, modular Enterprise Resource Planning (ERP) and CRM suite. This repository is a fork/customization of the official Odoo 18.0 source for local development and customization purposes.

**Core Purpose**: Develop, customize, and extend Odoo business application modules for ERP use cases including sales, accounting, inventory, HR, manufacturing, and ecommerce.

## Goals

- Develop and test custom Odoo addon modules
- Customize existing Odoo business workflows
- Extend Odoo functionality for specific business requirements
- Maintain a stable local Docker-based development environment

## Repository Structure

- **Type**: Poly-repo
- **Workspace Tool**: None
- **Workspace Root**: N/A

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `odoo/` | Core Odoo framework (Python package, ORM, HTTP, CLI) |
| `addons/` | 621+ official Odoo addon modules |
| `docker/` | Docker configuration files (odoo.conf, Dockerfile) |
| `setup/` | Installation and packaging utilities |
| `debian/` | Debian packaging configuration |
| `doc/` | Documentation |
| `.github/` | GitHub workflows and issue templates |

### Key Entry Points

| File | Purpose |
|------|---------|
| `odoo-bin` | Main CLI executable |
| `requirements.txt` | Python dependencies |
| `docker-compose.yml` | Full stack Docker setup |
| `Dockerfile` | Container image definition |
| `setup.py` | Package setup |

## Git Configuration

- **Repository**: Yes
- **Provider**: GitHub
- **CLI Available**: gh
- **Remote URL**: https://github.com/DaKaZ/odoo.git
- **Default Branch**: 19.0
- **Archive Strategy**: push-and-pr

## Stakeholders

- **Odoo S.A.** — Upstream maintainer
- **Development Team** — Local customization and extension developers
- **End Users** — Business users operating Odoo modules

## Scope

This is a development environment for the full Odoo 18.0 platform. Custom work should be organized as addon modules in the `addons/` directory or in a separate custom addons path.
