# Enterprise and government readiness

Load this file at the Enterprise level: when selling to companies or government, or handling regulated data. This is what security reviews, procurement teams and auditors ask for. Many items are documents and processes, not code: mark them CAN'T TELL and ask the user.

## Identity and access
- [ ] 🔴 ENT-001 **SSO** (SAML or OIDC) for customer orgs, with **SCIM** or just-in-time provisioning and deprovisioning.
- [ ] 🔴 ENT-002 **Role-based access** with org-level admins. Customer admins can manage their own users.
- [ ] 🔴 ENT-003 **MFA required** for your own admin and production access (cloud, GitHub, DB, domain registrar, email).
- [ ] 🟡 ENT-004 **Access reviews** every quarter. Leavers are removed the same day. Shared accounts are avoided.
- [ ] 🟡 ENT-005 **Break-glass** emergency access is documented and logged.

## Audit and integrity
- [ ] 🔴 ENT-006 **Audit logs** for security-relevant events (logins, permission changes, exports, deletions, admin actions), exportable to the customer.
- [ ] 🟡 ENT-007 **Tamper evidence:** logs are append-only, or copied somewhere admins of the main system can't change them (a separate account, object lock, hash chaining). Be accurate about what "tamper-proof" means.
- [ ] 🟡 ENT-008 **Change management:** PR review required, protected branches, deploys traceable to commits, separation of duties for production changes.

## Data
- [ ] 🔴 ENT-009 **Data residency** known and matching what customers or regulations require (e.g. India-only hosting for some government work).
- [ ] 🔴 ENT-010 **Encryption** at rest and in transit, with key management documented.
- [ ] 🟡 ENT-011 **Tenant isolation** proven by tests: no cross-tenant reads in APIs, search, exports, caches or AI features.
- [ ] 🟡 ENT-012 **Customer data export and deletion** at contract end, with a timeline.
- [ ] 🟡 ENT-013 **Backups:** encrypted and off-site, with documented RPO and RTO targets (how much data you could lose, how long recovery takes), and **restore tested** with a date recorded.

## Security program
- [ ] 🟡 ENT-014 **Threat model** for the main flows and data.
- [ ] 🟡 ENT-015 **Third-party penetration test** within the last 12 months, with findings fixed. Government work may need a CERT-In-empanelled auditor or STQC.
- [ ] 🟡 ENT-016 **Vulnerability management:** dependency scanning in CI, an SLA for patching criticals, `security.txt`.
- [ ] 🟡 ENT-017 **SBOM** (software bill of materials) can be generated (e.g. `npx @cyclonedx/cyclonedx-npm`).
- [ ] 🟡 ENT-018 **Secrets management:** a vault or platform secrets, rotation schedule, no shared credentials.
- [ ] 🟡 ENT-019 **Incident response plan** with notification timelines, tested with a tabletop exercise.
- [ ] 🟢 ENT-020 **SOC 2 Type II / ISO 27001 readiness.** Policies exist (access, change, incident, vendor, BCP). A compliance tool (Vanta, Drata, Sprinto) helps when a certification is needed.

## Reliability and operations
- [ ] 🟡 ENT-021 **SLOs and an SLA**, uptime monitoring, a public status page, and incident communication.
- [ ] 🟡 ENT-022 **Disaster recovery and business continuity plan:** a cloud region failure, a lost account, a key person unavailable.
- [ ] 🟡 ENT-023 **Bus factor and ownership:** at least two people can access and operate production. The domain, cloud, code and DB are owned by the company, not a personal account. No production on a personal-name domain.
- [ ] 🟡 ENT-024 **Environments:** dev, staging and production are isolated, with no production data in lower environments (or it's masked).

## Procurement and compliance documents
- [ ] 🟡 ENT-025 **Security questionnaire answers** ready (CAIQ, SIG-lite, or the customer's own).
- [ ] 🟡 ENT-026 **Trust page:** security overview, subprocessors, DPA, status, contact.
- [ ] 🟡 ENT-027 **Accessibility conformance report** (VPAT or WCAG report). Government sites may need GIGW (India), Section 508 (US) or EN 301 549 (EU).
- [ ] 🟡 ENT-028 **Insurance** (cyber, professional liability) if contracts require it. → ask the user.
