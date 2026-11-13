const router = require('express').Router();
const db = require('../db');
const { requireUser } = require('../auth');

// Private recipe notes.
router.get('/notes/:id', requireUser, async (req, res) => {
  const note = await db.get('notes', req.params.id);
  if (!note || note.userId !== req.user.id) return res.status(404).json({ error: 'Note not found.' });
  res.json(note);
});

module.exports = router;
