const sqlite3 = require('sqlite3').verbose();

function createConnection() {
  return new sqlite3.Database(':memory:');
}

function initSchema(db) {
  return new Promise((resolve, reject) => {
    db.serialize(() => {
      db.run('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, pass TEXT)');
      db.run('CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT, price REAL, active INTEGER)');
      db.run('CREATE TABLE enrollments (id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER)');
      db.run('CREATE TABLE payments (id INTEGER PRIMARY KEY, enrollment_id INTEGER, amount REAL, status TEXT)');
      db.run(
        'CREATE TABLE audit_logs (id INTEGER PRIMARY KEY, action TEXT, created_at DATETIME)',
        (err) => (err ? reject(err) : resolve())
      );
    });
  });
}

function seedData(db, seedPasswordHash) {
  return new Promise((resolve, reject) => {
    db.serialize(() => {
      db.run('INSERT INTO users (name, email, pass) VALUES (?, ?, ?)', [
        'Leonan',
        'leonan@fullcycle.com.br',
        seedPasswordHash,
      ]);
      db.run('INSERT INTO courses (title, price, active) VALUES (?, ?, 1), (?, ?, 1)', [
        'Clean Architecture',
        997.0,
        'Docker',
        497.0,
      ]);
      db.run('INSERT INTO enrollments (user_id, course_id) VALUES (1, 1)');
      db.run(
        "INSERT INTO payments (enrollment_id, amount, status) VALUES (1, 997.00, 'PAID')",
        (err) => (err ? reject(err) : resolve())
      );
    });
  });
}

// Helpers promisificados usados pelos models — nenhum acesso a dados fora deste arquivo
// deve chamar sqlite3 diretamente com callback.
function run(db, sql, params = []) {
  return new Promise((resolve, reject) => {
    db.run(sql, params, function callback(err) {
      if (err) return reject(err);
      resolve({ lastID: this.lastID, changes: this.changes });
    });
  });
}

function get(db, sql, params = []) {
  return new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => (err ? reject(err) : resolve(row)));
  });
}

function all(db, sql, params = []) {
  return new Promise((resolve, reject) => {
    db.all(sql, params, (err, rows) => (err ? reject(err) : resolve(rows)));
  });
}

module.exports = { createConnection, initSchema, seedData, run, get, all };
