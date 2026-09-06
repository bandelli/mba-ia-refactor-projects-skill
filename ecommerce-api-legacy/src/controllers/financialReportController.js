const courseModel = require('../models/courseModel');
const enrollmentModel = require('../models/enrollmentModel');
const userModel = require('../models/userModel');
const paymentModel = require('../models/paymentModel');

async function financialReport(req, res, next) {
  try {
    const db = req.app.locals.db;

    const courses = await courseModel.findAll(db);
    if (!courses.length) {
      return res.json([]);
    }

    const courseIds = courses.map((c) => c.id);
    const enrollments = await enrollmentModel.findByCourseIds(db, courseIds);

    const enrollmentIds = enrollments.map((e) => e.id);
    const userIds = enrollments.map((e) => e.user_id);

    // Uma query por coleção (courses, enrollments, payments, users), nunca uma
    // query por linha de outra coleção — é isso que elimina o N+1 original.
    const [payments, users] = await Promise.all([
      paymentModel.findByEnrollmentIds(db, enrollmentIds),
      userModel.findByIds(db, userIds),
    ]);

    const usersById = Object.fromEntries(users.map((u) => [u.id, u]));
    const paymentByEnrollmentId = Object.fromEntries(payments.map((p) => [p.enrollment_id, p]));
    const enrollmentsByCourseId = {};
    enrollments.forEach((e) => {
      (enrollmentsByCourseId[e.course_id] ||= []).push(e);
    });

    const report = courses.map((course) => {
      const courseEnrollments = enrollmentsByCourseId[course.id] || [];
      let revenue = 0;

      const students = courseEnrollments.map((enr) => {
        const payment = paymentByEnrollmentId[enr.id];
        const user = usersById[enr.user_id];
        if (payment && payment.status === 'PAID') {
          revenue += payment.amount;
        }
        return {
          student: user ? user.name : 'Unknown',
          paid: payment ? payment.amount : 0,
        };
      });

      return { course: course.title, revenue, students };
    });

    res.json(report);
  } catch (err) {
    next(err);
  }
}

module.exports = { financialReport };
