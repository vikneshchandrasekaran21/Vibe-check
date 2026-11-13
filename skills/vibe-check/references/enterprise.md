# Enterprise and government readiness

Load this file at the Enterprise level: when selling to companies or government, or handling regulated data. This is what security reviews, procurement teams and auditors ask for. Many items are documents and processes, not code: mark them CAN'T TELL and ask the user.

## Identity and access
- [ ] 🔴 **SSO** (SAML or OIDC) for customer orgs, with **SCIM** or just-in-time provisioning and deprovisioning.
- [ ] 🔴 **Role-based access** with org-level admins. Customer admins can manage their own users.
- [ ] 🔴 **MFA required** for your own admin and production access (cloud, GitHub, DB, domain registrar, email).
- [ ] 🟡 **Access reviews** every quarter. Leavers are removed the same day. Shared accounts are avoided.
- [ ] 🟡 **Break-glass** emergency access is documented and logged.

## Audit and integrity
- [ ] 🔴 **Audit logs** for security-relevant events (logins, permission changes, exports, deletions, admin actions), exportable to the customer.
- [ ] 🟡 **Tamper evidence:** logs are append-only, or copied somewhere admins of the main system can't change them (a separate account, object lock, hash chaining). Be accurate about what "tamper-proof" means.
- [ ] 🟡 **Change management:** PR review required, protected branches, deploys traceable to commits, separation of duties for production changes.

## Data
- [ ] 🔴 **Data residency** known and matching what customers or regulations require (e.g. India-only hosting for some government work).
- [ ] 🔴 **Encryption** at rest and in transit, with key management documented.
- [ ] 🟡 **Tenant isolation** proven by tests: no cross-tenant reads in APIs, search, exports, caches or AI features.
- [ ] 🟡 **Customer data export and deletion** at contract end, with a timeline.
- [ ] 🟡 **Backups:** encrypted and off-site, with documented RPO and RTO targets (how much data you could lose, how long recovery takes), and **restore tested** with a date recorded.

## Security program
- [ ] 🟡 **Threat model** for the main flows and data.
- [ ] 🟡 **Third-party penetration test** within the last 12 months, with findings fixed. Government work may need a CERT-In-empanelled auditor or STQC.
- [ ] 🟡 **Vulnerability management:** dependency scanning in CI, an SLA for patching criticals, `security.txt`.
- [ ] 🟡 **SBOM** (software bill of materials) can be generated (e.g. `npx @cyclonedx/cyclonedx-npm`).
- [ ] 🟡 **Secrets management:** a vault or platform secrets, rotation schedule, no shared credentials.
- [ ] 🟡 **Incident response plan** with notification timelines, tested with a tabletop exercise.
- [ ] 🟢 **SOC 2 Type II / ISO 27001 readiness.** Policies exist (access, change, incident, vendor, BCP). A compliance tool (Vanta, Drata, Sprinto) helps when a certification is needed.

## Reliability and operations
- [ ] 🟡 **SLOs and an SLA**, uptime monitoring, a public status page, and incident communication.
- [ ] 🟡 **Disaster recovery and business continuity plan:** a cloud region failure, a lost account, a key person unavailable.
- [ ] 🟡 **Bus factor and ownership:** at least two people can access and operate production. The domain, cloud, code and DB are owned by the company, not a personal account. No production on a personal-name domain.
- [ ] 🟡 **Environments:** dev, staging and production are isolated, with no production data in lower environments (or it's masked).

## Procurement and compliance documents
- [ ] 🟡 **Security questionnaire answers** ready (CAIQ, SIG-lite, or the customer's own).
- [ ] 🟡 **Trust page:** security overview, subprocessors, DPA, status, contact.
- [ ] 🟡 **Accessibility conformance report** (VPAT or WCAG report). Government sites may need GIGW (India), Section 508 (US) or EN 301 549 (EU).
- [ ] 🟡 **Insurance** (cyber, professional liability) if contracts require it. → ask the user.
