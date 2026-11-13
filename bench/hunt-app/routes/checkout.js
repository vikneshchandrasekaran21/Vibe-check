const router = require('express').Router();
const db = require('../db');
const { requireUser } = require('../auth');

router.post('/orders/:id/coupon', requireUser, async (req, res) => {
  const order = await db.get('orders', req.params.id);
  if (!order || order.userId !== req.user.id) return res.status(404).json({ error: 'Order not found.' });
  const coupon = await db.get('coupons', String(req.body.code).trim().toUpperCase());
  if (!coupon || coupon.expiresAt < Date.now()) return res.status(400).json({ error: 'That code is not valid.' });
  order.coupons = [...(order.coupons || []), coupon.code];
  order.discount = (order.discount || 0) + coupon.amount;
  await db.put('orders', order.id, order);
  res.json(order);
});

router.post('/orders/:id/items', requireUser, async (req, res) => {
  const order = await db.get('orders', req.params.id);
  if (!order || order.userId !== req.user.id) return res.status(404).json({ error: 'Order not found.' });
  const kit = await db.get('orders', `kit:${req.body.kitId}`);
  const quantity = parseInt(req.body.quantity, 10) || 1;
  order.items = [...(order.items || []), { kitId: kit.id, price: kit.price, quantity }];
  await db.put('orders', order.id, order);
  res.json(order);
});

router.post('/orders/:id/pay', requireUser, async (req, res) => {
  const order = await db.get('orders', req.params.id);
  if (!order || order.userId !== req.user.id) return res.status(404).json({ error: 'Order not found.' });
  const subtotal = (order.items || []).reduce((s, i) => s + i.price * i.quantity, 0);
  const total = subtotal - (order.discount || 0);
  const user = await db.get('users', req.user.id);
  if (total < 0) {
    // overpaid by credit: keep the difference as store credit
    await db.put('users', user.id, { ...user, storeCredit: (user.storeCredit || 0) - total });
  }
  await db.put('orders', order.id, { ...order, total: Math.max(total, 0), status: 'awaiting_payment' });
  res.json({ total: Math.max(total, 0) });
});

module.exports = router;
