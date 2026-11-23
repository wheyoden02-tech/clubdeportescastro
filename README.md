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

4. Pulsa **Save and Deploy**. Abre la dirección pages.dev que aparezca al terminar. Desde tu celular, revisa la portada, reproduce y pausa el giro de la camiseta y toca Instagram y Facebook. Puedes compartir esta dirección con la persona del club para revisar la propuesta antes de conectar el .cl.

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

Los hitos se redactaron a partir del artículo de [Club Deportes Castro](https://es.wikipedia.org/wiki/Club_Deportes_Castro) entregado para este proyecto. Los perfiles sociales se identificaron en la grabación proporcionada. La foto, el escudo y la animación de la camiseta provienen del material compartido. La licencia de la tipografía Barlow Condensed está en public/assets/OFL.txt.

