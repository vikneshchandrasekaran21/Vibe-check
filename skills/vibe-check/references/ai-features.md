# AI and LLM features

Use this file only if the app calls an LLM or AI API (chatbots, generation, agents, RAG, AI image or voice). Mark each item PASS / FAIL / N/A / CAN'T TELL, with evidence.

## Keys and cost

- [ ] 🔴 **AI provider keys stay on the server.** No OpenAI, Anthropic, Gemini or Replicate key in client code or a public env var. The browser calls your backend, never the provider directly.
- [ ] 🔴 **Per-user limits:** rate limits, daily or monthly quotas, `max_tokens` on every call, and a limit on input size (characters, file size, pages).
- [ ] 🔴 **Spend cap and billing alert** set at the provider (ask the user).
- [ ] 🔴 **Anonymous users can't run up the bill.** Unauthenticated AI endpoints get strict limits or CAPTCHA.
- [ ] 🟡 **Calls are triggered deliberately:** not on every keystroke, render or retry loop. Debounce and cancel in-flight requests.
- [ ] 🟡 **Streaming and long calls** have timeouts and handle user cancellation.
- [ ] 🟢 **Cache** repeated identical prompts where that's safe.

## Prompt injection and output handling

- [ ] 🔴 **LLM output is treated as untrusted input.** It is never rendered as raw HTML (sanitize markdown output), never run as code or SQL, and never used as a URL, file path or shell argument without validation.
- [ ] 🔴 **Prompt injection is assumed.** Text from users, uploaded documents, web pages, emails or RAG sources can contain instructions. The model's permissions must be safe even if it obeys them.
- [ ] 🔴 **Tool and agent permissions are least-privilege.** Tools run with the *end user's* permissions (not admin or service-role). Destructive or costly actions (sending email, payments, deleting, posting) need explicit user confirmation.
- [ ] 🔴 **No data leaks across users.** RAG retrieval and conversation history are filtered by the current user or tenant on the server, not by asking the model.
- [ ] 🟡 **System prompts contain no secrets.** Assume users can extract the system prompt.
- [ ] 🟡 **Structured output is validated** against a schema before use.
- [ ] 🟡 **No exfiltration through rendered markdown.** Images and links in model output can't send data to attacker URLs (restrict image domains or strip external images).

## Privacy, safety and honesty

- [ ] 🔴 **The privacy policy names the AI providers** and says what data is sent to them. Check the provider's data-retention and training terms (opt out of training where possible).
- [ ] 🔴 **No sensitive data sent unnecessarily:** health records, government IDs, passwords and payment data are stripped before prompts.
- [ ] 🟡 **Content moderation** on user prompts and on outputs if the app is public or generates images, so it can't be used to produce harmful content under your brand.
- [ ] 🟡 **AI disclosure.** Users know they're talking to AI. AI-generated content is labelled where laws or platforms require it (EU AI Act transparency rules, app store policies).
- [ ] 🟡 **High-stakes outputs** (health, legal, finance, safety) carry disclaimers and a path to a human.
- [ ] 🟡 **Hallucination handling.** Citations or sources where accuracy matters, and the UI doesn't present guesses as facts.
- [ ] 🟡 **Logs of prompts and outputs** are access-controlled, have a retention limit, and are covered by deletion requests.
- [ ] 🟢 **Evals.** A small set of test prompts (including jailbreak and injection attempts) run before changing models or prompts.
- [ ] 🟢 **Fallback** when the provider is down or rate-limits you, so users see a clear message instead of a hang.
