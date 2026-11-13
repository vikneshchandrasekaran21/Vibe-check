# Children, students and education

Load this file when anyone under 18 can use the app, or when it serves schools, colleges or students. Children's data carries the strictest obligations, and the biggest consequences if it leaks. Flag every legal item for a lawyer, and for the institution if a school, college or government body runs the program.

**Laws to name, depending on where users are:** India DPDP Act (under 18 = child: verifiable parental consent, no tracking, no behavioural monitoring, no targeted ads). US COPPA (under 13), FERPA (school records), and state student-privacy laws. EU/UK GDPR (age of consent 13–16 by country) and the UK Age-Appropriate Design Code.

## Age and consent
- [ ] 🔴 **The age or school level is known.** The app can tell whether a user is a minor (date of birth, class or grade, or the institution says so).
- [ ] 🔴 **Verifiable parental or guardian consent** before collecting a minor's personal data, where the law requires it. **A checkbox the child ticks is not verifiable consent.** The decision on the method belongs to the institution and its lawyer; flag it rather than inventing one.
- [ ] 🔴 **Consent is recorded:** who consented, for which child, when, how, and which version of the notice.
- [ ] 🟡 **Consent can be withdrawn**, and withdrawing it triggers deletion.
- [ ] 🟡 **The notice for children and parents** uses plain language, in the users' languages.

## Data minimization and retention
- [ ] 🔴 **Only necessary data is collected.** No extra fields "for later". Every field in the data map has a purpose.
- [ ] 🔴 **Retention limits exist and are enforced:** photos, documents and records of minors are deleted or anonymized on a schedule (e.g. X days after the event or term). **Keeping minors' data forever is a 🔴.**
- [ ] 🔴 **Photos and media:** EXIF and GPS metadata is stripped unless needed and disclosed. Faces of minors aren't public. Access to media is logged.
- [ ] 🟡 **Pseudonymization is described accurately:** hashed or coded IDs and phone numbers are described honestly (hashes of phone numbers can often be reversed by brute force; don't claim "cannot be reversed").

## Tracking, ads and profiling
- [ ] 🔴 **No third-party trackers, ad pixels or session replay** on pages minors use.
- [ ] 🔴 **No targeted advertising or behavioural profiling** of minors.
- [ ] 🟡 **Third-party embeds and fonts** (YouTube, Google Fonts, chat widgets) are disclosed. Self-host where possible.

## Access and safety
- [ ] 🔴 **Least-privilege staff access.** Teachers and staff see only their own students. Admin access is limited, logged and reviewed.
- [ ] 🔴 **Students' personal details are never returned** by any public page, API, export or search.
- [ ] 🟡 **No public profiles or open messaging** between adults and minors unless that's the product's purpose, and then with moderation and reporting.
- [ ] 🟡 **Exports** (CSV, PDF) containing student data are restricted, logged and watermarked where possible.

## Institutions and government programs
- [ ] 🟡 **Roles are clear:** who is the data fiduciary or controller (school, district, department), and who is the processor (you). A written agreement exists or is planned.
- [ ] 🟡 **Hosting and certification requirements asked about** (e.g. Indian government programs may need MeitY-empanelled hosting, a CERT-In-empanelled or STQC security audit, and GIGW website compliance). → ask the user.
- [ ] 🟡 **A named grievance officer or contact** is in the privacy policy, with a response timeline.
- [ ] 🟡 **Breach plan for student data:** who notifies the institution, parents and regulator, and how fast.
