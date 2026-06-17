from flask import Flask, request, render_template_string

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────────────
# ESTILOS COMUNES (compartidos entre todas las páginas)
# ─────────────────────────────────────────────────────────────────────────
BASE_STYLE = """
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: Arial, Helvetica, sans-serif;
    }

    body {
      background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
      min-height: 100vh;
      color: white;
    }

    .navbar {
      width: 100%;
      height: 70px;
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 50px;
      position: fixed;
      top: 0;
      left: 0;
      z-index: 100;
    }

    .logo-nav {
      color: white;
      font-size: 28px;
      font-weight: bold;
      text-decoration: none;
    }

    .menu {
      display: flex;
      gap: 30px;
      align-items: center;
    }

    .menu a {
      color: white;
      text-decoration: none;
      font-size: 16px;
      transition: 0.3s;
      padding: 6px 4px;
      border-bottom: 2px solid transparent;
    }

    .menu a:hover,
    .menu a.active {
      color: #60a5fa;
      border-bottom: 2px solid #60a5fa;
    }

    .cart-link {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .cart-badge {
      background: #ef4444;
      color: white;
      font-size: 12px;
      font-weight: bold;
      border-radius: 50%;
      min-width: 20px;
      height: 20px;
      padding: 0 4px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .container {
      width: 100%;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding-top: 90px;
      padding-bottom: 40px;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-30px); }
      to   { opacity: 1; transform: translateY(0); }
    }
"""

# ─────────────────────────────────────────────────────────────────────────
# SCRIPT DEL CARRITO (compartido entre todas las páginas)
# Usa localStorage para persistir el carrito entre páginas del sitio.
# ─────────────────────────────────────────────────────────────────────────
CART_SCRIPT = """
<script>
  const CARRITO_KEY = "carritoDanixps";

  function obtenerCarrito() {
    const data = localStorage.getItem(CARRITO_KEY);
    return data ? JSON.parse(data) : [];
  }

  function guardarCarrito(carrito) {
    localStorage.setItem(CARRITO_KEY, JSON.stringify(carrito));
  }

  function actualizarContadorCarrito() {
    const carrito = obtenerCarrito();
    const badge = document.getElementById("cart-badge");
    if (badge) {
      badge.textContent = carrito.length;
    }
  }

  function agregarAlCarrito(nombre, precio, emoji) {
    const carrito = obtenerCarrito();
    carrito.push({ nombre: nombre, precio: precio, emoji: emoji });
    guardarCarrito(carrito);
    actualizarContadorCarrito();

    if (typeof renderizarCarrito === "function") {
      renderizarCarrito();
    }
  }

  function eliminarDelCarrito(index) {
    const carrito = obtenerCarrito();
    carrito.splice(index, 1);
    guardarCarrito(carrito);
    actualizarContadorCarrito();

    if (typeof renderizarCarrito === "function") {
      renderizarCarrito();
    }
  }

  function vaciarCarrito() {
    guardarCarrito([]);
    actualizarContadorCarrito();
    if (typeof renderizarCarrito === "function") {
      renderizarCarrito();
    }
  }

  document.addEventListener("DOMContentLoaded", actualizarContadorCarrito);
</script>
"""

# ─────────────────────────────────────────────────────────────────────────
# NAVBAR (recibe la página activa para resaltarla)
# ─────────────────────────────────────────────────────────────────────────
def navbar(active=""):
    def cls(name):
        return "active" if name == active else ""
    return f"""
    <div class="navbar">
      <a href="/" class="logo-nav">DANIXPS STORE</a>
      <div class="menu">
        <a href="/" class="{cls('inicio')}">Inicio</a>
        <a href="/servicios" class="{cls('servicios')}">Servicios</a>
        <a href="/categorias" class="{cls('categorias')}">Categorías</a>
        <a href="/categoria/hombre" class="{cls('hombre')}">Ropa Hombre</a>
        <a href="/categoria/mujer" class="{cls('mujer')}">Ropa Mujer</a>
        <a href="/contacto" class="{cls('contacto')}">Contacto</a>
        <a href="/carrito" class="cart-link {cls('carrito')}">🛒 Mi Carrito <span class="cart-badge" id="cart-badge">0</span></a>
      </div>
    </div>
    """

