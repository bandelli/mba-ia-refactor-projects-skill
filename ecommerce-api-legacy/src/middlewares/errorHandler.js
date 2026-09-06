// Middleware de erro central do Express — precisa ficar por último em app.js
// e ter exatamente 4 argumentos para o Express reconhecê-lo como error handler.
function errorHandler(err, req, res, next) { // eslint-disable-line no-unused-vars
  console.error(err);
  res.status(500).json({ error: 'Erro interno do servidor' });
}

module.exports = errorHandler;
