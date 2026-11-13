# Payments, wallets and financial features

Load this file when the app takes payments, holds balances, pays out to users, lends, invests, or handles financial data. Also check the payments items in `legal-privacy.md` and the Stripe/Razorpay section of `platforms.md`.

## Payments
- [ ] 🔴 FIN-001 **No card numbers anywhere in your systems:** logs, DB, analytics, support tools and error tracking. (Hosted checkout is checked in `legal-privacy.md`.)
- [ ] 🔴 FIN-002 **Amounts, currency and tax** are calculated on the server.
- [ ] 🔴 FIN-003 **Webhooks are verified and idempotent.** Entitlements are granted and revoked only from verified events (paid, refunded, disputed, cancelled, failed).
- [ ] 🔴 FIN-004 **Test and live modes are separate.** Failure, refund, dispute and cancel flows were rehearsed in test mode.
- [ ] 🟡 FIN-005 **Reconciliation:** a daily check that your records match the processor's (missed webhooks happen).
- [ ] 🟡 FIN-006 **Invoices and receipts** meet local rules (e.g. GST invoices in India, VAT in the EU). → accountant.
- [ ] 🟡 FIN-007 **Recurring payments** follow local mandate rules (e.g. RBI e-mandate and pre-debit notifications in India).

## Money movement and balances
- [ ] 🔴 FIN-008 **A ledger, not a balance column:** balances come from immutable, double-entry transactions. No `UPDATE balance = …` without a transaction record.
- [ ] 🔴 FIN-009 **Atomic transfers,** with constraints that prevent negative balances and double spends (see `fixes.md`, race conditions).
- [ ] 🔴 FIN-010 **Payouts** need verified identity and bank details, with limits, delays for new accounts, and manual review for unusual amounts.
- [ ] 🟡 FIN-011 **Fraud controls:** velocity limits, device and IP signals, card-testing protection on checkout, alerts for spikes in refunds or disputes.

## Regulation (flag for a lawyer; don't decide)
- [ ] 🔴 FIN-012 **Licensing check:** holding customer funds, wallets, lending, investment advice, crypto, or cross-border transfers may need a licence or a regulated partner (RBI PA/PPI rules in India, money transmitter licences in the US, EMI in the EU). → lawyer.
- [ ] 🟡 FIN-013 **KYC/AML** obligations if you onboard payees or hold funds.
- [ ] 🟡 FIN-014 **Financial advice disclaimers,** and no guaranteed-return claims.
- [ ] 🟡 FIN-015 **Data retention** for financial records follows the legal minimums (often 5–8 years), while other personal data is still minimized.
