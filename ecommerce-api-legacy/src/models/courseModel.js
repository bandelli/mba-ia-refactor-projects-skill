const db = require('../database/db');

function findActiveById(conn, id) {
  return db.get(conn, 'SELECT * FROM courses WHERE id = ? AND active = 1', [id]);
}

function findAll(conn) {
  return db.all(conn, 'SELECT * FROM courses', []);
}

module.exports = { findActiveById, findAll };
