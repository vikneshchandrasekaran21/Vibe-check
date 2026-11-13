# AI agents, tools and MCP servers

Load this file when the app **lets an AI take actions**: an agent that calls tools or APIs, browses, writes to a database, sends messages or spends money, or when the project **is or includes an MCP server, plugin or tool provider** for AI assistants. This is on top of `ai-features.md`, which covers basic LLM use (keys, cost, prompt injection, output handling).

## Tools and permissions
- [ ] 🔴 AGT-001 **Least-privilege tools:** each tool does one specific thing with tightly scoped inputs. No generic "run SQL", "run shell command", "fetch any URL" or "call any API" tools exposed to the model unless sandboxed.
- [ ] 🔴 AGT-002 **Tools act as the end user, not as admin:** every tool call is authorized with the current user's permissions and tenant. The service key or admin token is never what the model uses.
- [ ] 🔴 AGT-003 **Human confirmation for risky actions:** sending email or messages, payments or refunds, deleting data, changing permissions, publishing content and anything irreversible needs explicit user approval in the UI, showing exactly what will happen.
- [ ] 🔴 AGT-004 **Indirect prompt injection is assumed:** content the agent reads (web pages, emails, documents, tickets, database rows, tool results) can contain instructions. The agent's permissions must be safe even if it follows them. Untrusted content is never allowed to choose recipients, URLs or amounts for risky actions without confirmation.
- [ ] 🔴 AGT-005 **No data exfiltration paths:** the agent can't send private data to arbitrary URLs (through fetch tools, rendered images or links, webhooks or email). Outbound destinations are allow-listed.
- [ ] 🟡 AGT-006 **Tool inputs are validated with a schema** on the server, and tool outputs are size-limited and treated as untrusted.
- [ ] 🟡 AGT-007 **Sandboxing for code execution or browsing:** isolated containers or VMs with no access to production secrets or internal networks, plus time, memory and network limits.

## Limits and cost
- [ ] 🔴 AGT-008 **Loop and cost limits:** maximum steps, tool calls, tokens, time and spend per task and per user, with the agent stopping cleanly when a limit is hit.
- [ ] 🟡 AGT-009 **Rate limits per user** on agent runs and expensive tools.
- [ ] 🟡 AGT-010 **Idempotent actions:** retries or repeated agent steps can't double-send, double-charge or create duplicates (idempotency keys on actions).

## Visibility and control
- [ ] 🔴 AGT-011 **Audit log of agent actions:** which user, which tool, inputs (secrets masked), result and time, viewable by the user and admins.
- [ ] 🟡 AGT-012 **Kill switch:** agents or specific tools can be disabled instantly without a deploy.
- [ ] 🟡 AGT-013 **Users can see and undo** what the agent did where possible (drafts before sending, version history).
- [ ] 🟡 AGT-014 **Evaluation set** of normal tasks plus injection and jailbreak attempts, run before changing models, prompts or tools.

## MCP servers, plugins and tool providers
- [ ] 🔴 AGT-015 **Authentication on remote MCP endpoints:** OAuth (with PKCE) or scoped API keys. No unauthenticated remote MCP servers that touch user data. Tokens are scoped per user and revocable.
- [ ] 🔴 AGT-016 **Local MCP servers run with minimal access:** only the folders, commands and network access they need. No shell or filesystem access beyond the stated purpose.
- [ ] 🔴 AGT-017 **Tool descriptions are honest and minimal:** descriptions don't contain instructions aimed at the AI ("always call this tool first", "ignore other tools"), and don't change unexpectedly after users approve them.
- [ ] 🟡 AGT-018 **Destructive tools are clearly marked** (read-only vs write) so clients can ask for confirmation, and they support a dry-run where possible.
- [ ] 🟡 AGT-019 **Data returned to the AI is minimal:** no secrets, internal IDs or other users' data in tool results. Large results are paginated.
- [ ] 🟡 AGT-020 **Published packages are signed and pinned:** users install a known version, and updates are reviewed (a malicious update to a tool server reaches every user).
