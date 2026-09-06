const courseModel = require('../models/courseModel');
const userModel = require('../models/userModel');
const enrollmentModel = require('../models/enrollmentModel');
const paymentModel = require('../models/paymentModel');
const auditLogModel = require('../models/auditLogModel');
const { hashPassword } = require('../utils/crypto');
const { logAndCache } = require('../services/cacheService');

async function checkout(req, res, next) {
  try {
    const { usr, eml, pwd, c_id: courseId, card } = req.body;

    if (!usr || !eml || !courseId || !card) {
      return res.status(400).json({ error: 'Bad Request' });
    }

    const db = req.app.locals.db;

    const course = await courseModel.findActiveById(db, courseId);
    if (!course) {
      return res.status(404).json({ error: 'Curso não encontrado' });
    }

    let user = await userModel.findByEmail(db, eml);
    let userId;
    if (!user) {
      const passwordHash = await hashPassword(pwd || '123456');
      const created = await userModel.create(db, { name: usr, email: eml, passwordHash });
      userId = created.lastID;
    } else {
      userId = user.id;
    }

    const status = card.startsWith('4') ? 'PAID' : 'DENIED';
    if (status === 'DENIED') {
      return res.status(400).json({ error: 'Pagamento recusado' });
    }

    const enrollment = await enrollmentModel.create(db, { userId, courseId });
    await paymentModel.create(db, { enrollmentId: enrollment.lastID, amount: course.price, status });
    await auditLogModel.record(db, `Checkout curso ${courseId} por ${userId}`);

    logAndCache(`last_checkout_${userId}`, course.title);

    res.status(200).json({ msg: 'Sucesso', enrollment_id: enrollment.lastID });
  } catch (err) {
    next(err);
  }
}

module.exports = { checkout };
