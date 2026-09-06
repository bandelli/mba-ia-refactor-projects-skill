const config = require('../config');

function requireAdminAuth(req, res, next) {
  const token = req.headers['x-admin-token'];
  if (!token || token !== config.adminToken) {
    return res.status(401).json({ error: 'Não autorizado' });
  }
  next();
}

module.exports = requireAdminAuth;
