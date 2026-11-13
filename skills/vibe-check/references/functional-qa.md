# Functional QA: does everything actually work?

AI-built apps often ship buttons that do nothing, links to pages that don't exist, and forms that look like they submit but don't. Check that every interactive element leads somewhere real.

**Method, best first:**
1. **Click-through (preferred):** run the app (`npm run dev`) or use staging, then use Playwright, a browser tool, or the vibe-check connector's `crawl_app`. Visit every route, click every button and link, and submit every form with valid and invalid data. On production, only follow links and open pages; never submit forms or create data.
2. **Static review (fallback):** trace every `onClick`, `onSubmit`, `<a href>`, `<Link to>`, `router.push` and form `action` to a handler or route that exists and does something.

Record each broken item with the page, the element (its text or selector), what happened, and what was expected. Include a screenshot if you can take one.

## Navigation and links
- [ ] 🔴 **No dead links:** every internal link and route resolves (no 404s). `href="#"` or `javascript:void(0)` appear only where a handler exists.
- [ ] 🔴 **No dead buttons:** every button has a handler that does something visible, or is clearly disabled with a reason.
- [ ] 🔴 **Main journeys work end to end:** signup → verify → onboarding → core action → result, plus login, logout and password reset.
- [ ] 🟡 **External links work** and open safely (`rel="noopener"` on `target="_blank"`).
- [ ] 🟡 **Back button and refresh** don't break state or re-submit forms.
- [ ] 🟡 **Deep links** to every page work when opened directly, logged in and logged out (with a sensible redirect to login).

## Forms
- [ ] 🔴 **Every form submits and saves**, and shows clear success feedback.
- [ ] 🔴 **Validation errors appear** next to the field, in words. The form keeps the user's input after an error.
- [ ] 🟡 **Double submit is prevented:** the button is disabled while a request is in flight.
- [ ] 🟡 **Long, empty, unicode and emoji input** doesn't break the layout or the save.
- [ ] 🟡 **File inputs** reject wrong types and sizes with a clear message.

## States
- [ ] 🔴 **Loading, empty and error states** exist for every screen that fetches data. No infinite spinners and no blank pages.
- [ ] 🟡 **Placeholder content is gone:** no lorem ipsum, "TODO", sample users, dummy prices, or `example.com` links.
- [ ] 🟡 **Permissions in the UI match the server:** users don't see buttons for actions they aren't allowed to do, and hidden buttons are still blocked on the server.
- [ ] 🟡 **Feature flags and half-built features** are hidden from users.

## Errors and assets
- [ ] 🔴 **No uncaught console errors** on the main pages.
- [ ] 🟡 **No failed network requests** (4xx/5xx) during normal use.
- [ ] 🟡 **No broken images, fonts or icons** (check for 404 assets).
- [ ] 🟡 **Emails and notifications** link to working pages (verification, reset, invites).

## Cross-device
- [ ] 🔴 **Main journeys work on a phone** (375px wide) and in Safari (iOS) and Chrome.
- [ ] 🟡 **Slow network** (throttle to "Fast 3G" or "Slow 4G"): no broken state, and timeouts show a message.
