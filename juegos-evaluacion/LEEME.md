# Juegos de evaluación (cosplay-inc.com/evaluacion)

Los 59 juegos de los cuatro momentos se generan a partir de los archivos de `contenido/`.
En cada pregunta, la respuesta correcta va primero; el juego baraja las opciones.

Para cambiar un texto o agregar un tema:
1. Editar el archivo de `contenido/` del área.
2. Copiar los archivos a `/tmp/gen/` y ejecutar:
   `python3 -I /tmp/gen/generar.py <ruta a apps/web/public/evaluacion>`
   (reemplaza los juegos generados y actualiza el índice sin tocar los demás).
3. Subir los cambios del repositorio del sitio.
