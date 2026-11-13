# Mobile apps (iOS and Android)

Load this file when the project contains a mobile app: native iOS or Android, React Native, Expo, Capacitor, Ionic, Flutter or a store-published PWA wrapper. App store rejections and mobile-only security problems are among the most common launch blockers. Check `Info.plist`, `PrivacyInfo.xcprivacy`, `AndroidManifest.xml`, `app.json`/`app.config.*`, `capacitor.config.*`, `build.gradle`, and the native project folders.

## App store requirements
- [ ] 🔴 MOB-001 **Account deletion inside the app** if the app lets people create accounts (Apple and Google both require it). The flow deletes server data too, not just the local session.
- [ ] 🔴 MOB-002 **Permission purpose strings for every permission the app can trigger:** `NSCameraUsageDescription`, `NSPhotoLibraryUsageDescription`, `NSMicrophoneUsageDescription`, `NSLocationWhenInUseUsageDescription` and so on, in clear words. A missing string makes iOS **crash** the app when that feature is used (for example "Take Photo" in a file picker on iPad).
- [ ] 🔴 MOB-003 **Privacy labels match reality:** App Store privacy "nutrition labels" and the Google Play Data safety form list every data type collected, including by SDKs (analytics, crash reporting, ads, AI, auth).
- [ ] 🔴 MOB-004 **Apple privacy manifest** (`PrivacyInfo.xcprivacy`) for the app, declaring required-reason APIs and tracking domains, and third-party SDKs that ship their own manifests are up to date.
- [ ] 🔴 MOB-005 **Digital goods use in-app purchase** where the store rules require it, and receipts or purchase tokens are **verified on the server**, never trusted from the device.
- [ ] 🔴 MOB-006 **Tracking permission:** if the app tracks users across other companies' apps or websites (ad SDKs, cross-app attribution), it asks with App Tracking Transparency on iOS before tracking.
- [ ] 🟡 MOB-007 **Sign in with Apple** is offered on iOS where Apple's rules require it (when other third-party social logins are offered).
- [ ] 🟡 MOB-008 **Target and minimum SDK versions** meet Google Play's current target API requirement and Apple's current SDK requirement.
- [ ] 🟡 MOB-009 **Store listing is honest:** screenshots, description, age rating and content questionnaire match the app (e.g. user chat or AI features change the rating). A support URL and privacy policy URL work.
- [ ] 🟡 MOB-010 **Review notes and a demo account** are prepared for app review if features need sign-in.

## Mobile security
- [ ] 🔴 MOB-011 **No secrets in the app bundle:** API secret keys, service-role keys and private tokens aren't in the JS bundle, `.env` files compiled into the app, `Info.plist`, `strings.xml` or `google-services.json` beyond the public config. Anything shipped in an app can be extracted.
- [ ] 🔴 MOB-012 **Tokens stored securely:** session and refresh tokens live in Keychain/Keystore (e.g. `expo-secure-store`, `@capacitor/preferences` with secure storage, `flutter_secure_storage`), not AsyncStorage, `localStorage` or plain files.
- [ ] 🔴 MOB-013 **HTTPS only:** no `NSAllowsArbitraryLoads` / `usesCleartextTraffic="true"` in production builds, except narrowly for documented local development.
- [ ] 🟡 MOB-014 **Deep links and universal/app links are verified** (`apple-app-site-association`, `assetlinks.json`), and parameters from links are validated before use (no account actions straight from a link).
- [ ] 🟡 MOB-015 **WebViews are locked down:** no JavaScript bridges exposed to remote content, only trusted domains loaded, and file access disabled unless needed.
- [ ] 🟡 MOB-016 **Debug features are off in release builds:** no dev menus, debug logs with personal data, test endpoints or `debuggable=true`.
- [ ] 🟢 MOB-017 **Screenshots and app switcher** hide sensitive screens (payment, health, private messages) where appropriate.

## Reliability and quality
- [ ] 🔴 MOB-018 **Crash and error reporting** (Sentry, Crashlytics or similar) in release builds, with personal data scrubbed.
- [ ] 🟡 MOB-019 **Forced update path:** the app can tell users to update when an old version is no longer supported, and the API stays backwards-compatible with versions still in use.
- [ ] 🟡 MOB-020 **Offline and poor network:** the app shows clear states, doesn't lose drafts, and retries safely (no double payments).
- [ ] 🟡 MOB-021 **Permissions are requested in context** (when the feature is first used), with a friendly explanation and a way forward if refused.
- [ ] 🟡 MOB-022 **Tested on real devices:** small and large phones, tablets (iPad split view and rotation), the oldest supported OS version, and dark mode.
- [ ] 🟢 MOB-023 **App size and startup time** are reasonable, and large assets load on demand.
- [ ] 🟢 MOB-024 **Push notifications** ask permission in context, can be turned off in settings, and don't show sensitive content on the lock screen.
