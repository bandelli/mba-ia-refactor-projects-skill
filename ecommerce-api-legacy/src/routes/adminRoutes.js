const express = require('express');
const { financialReport } = require('../controllers/financialReportController');
const requireAdminAuth = require('../middlewares/auth');

const router = express.Router();

router.get('/admin/financial-report', requireAdminAuth, financialReport);

module.exports = router;
