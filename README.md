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

Edita public/index.html para cambiar textos y enlaces, public/estilos.css para el diseño y public/assets para el material visual. Cada push a main activa una nueva publicación en Pages una vez que esté conectado.

### Plantilla (una vez por temporada)

Toda la plantilla está en **public/datos/plantilla.js**. En GitHub, abre ese archivo, pulsa el lápiz (Edit), cambia los nombres, números, posiciones o el entrenador y guarda con **Commit changes**. Pages publica el cambio en uno o dos minutos. El archivo explica el formato en sus primeras líneas, y no hace falta tocar el diseño.

### Últimos partidos (automático)

**public/datos/resultados.js** se genera solo. Dos veces al día, GitHub ejecuta scripts/actualizar_resultados.py, que lee la [ficha pública del club en la LNB](https://lnbchile.com/liga/uno/equipos/17), y si hay partidos nuevos guarda el cambio y Pages lo publica. Para que funcione:

1. En GitHub, abre **Settings → Actions → General**. En **Workflow permissions** elige **Read and write permissions** y guarda.
2. En la pestaña **Actions**, abre **Actualizar resultados** y pulsa **Run workflow** para probarlo una vez.

Si la liga cambia su página y el lector deja de entenderla, el archivo no se modifica (la web sigue mostrando los últimos datos buenos) y GitHub envía un correo avisando del error. GitHub pausa las tareas programadas de un repositorio que pasa 60 días sin cambios. Para evitarlo, la misma tarea deja un commit vacío cuando pasan 40 días sin ninguno, así que sigue activa sola entre temporadas.

La ficha pública solo trae resultados ya jugados. Para mostrar el próximo partido, el club debe pedir a la LNB acceso oficial a su calendario (API o widget).

Los hitos se redactaron a partir del artículo de [Club Deportes Castro](https://es.wikipedia.org/wiki/Club_Deportes_Castro) entregado para este proyecto. Los perfiles sociales se identificaron en la grabación proporcionada. La foto, el escudo y la animación de la camiseta provienen del material compartido. Las licencias de DM Sans y Archivo Narrow están en public/assets.

