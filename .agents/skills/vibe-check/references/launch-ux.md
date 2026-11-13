# UX, launch basics, email and abuse

Mark each item PASS / FAIL / N/A / CAN'T TELL, with evidence. 🔴 blocks launch · 🟡 before scale · 🟢 recommended.

## Accessibility (WCAG 2.2 AA)

- [ ] 🔴 UX-001 **Real controls:** `<button>` and `<a>` instead of clickable `<div>`s, and every input has a `<label>`.
- [ ] 🔴 UX-002 **Keyboard works everywhere**, with a visible focus state and no keyboard traps in modals or menus.
- [ ] 🔴 UX-003 **Alt text** on meaningful images, and empty `alt=""` on decorative ones.
- [ ] 🟡 UX-004 **Colour contrast** at least 4.5:1 for text, and colour isn't the only signal (for example, red borders on errors also need text).
- [ ] 🟡 UX-005 **Forms announce errors** next to the field, with text.
- [ ] 🟡 UX-006 **Respects `prefers-reduced-motion`**, and nothing flashes.
- [ ] 🟢 UX-007 **Run axe or Lighthouse accessibility** and fix serious issues.

## Responsive and performance

- [ ] 🔴 UX-008 **Works on a phone.** Check key pages at 375px wide: no horizontal scroll, tap targets at least 44px, and modals fit on screen.
- [ ] 🟡 UX-009 **Performance budget:** LCP under 2.5s, INP under 200ms, CLS under 0.1 on mobile (Lighthouse or PageSpeed Insights).
- [ ] 🟡 UX-010 **JS bundle size** is reasonable. Big libraries and below-the-fold content load lazily.
- [ ] 🟡 UX-011 **Images** are optimized and sized, and fonts don't block rendering.

## Launch basics

- [ ] 🔴 UX-012 **Custom 404 and 500 pages** that don't leak stack traces.
- [ ] 🔴 UX-013 **Empty, loading and error states** for every screen that loads data.
- [ ] 🔴 UX-014 **A support contact** (email or form) is visible.
- [ ] 🟡 UX-015 **Staging and preview sites aren't indexed** (`noindex` or password protection). Production isn't accidentally `noindex`.
- [ ] 🟡 UX-016 **SEO basics:** a unique `<title>` and meta description per page, Open Graph and social images, `sitemap.xml`, `robots.txt`, canonical URLs, and a favicon.
- [ ] 🟡 UX-017 **Analytics** for key events (signup, activation, payment), installed in a consent-respecting way.
- [ ] 🟡 UX-018 **Browser support:** tested in Chrome, Safari (including iOS Safari) and Firefox.
- [ ] 🟢 UX-019 **Changelog or status page** so users know what changed.

## Email

- [ ] 🔴 UX-020 **Sending domain authenticated:** SPF, DKIM and DMARC set (otherwise mail lands in spam, and Gmail and Yahoo require it for bulk senders).
- [ ] 🔴 UX-021 **Transactional email** (verification, reset, receipts) uses a real provider (Resend, Postmark, SES, SendGrid), not a personal Gmail account.
- [ ] 🔴 UX-022 **Marketing email** has opt-in consent, a one-click unsubscribe and a physical address (CAN-SPAM and GDPR rules).
- [ ] 🟡 UX-023 **Bounces and complaints** are handled. Emails that bounce stop being sent to.
- [ ] 🟡 UX-024 **No user-controlled content in emails** that could make them phishing tools (for example, the name field in "X invited you").

## Abuse and fraud

- [ ] 🔴 UX-025 **Signup abuse:** rate limits and bot protection. Disposable-email blocking if free tiers are valuable.
- [ ] 🔴 UX-026 **SMS and OTP pumping:** rate limits per number and IP, and country restrictions if you only serve some countries.
- [ ] 🟡 UX-027 **Free-tier and trial abuse:** limits per account, device or card. Watch for credit farming.
- [ ] 🟡 UX-028 **User-generated content:** report, block and moderation tools. Uploaded files can't be used to host malware or phishing on your domain.
- [ ] 🟡 UX-029 **Invites and sharing links** expire and can be revoked. Share links aren't guessable.

## Mobile apps

Mobile apps have their own module: see `mobile.md` (store requirements, permission strings, privacy manifests, secure token storage, deep links, crash reporting).
