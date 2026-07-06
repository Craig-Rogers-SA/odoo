# Product Brief

> This document captures the business and product context for development teams.

## Product Overview

- **Name**: Odoo 18.0
- **Value Proposition**: Integrated, modular open-source ERP covering sales, accounting, inventory, HR, manufacturing, and ecommerce — deployable with minimal setup, highly customizable, and unified across all business functions.
- **Product Type**: Open Source Enterprise Resource Planning (ERP) + CRM Platform
- **Stage**: Mature (Production/Stable — Development Status 5)

## Key Functionality

- **Invoicing & Accounting** — Financial management, bank reconciliation, EDI/UBL/CII, multi-company
- **CRM** — Lead management, sales funnel, email integration, gamification, campaigns
- **Sales** — Quotations to invoices, contracts, recurring billing, customer portal
- **eCommerce & Website** — Drag-and-drop builder, product catalog, SEO, multi-language
- **Inventory & Warehouse** — Stock tracking, multi-warehouse, barcode scanning, procurement
- **Manufacturing (MRP)** — Bill of materials, production scheduling, work orders, capacity planning
- **Human Resources** — Employee management, recruitment, payroll, leave management, appraisals
- **Project Management** — Kanban/Gantt tasks, time tracking, customer contract integration
- **Point of Sale** — Retail/restaurant, offline-capable, hardware integration
- **Messaging & Collaboration** — Chatter, email integration, live chat, document sharing
- **Marketing Automation** — Mass mailing, campaigns, UTM tracking
- **Reporting & Analytics** — Dashboards, forecasting, financial reporting

## Markets Serviced

- **Primary Markets**: Retail, Manufacturing, Professional Services, Distribution & Logistics
- **Secondary Markets**: Hospitality & Restaurants, Technology, Education, Non-profit, Financial Services
- **Geographic Focus**: Global — 228 localization modules covering Europe, Americas, Asia-Pacific, Middle East, Africa
- **Market Size**: SMB to Enterprise (scalable from single-person to global enterprise)

## Competitive Landscape

- **Direct Competitors**: SAP Business One, Microsoft Dynamics 365, NetSuite, Sage, Epicor
- **Indirect Competitors**: QuickBooks (accounting), Salesforce (CRM), HubSpot (marketing), Shopify (ecommerce)
- **Key Differentiators**: Open source (LGPL-3), modular install, low cost of entry, integrated suite vs. best-of-breed, 40+ languages out of the box
- **Competitive Advantages**: Unified data model across all modules, large addon ecosystem, 228+ localizations

## Key Personas

### Primary Users

| Persona | Role | Goals | Pain Points | Success Metrics |
|---------|------|-------|-------------|-----------------|
| Business Owner / Admin | System Administrator | Configure modules, manage users, customize workflows | Complex setup, permissions sprawl | Time-to-configure, user adoption |
| Sales Rep | Internal User (Sales) | Manage leads, create quotes, track opportunities | Slow data entry, missing context | Pipeline velocity, quota attainment |
| Accountant | Finance User | Reconcile accounts, generate reports, process invoices | Manual reconciliation, compliance | Close cycle time, error rate |
| Warehouse Manager | Inventory User | Track stock, process receipts, manage procurement | Stockouts, receiving errors | Inventory accuracy, order fill rate |
| Manufacturing Planner | MRP User | Schedule production, manage BOM, track orders | Demand variability, resource conflicts | On-time delivery, capacity utilization |
| HR Manager | HR User | Manage employees, run payroll, track attendance | Manual workflows, compliance changes | Onboarding time, payroll accuracy |

### Secondary Users

| Persona | Role | Goals |
|---------|------|-------|
| Project Manager | Project User | Track tasks, bill time, manage budgets |
| POS Cashier | POS User | Process transactions quickly, manage cash |
| Buyer / Purchaser | Purchase User | Manage suppliers, PO approvals, 3-way match |

### Administrators/Operators

| Persona | Role | Responsibilities |
|---------|------|------------------|
| IT Admin | System Administrator | Module installation, user management, security policies |
| ERP Manager | Access Rights Manager | Role configuration, permission assignment |
| Database Admin | Infrastructure | PostgreSQL management, backups, upgrades |

## User Flows

- **Primary Flow**: Lead → Quote → Sale Order → Delivery → Invoice → Payment (Sales-to-Cash)
- **Onboarding**: Admin creates user → assigns groups → user receives login → self-service portal invite for external users
- **Key Workflows**:
  - Purchase Order Cycle: Need → PO → Receipt → Supplier Invoice → Payment
  - Manufacturing Order: Sales Demand → MRP → Work Orders → Production → Inventory → Accounting
  - Employee Onboarding: Recruitment → Hire → Contract → Payroll Setup → Leave Management
  - eCommerce Journey: Browse → Cart → Checkout → Payment → Fulfillment → Portal Tracking
  - Project Billing: Contract → Tasks → Timesheets → Invoice (T&M)

## Success Metrics & KPIs

### Business Metrics
- Module adoption rate across business functions
- Time-to-value for new module deployments
- Reduction in manual data entry / process automation rate

### Technical Metrics
- HTTP response time: <200ms for list views, <500ms for form operations
- Report generation: <3s
- POS transaction: <100ms
- Uptime target: 99.9%+

## Non-Functional Requirements

### Performance

- **Response Time**: <200ms list views, <500ms form ops, <3s reports
- **Throughput**: Horizontally scalable via load balancer + worker pools
- **Concurrent Users**: Gevent-based async I/O (Unix) + worker pool configuration
- **Page Load Time**: Assets bundled/minified, lazy loading of backend assets

### Scalability

