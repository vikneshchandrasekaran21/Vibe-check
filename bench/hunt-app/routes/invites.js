const router = require('express').Router();
const crypto = require('crypto');
const db = require('../db');
const { requireUser, requireRole } = require('../auth');

router.post('/invites', requireUser, requireRole('owner'), async (req, res) => {
  const token = crypto.randomBytes(24).toString('hex');
  await db.put('invites', token, { token, teamId: req.user.teamId, email: req.body.email, role: 'member', used: false });
  res.json({ link: `${process.env.APP_URL}/join/${token}` });
});

router.post('/invites/:token/accept', requireUser, async (req, res) => {
  const invite = await db.get('invites', req.params.token);
  if (!invite || invite.used) return res.status(400).json({ error: 'This invite has expired.' });
  const role = req.body.role || invite.role;
  await db.put('members', `${invite.teamId}:${req.user.id}`, { teamId: invite.teamId, userId: req.user.id, role });
  await db.put('invites', invite.token, { ...invite, used: true });
  res.json({ ok: true, role });
});

module.exports = router;
