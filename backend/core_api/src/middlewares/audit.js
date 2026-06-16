const supabase = require('../services/supabase');

const auditLogger = async (req, res, next) => {
    const logEntry = {
        timestamp: new Date().toISOString(),
        method: req.method,
        path: req.originalUrl,
        ip: req.ip,
        user_agent: req.headers['user-agent'],
        user_id: req.user ? req.user.id : 'anonymous'
    };

    console.log(`[AUDIT] ${logEntry.timestamp} | ${logEntry.method} ${logEntry.path} | User: ${logEntry.user_id} | IP: ${logEntry.ip}`);
    
    // Insert into Supabase
    try {
        await supabase.from('audit_logs').insert([logEntry]);
    } catch (err) {
        console.error('[AUDIT ERROR] No se pudo guardar el log en Supabase', err.message);
    }

    next();
};

module.exports = { auditLogger };
