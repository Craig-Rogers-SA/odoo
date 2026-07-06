# System Patterns

## Guiding Principles

| Principle | Description |
|-----------|-------------|
| **Modular Addon Architecture** | All business functionality is organized as independent, installable addon modules. Each addon can be developed, tested, and deployed independently. |
| **ORM-First Design** | All data interactions flow through `odoo/models.py`. Direct database queries are discouraged; the ORM abstracts PostgreSQL and provides caching, validation, and access control. |
| **Multi-Tenant Enterprise Design** | Supports multiple isolated databases per deployment. Context and environment objects ensure data and permission separation across tenants. |
| **Convention-over-Configuration** | Standard addon directories (`models/`, `views/`, `controllers/`, `tests/`, `data/`, `security/`) are recognized automatically. Module manifests declare dependencies declaratively. |
| **Request-Based Environment** | All runtime access (user context, DB connection, permissions) flows through an implicit Environment object attached to the current request thread. |
| **Declarative Data Modeling** | Fields are declared with rich metadata. Computed fields use `@api.depends()`. All field changes trigger automatic validation. |
| **Access Control at Multiple Layers** | Security enforced at field level (`ir.model.access`), record level (`ir.rule`), and method level (`@api.private`). |
| **Separation of Concerns via Mixins** | Business logic organized horizontally through mixins (`mail.thread`, `utm.mixin`, `mail.activity.mixin`) composed into models. |
| **Backward Compatibility Priority** | Strict backward compatibility through versioning and deprecated API support across major releases. |
| **Imperative Inheritance Model** | Two types: Classical (`_inherit` — override/extend) and Prototype (`_inherits` — delegate/compose). |

## Architecture Overview

Odoo is a layered, modular ERP web application:

```
Browser / Client
       ↓
  HTTP Layer (Werkzeug/WSGI)
       ↓
  Controller Layer (odoo/http.py + addons/*/controllers/)
       ↓
  ORM Layer (odoo/models.py + odoo/fields.py)
       ↓
  PostgreSQL (via psycopg2)
```

## Directory Structure

```
odoo/                    # Core framework
├── api.py               # Decorator API (@depends, @constrains, etc.)
├── models.py            # ORM (BaseModel, CRUD, recordsets, caching)
├── fields.py            # Field type definitions
├── http.py              # WSGI entry point, routing, request handling
├── exceptions.py        # UserError, AccessError, ValidationError
├── sql_db.py            # DB connection pooling, cursor management
├── cli/                 # Entry point commands (server, shell, scaffold)
├── modules/             # Module loading, registry, dependency resolution
├── osv/                 # Domain language parser (filter → SQL)
├── service/             # RPC dispatch, auth, DB management
├── tools/               # Shared utilities (cache, config, translate, sql)
└── tests/               # Base test case classes
addons/                  # 621+ official business modules
├── base/                # Core system addon (ir.model, ir.rule, ir.http)
├── account/             # Accounting and invoicing
├── crm/                 # Customer relationship management
├── sale/                # Sales management
├── purchase/            # Purchase management
├── stock/               # Inventory management
├── mrp/                 # Manufacturing
├── hr/                  # Human resources
├── project/             # Project management
├── website/             # eCommerce and website builder
└── pos_*                # Point of Sale
```

## Addon (Module) Layout Convention

Every addon follows this standard structure:

```
addons/MODULE_NAME/
├── __manifest__.py      # Module metadata and declarations
├── __init__.py          # Python package entry
├── models/              # ORM model definitions (model_name.py)
├── controllers/         # HTTP route handlers (main.py)
├── views/               # XML UI definitions (list/form/tree/graph views)
├── data/                # Fixture data (XML/CSV)
├── demo/                # Demo data
├── report/              # Report definitions and templates
├── wizard/              # Transient models for multi-step dialogs
├── security/            # ir.model.access.csv + ir_rule.xml
├── tests/               # Test suite (test_*.py)
├── static/              # Frontend assets (JS, CSS, XML templates)
└── i18n/                # Translation files (.pot, .po)
```

## Key Patterns

### ORM Model Definition