- **Users**: Single server for small teams; multi-server + PostgreSQL replication for enterprise
- **Data Volume**: PostgreSQL scales to terabytes; filesystem/cloud storage for attachments
- **Growth Rate**: Module-by-module activation as business grows
- **Peak Load**: Configurable worker count, reverse proxy mode

### Security

- **Authentication**: Username/password (PBKDF2-SHA512), LDAP, OAuth 2.0, TOTP MFA, Passkey/WebAuthn, Password Policy addon
- **Authorization**: Group-based RBAC (40+ predefined groups), record-level rules (`ir.rule`), field-level restrictions
- **Compliance**: EDI/PEPPOL electronic invoicing, 228+ tax localization modules, GDPR user data deletion workflows
- **Data Classification**: Customer PII, financial records, employee data (each with access controls)
- **Encryption**: PBKDF2-SHA512 for passwords, SSL/TLS for transport, API key management (90-day default)

### Availability & Reliability

- **Uptime Target**: 99.9%+ (via reverse proxy + multi-worker)
- **Recovery**: Auto-retry on serialization errors; graceful shutdown
- **Disaster Recovery**: External PostgreSQL HA setup; filesystem/cloud backup for filestore
- **Backup Strategy**: Standard PostgreSQL backup tools; configurable cloud storage (Azure, GCS, S3)

### Data & Privacy

- **Data Residency**: On-premise or cloud (customer-managed); Odoo Cloud for hosted
- **Data Retention**: Configurable archival, soft-delete for compliance
- **Privacy Requirements**: GDPR right-to-be-forgotten (`res_users_deletion`), data export, consent tracking
- **PII Handling**: Portal access restrictions, employee data isolation, anonymization options
- **Data Portability**: CSV/Excel export, full database export

### Accessibility

- **Target Compliance**: WCAG AA (responsive design, keyboard navigation)
- **Key Requirements**:
  - [x] Keyboard navigation
  - [x] Color contrast compliance (Bootstrap-based)
  - [ ] Screen reader compatibility (partial)
  - [x] Focus indicators
  - [x] Alt text for images

### Internationalization (i18n)

- **Supported Languages**: 40+ languages, community translations via Weblate
- **Localization Needs**:
  - [x] Currency formatting
  - [x] Date/time formatting (48+ timezone support)
  - [x] Number formatting
  - [x] RTL support (Arabic, Hebrew)
  - [x] Cultural considerations (228 L10n modules)

### Browser/Platform Support

- **Browsers**: Chrome, Firefox, Safari, Edge (modern versions; IE not supported)
- **Mobile**: Responsive design; native iOS/Android apps (web-based)
- **Desktop**: Windows, macOS, Linux

## Integration Points

### External Systems

| System | Purpose | Protocol | Direction |
|--------|---------|----------|-----------|
| Payment Gateways (17) | Stripe, PayPal, Adyen, Mollie, etc. | REST/Webhooks | Both |
| Email/SMTP | Gmail, Outlook, custom SMTP | SMTP/IMAP | Both |
| LDAP | Enterprise directory authentication | LDAP | Inbound |
| Google Calendar | Meeting synchronization | OAuth/REST | Both |
| Google Maps | Partner geolocation | REST | Outbound |
| Google Analytics | Website tracking | JavaScript | Outbound |
| Bank Feeds | OFX/SWIFT import | File/REST | Inbound |
| Shipping Carriers | Rate quotes, tracking | REST | Outbound |
| SMS Gateways | Notifications via Twilio/AWS SNS | REST | Outbound |
| IAP Services | Lead enrichment, OCR, lead mining | REST | Outbound |

### APIs Provided

| API | Purpose | Consumers |
|-----|---------|-----------|
| JSON-RPC 2.0 | Full ORM method access | External apps, integrations |
| REST controllers | Custom endpoints | Frontend, third-party |
| WebSocket | Real-time notifications | Browser clients |
| EDI/PEPPOL | Electronic invoicing | Business partners, tax authorities |

### Data Sources

| Source | Type | Frequency |
|--------|------|-----------|
| PostgreSQL | Database | Real-time |
| Filesystem / Cloud | Attachment storage | On-demand |
| Email servers | Mail gateway | Scheduled/real-time |
| Bank statements | OFX import | Scheduled |

## Constraints & Assumptions

### Technical Constraints

- PostgreSQL required (no MySQL, SQLite)
- Python 3.10+ required
- JavaScript enabled in browser (mandatory)
- 2GB RAM minimum (4GB+ recommended for production)
- Internet connection required (except POS in offline mode)
- X-Sendfile requires web server support for efficient file serving

### Business Constraints

- Open source (LGPL-3) vs. Enterprise edition distinction
- Annual major release cycle (18.0 → 19.0)
- Odoo S.A. controls upstream; customizations should stay in addons, not core patches

### Assumptions

- Custom development organized as addon modules (not core patches)
- PostgreSQL DBA manages backups, upgrades, HA
- Deployment via Docker for local development
- Integration responsibility lies with the implementing team for external systems

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Upstream merge conflicts on core patches | High | High | Keep customizations in addons, avoid patching core |
| PostgreSQL performance degradation | Medium | High | Index optimization, connection pooling, query analysis |
| Module dependency conflicts | Medium | Medium | Declare all dependencies in manifest, test isolation |
| Security vulnerabilities in dependencies | Medium | High | Regular `pip audit`, pin to tested version ranges |

## Open Questions

- [ ] What custom addons are planned for this development environment?
- [ ] Is this targeting Odoo Community or Enterprise edition features?
- [ ] What is the target deployment environment (on-premise, Odoo Cloud, self-hosted cloud)?

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-07-01 | Banyan Init Agent | Initial creation from codebase discovery |

## Last Refreshed

2026-07-01
