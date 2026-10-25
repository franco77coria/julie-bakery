const fs = require('fs');
const path = require('path');

const LOCAL_DATA_FILE = path.join(process.cwd(), 'data', 'catalog.json');
const DEFAULT_DATA_FILE = path.join(process.cwd(), 'data', 'default_catalog.json');

// Memoria caché para serverless warm invocations
let memoryCache = null;
let lastCacheTime = 0;

function readLocalDefault() {
    try {
        if (fs.existsSync(LOCAL_DATA_FILE)) {
            const raw = fs.readFileSync(LOCAL_DATA_FILE, 'utf-8');
            return JSON.parse(raw);
        }
        if (fs.existsSync(DEFAULT_DATA_FILE)) {
            const raw = fs.readFileSync(DEFAULT_DATA_FILE, 'utf-8');
            return JSON.parse(raw);
        }
    } catch (e) {
        console.error('Error reading local file:', e);
    }
    return {
        updatedAt: new Date().toISOString(),
        settings: { whatsapp: '5491138951241', adminUser: '', adminPass: '' },
        categories: [],
        products: []
    };
}

async function getCatalog() {
    const hasBlob = Boolean(process.env.BLOB_READ_WRITE_TOKEN);
    const hasKV = Boolean(process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN);

    // 1. Vercel KV / Upstash Redis
    if (hasKV) {
        try {
            const res = await fetch(`${process.env.KV_REST_API_URL}/get/julie_catalog`, {
                headers: { Authorization: `Bearer ${process.env.KV_REST_API_TOKEN}` },
                cache: 'no-store'
            });
            if (res.ok) {
                const data = await res.json();
                if (data && data.result) {
                    const parsed = typeof data.result === 'string' ? JSON.parse(data.result) : data.result;
                    return parsed;
                }
            }
        } catch (e) {
            console.error('KV get error:', e);
        }
    }

    // 2. Vercel Blob
    if (hasBlob) {
        try {
            const { list } = require('@vercel/blob');
            const blobs = await list({ prefix: 'data/catalog' });
            if (blobs && blobs.blobs && blobs.blobs.length > 0) {
                // Ordenar por fecha de subida descendente para garantizar la versión más reciente
                blobs.blobs.sort((a, b) => new Date(b.uploadedAt) - new Date(a.uploadedAt));
                const targetBlob = blobs.blobs[0];
                const res = await fetch(targetBlob.url, { cache: 'no-store' });
                if (res.ok) {
                    const catalog = await res.json();
                    return catalog;
                }
            }
        } catch (e) {
            console.error('Blob get error:', e);
        }
    }

    // 3. Fallback a archivo local o memoria
    return readLocalDefault();
}

async function saveCatalog(catalogData) {
    catalogData.updatedAt = new Date().toISOString();

    const hasBlob = Boolean(process.env.BLOB_READ_WRITE_TOKEN);
    const hasKV = Boolean(process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN);
    let savedInCloud = false;

    // 1. Guardar en Vercel KV si está disponible
    if (hasKV) {
        try {
            const res = await fetch(`${process.env.KV_REST_API_URL}/set/julie_catalog`, {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${process.env.KV_REST_API_TOKEN}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(JSON.stringify(catalogData))
            });
            if (res.ok) {
                savedInCloud = true;
            }
        } catch (e) {
            console.error('KV save error:', e);
        }
    }

    // 2. Guardar en Vercel Blob si está disponible
    if (hasBlob) {
        try {
            const { put } = require('@vercel/blob');
            const jsonString = JSON.stringify(catalogData, null, 2);
            await put('data/catalog.json', jsonString, {
                access: 'public',
                addRandomSuffix: false,
                allowOverwrite: true,
                contentType: 'application/json'
            });
            savedInCloud = true;
        } catch (e) {
            console.error('Blob save error:', e);
        }
    }

    // 3. Guardar en archivo local (persistente en desarrollo)
    try {
        const dir = path.dirname(LOCAL_DATA_FILE);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(LOCAL_DATA_FILE, JSON.stringify(catalogData, null, 2), 'utf-8');
    } catch (e) {
        // En Vercel serverless el filesystem puede ser de solo lectura fuera de /tmp
    }

    return {
        success: true,
        savedInCloud,
        updatedAt: catalogData.updatedAt
    };
}

