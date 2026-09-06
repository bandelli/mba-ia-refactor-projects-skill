const db = require('../database/db');

function record(conn, action) {
  return db.run(conn, "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))", [action]);
}

module.exports = { record };
