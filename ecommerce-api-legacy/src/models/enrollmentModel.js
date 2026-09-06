const db = require('../database/db');

function create(conn, { userId, courseId }) {
  return db.run(conn, 'INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [userId, courseId]);
}

function findByCourseIds(conn, courseIds) {
  if (!courseIds.length) return Promise.resolve([]);
  const placeholders = courseIds.map(() => '?').join(',');
  return db.all(conn, `SELECT * FROM enrollments WHERE course_id IN (${placeholders})`, courseIds);
}

function findIdsByUserId(conn, userId) {
  return db.all(conn, 'SELECT id FROM enrollments WHERE user_id = ?', [userId]);
}

function deleteByUserId(conn, userId) {
  return db.run(conn, 'DELETE FROM enrollments WHERE user_id = ?', [userId]);
}

module.exports = { create, findByCourseIds, findIdsByUserId, deleteByUserId };
