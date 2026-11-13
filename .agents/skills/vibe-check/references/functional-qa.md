# Functional QA: does everything actually work?

AI-built apps often ship buttons that do nothing, links to pages that don't exist, and forms that look like they submit but don't. Check that every interactive element leads somewhere real.

**Method, best first:**
1. **Click-through (preferred):** run the app (`npm run dev`) or use staging, then use Playwright, a browser tool, or the vibe-check connector's `crawl_app`. Visit every route, click every button and link, and submit every form with valid and invalid data. On production, only follow links and open pages; never submit forms or create data.
2. **Static review (fallback):** trace every `onClick`, `onSubmit`, `<a href>`, `<Link to>`, `router.push` and form `action` to a handler or route that exists and does something.

Record each broken item with the page, the element (its text or selector), what happened, and what was expected. Include a screenshot if you can take one.

## Navigation and links
- [ ] 🔴 QA-001 **No dead links:** every internal link and route resolves (no 404s). `href="#"` or `javascript:void(0)` appear only where a handler exists.
- [ ] 🔴 QA-002 **No dead buttons:** every button has a handler that does something visible, or is clearly disabled with a reason.
- [ ] 🔴 QA-003 **Main journeys work end to end:** signup → verify → onboarding → core action → result, plus login, logout and password reset.
- [ ] 🟡 QA-004 **External links work** and open safely (`rel="noopener"` on `target="_blank"`).
- [ ] 🟡 QA-005 **Back button and refresh** don't break state or re-submit forms.
- [ ] 🟡 QA-006 **Deep links** to every page work when opened directly, logged in and logged out (with a sensible redirect to login).

## Forms
- [ ] 🔴 QA-007 **Every form submits and saves**, and shows clear success feedback.
- [ ] 🔴 QA-008 **Validation errors appear** next to the field, in words. The form keeps the user's input after an error.
- [ ] 🟡 QA-009 **Double submit is prevented:** the button is disabled while a request is in flight.
- [ ] 🟡 QA-010 **Long, empty, unicode and emoji input** doesn't break the layout or the save.
- [ ] 🟡 QA-011 **File inputs** reject wrong types and sizes with a clear message.

## States
- [ ] 🔴 QA-012 **Loading, empty and error states** exist for every screen that fetches data. No infinite spinners and no blank pages.
- [ ] 🟡 QA-013 **Placeholder content is gone:** no lorem ipsum, "TODO", sample users, dummy prices, or `example.com` links.
- [ ] 🟡 QA-014 **Permissions in the UI match the server:** users don't see buttons for actions they aren't allowed to do, and hidden buttons are still blocked on the server.
- [ ] 🟡 QA-015 **Feature flags and half-built features** are hidden from users.

## Errors and assets
- [ ] 🔴 QA-016 **No uncaught console errors** on the main pages.
- [ ] 🟡 QA-017 **No failed network requests** (4xx/5xx) during normal use.
- [ ] 🟡 QA-018 **No broken images, fonts or icons** (check for 404 assets).
- [ ] 🟡 QA-019 **Emails and notifications** link to working pages (verification, reset, invites).

## Cross-device
- [ ] 🔴 QA-020 **Main journeys work on a phone** (375px wide) and in Safari (iOS) and Chrome.
- [ ] 🟡 QA-021 **Slow network** (throttle to "Fast 3G" or "Slow 4G"): no broken state, and timeouts show a message.

## Messages and microcopy
- [ ] 🔴 QA-022 **Error messages are clear and helpful:** they say what went wrong and what to do next, in plain words ("Your card was declined. Try another card."). No raw codes, "undefined", "null", `[object Object]`, stack traces or "Something went wrong" with no way forward.
- [ ] 🔴 QA-023 **Every important action confirms success:** saving, sending, paying, uploading, inviting and deleting all show a visible confirmation, and the result appears without a refresh.
- [ ] 🔴 QA-024 **Destructive actions ask first:** deleting, cancelling a subscription, leaving a team or removing data shows a confirmation that names what will be lost. Undo is offered where it's cheap.
- [ ] 🟡 QA-025 **Payment results are unambiguous:** success, failure, pending and cancelled each have a clear screen. Users are never left unsure whether they were charged.
- [ ] 🟡 QA-026 **Messages are consistent:** same tone, terms and capitalisation across the app (e.g. "Delete" vs "Remove"), and in the users' language(s).
- [ ] 🟡 QA-027 **No typos or grammar mistakes** in UI text, emails, error messages and legal pages. Run a spell-check over the copy.
- [ ] 🟡 QA-028 **Empty and first-use states guide the user:** a short explanation and a clear next action, not a blank screen.
- [ ] 🟢 QA-029 **Notifications and toasts** stay long enough to read, can be dismissed, and are announced to screen readers.

## Edge cases
- [ ] 🔴 QA-030 **Money and numbers are correct:** prices, taxes, discounts and totals round correctly (integers in the smallest currency unit, no floating-point errors), with the right currency symbol and format. Zero, negative and very large amounts are handled.
- [ ] 🟡 QA-031 **Unusual input works:** very long names and text, empty optional fields, emoji, non-Latin scripts (e.g. Hindi, Tamil, Arabic), apostrophes and quotes (`O'Brien`), and leading or trailing spaces.
- [ ] 🟡 QA-032 **Dates and times are right for the user:** time zones (including users in a different time zone from the server), daylight saving, midnight and month-end, and date formats for the region.
- [ ] 🟡 QA-033 **Lists behave at the edges:** zero, one and many items. The last page of pagination, sorting, filtering and search with no results all work.
- [ ] 🟡 QA-034 **Limits are explained:** hitting a plan limit, quota, file size or character limit shows a clear message and what to do, never a silent failure.
- [ ] 🟡 QA-035 **Files at the edges:** the largest allowed upload, wrong file types, an interrupted upload and duplicate file names.

## Sessions and journeys
- [ ] 🔴 QA-036 **Smoke test of every main journey, for every user role** (e.g. visitor, free user, paid user, admin, parent/child): sign up, log in, the core action, pay, cancel, log out, delete account. Each step works and shows the right screens.
- [ ] 🟡 QA-037 **Session expiry mid-task:** if the session expires while someone is filling a form or paying, they're asked to sign in again without losing their work or being charged twice.
- [ ] 🟡 QA-038 **Multiple tabs and devices:** logging out, changing plan or editing data in one tab or device is reflected in others, with no stale or conflicting saves.
- [ ] 🟡 QA-039 **Role changes take effect immediately:** downgraded, removed or banned users lose access straight away, including in open sessions.
- [ ] 🟡 QA-040 **Notifications and emails** for each journey (welcome, receipt, password reset, invite, alerts) are sent once, arrive, show the right details and link to working pages.
