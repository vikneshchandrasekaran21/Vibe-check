const router = require('express').Router();
const db = require('../db');

// New sign-ups with a referral code give the referrer 10 credits.
router.post('/signup', async (req, res) => {
  const email = String(req.body.email).trim().toLowerCase();
  if ((await db.find('users', (u) => u.email === email)).length) return res.status(409).json({ error: 'Email already registered.' });
  const id = `u_${Date.now()}`;
  await db.put('users', id, { id, email, credits: 0, plan: 'free', scansUsed: 0, role: 'customer' });
  if (req.body.ref) {
    const referrer = (await db.find('users', (u) => u.referralCode === req.body.ref))[0];
    if (referrer) await db.put('users', referrer.id, { ...referrer, credits: referrer.credits + 10 });
  }
  res.json({ ok: true, id });
});

module.exports = router;
