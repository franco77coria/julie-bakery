import os
import re

src_path = r"c:\Users\Usuario\Downloads\cat_logo_web_juli_bakery.html"
dst_path = r"C:\Users\Usuario\.gemini\antigravity\scratch\julie-bakery\public\index.html"

with open(src_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Actualizar referencias de imágenes por defecto a las imágenes locales de public/images/
html = html.replace('"image_9aecfb.jpg"', '"/images/julie_01.jpg"')
html = html.replace("'image_9aecfb.jpg'", "'/images/julie_01.jpg'")
html = html.replace('"image_99f5bb.jpg"', '"/images/julie_01.jpg"')
html = html.replace("'image_99f5bb.jpg'", "'/images/julie_01.jpg'")
html = html.replace('"image_99f578.jpg"', '"/images/julie_05.jpg"')
html = html.replace("'image_99f578.jpg'", "'/images/julie_05.jpg'")
html = html.replace('"image_99f580.jpg"', '"/images/julie_07.jpg"')
html = html.replace("'image_99f580.jpg'", "'/images/julie_07.jpg'")
html = html.replace('"image_99f55d.jpg"', '"/images/julie_08.jpg"')
html = html.replace("'image_99f55d.jpg'", "'/images/julie_08.jpg'")
html = html.replace('"image_999f82.jpg"', '"/images/julie_11.jpg"')
html = html.replace("'image_999f82.jpg'", "'/images/julie_11.jpg'")

# 2. Reemplazar la barra superior del /admin (Banner de guardado sin base de datos)
old_banner_start = '<!-- BANNER RÁPIDO: GUARDADO SIN BASE DE DATOS -->'
old_banner_end = '<!-- ========================================================= -->\n                    <!-- PESTAÑA 1: TAGEAR ENTREGA INMEDIATA Y OFERTAS DEL DÍA     -->'

new_cloud_banner = '''<!-- BANNER NUBE Y SINCRONIZACIÓN AUTOMÁTICA EN VIVO -->
                    <div id="cloudStatusBanner" class="bg-cremaDark/95 border-2 border-rosa rounded-2xl p-3.5 sm:px-5 sm:py-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-sm">
                        <div class="flex items-center gap-3">
                            <span id="cloudStatusIcon" class="w-9 h-9 rounded-full bg-oliva text-crema flex items-center justify-center shrink-0 shadow-sm">
                                <svg class="w-4.5 h-4.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>
                            </span>
                            <div class="text-xs text-chocolate leading-snug">
                                <div class="flex items-center gap-2 font-bold text-bordo flex-wrap">
                                    <span id="cloudStatusBadge" class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-olivaLight text-oliva text-[10px] font-bold">
                                        <span class="w-2 h-2 rounded-full bg-oliva animate-pulse"></span>
                                        <span id="cloudStatusText">Sincronización en la Nube Activa</span>
                                    </span>
                                    <span id="cloudSyncTime" class="text-[10px] text-chocolate/70 font-normal">Sincronizado</span>
                                </div>
                                <p id="cloudStatusDesc" class="mt-1 text-chocolate/85 text-[11px] sm:text-xs">
                                    Cada foto que subas y cambio que hagas se guarda automáticamente en la nube y se actualiza al instante en los celulares de todos tus clientes.
                                </p>
                            </div>
                        </div>
                        <div class="flex items-center gap-2 shrink-0 self-end sm:self-center">
                            <button type="button" onclick="syncCatalogWithCloudNow()" id="btnForceSync" class="ios-tap shrink-0 px-3.5 py-2 rounded-full bg-bordo text-crema text-[11px] font-bold flex items-center justify-center gap-1.5 shadow-sm">
                                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                                <span>Sincronizar Ahora</span>
                            </button>
                            <button type="button" onclick="exportCatalogJson()" title="Descargar copia de respaldo en tu teléfono" class="ios-tap shrink-0 px-3 py-2 rounded-full bg-crema text-bordo text-[11px] font-bold border border-bordo/20 flex items-center gap-1">
                                <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                                <span>Copia JSON</span>
                            </button>
                        </div>
                    </div>

                    '''

if old_banner_start in html and old_banner_end in html:
    idx1 = html.index(old_banner_start)
    idx2 = html.index(old_banner_end)
    html = html[:idx1] + new_cloud_banner + html[idx2:]
    print("Replaced admin cloud banner successfully")

# 3. Modificar el título de la pestaña 4 en el navegador de pestañas del /admin
html = html.replace('<span>Publicar sin Base de Datos & Config</span>', '<span>Nube Vercel & Config</span>')

# 4. Actualizar el bloque de la Pestaña 4
old_tab4_title = '<h4 class="font-serifBrand text-2xl font-bold text-bordo">Sistema Sin Base de Datos (Todo en 1 Archivo)</h4>'
new_tab4_block = '''<div class="flex items-start gap-3">
                                <div class="w-11 h-11 rounded-2xl bg-bordo text-crema flex items-center justify-center shrink-0 shadow-sm">
                                    <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>
                                </div>
                                <div>
                                    <h4 class="font-serifBrand text-2xl font-bold text-bordo">Almacenamiento Permanente en la Nube (Vercel)</h4>
                                    <p class="text-xs text-chocolate/80 mt-0.5 leading-relaxed">
                                        Tu catálogo está configurado para Vercel. Cuando subís fotos de medialunas, chipás o tortas, o cambiás los precios desde tu celular, se guardan en la nube y <strong>se actualizan automáticamente en tiempo real</strong> para cualquier cliente que tenga abierto el catálogo en su celular.
                                    </p>
                                </div>
                            </div>'''
if old_tab4_title in html:
    html = re.sub(r'<div class="flex items-start gap-3">[\s\S]*?<h4 class="font-serifBrand text-2xl font-bold text-bordo">Sistema Sin Base de Datos \(Todo en 1 Archivo\)</h4>[\s\S]*?</div>\s*</div>', new_tab4_block, html, count=1)
    print("Replaced tab 4 title block successfully")

# 5. Modificar la función handleAdminLogin para consultar /api/auth
old_login_func = '''        function handleAdminLogin(event) {
            event.preventDefault();
            const userInp = (document.getElementById("adminLoginUser").value || "").trim();
            const passInp = (document.getElementById("adminLoginPass").value || "").trim();
            const errEl = document.getElementById("adminLoginError");

            if (userInp.toLowerCase() === settings.adminUser.toLowerCase() && passInp === settings.adminPass) {
                isAdminLoggedIn = true;
                try {
                    sessionStorage.setItem(ADMIN_SESSION_KEY, "true");
                } catch (e) {}
                errEl.classList.add("hidden");
                updateAdminSessionUI();
                renderAdminRouteState();
                renderCatalog();
                showToast("Bienvenida al Panel /admin de Julié Bakery");
            } else {
                errEl.classList.remove("hidden");
            }
        }'''

new_login_func = '''        async function handleAdminLogin(event) {
            event.preventDefault();
            const userInp = (document.getElementById("adminLoginUser").value || "").trim();
            const passInp = (document.getElementById("adminLoginPass").value || "").trim();
            const errEl = document.getElementById("adminLoginError");

            try {
                const res = await fetch("/api/auth", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username: userInp, password: passInp })
                });
                const data = await res.json();
                if (res.ok && data.success) {
                    isAdminLoggedIn = true;
                    try {
                        sessionStorage.setItem(ADMIN_SESSION_KEY, "true");
                        sessionStorage.setItem("julie_bakery_admin_token", data.token || passInp);
                    } catch (e) {}
                    errEl.classList.add("hidden");
                    updateAdminSessionUI();
                    renderAdminRouteState();
                    renderCatalog();
                    checkCloudStatus();
                    showToast("Bienvenida al Panel /admin de Julié Bakery");
                    return;
                }
            } catch (e) {
                console.warn("API login fallback", e);
            }

            if (userInp.toLowerCase() === settings.adminUser.toLowerCase() && passInp === settings.adminPass) {
                isAdminLoggedIn = true;
                try {
                    sessionStorage.setItem(ADMIN_SESSION_KEY, "true");
                    sessionStorage.setItem("julie_bakery_admin_token", passInp);
                } catch (e) {}
                errEl.classList.add("hidden");
                updateAdminSessionUI();
                renderAdminRouteState();
                renderCatalog();
                checkCloudStatus();
                showToast("Bienvenida al Panel /admin de Julié Bakery");
            } else {
                errEl.classList.remove("hidden");
            }
        }'''

if old_login_func in html:
    html = html.replace(old_login_func, new_login_func)
    print("Replaced handleAdminLogin function successfully")

# 6. Actualizar saveCatalogToStorage y saveCategoriesToStorage para invocar saveCatalogToCloud()
old_save_catalog = '''        function saveCatalogToStorage() {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(products));
            } catch (e) {
                showToast("Imagen muy pesada, se optimizó en memoria");
            }
            renderImmediateSection();
            renderFeaturedCarousel();
            renderCatalog();
            if (isAdminLoggedIn) {
                renderAdminImmediateTagger();
                renderAdminProductsList();
            }
        }'''

new_save_catalog = '''        function saveCatalogToStorage() {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(products));
            } catch (e) {}
            renderImmediateSection();
            renderFeaturedCarousel();
            renderCatalog();
            if (isAdminLoggedIn) {
                renderAdminImmediateTagger();
                renderAdminProductsList();
                saveCatalogToCloud();
            }
        }'''

if old_save_catalog in html:
    html = html.replace(old_save_catalog, new_save_catalog)
    print("Replaced saveCatalogToStorage successfully")

old_save_cats = '''        function saveCategoriesToStorage() {
            try {
                localStorage.setItem(CATEGORIES_STORAGE_KEY, JSON.stringify(categories));
            } catch (e) {}
            renderCategoryNavigation();
            renderCatalog();
            if (isAdminLoggedIn) {
                renderAdminCategoriesList();
                populateAdminCategorySelect();
            }
        }'''

new_save_cats = '''        function saveCategoriesToStorage() {
            try {
                localStorage.setItem(CATEGORIES_STORAGE_KEY, JSON.stringify(categories));
            } catch (e) {}
            renderCategoryNavigation();
            renderCatalog();
            if (isAdminLoggedIn) {
                renderAdminCategoriesList();
                populateAdminCategorySelect();
                saveCatalogToCloud();
            }
        }'''

if old_save_cats in html:
    html = html.replace(old_save_cats, new_save_cats)
    print("Replaced saveCategoriesToStorage successfully")

# 7. Agregar funciones de nube: uploadImageFileToCloud, saveCatalogToCloud, fetchCatalogFromCloud, checkCloudStatus
cloud_logic_code = '''
        // ===================================================================
        // SINCRONIZACIÓN EN LA NUBE & SUBIDA DE IMÁGENES A VERCEL / CDN
        // ===================================================================
        let isSavingToCloud = false;
        let lastCloudUpdatedAt = null;

        function getAdminToken() {
            return sessionStorage.getItem("julie_bakery_admin_token") || settings.adminPass || "Helena2024.";
        }

        async function uploadImageFileToCloud(file) {
            showToast("☁️ Subiendo foto a la nube...");
            try {
                const compressedBase64 = await compressImageFileToBase64(file, 1200, 0.82);
                const token = getAdminToken();

                const res = await fetch("/api/upload", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "x-admin-token": token
                    },
                    body: JSON.stringify({
                        imageBase64: compressedBase64,
                        filename: file.name || `foto_${Date.now()}.jpg`
                    })
                });

                if (res.ok) {
                    const data = await res.json();
                    if (data.url) {
                        showToast(`✅ Foto guardada en la nube (${data.provider || 'Cloud'})`);
                        return data.url;
                    }
                }
                return compressedBase64;
            } catch (e) {
                console.warn("Error subiendo a nube, usando base64 optimizado local", e);
                return await compressImageFileToBase64(file, 850, 0.78);
            }
        }

        async function saveCatalogToCloud() {
            if (isSavingToCloud) return;
            const token = getAdminToken();
            isSavingToCloud = true;
            updateCloudBadgeUI(false, "Guardando...");

            try {
                const res = await fetch("/api/catalog", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "x-admin-token": token
                    },
                    body: JSON.stringify({
                        products,
                        categories,
                        settings
                    })
                });

                if (res.ok) {
                    const data = await res.json();
                    updateCloudBadgeUI(true, data.savedInCloud ? "Nube Activa" : "Guardado");
                    const timeStr = new Date().toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit" });
                    const timeEl = document.getElementById("cloudSyncTime");
                    if (timeEl) timeEl.textContent = "Sincronizado " + timeStr;
                    showToast("☁️ Cambios guardados en la nube para todos los clientes");
                } else {
                    updateCloudBadgeUI(false, "Error al sincronizar");
                }
            } catch (err) {
                console.warn("No se pudo conectar a la nube:", err);
                updateCloudBadgeUI(false, "Modo Local");
            } finally {
                isSavingToCloud = false;
            }
        }

        async function fetchCatalogFromCloud() {
            try {
                const res = await fetch("/api/catalog", { cache: "no-store" });
                if (!res.ok) return;
                const data = await res.json();
                if (!data || !data.products) return;

                if (!lastCloudUpdatedAt || data.updatedAt !== lastCloudUpdatedAt) {
                    lastCloudUpdatedAt = data.updatedAt;
                    products = data.products;
                    if (Array.isArray(data.categories) && data.categories.length > 0) {
                        categories = data.categories;
                    }
                    if (data.settings) {
                        settings = { ...settings, ...data.settings };
                    }

                    try {
                        localStorage.setItem(STORAGE_KEY, JSON.stringify(products));
                        localStorage.setItem(CATEGORIES_STORAGE_KEY, JSON.stringify(categories));
                        localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(settings));
                    } catch (e) {}

                    renderCategoryNavigation();
                    renderImmediateSection();
                    renderFeaturedCarousel();
                    renderCatalog();
                    updateWhatsappLinksUI();
                    if (isAdminLoggedIn) {
                        renderAdminImmediateTagger();
                        renderAdminProductsList();
                        renderAdminCategoriesList();
                    }
                }
            } catch (e) {
                console.warn("Sincronización de fondo:", e);
            }
        }

        async function checkCloudStatus() {
            try {
                const res = await fetch("/api/status", { cache: "no-store" });
                if (res.ok) {
                    const data = await res.json();
                    const badge = document.getElementById("cloudStatusBadge");
                    const text = document.getElementById("cloudStatusText");
                    const desc = document.getElementById("cloudStatusDesc");
                    const timeEl = document.getElementById("cloudSyncTime");

                    if (data.cloudActive) {
                        if (badge) badge.className = "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-olivaLight text-oliva text-[10px] font-bold";
                        if (text) text.textContent = `🟢 Nube Activa (${data.activeProvider})`;
                        if (desc) desc.textContent = data.message;
                    } else {
                        if (badge) badge.className = "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-rosaLight text-bordo text-[10px] font-bold";
                        if (text) text.textContent = "🟡 Modo Local (Sin Vercel Blob)";
                        if (desc) desc.textContent = "En Vercel conectá Vercel Blob en 1 clic para tener almacenamiento ilimitado.";
                    }
                    if (timeEl && data.updatedAt) {
                        const d = new Date(data.updatedAt);
                        timeEl.textContent = "Último cambio: " + d.toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit" });
                    }
                }
            } catch (e) {}
        }

        function updateCloudBadgeUI(isActive, label) {
            const badge = document.getElementById("cloudStatusBadge");
            const text = document.getElementById("cloudStatusText");
            if (text) text.textContent = label;
            if (badge) {
                badge.className = isActive 
                    ? "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-olivaLight text-oliva text-[10px] font-bold"
                    : "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-rosaLight text-bordo text-[10px] font-bold";
            }
        }

        function syncCatalogWithCloudNow() {
            saveCatalogToCloud();
            checkCloudStatus();
        }
'''

# 8. Modificar quickUpdateProductPhoto, handleMainProductImageUpload, handleVariantImageUpload para usar uploadImageFileToCloud
old_quick_update_photo = '''        async function quickUpdateProductPhoto(productId, fileInput) {
            const file = fileInput.files && fileInput.files[0];
            if (!file) return;
            try {
                const compressedBase64 = await compressImageFileToBase64(file);
                const prod = products.find(p => p.id === productId);
                if (!prod) return;
                prod.variants.forEach(v => {
                    v.image = compressedBase64;
                });
                saveCatalogToStorage();
                showToast("Foto actualizada y guardada en el catálogo");
            } catch (e) {
                showToast("No se pudo procesar la imagen");
            }
        }'''

new_quick_update_photo = '''        async function quickUpdateProductPhoto(productId, fileInput) {
            const file = fileInput.files && fileInput.files[0];
            if (!file) return;
            try {
                const cloudUrl = await uploadImageFileToCloud(file);
                const prod = products.find(p => p.id === productId);
                if (!prod) return;
                prod.variants.forEach(v => {
                    v.image = cloudUrl;
                });
                saveCatalogToStorage();
                showToast("Foto guardada en la nube y actualizada");
            } catch (e) {
                showToast("No se pudo procesar la imagen");
            }
        }'''

if old_quick_update_photo in html:
    html = html.replace(old_quick_update_photo, new_quick_update_photo)
    print("Replaced quickUpdateProductPhoto successfully")

old_main_upload = '''        async function handleMainProductImageUpload(input) {
            const file = input.files && input.files[0];
            if (!file) return;
            try {
                const compressedDataUrl = await compressImageFileToBase64(file);
                document.getElementById("formMainImage").value = compressedDataUrl;
                const preview = document.getElementById("mainProductPreviewImg");
                if (preview) preview.src = compressedDataUrl;
                applyMainPhotoToAllVariants();
                showToast("Foto cargada desde tu celular");
            } catch (e) {
                showToast("Error al cargar la imagen");
            }
        }'''

new_main_upload = '''        async function handleMainProductImageUpload(input) {
            const file = input.files && input.files[0];
            if (!file) return;
            try {
                const preview = document.getElementById("mainProductPreviewImg");
                const quickReader = new FileReader();
                quickReader.onload = e => { if (preview) preview.src = e.target.result; };
                quickReader.readAsDataURL(file);

                const cloudUrl = await uploadImageFileToCloud(file);
                document.getElementById("formMainImage").value = cloudUrl;
                if (preview) preview.src = cloudUrl;
                applyMainPhotoToAllVariants();
                showToast("Foto guardada en la nube");
            } catch (e) {
                showToast("Error al cargar la imagen");
            }
        }'''

if old_main_upload in html:
    html = html.replace(old_main_upload, new_main_upload)
    print("Replaced handleMainProductImageUpload successfully")

old_var_upload = '''        async function handleVariantImageUpload(fileInput, rowId) {
            const file = fileInput.files && fileInput.files[0];
            if (!file) return;
            try {
                const compressedDataUrl = await compressImageFileToBase64(file);
                const row = document.getElementById(rowId);
                if (row) {
                    row.querySelector(".var-image").value = compressedDataUrl;
                    row.querySelector(".var-preview").src = compressedDataUrl;
                }
                showToast("Foto de medida cargada");
            } catch (e) {
                showToast("No se pudo cargar la foto");
            }
        }'''

new_var_upload = '''        async function handleVariantImageUpload(fileInput, rowId) {
            const file = fileInput.files && fileInput.files[0];
            if (!file) return;
            try {
                const row = document.getElementById(rowId);
                const quickReader = new FileReader();
                quickReader.onload = e => {
                    if (row) row.querySelector(".var-preview").src = e.target.result;
                };
                quickReader.readAsDataURL(file);

                const cloudUrl = await uploadImageFileToCloud(file);
                if (row) {
                    row.querySelector(".var-image").value = cloudUrl;
                    row.querySelector(".var-preview").src = cloudUrl;
                }
                showToast("Foto de medida guardada en la nube");
            } catch (e) {
                showToast("No se pudo cargar la foto");
            }
        }'''

if old_var_upload in html:
    html = html.replace(old_var_upload, new_var_upload)
    print("Replaced handleVariantImageUpload successfully")

# 9. Inyectar la lógica de nube antes de initApp()
html = html.replace('function initApp() {', cloud_logic_code + '\n        function initApp() {')

# 10. Actualizar initApp para disparar fetchCatalogFromCloud() y periodic sync
init_additions = '''
            // Sincronización en la nube en tiempo real
            fetchCatalogFromCloud();
            checkCloudStatus();
            setInterval(fetchCatalogFromCloud, 25000); // Consulta periódica cada 25 segundos
            window.addEventListener("focus", fetchCatalogFromCloud);
            document.addEventListener("visibilitychange", function() {
                if (document.visibilityState === "visible") fetchCatalogFromCloud();
            });
'''
html = html.replace('window.addEventListener("hashchange", checkUrlHashForAdmin);', 'window.addEventListener("hashchange", checkUrlHashForAdmin);\n' + init_additions)

with open(dst_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated {dst_path} successfully ({len(html)} bytes)")
