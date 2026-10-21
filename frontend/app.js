// En local/Docker el frontend va por Nginx (/api -> backend:8000).
// En la nube (Netlify/GitHub Pages) no hay Nginx, hay que apuntar
// a la URL pública del backend en Render.
// Cómo usarlo: crear frontend/config.js con:
//   window.__BACKEND_URL__ = "https://tu-backend.onrender.com";
// Si ese archivo no existe, se usa "/api" (comportamiento original).
const API = (window.__BACKEND_URL__ || "/api").replace(/\/$/, "");

// Mensaje de bienvenida con el nombre del usuario 1
async function cargarBienvenida() {
  const saludo = document.getElementById("saludo");
  try {
    const respuesta = await fetch(API + "/usuarios/1");
    if (!respuesta.ok) throw new Error("HTTP " + respuesta.status);
    const usuario = await respuesta.json();
    saludo.textContent = "¡Bienvenido/a, " + usuario.nombre + "!";
  } catch (error) {
    saludo.textContent = "No se pudo conectar con el backend";
    console.error(error);
  }
}

// Lista con todos los usuarios de la tabla
async function cargarUsuarios() {
  const lista = document.getElementById("lista");
  lista.innerHTML = "";
  try {
    const respuesta = await fetch(API + "/usuarios");
    const usuarios = await respuesta.json();
    usuarios.forEach(function (u) {
      const item = document.createElement("li");
      item.textContent = u.id + " · " + u.nombre + " (" + u.email + ")";
      lista.appendChild(item);
    });
  } catch (error) {
    lista.textContent = "Error al cargar los usuarios";
  }
}

function recargar() {
  cargarBienvenida();
  cargarUsuarios();
}

recargar();
