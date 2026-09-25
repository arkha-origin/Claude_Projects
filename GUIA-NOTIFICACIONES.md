# Guía: activar las notificaciones por correo y WhatsApp

El sistema ya sabe **qué** avisar y a **quién**. Solo falta conectarle un buzón de correo y un número de WhatsApp. Todo se configura en el servidor, en el archivo `/opt/cosplay-inc/.env`.

> **Importante:** las claves y contraseñas se escriben **solo** en ese archivo del servidor. Nunca las pegues en el chat, en GitHub ni en un documento compartido.

---

## Paso 1 · El correo (unos 20 minutos)

### 1.1 Crea un buzón para enviar
Crea un buzón del dominio, por ejemplo `notificaciones@cosplay-inc.com`, en el proveedor donde tengan el dominio (Google Workspace, Zoho, el hosting…).

- Si es **Google Workspace o Gmail**: activa la verificación en dos pasos en esa cuenta y crea una **contraseña de aplicación** (Cuenta de Google → Seguridad → Contraseñas de aplicaciones). Esa es la contraseña que se usa, no la normal.
- Si es **Zoho** u otro proveedor: busca en su ayuda "datos SMTP" y anota servidor, puerto, usuario y contraseña.

### 1.2 Decide a dónde llegan los avisos del equipo
Es el correo donde ustedes quieren recibir las cotizaciones y las selecciones de fotos de los clientes (puede ser el mismo buzón u otro, por ejemplo `equipo@cosplay-inc.com`).

### 1.3 Escríbelo en el servidor
Entra al servidor, abre `/opt/cosplay-inc/.env` y agrega estas líneas, con tus datos en lugar de los ejemplos:

```
SMTP_HOST=smtp.gmail.com             # o el servidor de tu proveedor
SMTP_PORT=465                        # 465 (SSL) o 587
SMTP_USER=notificaciones@cosplay-inc.com
SMTP_PASSWORD=                       # la contraseña de aplicación, aquí y solo aquí
CORREO_REMITENTE=Cosplay Inc <notificaciones@cosplay-inc.com>
CORREO_EQUIPO=equipo@cosplay-inc.com # a dónde llegan los avisos para ustedes
```

### 1.4 Para que no caiga en spam
En el panel DNS del dominio, revisen que existan los registros **SPF**, **DKIM** y **DMARC** del proveedor de correo (el proveedor da los valores exactos para copiar). Sin ellos, los correos a clientes suelen irse a spam.

### 1.5 Reinicia y comprueba
1. En GitHub: **Actions → Desplegar → Run workflow** (así la app vuelve a leer el `.env`).
2. En la plataforma: **Administración → Mensajes**. "Correo" debe aparecer como **activo**.
3. Prueba de verdad: manda una solicitud desde `/sesionpersonalizada`. Debe llegarte el aviso a `CORREO_EQUIPO` y la confirmación al correo que pusiste en el formulario.

---

## Paso 2 · WhatsApp (1 a 3 días, por las aprobaciones de Meta)

WhatsApp no deja que una empresa escriba primero con mensajes libres: exige la **API oficial de Meta** y **plantillas aprobadas**.

### 2.1 Cuenta y número
1. En **business.facebook.com**, entra con la cuenta comercial de Cosplay Inc. Si Meta lo pide, verifica el negocio.
2. En **developers.facebook.com → Mis apps**, crea una app de tipo **Empresa** y agrégale el producto **WhatsApp**.
3. En **WhatsApp → Configuración de la API**, agrega el número de la empresa.
   - Ojo: un número que hoy está en la app normal de WhatsApp (o en WhatsApp Business) hay que migrarlo o borrarlo de la app antes de usarlo en la API.
4. Copia el **Identificador del número de teléfono** (Phone number ID). No es el número: es un código largo.

### 2.2 Token permanente
El token de prueba vence en 24 horas; hace falta uno permanente:
1. **Configuración del negocio → Usuarios del sistema** → crea un usuario del sistema administrador.
2. Asígnale la app y la cuenta de WhatsApp.
3. **Generar token**, con los permisos `whatsapp_business_messaging` y `whatsapp_business_management`, sin vencimiento.

