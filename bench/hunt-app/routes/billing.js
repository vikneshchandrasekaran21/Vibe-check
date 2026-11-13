const router = require('express').Router();
const db = require('../db');
const { requireUser } = require('../auth');

const PLANS = { free: { scans: 5 }, plus: { scans: 50 }, pro: { scans: 500 } };

router.post('/scan', requireUser, async (req, res) => {
  const user = await db.get('users', req.user.id);
  if (user.scansUsed >= PLANS[user.plan].scans) return res.status(402).json({ error: 'Monthly limit reached.' });
  await db.put('users', user.id, { ...user, scansUsed: user.scansUsed + 1 });
  res.json({ ok: true });
});

// Switching plans takes effect immediately (upgrades are prorated by the payment provider).
router.post('/plan', requireUser, async (req, res) => {
  if (!PLANS[req.body.plan]) return res.status(400).json({ error: 'Unknown plan.' });
  const user = await db.get('users', req.user.id);
  await db.put('users', user.id, { ...user, plan: req.body.plan, scansUsed: 0 });
  res.json({ ok: true });
});

module.exports = router;
