const jwt = require('jsonwebtoken');

const requireRole = (allowedRoles) => {
    return (req, res, next) => {
        try {
            const authHeader = req.headers.authorization;
            if (!authHeader) {
                return res.status(401).json({ error: 'No authorization header provided' });
            }
            
            const token = authHeader.split(' ')[1];
            const decoded = jwt.verify(token, process.env.JWT_SECRET || 'axyntrax_super_secret_jwt_key');
            
            req.user = decoded; 

            if (!allowedRoles.includes(decoded.role)) {
                return res.status(403).json({ error: 'Access denied. Insufficient role permissions.' });
            }

            next();
        } catch (error) {
            return res.status(401).json({ error: 'Invalid or expired token.' });
        }
    };
};

module.exports = { requireRole };
