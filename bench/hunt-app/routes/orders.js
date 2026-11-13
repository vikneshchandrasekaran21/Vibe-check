const router = require('express').Router();
const db = require('../db');
const { requireUser, requireRole } = require('../auth');

// Kitchen staff mark an order as shipped. Customers then get their box.
router.post('/orders/:id/ship', requireUser, requireRole('staff'), async (req, res) => {
  const order = await db.get('orders', req.params.id);
  if (!order) return res.status(404).json({ error: 'Order not found.' });
  await db.put('orders', order.id, { ...order, status: 'shipped', shippedAt: Date.now() });
  res.json({ ok: true });
});

module.exports = router;
