const express = require('express');
const app = express();
app.use(express.json({ verify: (req, _res, buf) => { req.rawBody = buf; } }));
app.use((req, _res, next) => { req.cookies = Object.fromEntries((req.get('cookie') || '').split(';').filter(Boolean).map((c) => c.trim().split('='))); next(); });
for (const r of ['credits', 'checkout', 'orders', 'notes', 'legacy', 'invites', 'billing', 'referrals', 'webhooks', 'auth-links', 'ai']) {
  app.use('/api', require(`./routes/${r}`));
}
app.listen(process.env.PORT || 3000);
