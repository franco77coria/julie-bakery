# 🍰 JULIÉ BAKERY — Catálogo & Pedidos Online (Vercel Edition)

Catálogo interactivo con estética artesanal y experiencia nativa de iPhone (iOS), adaptado para despliegue en **Vercel** con **almacenamiento en la nube** y **sincronización automática en tiempo real para todos los clientes**.

---

## ✨ Características Principales

1. **Sincronización en la Nube en Tiempo Real**:
   - Cuando Julie sube un nuevo producto, cambia precios o activa "Entrega Inmediata", los cambios se guardan en la nube (`/api/catalog`) y **se actualizan al instante en los celulares de todos los clientes**.
   - No requiere descargar ningún archivo ni re-desplegar la web.

2. **Almacenamiento Permanente de Fotos en la Nube**:
   - Soporte nativo para **Vercel Blob** (`@vercel/blob`).
   - Las fotos que Julie saca con su celular o sube desde la galería se optimizan y guardan directamente en el CDN global de Vercel.
   - También compatible con Cloudinary si se prefiere.

3. **Panel Privado `/admin` Responsive**:
   - Acceso con usuario y contraseña privado (diseñado para usar cómodo desde el teléfono móvil).
   - Pestaña de **Entrega Inmediata & Ofertas del Día** con interruptores de 1 toque.
   - Gestor de medidas (por unidad, docena, gramos, 1/4 kg, 1/2 kg, 1 kg) y combinaciones de gustos.
   - Indicador de estado de la nube en vivo (🟢 Nube Conectada).

4. **Pedidos en 1 Toque a WhatsApp**:
   - Integración directa con el número oficial `11 3895-1241`.
   - Bandeja de pedido detallada con combinaciones de gustos, medidas, nombre del cliente y notas.

5. **Diseño Oficial de Marca**:
   - Paleta oficial: Crema `#F9F4EC`, Rosa `#D9B3A7`, Bordó `#8B3F46`, Chocolate `#5B3A29` y Verde Oliva `#7D8A6A`.
   - Tipografías: *Cormorant Garamond*, *Great Vibes* y *Plus Jakarta Sans*.
   - 100% Íconos SVG vectoriales (cero emojis).
   - Sin zoom accidental en móviles (Safari iOS).

---

## 🚀 Despliegue en Vercel (Paso a Paso)

### Opción 1: Conectar con GitHub / GitLab (Recomendado)
1. Subí esta carpeta a tu repositorio en GitHub.
2. Ingresá a [vercel.com](https://vercel.com) y tocá **"Add New Project"**.
3. Seleccioná tu repositorio y dale a **Deploy**.
4. **Activar la Nube (1 Clic)**:
   - Una vez creado el proyecto en Vercel, andá a la pestaña **Storage**.
   - Tocá **"Create Database"** o **"Connect Store"** y elegí **Blob**.
   - ¡Listo! Vercel conectará automáticamente el token `BLOB_READ_WRITE_TOKEN`. A partir de ese momento, todas las fotos y cambios de productos se guardarán en la nube permanente de Vercel.

### Opción 2: Desde la terminal con Vercel CLI
```bash
# Iniciar sesión si no lo hiciste
vercel login

# Desplegar a producción
vercel --prod
```

---

## 🔐 Credenciales del Panel `/admin`

- **Enlace de acceso**: Entrar a `#/admin` en el navegador (o tocar *"Panel /admin"* en el pie de página).
- **Usuario**: `julie.bakery`
- **Contraseña**: `Helena2024.`
- *(Podés cambiar el usuario y contraseña cuando quieras desde la pestaña "Nube & Config" en el panel /admin)*.

---

## 📁 Estructura del Proyecto

```
julie-bakery/
├── api/
│   ├── _storage.js        # Motor de almacenamiento en la nube (Vercel Blob / KV / Local)
│   ├── catalog.js         # GET y POST /api/catalog (Lectura y guardado en tiempo real)
│   ├── upload.js          # POST /api/upload (Subida de fotos al CDN)
│   ├── auth.js            # POST /api/auth (Autenticación del panel /admin)
│   └── status.js          # GET /api/status (Estado de conexión a la nube)
├── data/
│   ├── catalog.json       # Base de datos local persistente
│   └── default_catalog.json # Respaldo inicial con productos de Julié
├── public/
│   ├── index.html         # Frontend responsive con diseño de marca y sync en vivo
│   └── images/            # Fotografías de packaging y productos de Julié Bakery
├── vercel.json            # Configuración de rutas y headers para Vercel
├── package.json           # Dependencias (@vercel/blob)
└── README.md
```

---

## 💻 Desarrollo Local

Para probarlo localmente en tu computadora:

```bash
# Instalar dependencias
npm install

# Iniciar servidor local
npm run dev
```

Abrí [http://localhost:3000](http://localhost:3000) en tu navegador.