```python
class CrmLead(models.Model):
    _name = 'crm.lead'
    _description = 'CRM Lead/Opportunity'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char('Lead Name', required=True)
    partner_id = fields.Many2one('res.partner', 'Customer')
    stage_id = fields.Many2one('crm.stage', tracking=True)
    probability = fields.Float(compute='_compute_probability', store=True)

    @api.depends('stage_id')
    def _compute_probability(self):
        for lead in self:
            lead.probability = lead.stage_id.probability

    @api.constrains('probability')
    def _check_probability(self):
        for lead in self:
            if not 0 <= lead.probability <= 100:
                raise ValidationError('Probability must be between 0 and 100')
```

### Controller (HTTP Route) Definition

```python
class CrmController(http.Controller):
    @http.route('/crm/leads', auth='user', type='json')
    def get_leads(self):
        leads = request.env['crm.lead'].search([('user_id', '=', request.env.uid)])
        return {'leads': leads.read(['name', 'stage_id'])}
```

### Module Manifest

```python
# __manifest__.py
{
    'name': 'CRM',
    'version': '18.0.1.0.0',
    'category': 'Sales/CRM',
    'depends': ['base', 'mail', 'utm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'data/crm_data.xml',
    ],
    'installable': True,
    'application': True,
}
```

### Domain Filter Syntax

```python
# Filter records
leads = env['crm.lead'].search([
    ('stage_id.name', '=', 'New'),
    ('user_id', '=', env.uid),
    '|',
    ('priority', '>', 1),
    ('partner_id', '!=', False),
])
```

### Mixin Composition Pattern

```python
class Account(models.Model):
    _name = 'account.move'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sequence.mixin']
    # Inherits chatter, activities, and sequential numbering
```

## Integration Patterns

| Pattern | Implementation |
|---------|---------------|
| JSON-RPC | POST `/web/dataset/call_kw` |
| REST endpoints | `@http.route('/path', type='json')` |
| Webhooks | Inbound routes in controllers |
| CSV Import | `ir.base_import` model |
| Email integration | `fetchmail` + `mail.thread` |
| EDI | `account.edi.*` models, UBL/CII formats |
| Payment | `payment.provider` base model |

## Testing Patterns

### Test Location
- Co-located within each addon: `addons/<module>/tests/test_*.py`
- Framework tests in `odoo/tests/`

### Base Test Classes

| Class | Scope | Use Case |
|-------|-------|----------|
| `TransactionCase` | Per-method (rollback) | Business logic, most tests |
| `SavepointCase` | Savepoints within transaction | Large data setup |
| `SingleTransactionCase` | Whole class | Read-only tests |
| `HttpCase` | Browser-based | Web UI tours and endpoints |

### Test Naming
- File: `test_<feature>.py` (e.g., `test_crm_lead.py`)
- Class: `Test<Feature>` or descriptive (e.g., `TestCRMLead`, `TestCRMLeadAssignment`)
- Method: `test_<scenario_description>` (e.g., `test_lead_convert_to_opportunity`)

### Framework & Assertions
- **Framework**: Python `unittest` (extended by Odoo)
- **Assertions**: Standard `assertEqual`, `assertIn`, `assertTrue` + `assertRecordValues` (Odoo-specific)

### Key Test Decorators & Helpers

```python
@tagged('post_install', '-at_install')  # Run after install, not during
@users('user_sales_leads')              # Execute as specific user
@freeze_time('2024-01-15 10:00:00')    # Control time
form = Form(self.env['crm.lead'])       # Test form interactions
new_test_user(env, login='test@...')   # Create test users
mute_logger('odoo.sql_db')             # Suppress noisy logs
```

### Test Setup Pattern

```python
class TestCrmCommon(TestSalesCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stage_new = cls.env['crm.stage'].create({'name': 'New'})
        cls.user_sales = new_test_user(cls.env, login='sales@test.com')

class TestCRMLead(TestCrmCommon):
    def test_lead_assignment(self):
        lead = self.env['crm.lead'].create({'name': 'Test Lead'})
        self.assertEqual(lead.stage_id, self.stage_new)
```

### Test Scope Emphasis
1. Business logic correctness (compute fields, constraints, state transitions)
2. Data integrity (cascade deletes, required field validation)
3. Integration flows (inter-module workflows)
4. Permission/access control verification
5. Form onchange behavior
6. API method contracts and RPC compatibility

### What Tests Deliberately Skip
- UI pixel-level styling tests
- Exhaustive browser compatibility tests (HttpCase covers core flows)
- Third-party integration tests (mocked where needed)