async function uploadImage({ buffer, filename, contentType }) {
    const hasBlob = Boolean(process.env.BLOB_READ_WRITE_TOKEN);
    const hasCloudinary = Boolean(process.env.CLOUDINARY_CLOUD_NAME && (process.env.CLOUDINARY_UPLOAD_PRESET || process.env.CLOUDINARY_API_KEY));

    const ext = (filename && filename.split('.').pop()) || 'jpg';
    const cleanExt = ext.replace(/[^a-zA-Z0-9]/g, '').toLowerCase() || 'jpg';
    const uniqueName = `julie_${Date.now()}_${Math.random().toString(36).substring(2, 8)}.${cleanExt}`;

    // 1. Vercel Blob (Nativo en Vercel)
    if (hasBlob) {
        try {
            const { put } = require('@vercel/blob');
            const blob = await put(`products/${uniqueName}`, buffer, {
                access: 'public',
                contentType: contentType || 'image/jpeg'
            });
            return {
                url: blob.url,
                provider: 'Vercel Blob',
                success: true
            };
        } catch (e) {
            console.error('Error subiendo a Vercel Blob:', e);
            throw new Error(`Error en Vercel Blob: ${e.message}`);
        }
    }

    // 2. Cloudinary (si está configurado)
    if (hasCloudinary) {
        try {
            const cloudName = process.env.CLOUDINARY_CLOUD_NAME;
            const preset = process.env.CLOUDINARY_UPLOAD_PRESET;
            const formData = new FormData();
            const blob = new Blob([buffer], { type: contentType || 'image/jpeg' });
            formData.append('file', blob);
            if (preset) formData.append('upload_preset', preset);
            formData.append('folder', 'julie_bakery');

            const res = await fetch(`https://api.cloudinary.com/v1_1/${cloudName}/image/upload`, {
                method: 'POST',
                body: formData
            });

            if (res.ok) {
                const data = await res.json();
                return {
                    url: data.secure_url || data.url,
                    provider: 'Cloudinary',
                    success: true
                };
            }
        } catch (e) {
            console.error('Error Cloudinary:', e);
        }
    }

    // 3. Fallback Local / Data URL
    try {
        const uploadDir = path.join(process.cwd(), 'public', 'images', 'uploads');
        if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });
        const filePath = path.join(uploadDir, uniqueName);
        fs.writeFileSync(filePath, buffer);
        return {
            url: `/images/uploads/${uniqueName}`,
            provider: 'Local Storage (En Vercel conectá Vercel Blob para la nube permanente)',
            success: true
        };
    } catch (e) {
        // En serverless si no hay filesystem ni Blob, devolvemos data URL optimizada
        const b64 = buffer.toString('base64');
        const mime = contentType || 'image/jpeg';
        return {
            url: `data:${mime};base64,${b64}`,
            provider: 'Inline Data Fallback',
            success: true
        };
    }
}

function getStorageStatus() {
    const hasBlob = Boolean(process.env.BLOB_READ_WRITE_TOKEN);
    const hasKV = Boolean(process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN);
    const hasCloudinary = Boolean(process.env.CLOUDINARY_CLOUD_NAME);

    let activeProvider = 'Local (Sin nube configurada aún)';
    if (hasBlob && hasKV) activeProvider = 'Vercel Blob + Vercel KV';
    else if (hasBlob) activeProvider = 'Vercel Blob (Nativo)';
    else if (hasKV) activeProvider = 'Vercel KV / Upstash';
    else if (hasCloudinary) activeProvider = 'Cloudinary';

    return {
        cloudActive: hasBlob || hasKV || hasCloudinary,
        hasBlob,
        hasKV,
        hasCloudinary,
        activeProvider,
        message: hasBlob 
            ? '¡Nube Vercel Blob conectada! Todo cambio y foto se guarda en la nube para todos los clientes.'
            : 'En Vercel agregá Vercel Blob en 1 clic desde la pestaña Storage para tener almacenamiento ilimitado.'
    };
}

module.exports = {
    getCatalog,
    saveCatalog,
    uploadImage,
    getStorageStatus
};
