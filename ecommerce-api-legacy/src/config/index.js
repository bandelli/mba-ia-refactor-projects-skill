require('dotenv').config();

module.exports = {
  dbUser: process.env.DB_USER || 'dev-db-user',
  dbPass: process.env.DB_PASS || 'dev-db-pass-change-me',
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || 'dev-payment-key-change-me',
  smtpUser: process.env.SMTP_USER || 'no-reply@example.com',
  adminToken: process.env.ADMIN_TOKEN || 'dev-admin-token-change-me',
  port: parseInt(process.env.PORT, 10) || 3000,
};
