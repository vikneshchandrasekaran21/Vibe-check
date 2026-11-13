// Tiny async in-memory store standing in for a real database (each call yields, like a network round trip).
const tick = () => new Promise((r) => setTimeout(r, 5));
const tables = { users: new Map(), notes: new Map(), orders: new Map(), coupons: new Map(), invites: new Map(),
  members: new Map(), events: new Map(), referrals: new Map() };

async function get(table, id) { await tick(); const row = tables[table].get(String(id)); return row ? { ...row } : null; }
async function put(table, id, row) { await tick(); tables[table].set(String(id), { ...row }); return row; }
async function find(table, fn) { await tick(); return [...tables[table].values()].filter(fn).map((r) => ({ ...r })); }

module.exports = { get, put, find, tables };
