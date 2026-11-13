# Desktop apps and browser extensions

Load this file when the project is an Electron, Tauri or other desktop app, or a browser extension (Chrome, Edge, Firefox, Safari). These run with more power on the user's computer than a website does, so mistakes are more dangerous.

## Electron and Tauri
- [ ] 🔴 DSK-001 **Electron isolation on:** `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true` for every window. Renderer code can't call Node APIs directly.
- [ ] 🔴 DSK-002 **Safe preload bridge:** `contextBridge` exposes only specific, validated functions, never `ipcRenderer` itself or generic "run this command" or "read this file" functions.
- [ ] 🔴 DSK-003 **No remote content with privileges:** the app doesn't load remote websites in privileged windows. External links open in the system browser (`shell.openExternal` with an allow-list of protocols), and navigation and new windows are restricted.
- [ ] 🔴 DSK-004 **Code signing and notarization:** builds are signed (Apple Developer ID + notarization on macOS, Authenticode on Windows), so users aren't trained to bypass security warnings.
- [ ] 🔴 DSK-005 **Secure auto-update:** updates come over HTTPS from a trusted source and are signature-checked (electron-updater with signing, Tauri updater with public key).
- [ ] 🟡 DSK-006 **Tauri allow-lists:** only the APIs, file paths and shell commands the app needs are enabled in the Tauri config or capabilities.
- [ ] 🟡 DSK-007 **Content Security Policy** set for app windows, and no `eval` or remote scripts.
- [ ] 🟡 DSK-008 **Local data protection:** tokens in the OS keychain (`keytar`, `safeStorage`, Tauri stronghold or keyring), not plain files. Local databases with sensitive data are encrypted.
- [ ] 🟡 DSK-009 **Electron is kept up to date** (old Chromium versions carry known vulnerabilities).
- [ ] 🟢 DSK-010 **Crash reporting and a way to collect logs** with the user's consent.

## Browser extensions
- [ ] 🔴 DSK-011 **Minimal permissions:** only the `permissions` and `host_permissions` the extension really needs. No `<all_urls>` unless essential (prefer `activeTab` and optional permissions requested in context).
- [ ] 🔴 DSK-012 **Manifest V3** for Chrome and Edge, with no remotely hosted code (all scripts packaged), as store policies require.
- [ ] 🔴 DSK-013 **Content scripts don't trust the page:** messages from web pages (`window.postMessage`) are validated, and page data is never passed to `eval`, `innerHTML` or privileged APIs without checking the sender and content.
- [ ] 🔴 DSK-014 **Data handling matches the store disclosure:** the Chrome Web Store privacy practices form, Firefox data collection disclosure and the privacy policy describe exactly what's collected (browsing history, page content), and limited-use rules are followed.
- [ ] 🟡 DSK-015 **Secrets aren't in the extension package:** API keys used by the extension are public-safe or go through your server.
- [ ] 🟡 DSK-016 **External messaging restricted:** `externally_connectable` lists only your own domains, if used.
- [ ] 🟡 DSK-017 **Store listing is accurate:** single, clear purpose, honest screenshots and description, a support contact.
- [ ] 🟢 DSK-018 **Update and rollback plan:** store review can delay fixes, so risky features are behind server-side flags.
