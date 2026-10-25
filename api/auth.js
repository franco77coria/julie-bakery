const { getCatalog, saveCatalog } = require('./_storage');

module.exports = async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-admin-token');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    const catalog = await getCatalog();
    const envUser = process.env.ADMIN_USER || '';
    const envPass = process.env.ADMIN_PASSWORD || '';
    const savedUser = envUser || (catalog.settings && catalog.settings.adminUser);
    const savedPass = envPass || (catalog.settings && catalog.settings.adminPass);
    const isConfigured = Boolean(savedUser && savedPass);

    if (req.method === 'GET') {
        return res.status(200).json({
            isConfigured,
            userHint: isConfigured ? savedUser : null
        });
    }

    if (req.method === 'POST') {
        try {
            let body = req.body;
            if (typeof body === 'string') {
                try { body = JSON.parse(body); } catch (e) {}
            }

            const { action, username, password, whatsapp } = body || {};

            // Configuración inicial si no existe contraseña configurada todavía
            if (action === 'setup' || !isConfigured) {
                if (!username || !password) {
                    return res.status(400).json({ error: 'Debes definir un usuario y una contraseña' });
                }

                catalog.settings = catalog.settings || {};
                catalog.settings.adminUser = username.trim();
                catalog.settings.adminPass = password.trim();
                if (whatsapp) {
                    catalog.settings.whatsapp = whatsapp.trim().replace(/\D/g, '');
                }

                await saveCatalog(catalog);

                return res.status(200).json({
                    success: true,
                    isSetup: true,
                    message: '¡Credenciales de administradora creadas exitosamente!',
                    token: catalog.settings.adminPass,
                    user: catalog.settings.adminUser
                });
            }

            // Inicio de sesión normal
            if (username && password) {
                const userMatch = (username.trim().toLowerCase() === savedUser.toLowerCase());
                const passMatch = (password === savedPass);

                if (userMatch && passMatch) {
                    return res.status(200).json({
                        success: true,
                        token: savedPass,
                        user: savedUser
                    });
                }
            }

            return res.status(401).json({
                success: false,
                error: 'Usuario o contraseña incorrectos. Por favor verificá los datos.'
            });
        } catch (error) {
            console.error('Error in /api/auth:', error);
            return res.status(500).json({ error: error.message });
        }
    }

    return res.status(405).json({ error: 'Método no permitido' });
};