# ─────────────────────────────────────────────────────────────────────────
# PÁGINA: INICIO (Login)
# ─────────────────────────────────────────────────────────────────────────
HTML_INICIO = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DANIXPS STORE</title>
  <style>
    __BASE_STYLE__

    .login-container {
      width: 400px;
      background: rgba(255, 255, 255, 0.1);
      padding: 40px;
      border-radius: 20px;
      backdrop-filter: blur(10px);
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
      color: white;
      animation: fadeIn 1s ease;
    }

    .logo { text-align: center; margin-bottom: 30px; }
    .logo h1 { font-size: 32px; }
    .logo p { color: #cbd5e1; margin-top: 10px; }

    .input-group { margin-bottom: 20px; }
    .input-group label { display: block; margin-bottom: 8px; font-weight: bold; }
    .input-group input {
      width: 100%;
      padding: 14px;
      border: none;
      border-radius: 10px;
      outline: none;
      transition: 0.3s;
    }
    .input-group input:focus {
      transform: scale(1.02);
      box-shadow: 0 0 15px #3b82f6;
    }

    .btn {
      width: 100%;
      padding: 14px;
      border: none;
      border-radius: 10px;
      background: #2563eb;
      color: white;
      font-size: 16px;
      cursor: pointer;
      transition: 0.3s;
      font-weight: bold;
    }
    .btn:hover { background: #1d4ed8; transform: scale(1.03); }

    .mensaje { margin-top: 20px; text-align: center; font-weight: bold; font-size: 18px; }
  </style>
</head>
<body>
  __NAVBAR__

  <div class="container">
    <div class="login-container">
      <div class="logo">
        <h1>DANIXPS</h1>
        <p>Tienda Virtual de Ropa</p>
      </div>
      <form id="loginForm">
        <div class="input-group">
          <label>Usuario</label>
          <input type="text" id="usuario" placeholder="Ingrese su usuario" required>
        </div>
        <div class="input-group">
          <label>Contraseña</label>
          <input type="password" id="password" placeholder="Ingrese su contraseña" required>
        </div>
        <button type="submit" class="btn">Iniciar Sesión</button>
      </form>
      <div class="mensaje" id="mensaje"></div>
    </div>
  </div>

  __CART_SCRIPT__

  <script>
    const usuarioCorrecto = "Daniel";
    const passwordCorrecta = "1234";

    const form = document.getElementById("loginForm");

    form.addEventListener("submit", function (event) {
      event.preventDefault();

      const usuario = document.getElementById("usuario").value;
      const password = document.getElementById("password").value;
      const mensaje = document.getElementById("mensaje");

      if (usuario === usuarioCorrecto && password === passwordCorrecta) {
        mensaje.style.color = "#22c55e";
        mensaje.innerHTML = "✔ Bienvenido Daniel";
      } else {
        mensaje.style.color = "#ef4444";
        mensaje.innerHTML = "❌ Usuario o contraseña incorrecta";
      }
    });
  </script>
</body>
</html>
""".replace("__BASE_STYLE__", BASE_STYLE)


# ─────────────────────────────────────────────────────────────────────────
# PÁGINA: CATEGORÍAS (listado general)
# ─────────────────────────────────────────────────────────────────────────
HTML_CATEGORIAS = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Categorías - DANIXPS STORE</title>
  <style>
    __BASE_STYLE__

    .content {
      width: 100%;
      max-width: 900px;
      text-align: center;
      padding: 0 20px;
      animation: fadeIn 1s ease;
    }

    .content h1 { font-size: 36px; margin-bottom: 10px; }
    .content p { color: #cbd5e1; margin-bottom: 40px; }

    .cards {
      display: flex;
      gap: 30px;
      justify-content: center;
      flex-wrap: wrap;
    }

    .card {
      width: 320px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 40px 30px;
      backdrop-filter: blur(10px);
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
      text-decoration: none;
      color: white;
      transition: 0.3s;
    }

    .card:hover {
      transform: translateY(-8px);
      box-shadow: 0 15px 50px rgba(59, 130, 246, 0.4);
    }

    .card .icon { font-size: 50px; margin-bottom: 15px; }
    .card h2 { font-size: 24px; margin-bottom: 10px; }
    .card p { color: #cbd5e1; font-size: 14px; margin-bottom: 0; }
  </style>
</head>
<body>
  __NAVBAR__

  <div class="container">
    <div class="content">
      <h1>Nuestras Categorías</h1>
      <p>Explora nuestra colección dividida por categoría</p>

      <div class="cards">
        <a href="/categoria/hombre" class="card">
          <div class="icon">👔</div>
          <h2>Ropa Hombre</h2>
          <p>Camisas, polos, pantalones y mucho más</p>
        </a>

        <a href="/categoria/mujer" class="card">
          <div class="icon">👗</div>
          <h2>Ropa Mujer</h2>
          <p>Vestidos, blusas, faldas y mucho más</p>
        </a>
      </div>
    </div>
  </div>

  __CART_SCRIPT__
</body>
</html>
""".replace("__BASE_STYLE__", BASE_STYLE)


# ─────────────────────────────────────────────────────────────────────────
# PÁGINA: CATEGORÍA INDIVIDUAL (Hombre / Mujer) - reutilizable
# ─────────────────────────────────────────────────────────────────────────
HTML_CATEGORIA_DETALLE = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__TITULO__ - DANIXPS STORE</title>
  <style>
    __BASE_STYLE__

    .content {
      width: 100%;
      max-width: 1000px;
      padding: 0 20px;
      animation: fadeIn 1s ease;
    }

    .content h1 { font-size: 36px; margin-bottom: 10px; text-align: center; }
    .content > p { color: #cbd5e1; margin-bottom: 40px; text-align: center; }

    .productos {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 25px;
    }

    .producto {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      padding: 25px 20px;
      text-align: center;
      backdrop-filter: blur(10px);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
      transition: 0.3s;
    }

    .producto:hover {
      transform: translateY(-6px);
      box-shadow: 0 12px 40px rgba(59, 130, 246, 0.35);
    }

    .producto .img-placeholder {
      width: 100%;
      height: 140px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 48px;
      margin-bottom: 15px;
    }

    .producto h3 { font-size: 18px; margin-bottom: 6px; }
    .producto .precio { color: #60a5fa; font-weight: bold; font-size: 18px; margin-bottom: 12px; }

    .producto .btn-comprar {
      display: inline-block;
      width: 100%;
      padding: 10px;
      border: none;
      border-radius: 8px;
      background: #2563eb;
      color: white;
      font-weight: bold;
      cursor: pointer;
      transition: 0.3s;
    }

    .producto .btn-comprar:hover { background: #1d4ed8; }
    .producto .btn-comprar.agregado { background: #16a34a; }

    .volver {
      display: block;
      text-align: center;
      margin-top: 40px;
      color: #93c5fd;
      text-decoration: none;
    }
    .volver:hover { text-decoration: underline; }
  </style>
</head>
<body>
  __NAVBAR__

  <div class="container">
    <div class="content">
      <h1>__TITULO__</h1>
      <p>__SUBTITULO__</p>

      <div class="productos">
        __PRODUCTOS__
      </div>

      <a href="/categorias" class="volver">← Volver a Categorías</a>
    </div>
  </div>

  __CART_SCRIPT__

  <script>
    function marcarAgregado(boton) {
      const textoOriginal = boton.textContent;
      boton.textContent = "✔ Agregado";
      boton.classList.add("agregado");
      setTimeout(() => {
        boton.textContent = textoOriginal;
        boton.classList.remove("agregado");
      }, 1200);
    }
  </script>
</body>
</html>
""".replace("__BASE_STYLE__", BASE_STYLE)


def producto_card(emoji, nombre, precio):
    nombre_js = nombre.replace("\\", "\\\\").replace("'", "\\'")
    return f"""
        <div class="producto">
          <div class="img-placeholder">{emoji}</div>
          <h3>{nombre}</h3>
          <div class="precio">S/ {precio}</div>
          <button class="btn-comprar" onclick="agregarAlCarrito('{nombre_js}', '{precio}', '{emoji}'); marcarAgregado(this);">Agregar al carrito</button>
        </div>
    """


PRODUCTOS_HOMBRE = [
    ("👕", "Polo Básico", "39.90"),
    ("👔", "Camisa Formal", "79.90"),
    ("🧥", "Casaca Jean", "129.90"),
    ("👖", "Pantalón Jean", "89.90"),
    ("🩳", "Short Deportivo", "49.90"),
    ("🧶", "Chompa de Lana", "99.90"),
]

PRODUCTOS_MUJER = [
    ("👗", "Vestido Casual", "89.90"),
    ("👚", "Blusa Elegante", "59.90"),
    ("🩱", "Body Deportivo", "45.90"),
    ("👖", "Jean Skinny", "94.90"),
    ("🧥", "Chaqueta Mujer", "119.90"),
    ("🥻", "Falda Plisada", "69.90"),
]


# ─────────────────────────────────────────────────────────────────────────
# PÁGINA: SERVICIOS
# ─────────────────────────────────────────────────────────────────────────
HTML_SERVICIOS = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Servicios - DANIXPS STORE</title>
  <style>
    __BASE_STYLE__

    .content {
      width: 100%;
      max-width: 900px;
      text-align: center;
      padding: 0 20px;
      animation: fadeIn 1s ease;
    }

    .content h1 { font-size: 36px; margin-bottom: 10px; }
    .content p.subtitle { color: #cbd5e1; margin-bottom: 40px; }

    .servicios {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 25px;
    }

    .servicio {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      padding: 30px 20px;
      backdrop-filter: blur(10px);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    }

    .servicio .icon { font-size: 40px; margin-bottom: 12px; }
    .servicio h3 { margin-bottom: 8px; }
    .servicio p { color: #cbd5e1; font-size: 14px; }
  </style>
</head>
<body>
  __NAVBAR__

  <div class="container">
    <div class="content">
      <h1>Nuestros Servicios</h1>
      <p class="subtitle">Todo lo que DANIXPS STORE tiene para ti</p>

      <div class="servicios">
        <div class="servicio">
          <div class="icon">🚚</div>
          <h3>Envíos a todo el Perú</h3>
          <p>Recibe tus pedidos en cualquier ciudad del país.</p>
        </div>
        <div class="servicio">
          <div class="icon">💳</div>
          <h3>Pagos Seguros</h3>
          <p>Aceptamos tarjetas, Yape y Plin.</p>
        </div>
        <div class="servicio">
          <div class="icon">🔄</div>
          <h3>Cambios y Devoluciones</h3>
          <p>Hasta 7 días para cambiar tu producto.</p>
        </div>
        <div class="servicio">
          <div class="icon">🎧</div>
          <h3>Atención al Cliente</h3>
          <p>Te ayudamos por WhatsApp, llamada o redes sociales.</p>
        </div>
      </div>
    </div>
  </div>

  __CART_SCRIPT__
</body>
</html>
""".replace("__BASE_STYLE__", BASE_STYLE)


# ─────────────────────────────────────────────────────────────────────────
# PÁGINA: CONTACTO (teléfono Perú, Facebook, Instagram)
# ─────────────────────────────────────────────────────────────────────────
HTML_CONTACTO = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Contacto - DANIXPS STORE</title>
  <style>
    __BASE_STYLE__

    .content {
      width: 100%;
      max-width: 600px;
      padding: 0 20px;
      animation: fadeIn 1s ease;
    }

    .contacto-card {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 40px;
      backdrop-filter: blur(10px);
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
      text-align: center;
    }

    .contacto-card h1 { font-size: 32px; margin-bottom: 10px; }
    .contacto-card > p { color: #cbd5e1; margin-bottom: 30px; }

    .info-item {
      display: flex;
      align-items: center;
      gap: 15px;
      background: rgba(255, 255, 255, 0.07);
      border-radius: 12px;
      padding: 16px 20px;
      margin-bottom: 16px;
      text-align: left;
      text-decoration: none;
      color: white;
      transition: 0.3s;
    }

    .info-item:hover {
      background: rgba(255, 255, 255, 0.15);
      transform: translateX(4px);
    }

    .info-item .icon {
      font-size: 28px;
      width: 40px;
      text-align: center;
      flex-shrink: 0;
    }

    .info-item .text strong {
      display: block;
      font-size: 14px;
      color: #93c5fd;
      margin-bottom: 2px;
    }

    .info-item .text span {
      font-size: 16px;
    }

    .redes {
      display: flex;
      gap: 16px;
      justify-content: center;
      margin-top: 30px;
    }

    .redes a {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.12);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      text-decoration: none;
      color: white;
      transition: 0.3s;
    }

    .redes a:hover {
      transform: scale(1.15);
    }

    .redes a.facebook:hover { background: #1877f2; }
    .redes a.instagram:hover { background: linear-gradient(45deg, #f58529, #dd2a7b, #8134af, #515bd4); }
    .redes a.whatsapp:hover { background: #25d366; }
  </style>
</head>
<body>
  __NAVBAR__

  <div class="container">
    <div class="content">
      <div class="contacto-card">
        <h1>Contáctanos</h1>
        <p>Estamos aquí para ayudarte. Escríbenos o llámanos.</p>

        <a href="tel:+51987654321" class="info-item">
          <div class="icon">📞</div>
          <div class="text">
            <strong>Teléfono / WhatsApp (Perú)</strong>
            <span>+51 987 654 321</span>
          </div>
        </a>

        <a href="mailto:contacto@danixpsstore.pe" class="info-item">
          <div class="icon">✉️</div>
          <div class="text">
            <strong>Correo electrónico</strong>
            <span>contacto@danixpsstore.pe</span>
          </div>
        </a>

        <div class="info-item" style="cursor:default;">
          <div class="icon">📍</div>
          <div class="text">
            <strong>Ubicación</strong>
            <span>Lima, Perú</span>
          </div>
        </div>

        <div class="redes">
          <a href="https://www.facebook.com/danixpsstore" target="_blank" class="facebook" title="Facebook">📘</a>
          <a href="https://www.instagram.com/danixpsstore" target="_blank" class="instagram" title="Instagram">📷</a>
          <a href="https://wa.me/51987654321" target="_blank" class="whatsapp" title="WhatsApp">💬</a>
        </div>
      </div>
    </div>
  </div>

  __CART_SCRIPT__
</body>
</html>
""".replace("__BASE_STYLE__", BASE_STYLE)


# ─────────────────────────────────────────────────────────────────────────
# PÁGINA: MI CARRITO
# ─────────────────────────────────────────────────────────────────────────
HTML_CARRITO = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mi Carrito - DANIXPS STORE</title>
  <style>
    __BASE_STYLE__

    .content {
      width: 100%;
      max-width: 700px;
      padding: 0 20px;
      animation: fadeIn 1s ease;
    }

    .content h1 { font-size: 36px; margin-bottom: 10px; text-align: center; }
    .content > p.subtitle { color: #cbd5e1; margin-bottom: 30px; text-align: center; }

    .carrito-vacio {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      padding: 50px 20px;
      text-align: center;
      color: #cbd5e1;
      backdrop-filter: blur(10px);
    }

    .carrito-vacio .icon { font-size: 50px; margin-bottom: 15px; }

    .carrito-item {
      display: flex;
      align-items: center;
      gap: 20px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 14px;
      padding: 18px 20px;
      margin-bottom: 16px;
      backdrop-filter: blur(10px);
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }

    .carrito-item .carrito-item-icon {
      font-size: 36px;
      width: 60px;
      height: 60px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .carrito-item .carrito-item-info {
      flex: 1;
    }

    .carrito-item .carrito-item-info h3 { font-size: 17px; margin-bottom: 4px; }
    .carrito-item .carrito-item-info p { color: #60a5fa; font-weight: bold; }

    .btn-eliminar {
      background: #ef4444;
      color: white;
      border: none;
      border-radius: 8px;
      padding: 10px 16px;
      font-weight: bold;
      cursor: pointer;
      transition: 0.3s;
      flex-shrink: 0;
    }

    .btn-eliminar:hover { background: #dc2626; }

    .carrito-resumen {
      margin-top: 25px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 14px;
      padding: 20px 25px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      backdrop-filter: blur(10px);
    }

    .carrito-resumen .total-label { font-size: 16px; color: #cbd5e1; }
    .carrito-resumen .total-monto { font-size: 24px; font-weight: bold; color: #60a5fa; }

    .acciones-carrito {
      display: flex;
      justify-content: space-between;
      margin-top: 25px;
      gap: 15px;
    }

    .btn-vaciar {
      background: rgba(255, 255, 255, 0.12);
      color: white;
      border: none;
      border-radius: 10px;
      padding: 12px 20px;
      font-weight: bold;
      cursor: pointer;
      transition: 0.3s;
    }

    .btn-vaciar:hover { background: rgba(239, 68, 68, 0.4); }

    .volver {
      display: inline-block;
      color: #93c5fd;
      text-decoration: none;
      padding: 12px 20px;
    }
    .volver:hover { text-decoration: underline; }
  </style>
</head>
<body>
  __NAVBAR__

  <div class="container">
    <div class="content">
      <h1>Mi Carrito</h1>
      <p class="subtitle">Revisa y gestiona los productos que agregaste</p>

      <div id="carrito-vacio" class="carrito-vacio" style="display:none;">
        <div class="icon">🛒</div>
        <p>Tu carrito está vacío. ¡Explora nuestras categorías y agrega productos!</p>
      </div>

      <div id="carrito-lista"></div>

      <div id="carrito-resumen" class="carrito-resumen" style="display:none;">
        <span class="total-label">Total</span>
        <span class="total-monto" id="carrito-total">S/ 0.00</span>
      </div>

      <div class="acciones-carrito">
        <a href="/categorias" class="volver">← Seguir comprando</a>
        <button class="btn-vaciar" onclick="vaciarCarrito()">Vaciar carrito</button>
      </div>
    </div>
  </div>

  __CART_SCRIPT__

  <script>
    function renderizarCarrito() {
      const carrito = obtenerCarrito();
      const contenedor = document.getElementById("carrito-lista");
      const vacioEl = document.getElementById("carrito-vacio");
      const resumenEl = document.getElementById("carrito-resumen");
      const totalEl = document.getElementById("carrito-total");

      if (carrito.length === 0) {
        contenedor.innerHTML = "";
        vacioEl.style.display = "block";
        resumenEl.style.display = "none";
        return;
      }

      vacioEl.style.display = "none";
      resumenEl.style.display = "flex";

      let total = 0;
      contenedor.innerHTML = carrito.map((item, index) => {
        total += parseFloat(item.precio);
        return `
          <div class="carrito-item">
            <div class="carrito-item-icon">${item.emoji}</div>
            <div class="carrito-item-info">
              <h3>${item.nombre}</h3>
              <p>S/ ${item.precio}</p>
            </div>
            <button class="btn-eliminar" onclick="eliminarDelCarrito(${index})">🗑 Eliminar</button>
          </div>
        `;
      }).join("");

      totalEl.textContent = "S/ " + total.toFixed(2);
    }

    document.addEventListener("DOMContentLoaded", renderizarCarrito);
  </script>
</body>
</html>
""".replace("__BASE_STYLE__", BASE_STYLE)


# ─────────────────────────────────────────────────────────────────────────
# RUTAS
# ─────────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def inicio():
    mensaje = ""
    if request.method == "POST":
        codigo = request.form.get("codigo", "")
        nombres = request.form.get("nombres", "")
        apellidos = request.form.get("apellidos", "")
        with open("personas.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"{codigo},{nombres},{apellidos}\n")
        mensaje = "Registro almacenado correctamente."
    html = (
        HTML_INICIO
        .replace("__NAVBAR__", navbar("inicio"))
        .replace("__CART_SCRIPT__", CART_SCRIPT)
    )
    return render_template_string(html, mensaje=mensaje)


@app.route("/servicios")
def servicios():
    html = (
        HTML_SERVICIOS
        .replace("__NAVBAR__", navbar("servicios"))
        .replace("__CART_SCRIPT__", CART_SCRIPT)
    )
    return render_template_string(html)


@app.route("/categorias")
def categorias():
    html = (
        HTML_CATEGORIAS
        .replace("__NAVBAR__", navbar("categorias"))
        .replace("__CART_SCRIPT__", CART_SCRIPT)
    )
    return render_template_string(html)


@app.route("/categoria/<nombre>")
def categoria_detalle(nombre):
    nombre = nombre.lower()

    if nombre == "hombre":
        titulo = "Ropa Hombre"
        subtitulo = "Encuentra el estilo perfecto para ti"
        productos = PRODUCTOS_HOMBRE
        active = "hombre"
    elif nombre == "mujer":
        titulo = "Ropa Mujer"
        subtitulo = "Las últimas tendencias en moda femenina"
        productos = PRODUCTOS_MUJER
        active = "mujer"
    else:
        # Categoría no reconocida -> redirige visualmente a la lista
        titulo = "Categoría no encontrada"
        subtitulo = "Por favor selecciona una categoría válida"
        productos = []
        active = "categorias"

    productos_html = "".join(producto_card(e, n, p) for e, n, p in productos)

    html = (
        HTML_CATEGORIA_DETALLE
        .replace("__NAVBAR__", navbar(active))
        .replace("__TITULO__", titulo)
        .replace("__SUBTITULO__", subtitulo)
        .replace("__PRODUCTOS__", productos_html)
        .replace("__CART_SCRIPT__", CART_SCRIPT)
    )
    return render_template_string(html)


@app.route("/contacto")
def contacto():
    html = (
        HTML_CONTACTO
        .replace("__NAVBAR__", navbar("contacto"))
        .replace("__CART_SCRIPT__", CART_SCRIPT)
    )
    return render_template_string(html)


@app.route("/carrito")
def carrito():
    html = (
        HTML_CARRITO
        .replace("__NAVBAR__", navbar("carrito"))
        .replace("__CART_SCRIPT__", CART_SCRIPT)
    )
    return render_template_string(html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
