const db = require('../database/db');

function findByEmail(conn, email) {
  return db.get(conn, 'SELECT * FROM users WHERE email = ?', [email]);
}

function findById(conn, id) {
  return db.get(conn, 'SELECT * FROM users WHERE id = ?', [id]);
}

function findByIds(conn, ids) {
  if (!ids.length) return Promise.resolve([]);
  const placeholders = ids.map(() => '?').join(',');
  return db.all(conn, `SELECT id, name, email FROM users WHERE id IN (${placeholders})`, ids);
}

function create(conn, { name, email, passwordHash }) {
  return db.run(conn, 'INSERT INTO users (name, email, pass) VALUES (?, ?, ?)', [name, email, passwordHash]);
}

function remove(conn, id) {
  return db.run(conn, 'DELETE FROM users WHERE id = ?', [id]);
}

module.exports = { findByEmail, findById, findByIds, create, remove };
