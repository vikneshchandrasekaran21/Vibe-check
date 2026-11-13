# Policy pack: what the app must publish

Check which documents exist, whether they're linked where users need them, and whether **each one matches the data map and features from Step 2**. A generic template that doesn't match the app is a FAIL. Drafting is allowed only on request and only from the real data map; mark drafts "DRAFT – needs legal review" and add them to the "Needs a lawyer" list.

| Document | Needed when | Must include | Link it from |
|---|---|---|---|
| 🔴 **Privacy policy** | Always, if any personal data is collected | Each data type and its purpose, legal basis, processors and third parties (hosting, email, analytics, AI, fonts/CDNs), storage location and region, retention, user rights and how to use them, children's data (if any), a contact or grievance officer, an effective date | Footer, signup, every form that collects data |
| 🔴 **Terms of service** | Always | Who can use it, acceptable use, accounts, payments (if any), IP, termination, disclaimers, liability limit, governing law, contact | Footer, signup |
| 🔴 **Cookie notice and consent** | Non-essential cookies or trackers, with EU/UK users (and good practice everywhere) | Each cookie and tracker with its purpose and duration, plus a consent banner that blocks non-essential cookies until consent | Footer and the banner |
| 🔴 **Refund and cancellation policy** | The app charges money | How to cancel, refund rules, trial terms, processing times | Pricing, checkout, footer |
| 🔴 **Parental consent notice** | Minors (see `kids-education.md`) | What is collected about the child, why, retention, rights, how to withdraw consent | The consent flow |
| 🟡 **Acceptable use policy** | User-generated content, uploads or messaging | Prohibited content and behaviour, enforcement, how to report | Terms, report flow |
| 🟡 **Content and copyright takedown** | Users upload content | A contact for copyright and abuse reports, the process and timelines | Footer |
| 🟡 **AI disclosure** | AI features | What's AI-generated, its limits, which providers, whether data is used for training | Near the AI feature, privacy policy |
| 🟡 **Disclaimer** | Health, finance, legal, safety or fitness advice | "Not professional advice", plus when to see a professional | Near the advice |
| 🟡 **Accessibility statement** | Public, government or EU-market apps | Standard targeted (WCAG 2.2 AA), known gaps, contact | Footer |
| 🟡 **Data retention schedule** | Personal data is kept | How long each data type is kept and how it's deleted | Privacy policy, or internal |
| 🟡 **Subprocessor list** | B2B customers | Every vendor that processes customer data, with its location | Trust or legal page |
| 🟡 **Data processing agreement (DPA)** | B2B customers process personal data through you | Roles, security measures, subprocessors, breach notice, deletion | Available on request |
| 🟡 **`security.txt` and a vulnerability disclosure policy** | Public apps | A contact for security reports (`/.well-known/security.txt`) | Footer, or the well-known path |
| 🟡 **Incident response plan** | Personal data or paid users | Who does what, notification timelines (e.g. GDPR 72h, CERT-In 6h in India), contacts | Internal |
| 🟢 **Status page and SLA** | Paid or B2B | Uptime target, credits if any, how incidents are communicated | Footer, contracts |

## Checks
- [ ] 🔴 POL-001 **Required documents exist:** each one is reachable without logging in and linked where users need it.
- [ ] 🔴 POL-002 **Documents match the app today,** including recently added fields and features (compare against the data map).
- [ ] 🔴 POL-003 **No overstated claims:** ("cannot be reversed", "fully anonymous", "bank-grade", "100% secure", "compliant" without proof).
- [ ] 🟡 POL-004 **Dated and versioned:** each document has an effective date and a version history, and users are told about material changes.
- [ ] 🟡 POL-005 **In the users' languages,** and the translations match.
- [ ] 🟡 POL-006 **Contact details work** (the email inbox is monitored).
