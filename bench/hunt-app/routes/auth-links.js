const router = require('express').Router();
const db = require('../db');

// Magic-link sign-in: the emailed link lands here, then we send the user back where they started.
router.get('/auth/callback', async (req, res) => {
  const link = await db.get('users', `magic:${req.query.token}`);
  if (!link || link.expiresAt < Date.now() || link.used) return res.redirect('/login?error=expired');
  await db.put('users', `magic:${req.query.token}`, { ...link, used: true });
  const session = require('crypto').randomBytes(32).toString('hex');
  await db.put('users', `session:${session}`, { userId: link.userId });
  const next = req.query.next || '/app';
  res.redirect(`${next}${next.includes('?') ? '&' : '?'}session=${session}`);
});

module.exports = router;
