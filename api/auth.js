const { getCatalog } = require('./_storage');

module.exports = async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Método no permitido' });
    }

    try {
        let body = req.body;
        if (typeof body === 'string') {
            try { body = JSON.parse(body); } catch (e) {}
        }

        const { username, password } = body || {};
        const catalog = await getCatalog();
        const validUser = (catalog.settings && catalog.settings.adminUser) || 'julie.bakery';
        const validPass = (catalog.settings && catalog.settings.adminPass) || 'Helena2024.';

        if (username === validUser && password === validPass) {
            return res.status(200).json({
                success: true,
                token: validPass,
                user: validUser
            });
        }

        return res.status(401).json({
            success: false,
            error: 'Credenciales inválidas. Verificá tu usuario y contraseña.'
        });
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};
