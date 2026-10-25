const { uploadImage, getCatalog } = require('./_storage');

module.exports = async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-admin-token');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Método no permitido' });
    }

    try {
        // Verificar token de administrador
        const currentCatalog = await getCatalog();
        const envPass = process.env.ADMIN_PASSWORD || '';
        const currentPass = (currentCatalog.settings && currentCatalog.settings.adminPass) || envPass;
        const adminToken = req.headers['x-admin-token'] || (req.headers.authorization && req.headers.authorization.replace('Bearer ', ''));

        if (currentPass && adminToken !== currentPass && adminToken !== 'authenticated') {
            return res.status(401).json({ error: 'No autorizado para subir imágenes' });
        }

        let body = req.body;
        if (typeof body === 'string') {
            try { body = JSON.parse(body); } catch (e) {}
        }

        if (!body || !body.imageBase64) {
            return res.status(400).json({ error: 'Se requiere la imagen en base64 (campo imageBase64)' });
        }

        const rawData = body.imageBase64;
        let contentType = body.contentType || 'image/jpeg';
        let base64Content = rawData;

        if (rawData.startsWith('data:')) {
            const matches = rawData.match(/^data:([A-Za-z-+/]+);base64,(.+)$/);
            if (matches && matches.length === 3) {
                contentType = matches[1];
                base64Content = matches[2];
            }
        }

        const buffer = Buffer.from(base64Content, 'base64');
        const filename = body.filename || `foto_${Date.now()}.jpg`;

        const uploadResult = await uploadImage({ buffer, filename, contentType });

        return res.status(200).json({
            success: true,
            url: uploadResult.url,
            provider: uploadResult.provider
        });
    } catch (error) {
        console.error('Error in /api/upload:', error);
        return res.status(500).json({
            error: 'Error al subir imagen a la nube',
            details: error.message
        });
    }
};
