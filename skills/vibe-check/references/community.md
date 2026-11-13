# Community, chat and marketplaces

Load this file when users can post content others see, message each other, join groups, follow each other, review things, or buy and sell from each other. These apps carry abuse, safety and legal duties that ordinary apps don't. Flag legal judgement calls for a lawyer.

## Safety tools
- [ ] 🔴 **Report button** on every piece of user content, profile and message, with a reason and an acknowledgement to the reporter.
- [ ] 🔴 **Block and mute:** users can block others, and blocking stops messages, mentions, follows and seeing each other's content.
- [ ] 🔴 **Moderation queue:** staff can review reports, remove content, warn, suspend and ban, with an audit log of every action and the reason.
- [ ] 🔴 **Automatic filtering** of obvious abuse: slurs, spam links, scams, and sexual or violent content in text and images (e.g. a moderation API or model), with stricter defaults where minors are present.
- [ ] 🔴 **Minors and adults:** if under-18s can use the app, check who can message them, whether adults can find or contact minors, and whether there's age-appropriate default privacy (see `kids-education.md`).
- [ ] 🟡 **Appeals:** users told why content was removed or an account suspended, with a way to appeal.
- [ ] 🟡 **New-account limits:** rate limits on posts, messages, invites and links for new or unverified accounts, to slow spam and raids.
- [ ] 🟡 **Images and files:** uploads are scanned or moderated before others see them, and EXIF/GPS metadata is stripped (see `security.md`).

## Chat and real-time
- [ ] 🔴 **WebSocket and real-time channels check authorization** on connect **and** on every subscribe or message: users can only join rooms, channels and conversations they belong to (Supabase Realtime, Firebase, Pusher, Socket.IO, Ably).
- [ ] 🔴 **Message rate limits and size limits** per user and per room.
- [ ] 🟡 **Message deletion and retention:** users can delete their messages, deleted messages are really removed, and the retention period is stated in the privacy policy.
- [ ] 🟡 **Links in messages** are shown safely (no auto-loading of untrusted previews from the server without SSRF protection).

## Legal duties (flag for a lawyer)
- [ ] 🔴 **Notice and takedown:** a way for anyone (not just users) to report illegal content or copyright infringement, with a contact address and response timeline. → lawyer.
- [ ] 🔴 **Child sexual abuse material:** a process to remove and report it to the authorities as the law requires (e.g. NCMEC in the US). Never just delete silently. → lawyer.
- [ ] 🟡 **Platform rules by region:** EU Digital Services Act (notice-and-action, statements of reasons, transparency), UK Online Safety Act (risk assessments, reporting, child safety), India IT Rules (grievance officer, takedown timelines). → lawyer.
- [ ] 🟡 **Community guidelines and terms** state what's not allowed and what happens, and they're linked at sign-up and in the report flow.

## Marketplaces and paid creators
- [ ] 🔴 **Seller or creator verification** before payouts (identity and bank details), with payout holds for new accounts and manual review of unusual amounts (see `fintech.md`).
- [ ] 🔴 **Money flows checked by a lawyer:** if users pay other users, or credits can be turned into money, check whether the business needs a payments licence or a regulated partner. → lawyer.
- [ ] 🟡 **Disputes and refunds** between buyers and sellers have a clear process and timeline.
- [ ] 🟡 **Fake reviews and ratings:** only real buyers or users can review, and incentivised reviews are labelled.
- [ ] 🟡 **Prohibited items and services** are listed and enforced (weapons, drugs, counterfeit goods, adult services where not allowed).
- [ ] 🟢 **Seller information** shown to buyers where e-commerce rules require it (e.g. EU, India).
