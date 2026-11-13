# UX, launch basics, email, abuse and mobile apps

Mark each item PASS / FAIL / N/A / CAN'T TELL, with evidence. 🔴 blocks launch · 🟡 before scale · 🟢 recommended.

## Accessibility (WCAG 2.2 AA)

- [ ] 🔴 **Real controls:** `<button>` and `<a>` instead of clickable `<div>`s, and every input has a `<label>`.
- [ ] 🔴 **Keyboard works everywhere**, with a visible focus state and no keyboard traps in modals or menus.
- [ ] 🔴 **Alt text** on meaningful images, and empty `alt=""` on decorative ones.
- [ ] 🟡 **Colour contrast** at least 4.5:1 for text, and colour isn't the only signal (for example, red borders on errors also need text).
- [ ] 🟡 **Forms announce errors** next to the field, with text.
- [ ] 🟡 **Respects `prefers-reduced-motion`**, and nothing flashes.
- [ ] 🟢 **Run axe or Lighthouse accessibility** and fix serious issues.

## Responsive and performance

- [ ] 🔴 **Works on a phone.** Check key pages at 375px wide: no horizontal scroll, tap targets at least 44px, and modals fit on screen.
- [ ] 🟡 **Performance budget:** LCP under 2.5s, INP under 200ms, CLS under 0.1 on mobile (Lighthouse or PageSpeed Insights).
- [ ] 🟡 **JS bundle size** is reasonable. Big libraries and below-the-fold content load lazily.
- [ ] 🟡 **Images** are optimized and sized, and fonts don't block rendering.

## Launch basics

- [ ] 🔴 **Custom 404 and 500 pages** that don't leak stack traces.
- [ ] 🔴 **Empty, loading and error states** for every screen that loads data.
- [ ] 🔴 **A support contact** (email or form) is visible.
- [ ] 🟡 **Staging and preview sites aren't indexed** (`noindex` or password protection). Production isn't accidentally `noindex`.
- [ ] 🟡 **SEO basics:** a unique `<title>` and meta description per page, Open Graph and social images, `sitemap.xml`, `robots.txt`, canonical URLs, and a favicon.
- [ ] 🟡 **Analytics** for key events (signup, activation, payment), installed in a consent-respecting way.
- [ ] 🟡 **Browser support:** tested in Chrome, Safari (including iOS Safari) and Firefox.
- [ ] 🟢 **Changelog or status page** so users know what changed.

## Email

- [ ] 🔴 **Sending domain authenticated:** SPF, DKIM and DMARC set (otherwise mail lands in spam, and Gmail and Yahoo require it for bulk senders).
- [ ] 🔴 **Transactional email** (verification, reset, receipts) uses a real provider (Resend, Postmark, SES, SendGrid), not a personal Gmail account.
- [ ] 🔴 **Marketing email** has opt-in consent, a one-click unsubscribe and a physical address (CAN-SPAM and GDPR rules).
- [ ] 🟡 **Bounces and complaints** are handled. Emails that bounce stop being sent to.
- [ ] 🟡 **No user-controlled content in emails** that could make them phishing tools (for example, the name field in "X invited you").

## Abuse and fraud

- [ ] 🔴 **Signup abuse:** rate limits and bot protection. Disposable-email blocking if free tiers are valuable.
- [ ] 🔴 **SMS and OTP pumping:** rate limits per number and IP, and country restrictions if you only serve some countries.
- [ ] 🟡 **Free-tier and trial abuse:** limits per account, device or card. Watch for credit farming.
- [ ] 🟡 **User-generated content:** report, block and moderation tools. Uploaded files can't be used to host malware or phishing on your domain.
- [ ] 🟡 **Invites and sharing links** expire and can be revoked. Share links aren't guessable.

## Mobile apps (iOS / Android / Expo / React Native / Flutter)

- [ ] 🔴 **No secrets in the app bundle.** Assume anything in the app can be extracted. Keys live on your server.
- [ ] 🔴 **In-app account deletion** (required by Apple and Google).
- [ ] 🔴 **Privacy disclosures:** App Store privacy labels and the Google Play Data safety form match actual data collection, including third-party SDKs.
- [ ] 🔴 **Payments follow store rules:** digital goods use in-app purchase where required. Purchases are validated on the server.
- [ ] 🟡 **Tokens in secure storage** (Keychain, Keystore, `expo-secure-store`), not AsyncStorage.
- [ ] 🟡 **Deep links and universal links** verified so they can't be hijacked, with parameters validated.
- [ ] 🟡 **Permissions** asked only when needed, with clear purpose strings.
- [ ] 🟡 **Forced update path** for breaking API changes. The API stays backward compatible with older app versions.
- [ ] 🟡 **Crash reporting** (Sentry, Crashlytics) and offline or poor-network handling.
