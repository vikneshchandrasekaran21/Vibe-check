const router = require('express').Router();
const db = require('../db');
const { requireUser } = require('../auth');

// Spend credits on a meal kit. Each kit costs `kit.cost` credits.
router.post('/spend', requireUser, async (req, res) => {
  const kit = await db.get('orders', `kit:${req.body.kitId}`);
  if (!kit) return res.status(404).json({ error: 'Kit not found.' });
  const user = await db.get('users', req.user.id);
  if (user.credits < kit.cost) return res.status(402).json({ error: 'Not enough credits.' });
  await db.put('users', user.id, { ...user, credits: user.credits - kit.cost });
  res.json({ ok: true, credits: user.credits - kit.cost });
});

// One free credit per day.
router.post('/daily', requireUser, async (req, res) => {
  const user = await db.get('users', req.user.id);
  const today = req.body.today || new Date().toISOString().slice(0, 10);
  if (user.lastDaily === today) return res.status(429).json({ error: 'Come back tomorrow.' });
  await db.put('users', user.id, { ...user, credits: user.credits + 1, lastDaily: today });
  res.json({ ok: true });
});

module.exports = router;
