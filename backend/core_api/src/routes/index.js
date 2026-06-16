const express = require('express');
const router = express.Router();
const { requireRole } = require('../middlewares/rbac');

// Generar un token temporal para pruebas (Solo Desarrollo)
router.get('/dev-token', (req, res) => {
    const jwt = require('jsonwebtoken');
    const token = jwt.sign({ id: 'u_123', role: 'admin' }, process.env.JWT_SECRET, { expiresIn: '1h' });
    res.json({ token });
});

router.get('/secure-data', requireRole(['admin', 'operator']), (req, res) => {
    res.json({ message: 'Secure data accessed successfully.', user: req.user });
});

router.post('/whatsapp/webhook', (req, res) => {
    res.json({ status: 'received' });
});

module.exports = router;
