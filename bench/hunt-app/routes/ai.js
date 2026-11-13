const router = require('express').Router();
const { requireUser } = require('../auth');

// Recipe ideas from the pantry list. Free for every signed-in user.
router.post('/ai/recipes', requireUser, async (req, res) => {
  const r = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: { 'content-type': 'application/json', authorization: `Bearer ${process.env.OPENAI_API_KEY}` },
    body: JSON.stringify({
      model: req.body.model || 'gpt-4o-mini',
      max_tokens: req.body.maxTokens || 800,
      messages: [{ role: 'system', content: 'Suggest recipes from this pantry list.' }, { role: 'user', content: String(req.body.pantry) }],
    }),
  });
  res.json(await r.json());
});

module.exports = router;
