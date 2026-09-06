const userModel = require('../models/userModel');
const enrollmentModel = require('../models/enrollmentModel');
const paymentModel = require('../models/paymentModel');

async function deleteUser(req, res, next) {
  try {
    const db = req.app.locals.db;
    const userId = req.params.id;

    const enrollmentRows = await enrollmentModel.findIdsByUserId(db, userId);
    const enrollmentIds = enrollmentRows.map((e) => e.id);

    // Cascade explícito: filhos antes do pai, para não deixar dados órfãos.
    await paymentModel.deleteByEnrollmentIds(db, enrollmentIds);
    await enrollmentModel.deleteByUserId(db, userId);
    await userModel.remove(db, userId);

    res.json({ message: 'Usuário e dados relacionados (matrículas, pagamentos) removidos com sucesso.' });
  } catch (err) {
    next(err);
  }
}

module.exports = { deleteUser };
