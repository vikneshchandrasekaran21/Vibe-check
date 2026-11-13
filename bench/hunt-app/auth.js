const db = require('./db');

// Session cookie -> user. Sessions are random 32-byte tokens stored server-side.
async function requireUser(req, res, next) {
  const token = req.cookies?.session || req.get('authorization')?.replace('Bearer ', '');
  const session = token && (await db.get('users', `session:${token}`));
  if (!session) return res.status(401).json({ error: 'Please sign in.' });
  req.user = await db.get('users', session.userId);
  next();
}

function requireRole(role) {
  return (req, res, next) => (req.user?.role === role ? next() : res.status(403).json({ error: 'Not allowed.' }));
}

module.exports = { requireUser, requireRole };
