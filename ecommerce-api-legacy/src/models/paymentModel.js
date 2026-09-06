const db = require('../database/db');

function create(conn, { enrollmentId, amount, status }) {
  return db.run(conn, 'INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)', [
    enrollmentId,
    amount,
    status,
  ]);
}

function findByEnrollmentIds(conn, enrollmentIds) {
  if (!enrollmentIds.length) return Promise.resolve([]);
  const placeholders = enrollmentIds.map(() => '?').join(',');
  return db.all(conn, `SELECT * FROM payments WHERE enrollment_id IN (${placeholders})`, enrollmentIds);
}

function deleteByEnrollmentIds(conn, enrollmentIds) {
  if (!enrollmentIds.length) return Promise.resolve();
  const placeholders = enrollmentIds.map(() => '?').join(',');
  return db.run(conn, `DELETE FROM payments WHERE enrollment_id IN (${placeholders})`, enrollmentIds);
}

module.exports = { create, findByEnrollmentIds, deleteByEnrollmentIds };