### 2.3 Plantillas (una por aviso al cliente)
En **WhatsApp Manager → Plantillas de mensajes**, crea estas plantillas en categoría **Utilidad**, en español. Las variables tienen que ir **en este orden exacto** (la pantalla Administración → Mensajes también lo muestra para copiar):

| Aviso | Cuándo sale | Variables en orden |
|---|---|---|
| Pago confirmado | Al confirmarse el pago de una reserva | {{1}} nombre · {{2}} evento · {{3}} código · {{4}} enlace |
| Galería lista | Cuando sus fotos ya están para elegir | {{1}} nombre · {{2}} enlace |
| Entrega lista | Cuando la foto final ya se puede descargar | {{1}} nombre · {{2}} enlace |
| Recordatorio de sesión | 30 y 15 minutos antes de su hora | {{1}} nombre · {{2}} minutos · {{3}} código |
| Turno llamado | Cuando le toca pasar al set | {{1}} nombre · {{2}} set · {{3}} código |
| Solicitud confirmada | Al pedir una sesión personalizada | {{1}} nombre · {{2}} código |

Meta tarda de minutos a 1–2 días en aprobarlas.

### 2.4 Escríbelo en el servidor
En `/opt/cosplay-inc/.env`:

```
WHATSAPP_TOKEN=                       # el token permanente, aquí y solo aquí
WHATSAPP_PHONE_ID=                    # el identificador del número
WHATSAPP_PLANTILLA_IDIOMA=es          # el MISMO idioma con que se aprobaron (es, es_CO…)
WHATSAPP_PLANTILLA_PAGO_CONFIRMADO=nombre_de_la_plantilla
WHATSAPP_PLANTILLA_GALERIA_LISTA=nombre_de_la_plantilla
WHATSAPP_PLANTILLA_ENTREGABLE_LISTO=nombre_de_la_plantilla
WHATSAPP_PLANTILLA_RECORDATORIO_SESION=nombre_de_la_plantilla
WHATSAPP_PLANTILLA_TURNO_LLAMADO=nombre_de_la_plantilla
WHATSAPP_PLANTILLA_SOLICITUD_CONFIRMADA=nombre_de_la_plantilla
```

### 2.5 Reinicia y comprueba
1. GitHub: **Actions → Desplegar → Run workflow**.
2. En el servidor, revisa todo contra Meta (no envía nada):
   ```
   cd /opt/cosplay-inc && npm run whatsapp:revisar
   ```
   Te dice si el token sirve, si el número es el correcto y si cada plantilla existe, está aprobada y tiene las variables correctas.
3. Prueba enviando un mensaje real a tu propio número:
   ```
   cd /opt/cosplay-inc && npm run whatsapp:revisar -- --probar 573001234567
   ```

---

## Qué le llega hoy a cada quien

**A los clientes** (por correo y WhatsApp, apenas conectes los dos canales):

- **Pago confirmado:** código de reserva y enlace.
- **Galería lista para elegir.**
- **Entrega lista para descargar.**
- **Recordatorio de sesión:** 30 y 15 minutos antes.
- **Turno llamado en el stand.**
- **Confirmación de su solicitud de sesión personalizada.**

**Al equipo** (al correo `CORREO_EQUIPO`, y además en el admin):

- **Nueva solicitud de sesión personalizada**, con el formulario completo.
- **Un cliente envió su selección de fotos**, con los nombres de archivo. También aparece en Fotos de clientes → Selecciones recibidas.

Los textos de todos estos mensajes se editan en **Administración → Textos**.

## Lo que falta decidir (dímelo y lo activo)

Hoy estas acciones **no** avisan a nadie por correo ni WhatsApp. Solo quedan registradas:

1. **Al equipo, cada venta nueva** (web o stand): "Nueva reserva de Fulano, $X".
2. **Al cliente, cuando crea la reserva** y todavía no ha pagado ("tu reserva está a la espera del pago").
3. **Al cliente, cuando envía su selección de fotos** ("recibimos tus fotos elegidas").
4. **Al cliente, si no se presentó** a su turno.
5. **Al equipo, cuando un cliente llega al stand** (check-in).

Para cada una: ¿se activa? ¿para el cliente, para el equipo o para ambos? Si se activa hacia el cliente por WhatsApp, también hará falta crear su plantilla en Meta (paso 2.3).
