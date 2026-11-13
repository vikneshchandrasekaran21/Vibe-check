# Health, medical, wellness and fitness

Load this file when the app collects health, medical, mental-health, fitness, fertility or biometric data, or gives health advice. Laws to flag for a lawyer: US HIPAA (if you work with covered entities) and state health-data laws (e.g. Washington's My Health My Data Act). EU/UK GDPR, where health data is a "special category" that needs explicit consent. India DPDP Act, plus telemedicine and Digital Health (ABDM) rules where relevant.

- [ ] 🔴 HLT-001 **Explicit, separate consent** for health data, not bundled into the terms.
- [ ] 🔴 HLT-002 **No health data sent to analytics, ad pixels, session replay or marketing tools** (including URL paths and event names that reveal conditions).
- [ ] 🔴 HLT-003 **Encryption at rest and in transit.** Field-level encryption for diagnoses, notes and documents.
- [ ] 🔴 HLT-004 **Strict access control** with audit logs on every read of health records.
- [ ] 🔴 HLT-005 **Medical disclaimer** and an emergency path ("If this is an emergency, call …") wherever advice or AI answers appear.
- [ ] 🔴 HLT-006 **AI features** don't diagnose or prescribe unless the product is approved for that. Output is labelled as AI, with a route to a human professional.
- [ ] 🟡 HLT-007 **A BAA or DPA** with every vendor that touches health data (hosting, email, AI provider). Many default plans don't allow health data.
- [ ] 🟡 HLT-008 **Retention and deletion** rules for health records, including backups and AI provider logs.
- [ ] 🟡 HLT-009 **Notifications** (push, email, SMS) don't reveal health details on lock screens or in subject lines.
- [ ] 🟡 HLT-010 **Regulatory status checked:** does the feature make the app a medical device or software as a medical device (CDSCO in India, FDA in the US, MDR in the EU)? → lawyer.
