# Guía para agentes de IA: web del Club Deportes Castro

Instrucciones para cualquier agente (Claude Code, Codex, Cursor u otro) que trabaje en este repositorio. El dueño del proyecto pide los cambios en español y en lenguaje cotidiano. Respóndele en español y sin tecnicismos.

## Qué es

Sitio estático para deportescastro.cl, el club de básquetbol de Castro, Chiloé. No hay build ni dependencias. La carpeta `public/` se publica tal cual en Cloudflare Pages, y cada push a `main` publica en uno o dos minutos.

| Archivo | Para qué sirve |
| --- | --- |
| `public/index.html` | Estructura y textos de la página |
| `public/estilos.css` | Diseño |
| `public/app.js` | Arma en el navegador las secciones de partidos y plantilla a partir de los archivos de datos |
| `public/datos/liga.js` | Últimos partidos, récord y lista de jugadores sacados de la LNB. **Lo genera un robot: no editar a mano** |
| `public/datos/plantilla.js` | Complementos manuales y opcionales: entrenador, más nombres completos y posiciones por jugador |
| `scripts/actualizar_datos_liga.py` | Robot que lee la ficha pública del club en la LNB y regenera `liga.js` |
| `.github/workflows/datos-liga.yml` | Ejecuta el robot en GitHub Actions dos veces al día |
| `public/assets/camiseta-giro.webp` | Animación recortada de la camiseta (410 cuadros) |

Los datos son archivos `.js` (`window.LIGA = {...}`, `window.PLANTILLA = {...}`) y no `.json` para que la página también funcione si se abre `public/index.html` directamente desde el disco.

## La plantilla se actualiza sola

La lista de jugadores (número y nombre) la trae el robot desde la LNB a `public/datos/liga.js`. La liga solo da nombres abreviados y sin tildes ("ALVAREZ, N."), sin posición y sin entrenador. Por eso existe `public/datos/plantilla.js`, que es **opcional** y sirve para mejorar cómo se ve:

```js
window.PLANTILLA = {
  entrenador: "Nombre del entrenador",
  nombres: {
    "416": { nombre: "Nicolás Álvarez Valenzuela", posicion: "Escolta" },
  },
};
```

- La clave (`"416"`) es el `id` del jugador en la LNB, que aparece en `liga.js`. No uses el número de camiseta, que puede repetirse o cambiar.
- Un jugador sin entrada en `nombres` se muestra igual, con formato "N. Alvarez". No es un error.
- Las entradas de jugadores que se fueron no molestan. Puedes dejarlas: si el jugador vuelve, recupera su nombre completo.
- `posicion` es opcional. Valores válidos: `Base`, `Escolta`, `Alero`, `Ala-pívot`, `Pívot` (abreviaturas habituales: B, E, A, AP, P). No la inventes.
- El título de la sección ("Plantilla 2027" o "Jugaron la temporada 2027") lo calcula `app.js` según la fecha del último partido. No se edita.

### Tarea frecuente: "salió la plantilla nueva" o "cambió el entrenador"

1. Si cambió el entrenador, actualiza `entrenador`. Si no se conoce, déjalo vacío (`""`) y la línea desaparece de la página.
2. Para completar nombres y posiciones, cruza la lista que pegue el usuario con los jugadores de `liga.js` (número y apellido) y agrega entradas en `nombres` con su `id`. Si un jugador de la lista del usuario todavía no está en `liga.js`, no lo agregues: aparecerá solo cuando la liga lo publique, normalmente al jugar su primer partido.
3. Coméntale al usuario los datos dudosos antes de publicar: números repetidos, nombres que difieren entre fuentes, o jugadores que figuran en una fuente y no en la otra. Si las fuentes se contradicen, no publiques el dato dudoso.
4. Comprueba que el archivo siga siendo válido: `node -e "global.window={};require('./public/datos/plantilla.js');console.log(Object.keys(window.PLANTILLA.nombres).length)"`, o abre la página.
5. Si el usuario lo pide, haz commit (mensaje en español, en imperativo, por ejemplo "Completar nombres de la plantilla 2027") y push a `main`.

### Fuentes y cuidados

- La fuente oficial es la ficha del club en la LNB: https://lnbchile.com/liga/uno/equipos/17. El robot ya la lee: muestra a todos los que jugaron la temporada, incluso si hubo cambios a mitad de año (por eso pueden repetirse números).
- El recuadro superior de Wikipedia ("Datos generales") suele estar desactualizado. Por ejemplo, en 2026 seguía mostrando a Damián Gamarra, que dirigió en 2022-2023. Dale prioridad a la tabla de plantilla (tiene fecha de actualización) y a la prensa reciente.
- El `robots.txt` de lnbchile.com bloquea a los bots de IA y la ruta `/api/` para todos. Los agentes de IA no deben leer lnbchile.com ni usar su API interna. Trabaja con lo que pegue el usuario o con otras fuentes. El robot de GitHub Actions sí puede leer la ficha pública, porque no es un agente de IA y no usa `/api/`.
- No redactes textos copiados de Wikipedia: reformúlalos.

## Robot de datos de la liga (automático)

- `.github/workflows/datos-liga.yml` ejecuta `scripts/actualizar_datos_liga.py` todos los días a las 10:00 y a las 04:30 UTC. También se puede lanzar a mano desde la pestaña Actions ("Run workflow").
- El script lee la ficha pública del club y extrae los últimos 5 partidos, el récord y la lista de jugadores. Reescribe `public/datos/liga.js` solo si algo cambió; en ese caso hace commit y Cloudflare Pages publica.
- Si la ficha viene sin partidos o sin jugadores (por ejemplo, al empezar una temporada), conserva los datos anteriores y no da error.
- Si la LNB rediseña su página y el script no la reconoce, termina con error sin tocar nada, y GitHub avisa por correo al dueño. En ese caso hay que ajustar las expresiones regulares de `extraer_partidos()`, `extraer_plantilla()` o `extraer_record()`. Para probar sin internet, guarda una copia del HTML de la ficha y ejecuta `python scripts/actualizar_datos_liga.py copia.html`.
- Los nombres de los rivales salen del diccionario `CODIGOS` del script. Si aparece un código desconocido (por ejemplo "XYZ"), se muestra tal cual: agrégalo al diccionario.
- La ficha pública no trae los próximos partidos. Para mostrarlos, el club tendría que conseguir acceso oficial con la LNB (secretaria@lnbchile.com). Si lo consiguen, la clave va como secreto de GitHub Actions, nunca dentro de `public/`.
- GitHub pausa las tareas programadas de repositorios públicos que pasan 60 días sin actividad. El último paso del workflow deja un commit vacío ("Mantener activa la actualización automática de datos de la liga") si pasan 40 días sin commits. No lo quites: el dueño no quiere tener que reactivar nada a mano.
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
- El pie de página incluye el crédito "Página diseñada por Sin Pausas", con enlace a https://sinpausas.cl. Es del autor del sitio: no lo quites.
