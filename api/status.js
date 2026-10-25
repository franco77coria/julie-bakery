const { getStorageStatus, getCatalog } = require('./_storage');

module.exports = async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    try {
        const status = getStorageStatus();
        const catalog = await getCatalog();

        return res.status(200).json({
            ...status,
            totalProducts: (catalog.products && catalog.products.length) || 0,
            totalCategories: (catalog.categories && catalog.categories.length) || 0,
            updatedAt: catalog.updatedAt || null,
            whatsapp: (catalog.settings && catalog.settings.whatsapp) || '5491138951241'
        });
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};
