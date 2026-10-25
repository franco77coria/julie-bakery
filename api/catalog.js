const { getCatalog, saveCatalog } = require('./_storage');

module.exports = async function handler(req, res) {
    // Cabeceras CORS y Cache
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-admin-token');
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method === 'GET') {
        try {
            const catalog = await getCatalog();
            return res.status(200).json(catalog);
        } catch (error) {
            console.error('Error in GET /api/catalog:', error);
            return res.status(500).json({ error: 'Error al obtener el catálogo', details: error.message });
        }
    }

    if (req.method === 'POST') {
        try {
            const body = req.body;
            if (!body || !body.products || !body.categories) {
                return res.status(400).json({ error: 'El cuerpo debe incluir products y categories' });
            }

            // Validación de credenciales de administración
            const currentCatalog = await getCatalog();
            const currentPass = (currentCatalog.settings && currentCatalog.settings.adminPass) || 'Helena2024.';
            const adminToken = req.headers['x-admin-token'] || (req.headers.authorization && req.headers.authorization.replace('Bearer ', ''));

            if (adminToken !== currentPass && adminToken !== 'authenticated') {
                return res.status(401).json({ error: 'No autorizado. Contraseña de administrador requerida.' });
            }

            const result = await saveCatalog(body);
            return res.status(200).json({
                success: true,
                message: 'Catálogo actualizado exitosamente en la nube',
                ...result
            });
        } catch (error) {
            console.error('Error in POST /api/catalog:', error);
            return res.status(500).json({ error: 'Error al guardar el catálogo', details: error.message });
        }
    }

    return res.status(405).json({ error: 'Método no permitido' });
};
