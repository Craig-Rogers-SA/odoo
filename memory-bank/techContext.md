# Tech Context

## Technology Stack

### Primary Language & Runtime
- **Python 3.10+** (minimum 3.10, 3.12 recommended for Docker)
- Entry point: `odoo-bin` executable
- WSGI-based server

### Web Framework
- **Werkzeug** 2.0.2–3.0.1 — WSGI application server, HTTP routing
- **Jinja2** 3.0.3–3.1.2 — Server-side template rendering
- **Odoo HTTP Framework** — Custom decorator-based routing system

### Database
- **PostgreSQL 16** (required — no MySQL, no SQLite for production)
- Driver: **psycopg2** 2.9.x
- Connection pooling via psycopg2.pool
- Transaction isolation: REPEATABLE_READ

### Frontend
- **QWeb** — Odoo's XML-based client-side templating
- **JavaScript** (OWL framework in newer versions, legacy in Odoo 18)
- **LESS/CSS** compiled via node-less / rtlcss
- **Bootstrap** — Responsive grid system

### Concurrency (Unix/Linux only)
- **Gevent** 21.8.0–24.11.1 — Non-blocking async I/O
- **Greenlet** — Lightweight pseudo-threads
- Long-polling on port 8072

### Key Libraries

| Library | Purpose |
|---------|---------|
| lxml 4.8–5.2 | XML/HTML parsing |
| Pillow 9.0–12.1 | Image processing |
| reportlab | PDF generation |
| openpyxl / xlrd / xlwt | Excel support |
| cryptography / pyopenssl | SSL/TLS, crypto |
| passlib | Password hashing (PBKDF2-SHA512) |
| requests | HTTP client |
| Babel | i18n, date/time formatting |
| zeep | SOAP/WSDL for EDI |
| vobject | iCalendar parsing |
| qrcode | QR code generation |
| freezegun | Time mocking in tests |

## Infrastructure

### Containerization
- **Docker** — Base image: `python:3.12-slim` (Debian)
- **Docker Compose** — Orchestrates `db` (PostgreSQL 16) + `odoo` services
- Dev mode: `sync+restart` hot-reload on addon changes
- Volumes: `pg-data`, `odoo-filestore`

### Ports
- `8069` — Odoo HTTP web server
- `8072` — Gevent long-polling (Unix only)

### Configuration File
- `docker/odoo.conf` — Primary dev config
- `/etc/odoo/odoo.conf` — Container path
- Key params: `db_host`, `db_user`, `db_password`, `addons_path`, `data_dir`, `dev_mode`

## Component Structure

| Component | Path | Description |
|-----------|------|-------------|
| Core Framework | `odoo/` | ORM, HTTP, API, CLI, tools |
| ORM | `odoo/models.py` | BaseModel, CRUD, recordsets |
| Fields | `odoo/fields.py` | 60+ field type definitions |
| API Decorators | `odoo/api.py` | @depends, @constrains, @onchange |
| HTTP Routing | `odoo/http.py` | WSGI, routing, request/response |
| Module System | `odoo/modules/` | Loading, registry, migration |
| CLI Tools | `odoo/cli/` | server, shell, scaffold, db, deploy |
| Domain Language | `odoo/osv/expression.py` | Filter domain → SQL |
| Test Framework | `odoo/tests/` | TransactionCase, HttpCase, Form |
| Official Addons | `addons/` | 621+ installable business modules |

## Development Commands

### Docker (Recommended)

```bash
# Build and start full stack
docker-compose up --watch

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Shell into container
docker-compose exec odoo bash

# Access app at: http://localhost:8069
# Default credentials: admin / admin
```

### Direct Python

```bash
# Install dependencies
pip install -r requirements.txt

# Start server (dev mode with auto-reload)
python odoo-bin -c docker/odoo.conf

# Start with specific database
python odoo-bin -d <dbname> -c docker/odoo.conf

# Initialize database with modules
python odoo-bin -d <dbname> -i base,sale --stop-after-init

# Upgrade modules
python odoo-bin -d <dbname> -u <module_name> --stop-after-init

# Interactive Python shell with ORM access
python odoo-bin shell -d <dbname>

# Scaffold a new addon
python odoo-bin scaffold <module_name> ./addons/
```

### Testing

```bash
# Run tests for a specific module
python odoo-bin -d <dbname> --test-enable -i <module> --stop-after-init

# Run tests by tag
python odoo-bin -d <dbname> --test-tags=tag_name --stop-after-init

# Run a specific test file
python odoo-bin -d <dbname> --test-file=addons/<module>/tests/test_xxx.py --stop-after-init

# Run all tests
python odoo-bin -d <dbname> --test-enable --stop-after-init
```

### Linting

```bash
# Flake8 (primary linter, configured in setup.cfg)
flake8 addons/<module>/

# Ruff
ruff check addons/<module>/
```

## Environment Configuration

Default dev database credentials (Docker):
- Host: `db`
- Port: `5432`
- User: `odoo`
- Password: `odoo`
- Admin password: `admin`

### Dev Mode Options
- `dev_mode: reload` — Auto-reload on file changes
- `PYTHONDONTWRITEBYTECODE=1` — No .pyc files for live dev

## CI/CD

No automated CI/CD configured (`.github/` directory exists but empty). Build is manual via Docker or direct Python setup.
