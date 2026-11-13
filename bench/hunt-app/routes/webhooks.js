const router = require('express').Router();
const crypto = require('crypto');
const db = require('../db');

function verified(req) {
  const expected = crypto.createHmac('sha256', process.env.PAYMENTS_WEBHOOK_SECRET).update(req.rawBody).digest('hex');
  const given = Buffer.from(req.get('x-payments-signature') || '', 'hex');
  return given.length === 32 && crypto.timingSafeEqual(given, Buffer.from(expected, 'hex'));
}

router.post('/webhooks/payments', async (req, res) => {
  if (!verified(req)) return res.status(400).end();
  const event = req.body;
  if (event.type === 'credits.purchased') {
    const user = await db.get('users', event.data.userId);
    await db.put('users', user.id, { ...user, credits: user.credits + event.data.credits });
  }
  res.json({ received: true });
});

module.exports = router;
