# Nginx liviano para servir archivos estáticos
FROM nginx:alpine

# Nuestra configuración (sirve la web + proxy y CORS hacia el backend)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# La página: HTML, CSS y JavaScript (+ config.js si existe para la nube)
COPY index.html styles.css app.js /usr/share/nginx/html/
COPY config.example.js /usr/share/nginx/html/config.js.example

EXPOSE 80
