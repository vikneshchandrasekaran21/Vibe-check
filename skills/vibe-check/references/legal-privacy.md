# Legal, privacy and compliance

**Flag; don't decide.** You are not a lawyer. Check what exists in the code and site, compare it with the data map from Step 1, and send anything that depends on jurisdiction, money, health or children to the "Needs a lawyer" list. Name the likely laws (GDPR/UK GDPR, CCPA/CPRA, India DPDP Act, COPPA, PIPEDA, LGPD and so on) based on where users are. Ask the user if you don't know.

## Policies and consent

- [ ] 🔴 **Privacy policy** exists, is linked in the footer and at signup, and **matches the data map**: what is collected, why, legal basis, which third parties (hosting, analytics, payments, email, AI providers), where it is stored, how long it's kept, and how to contact you.
- [ ] 🔴 **Terms of service** cover acceptable use, account termination, payment terms, liability limits, governing law and a contact address.
- [ ] 🔴 **Cookie and tracker consent** where required (EU/UK, and increasingly elsewhere). **No non-essential analytics, ads pixels or session replay load before consent.** Verify this in code: look for GA, GTM, Meta Pixel, Hotjar, PostHog or Clarity initialized unconditionally.
- [ ] 🔴 **Consent on forms that collect personal data:** a clear notice plus a link to the privacy policy. Marketing opt-in is unticked by default and separate from the terms.
- [ ] 🟡 **Cookie policy** lists every cookie and tracker and its purpose.
- [ ] 🟡 **Do Not Sell/Share link and Global Privacy Control** support if California users are in scope and the app shares data for ads.

## User data rights

- [ ] 🔴 **Data collected is explained** in plain words: a list of fields.
- [ ] 🔴 **Purpose for each field.** If there's no purpose, recommend not collecting it (data minimization).
- [ ] 🔴 **Account and data deletion** that users can trigger themselves or request easily. It covers the DB, file storage, logs where feasible, and third parties (payments, email lists, analytics, AI provider logs). App stores require in-app account deletion.
- [ ] 🟡 **Data export** (a "download my data" option).
- [ ] 🟡 **Data correction** (users can edit their profile data).
- [ ] 🟡 **Retention rules.** Old data, logs and backups expire on a schedule.
- [ ] 🟡 **Breach plan.** Who to notify and how fast (GDPR: 72 hours to the regulator. India DPDP: notify the Board and affected users).

## Third parties and licensing

- [ ] 🔴 **Every third-party API's terms checked:** commercial use allowed, caching and storage limits, attribution, rate limits, and whether you can resell or redistribute the data. Scraping targets' terms checked.
- [ ] 🔴 **Open-source licenses scanned** (`npx license-checker --summary`, `pip-licenses`, FOSSA, Snyk). Flag GPL, AGPL, SSPL or "non-commercial" licenses in closed-source or SaaS code.
- [ ] 🔴 **No unlicensed copyrighted assets:** images, icons, illustrations, music, video, logos, and stock photos without a license.
- [ ] 🔴 **Fonts are licensed for the web.** Google Fonts and other OFL/Apache fonts are fine. A commercial font (Adobe, Monotype, foundry fonts) needs a **web/app license**: a desktop license doesn't cover `@font-face` or embedding in an app. Check every `@font-face`, `next/font` and font file in `public/`.
- [ ] 🟡 **Asset register:** a list (e.g. `CREDITS.md` or `/licenses`) of every third-party image, icon set, font, illustration and audio file, with its source and license. Images AI tools pulled from the web without a source are a FAIL.
- [ ] 🟡 **Attribution given** where licenses require it (CC-BY, MIT/BSD notices, OpenStreetMap, some icon sets).
- [ ] 🟡 **UI kits, templates, themes and fonts** are licensed for this use (many paid kits forbid SaaS or resale use).
- [ ] 🟡 **AI-generated content.** Check the AI provider's output terms. Generated images or text don't imitate real brands, trademarks, real people or copyrighted characters.
- [ ] 🟡 **Trademark check:** the app name and logo don't clash with an existing brand in the same space.

## Money

- [ ] 🔴 **Refund and cancellation policy** if you charge. Cancelling is as easy as signing up (FTC click-to-cancel style rules, app store rules).
- [ ] 🔴 **Card data never touches your servers.** Use hosted checkout or elements (Stripe, Razorpay, Paddle, Lemon Squeezy) to stay out of PCI scope.
- [ ] 🔴 **Prices shown include or clearly state taxes and recurring charges.** Trials say when billing starts.
- [ ] 🟡 **Tax.** GST/VAT/sales tax registration and invoices. Consider a merchant of record (Paddle, Lemon Squeezy) if unsure. → lawyer or accountant.
- [ ] 🟡 **Business details shown** where required: legal entity name, address and contact (EU, India e-commerce rules).

## Product-specific

- [ ] 🟡 **Age restrictions.** COPPA (US, under 13), GDPR (under 13–16 depending on country), India DPDP (under 18 needs verifiable parental consent; no tracking or targeted ads to children). Age gate if needed.
- [ ] 🟡 **Disclaimers** for health, fitness, finance, investment, legal or AI-generated advice.
- [ ] 🟡 **User-generated content:** a report and takedown process, a DMCA or copyright contact, and moderation. In India, intermediary rules can require a grievance officer. → lawyer.
- [ ] 🟡 **Regulated data or industries:** health (HIPAA), finance, education (FERPA), kids, crypto or gambling. → lawyer before launch.
- [ ] 🟡 **Accessibility law.** ADA (US), the European Accessibility Act (EU, in force from June 2025) and similar may apply. See `launch-ux.md`.

## Honesty

- [ ] 🔴 **Marketing claims are true:** no fake testimonials, logos, user counts, reviews or "as seen in". No "SOC 2 / HIPAA / GDPR compliant", "bank-grade security" or "end-to-end encrypted" unless it's actually true and can be backed up.
- [ ] 🔴 **No dark patterns:** no pre-ticked boxes, hidden fees, fake countdown timers, confirmshaming, or hard-to-find cancel buttons.

## Final legal pass

- [ ] 🔴 **List everything for a lawyer**, with the specific question to ask, the jurisdiction, and the relevant page or file.
