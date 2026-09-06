const express = require('express');

const config = require('./config');
const { createConnection, initSchema, seedData } = require('./database/db');
const { hashPassword } = require('./utils/crypto');
const errorHandler = require('./middlewares/errorHandler');
const checkoutRoutes = require('./routes/checkoutRoutes');
const adminRoutes = require('./routes/adminRoutes');
const userRoutes = require('./routes/userRoutes');

async function start() {
  const app = express();
  app.use(express.json());

  const db = createConnection();
  await initSchema(db);
  const seedPasswordHash = await hashPassword('123');
  await seedData(db, seedPasswordHash);

  app.locals.db = db;

  app.use('/api', checkoutRoutes);
  app.use('/api', adminRoutes);
  app.use('/api', userRoutes);

  app.use(errorHandler);

  app.listen(config.port, () => {
    console.log(`API de cursos rodando na porta ${config.port}...`);
  });
}

start().catch((err) => {
  console.error('Falha ao iniciar aplicação', err);
  process.exit(1);
});
