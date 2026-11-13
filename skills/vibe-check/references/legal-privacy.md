# Legal, privacy and compliance

**Flag; don't decide.** You are not a lawyer. Check what exists in the code and site, compare it with the data map from Step 1, and send anything that depends on jurisdiction, money, health or children to the "Needs a lawyer" list. Name the likely laws (GDPR/UK GDPR, CCPA/CPRA, India DPDP Act, COPPA, PIPEDA, LGPD and so on) based on where users are. Ask the user if you don't know.

## Policies and consent

- [ ] 🔴 LEG-001 **Privacy policy** exists, is linked in the footer and at signup, and **matches the data map**: what is collected, why, legal basis, which third parties (hosting, analytics, payments, email, AI providers), where it is stored, how long it's kept, and how to contact you.
- [ ] 🔴 LEG-002 **Terms of service** cover acceptable use, account termination, payment terms, liability limits, governing law and a contact address.
- [ ] 🔴 LEG-003 **Cookie and tracker consent** where required (EU/UK, and increasingly elsewhere). **No non-essential analytics, ads pixels or session replay load before consent.** Verify this in code: look for GA, GTM, Meta Pixel, Hotjar, PostHog or Clarity initialized unconditionally.
- [ ] 🔴 LEG-004 **Consent on forms that collect personal data:** a clear notice plus a link to the privacy policy. Marketing opt-in is unticked by default and separate from the terms.
- [ ] 🟡 LEG-005 **Cookie policy** lists every cookie and tracker and its purpose.
- [ ] 🟡 LEG-006 **Do Not Sell/Share link and Global Privacy Control** support if California users are in scope and the app shares data for ads.

## User data rights

- [ ] 🔴 LEG-007 **Data collected is explained** in plain words: a list of fields.
- [ ] 🔴 LEG-008 **Purpose for each field.** If there's no purpose, recommend not collecting it (data minimization).
- [ ] 🔴 LEG-009 **Account and data deletion** that users can trigger themselves or request easily. It covers the DB, file storage, logs where feasible, and third parties (payments, email lists, analytics, AI provider logs). App stores require in-app account deletion.
- [ ] 🟡 LEG-010 **Data export** (a "download my data" option).
- [ ] 🟡 LEG-011 **Data correction** (users can edit their profile data).
- [ ] 🟡 LEG-012 **Retention rules.** Old data, logs and backups expire on a schedule.
- [ ] 🟡 LEG-013 **Breach plan.** Who to notify and how fast (GDPR: 72 hours to the regulator. India DPDP: notify the Board and affected users).

## Third parties and licensing

- [ ] 🔴 LEG-014 **Every third-party API's terms checked:** commercial use allowed, caching and storage limits, attribution, rate limits, and whether you can resell or redistribute the data. Scraping targets' terms checked.
- [ ] 🔴 LEG-015 **Open-source licenses scanned** (`npx license-checker --summary`, `pip-licenses`, FOSSA, Snyk). Flag GPL, AGPL, SSPL or "non-commercial" licenses in closed-source or SaaS code.
- [ ] 🔴 LEG-016 **No unlicensed copyrighted assets:** images, icons, illustrations, music, video, logos, and stock photos without a license.
- [ ] 🔴 LEG-017 **Fonts are licensed for the web.** Google Fonts and other OFL/Apache fonts are fine. A commercial font (Adobe, Monotype, foundry fonts) needs a **web/app license**: a desktop license doesn't cover `@font-face` or embedding in an app. Check every `@font-face`, `next/font` and font file in `public/`.
- [ ] 🟡 LEG-018 **Asset register:** a list (e.g. `CREDITS.md` or `/licenses`) of every third-party image, icon set, font, illustration and audio file, with its source and license. Images AI tools pulled from the web without a source are a FAIL.
- [ ] 🟡 LEG-019 **Attribution given** where licenses require it (CC-BY, MIT/BSD notices, OpenStreetMap, some icon sets).
- [ ] 🟡 LEG-020 **UI kits, templates, themes and fonts** are licensed for this use (many paid kits forbid SaaS or resale use).
- [ ] 🟡 LEG-021 **AI-generated content.** Check the AI provider's output terms. Generated images or text don't imitate real brands, trademarks, real people or copyrighted characters.
- [ ] 🟡 LEG-022 **Trademark check:** the app name and logo don't clash with an existing brand in the same space.

## Money

- [ ] 🔴 LEG-023 **Refund and cancellation policy** if you charge. Cancelling is as easy as signing up (FTC click-to-cancel style rules, app store rules).
- [ ] 🔴 LEG-024 **Card data never touches your servers.** Use hosted checkout or elements (Stripe, Razorpay, Paddle, Lemon Squeezy) to stay out of PCI scope.
- [ ] 🔴 LEG-025 **Prices shown include or clearly state taxes and recurring charges.** Trials say when billing starts.
- [ ] 🟡 LEG-026 **Tax.** GST/VAT/sales tax registration and invoices. Consider a merchant of record (Paddle, Lemon Squeezy) if unsure. → lawyer or accountant.
- [ ] 🟡 LEG-027 **Business details shown** where required: legal entity name, address and contact (EU, India e-commerce rules).

## Product-specific

- [ ] 🟡 LEG-028 **Age restrictions.** COPPA (US, under 13), GDPR (under 13–16 depending on country), India DPDP (under 18 needs verifiable parental consent; no tracking or targeted ads to children). Age gate if needed.
- [ ] 🟡 LEG-029 **Disclaimers** for health, fitness, finance, investment, legal or AI-generated advice.
- [ ] 🟡 LEG-030 **Takedown process for user content:** a report and takedown process, a DMCA or copyright contact, and moderation. In India, intermediary rules can require a grievance officer. → lawyer.
- [ ] 🟡 LEG-031 **Regulated data or industries:** health (HIPAA), finance, education (FERPA), kids, crypto or gambling. → lawyer before launch.
- [ ] 🟡 LEG-032 **Accessibility law.** ADA (US), the European Accessibility Act (EU, in force from June 2025) and similar may apply. See `launch-ux.md`.

## Honesty

- [ ] 🔴 LEG-033 **Marketing claims are true:** no fake testimonials, logos, user counts, reviews or "as seen in". No "SOC 2 / HIPAA / GDPR compliant", "bank-grade security" or "end-to-end encrypted" unless it's actually true and can be backed up.
- [ ] 🔴 LEG-034 **No dark patterns:** no pre-ticked boxes, hidden fees, fake countdown timers, confirmshaming, or hard-to-find cancel buttons.

## Final legal pass

- [ ] 🔴 LEG-035 **List everything for a lawyer**, with the specific question to ask, the jurisdiction, and the relevant page or file.

## Who really uses the app
- [ ] 🔴 LEG-036 **The real audience is assessed from evidence, not assumed:** the answer to "can children use it?" is checked against `.vibe-check/profile.md` (date-of-birth or age fields, school, student, teacher or parent data, kid-oriented wording or design), the app-store age rating and category, the marketing site, and public reviews that mention children. Not asking for a date of birth, or banning minors in the terms, doesn't settle it: some laws apply when children are **likely** to use a service or when it's **directed** to them by its content, whether or not it asks for age. If the evidence points to minors, run `references/kids-education.md`, record the evidence, and put the legal question under *Needs a lawyer*.
