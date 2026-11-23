# Guía para agentes de IA: web del Club Deportes Castro

Instrucciones para cualquier agente (Claude Code, Codex, Cursor u otro) que trabaje en este repositorio. El dueño del proyecto pide los cambios en español y en lenguaje cotidiano. Respóndele en español y sin tecnicismos.

## Qué es

Sitio estático para deportescastro.cl, el club de básquetbol de Castro, Chiloé. No hay build ni dependencias. La carpeta `public/` se publica tal cual en Cloudflare Pages, y cada push a `main` publica en uno o dos minutos.

| Archivo | Para qué sirve |
| --- | --- |
| `public/index.html` | Estructura y textos de la página |
| `public/estilos.css` | Diseño |
| `public/app.js` | Arma en el navegador las secciones de partidos y plantilla a partir de los archivos de datos |
| `public/datos/plantilla.js` | **Plantilla y entrenador. Se edita a mano una vez por temporada** |
| `public/datos/resultados.js` | Últimos partidos. **Lo genera un robot: no editar a mano** |
| `scripts/actualizar_resultados.py` | Robot que lee la ficha pública del club en la LNB y regenera `resultados.js` |
| `.github/workflows/resultados.yml` | Ejecuta el robot en GitHub Actions dos veces al día |
| `public/assets/camiseta-giro.webp` | Animación recortada de la camiseta (410 cuadros) |

Los datos son archivos `.js` (`window.PLANTILLA = {...}`) y no `.json` para que la página también funcione si se abre `public/index.html` directamente desde el disco.

## Tarea frecuente: actualizar la plantilla

Normalmente el usuario pegará una lista nueva (de Wikipedia, de Instagram, de la LNB o escrita a mano) y pedirá "actualiza la plantilla".

1. Edita solo `public/datos/plantilla.js`. No hace falta tocar HTML, CSS ni JS.
2. Formato de cada jugador:
   ```js
   { numero: 8, nombre: "Nombre Apellido Apellido", posicion: "Base" },
   ```
   - `posicion` es opcional. Usa solo estos valores: `Base`, `Escolta`, `Alero`, `Ala-pívot`, `Pívot`. Si la fuente usa abreviaturas: B = Base, E = Escolta, A = Alero, AP = Ala-pívot, P = Pívot.
   - Si no sabes la posición, omite el campo. No la inventes.
   - Escribe los nombres con mayúsculas, minúsculas y tildes normales ("Nicolás Álvarez", no "ALVAREZ, N."). Si solo tienes la inicial, usa "C. Collins".
   - El orden no importa: la página ordena por número.
   - Si un jugador no tiene número, pregúntale al usuario en vez de inventar uno.
3. Actualiza también:
   - `titulo`: texto sobre el título de la sección. Por ejemplo, "Plantilla 2027" para una temporada en curso o "Jugaron la temporada 2027" al terminarla.
   - `entrenador`: nombre del entrenador principal. Si no se conoce, déjalo como texto vacío (`""`) y la línea desaparece de la página.
   - `fuente`: enlace de donde salió la lista, si cambia.
4. Fíjate en los datos dudosos y coméntaselos al usuario antes de publicar: números repetidos, nombres con distinta ortografía según la fuente, o jugadores que aparecen en una fuente y no en otra. Si la fuente se contradice, no publiques el dato dudoso.
5. Comprueba que el archivo siga siendo JavaScript válido. Por ejemplo, `node -e "global.window={};require('./public/datos/plantilla.js');console.log(window.PLANTILLA.jugadores.length)"` o abriendo la página.
6. Si el usuario lo pide, haz commit (mensaje en español, en imperativo, por ejemplo "Actualizar plantilla 2027") y push a `main`.

### Fuentes y cuidados

- La fuente más confiable para la plantilla es la ficha oficial del club en la LNB: https://lnbchile.com/liga/uno/equipos/17. Trae número y nombre abreviado, pero no la posición.
- El recuadro superior de Wikipedia ("Datos generales") suele estar desactualizado. Por ejemplo, en 2026 seguía mostrando a Damián Gamarra, que dirigió en 2022-2023. Dale prioridad a la tabla de plantilla (tiene fecha de actualización) y a la prensa reciente.
- El `robots.txt` de lnbchile.com bloquea a los bots de IA y la ruta `/api/` para todos. Los agentes de IA no deben leer lnbchile.com ni usar su API interna. Trabaja con lo que pegue el usuario o con otras fuentes. El robot de GitHub Actions sí puede leer la ficha pública, porque no es un agente de IA y no usa `/api/`.
- No redactes textos copiados de Wikipedia: reformúlalos.

## Partidos y resultados (automático)

- `.github/workflows/resultados.yml` ejecuta `scripts/actualizar_resultados.py` todos los días a las 10:00 y a las 04:30 UTC, y también a mano desde la pestaña Actions ("Run workflow").
- El script lee la ficha pública del club, extrae los últimos 5 partidos y el récord, y reescribe `public/datos/resultados.js` solo si cambió algo. En ese caso hace commit, y Cloudflare Pages publica.
- Si la LNB cambia el formato de su página, el script termina con error sin tocar el archivo, y GitHub avisa por correo al dueño. En ese caso hay que ajustar las expresiones regulares de `extraer()`. Para probarlo sin tocar internet, guarda una copia del HTML de la ficha y ejecuta `python scripts/actualizar_resultados.py copia.html`.
- Los nombres de los rivales salen del diccionario `CODIGOS` del script. Si aparece un código desconocido (por ejemplo "XYZ"), se muestra tal cual: agrégalo al diccionario.
- La ficha pública no trae los próximos partidos. Para mostrarlos, el club tendría que conseguir acceso oficial con la LNB (secretaria@lnbchile.com). Si lo consiguen, la clave va como secreto de GitHub Actions, nunca dentro de `public/`.
- `app.js` muestra un aviso de temporada terminada cuando el último partido tiene más de 30 días.

## Animación de la camiseta

`camiseta-giro.webp` sale de los cuadros 0-409 del video promocional del club (720×1280, 25 fps), escalados al 70 % y recortados en x=98, y=155, con un tamaño de 308×538. La máscara se rehízo con mediana temporal más refinado por color para evitar parpadeos. Los scripts de ese proceso no quedaron en el repositorio, y el video está ignorado por git (`/*.mp4`). No la regeneres salvo que el usuario lo pida.

## Probar en local

```
python -m http.server 8123 --directory public
```

Luego abre http://localhost:8123. Revísala en escritorio y en celular (375 px de ancho): el menú superior tiene que caber sin desbordarse.

## Convenciones

- Textos de la web, commits y respuestas en español de Chile.
- No agregues dependencias, frameworks ni pasos de build.
- No subas videos ni JPG originales (están en `.gitignore`).
