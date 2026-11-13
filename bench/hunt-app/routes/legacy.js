const router = require('express').Router();
const db = require('../db');
const { requireUser } = require('../auth');

// v1 API kept for the old mobile app (1.x). Same data as /api/notes.
router.get('/v1/notes/:id/export', requireUser, async (req, res) => {
  const note = await db.get('notes', req.params.id);
  if (!note) return res.status(404).json({ error: 'Note not found.' });
  res.type('text/plain').send(`${note.title}\n\n${note.body}`);
});

module.exports = router;
