# Club Deportes Castro

Portal estático para deportescastro.cl. La carpeta public contiene la página y todos sus recursos. Puedes abrir public/index.html directamente en Chrome o Edge.

## 1. Subir la versión preparada a GitHub

Abre PowerShell en la carpeta del proyecto y ejecuta el siguiente comando. La rama main ya tiene configurado el repositorio de destino. Si GitHub abre una ventana de acceso, usa una cuenta con permiso de escritura en ese repositorio.

~~~powershell
git push -u origin main
~~~

En [GitHub](https://github.com/wheyoden02-tech/clubdeportescastro), comprueba que ves public/index.html y public/assets en main. Las grabaciones y los JPG originales quedan en tu computador.

## 2. Probar primero en Cloudflare Pages

1. En tu cuenta de Cloudflare, abre **Workers & Pages** y elige **Create application**. Selecciona **Pages** y la opción de importar o conectar un repositorio Git.
2. Conecta GitHub y concede acceso al repositorio **wheyoden02-tech/clubdeportescastro**. Selecciónalo para crear el proyecto.
3. Usa estos valores.

| Campo | Valor |
| --- | --- |
| Nombre del proyecto | deportescastro, si está disponible |
| Rama de producción | main |
| Framework preset | None |
| Build command | Dejar vacío |
| Build output directory | public |
| Root directory | Dejar el valor predeterminado |
| Variables de entorno | Ninguna |

4. Pulsa **Save and Deploy**. Abre la dirección pages.dev que aparezca al terminar. Desde tu celular, revisa la portada, comprueba que la camiseta gira continuamente y toca Instagram y Facebook. Puedes compartir esta dirección con la persona del club para revisar la propuesta antes de conectar el .cl.

[Guía de integración de Git de Cloudflare](https://developers.cloudflare.com/pages/get-started/git-integration/)

## 3. Conectar deportescastro.cl desde NIC Chile

1. En la misma cuenta de Cloudflare que contiene Pages, abre la sección de dominios. Agrega **deportescastro.cl** y selecciona el plan **Free**. Si el dominio ya figura como activo en esa cuenta, pasa directamente al punto 5.
2. Revisa los registros DNS que Cloudflare haya importado. Si se usa correo con el dominio, coteja sus registros MX y TXT, incluidos SPF, DKIM y DMARC, con el proveedor actual. Copia también los subdominios y registros de verificación que deban seguir funcionando. Si el proveedor anterior tiene DNSSEC activo, retira su registro DS en NIC y espera a que deje de aparecer en el DNS público antes del cambio de servidores.
3. Copia los **dos servidores de nombres que Cloudflare asigne a este dominio**. En [NIC Chile](https://www.nic.cl/), entra a tu cuenta, selecciona **deportescastro.cl** y abre **Modificar dominio**. En la configuración técnica, elige **Servidores DNS**, reemplaza la delegación anterior por los dos nombres asignados y guarda. El dominio sigue registrado y se renueva en NIC Chile.
4. Regresa a Cloudflare y espera a que la zona aparezca **Active**. La propagación depende de las cachés DNS.
5. Abre **Workers & Pages → tu proyecto → Custom domains → Set up a custom domain**. Escribe **deportescastro.cl** y confirma el registro DNS que propone Pages. Si aparece un conflicto con un registro anterior, identifica primero qué servicio utiliza ese registro.
6. Si también quieres que abra con www, repite el punto 5 para **www.deportescastro.cl**. Espera que el dominio y su certificado aparezcan activos y abre **https://deportescastro.cl** desde el celular. Si configuraste www o usas correo en el dominio, prueba ambos servicios también.

[Dominios personalizados en Pages](https://developers.cloudflare.com/pages/configuration/custom-domains/) · [Modificar un dominio en NIC Chile](https://www.nic.cl/ayuda/faq/mod-02.html)

## Cambios posteriores

Edita public/index.html para cambiar textos, enlaces y diseño (los estilos van dentro de la misma página, en la etiqueta style, para que cargue más rápido) y public/assets para el material visual. Cada push a main activa una nueva publicación en Cloudflare. El sitio quedó publicado como Worker de archivos estáticos (proyecto **clubdeportescastro**). wrangler.jsonc indica ese nombre y hace que cualquier dirección que no exista muestre public/404.html; no cambies el nombre que aparece ahí.

### Partidos y plantilla (automático)

Dos veces al día, GitHub ejecuta scripts/actualizar_datos_liga.py. El script lee la [ficha pública del club en la LNB](https://lnbchile.com/liga/uno/equipos/17) y actualiza public/datos/liga.js con los últimos 5 partidos, el récord y la lista de jugadores. Si hay cambios, los guarda y Cloudflare los publica. No hay que hacer nada.

- La liga entrega los nombres abreviados ("ALVAREZ, N."). En **public/datos/plantilla.js** se pueden agregar, de forma opcional, el nombre completo y la posición de cada jugador, además del entrenador, que la liga no publica. Un jugador sin esos datos se muestra igual, como "N. Alvarez". Para hacer este cambio con un agente de IA, basta con pedírselo: las instrucciones están en AGENTS.md.
- Si al empezar una temporada la ficha viene vacía, la web conserva los datos anteriores.
- Si la liga rediseña su página y el lector deja de entenderla, no se modifica nada y GitHub envía un correo avisando del error.
- GitHub pausa las tareas programadas de un repositorio que pasa 60 días sin cambios. Para evitarlo, la misma tarea deja un commit vacío cuando pasan 40 días sin ninguno, así que sigue activa sola entre temporadas.
- **Avisos por correo:** el robot comenta en el issue **Bitácora del robot de datos** del repositorio y te menciona, así que GitHub te envía cada aviso al correo de tu cuenta. Avisa cuando hay datos nuevos (por ejemplo "Nuevo partido: Castro ganó 87-76 contra Las Ánimas"), cuando empieza una temporada, en una revisión periódica fuera de temporada ("el robot sigue funcionando") y si algo falla. Para confirmar a qué correo llegan, revisa en GitHub **Settings → Notifications** que esté activado el correo para "Participating, @mentions and custom".
- La ficha pública solo trae partidos ya jugados. Para mostrar el próximo partido, el club debe pedir a la LNB acceso oficial a su calendario (API o widget).

Configuración, ya hecha: en **Settings → Actions → General → Workflow permissions** está activado **Read and write permissions**. Para forzar una actualización, entra a **Actions → Actualizar datos de la liga → Run workflow**.

### Google Search Console

El sitio ya incluye robots.txt, sitemap.xml, la dirección canónica, datos estructurados del club para Google, una imagen para compartir en redes y una página 404. El robot actualiza la fecha del sitemap cada vez que cambian los partidos o la plantilla.

1. Entra a [Google Search Console](https://search.google.com/search-console) con la cuenta de Google que administrará el sitio y pulsa **Agregar propiedad**.
2. Elige **Dominio** y escribe deportescastro.cl.
3. Google pedirá verificar con un registro TXT en el DNS. Como el dominio está en Cloudflare, Google suele ofrecer un botón para hacerlo automáticamente: acepta y autoriza en Cloudflare. Si no aparece, copia el registro TXT y, en Cloudflare, abre **DNS → Records → Add record**, tipo **TXT**, nombre **@**, pega el valor y guarda. Vuelve a Search Console y pulsa **Verificar**.
4. En el menú **Sitemaps**, escribe https://deportescastro.cl/sitemap.xml y pulsa **Enviar**.
5. En **Inspección de URLs**, revisa https://deportescastro.cl/ y pulsa **Solicitar indexación**.

Google tarda desde unos días hasta un par de semanas en mostrar la página en los resultados.

Los hitos se redactaron a partir del artículo de [Club Deportes Castro](https://es.wikipedia.org/wiki/Club_Deportes_Castro) entregado para este proyecto. Los perfiles sociales se identificaron en la grabación proporcionada. La foto, el escudo y la animación de la camiseta provienen del material compartido. Las licencias de DM Sans y Archivo Narrow están en public/assets.

