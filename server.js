const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 3000;
const PUBLIC_DIR = path.join(__dirname, 'public');

const catalogHandler = require('./api/catalog');
const uploadHandler = require('./api/upload');
const authHandler = require('./api/auth');
const statusHandler = require('./api/status');

const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.webp': 'image/webp'
};

function parseBody(req) {
    return new Promise((resolve) => {
        let chunks = [];
        req.on('data', chunk => chunks.push(chunk));
        req.on('end', () => {
            const raw = Buffer.concat(chunks).toString('utf-8');
            try {
                resolve(JSON.parse(raw));
            } catch (e) {
                resolve(raw);
            }
        });
    });
}

function mockRes(res) {
    const customRes = {
        _headers: {},
        statusCode: 200,
        setHeader(name, value) {
            this._headers[name.toLowerCase()] = value;
            res.setHeader(name, value);
        },
        status(code) {
            this.statusCode = code;
            res.statusCode = code;
            return this;
        },
        json(data) {
            this.setHeader('Content-Type', 'application/json; charset=utf-8');
            res.statusCode = this.statusCode;
            res.end(JSON.stringify(data));
        },
        end(data) {
            res.statusCode = this.statusCode;
            res.end(data);
        }
    };
    return customRes;
}

const server = http.createServer(async (req, res) => {
    const parsedUrl = url.parse(req.url, true);
    let pathname = parsedUrl.pathname;

    // API Routes
    if (pathname.startsWith('/api/')) {
        req.body = await parseBody(req);
        req.query = parsedUrl.query;
        const resWrapper = mockRes(res);

        if (pathname === '/api/catalog') {
            return catalogHandler(req, resWrapper);
        } else if (pathname === '/api/upload') {
            return uploadHandler(req, resWrapper);
        } else if (pathname === '/api/auth') {
            return authHandler(req, resWrapper);
        } else if (pathname === '/api/status') {
            return statusHandler(req, resWrapper);
        } else {
            return resWrapper.status(404).json({ error: 'Ruta API no encontrada' });
        }
    }

    // Static Files in public/
    if (pathname === '/' || pathname === '') {
        pathname = '/index.html';
    }

    const filePath = path.join(PUBLIC_DIR, decodeURIComponent(pathname));

    if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
        const ext = path.extname(filePath).toLowerCase();
        const contentType = MIME_TYPES[ext] || 'application/octet-stream';
        res.writeHead(200, { 'Content-Type': contentType });
        fs.createReadStream(filePath).pipe(res);
    } else {
        // Fallback a index.html para SPA routing si no es archivo estático
        const indexPath = path.join(PUBLIC_DIR, 'index.html');
        if (fs.existsSync(indexPath)) {
            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
            fs.createReadStream(indexPath).pipe(res);
        } else {
            res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
            res.end('404 No Encontrado');
        }
    }
});

server.listen(PORT, () => {
    console.log(`🍰 Julié Bakery Dev Server corriendo en http://localhost:${PORT}`);
});
