require('dotenv').config();
require('dotenv').config({ path: 'C:\\AXYNTRAX\\AXYNTRAX_VAULT\\master_keys.env' });
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const routes = require('./routes');
const { auditLogger } = require('./middlewares/audit');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(morgan('dev'));
app.use(auditLogger);

app.use('/api/v1', routes);

app.get('/health', (req, res) => {
    res.status(200).json({ status: 'UP', service: 'AXYNTRAX Core API', timestamp: new Date() });
});

app.listen(PORT, () => {
    console.log(`[AXYNTRAX] Core API running on port ${PORT}`);
});
