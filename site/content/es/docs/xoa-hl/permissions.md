---
title: "Administrar usuarios, grupos y permisos"
linkTitle: "Usuarios y permisos"
description: "Cree usuarios y grupos, conceda acceso a una VM, delegue recursos y pruebe el acceso LDAP o SAML."
weight: 70
translationKey: xoa-manual-permissions
translationStatus: draft
sourceRevision: sha256:7986e2d599b33c8226ca026293155fa3e4b8333a5816aa94d93ee28ffab32990
glossaryTerms: ["appliance", "vm", "host", "pool"]
---

Cree un usuario de prueba, dele acceso a una VM y pruebe después un grupo, un conjunto de recursos delegado y el acceso externo (LDAP o SAML). Trabaje como administrador en el **appliance XOA-HL** y acceda como usuario de prueba en una segunda sesión de navegador independiente. Use una VM de prueba desechable. Mantenga abierta la sesión de administrador durante todo el proceso. Nunca cambie la última cuenta administradora ni sus propios permisos durante las pruebas. Para añadir códigos de un solo uso al acceso de una cuenta local, consulte [Proteger el acceso con un código de un solo uso](/docs/xoa-hl/sign-in-otp/).

{{< callout type="info" >}}
**Se aplica a** la imagen `xoa-image-20261022-a280852`, paquete `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Basado en el código publicado; aún no probado en un laboratorio. En el plan de código abierto predeterminado de esta compilación, el código habilita las pantallas ACL y Self service: no hace falta una suscripción Vates.
{{< /callout >}}

## Conozca los dos tipos de roles {#roles}

**Settings → Users** (`/#/settings/users`) establece el permiso global de cada cuenta:

- **User** es una cuenta normal.
- **Admin** es un administrador. Omite todas las reglas de objetos.

Una regla de acceso (ACL) da a un usuario o grupo un rol sobre un objeto. El rol de objeto **Admin** no es el **Admin** global: solo se aplica al objeto seleccionado y su ámbito.

| Rol de objeto | Qué permite |
| --- | --- |
| Viewer | Ver |
| Operator | Ver y operar |
| Admin | Ver, operar y administrar |

Empiece con **Viewer** sobre una VM de prueba. Una regla de host o pool puede dar acceso a más objetos que una regla de una VM. Una regla de grupo se aplica a todos sus miembros. Los permisos se suman y no hay reglas de denegación. Quitar una regla no quita el acceso que procede de otro grupo, objeto u objeto padre.

## Dé acceso a una VM a un usuario de prueba {#vm-access}

Estos cuatro pasos forman una prueba: cree un usuario normal, concédale **Viewer** en una VM desechable, compruebe lo que puede hacer y quite el acceso.

### Cree un usuario de prueba {#create-a-test-user}

1. En **Settings → Users**, cree un usuario de prueba independiente con correo o identificador propio y contraseña única.
2. Seleccione **User**, no **Admin**. Compruebe el permiso mostrado por la cuenta.
3. En la segunda sesión, acceda con este usuario. Anote lo que ve antes de añadir reglas.

Compruebe que esta sesión es realmente la del usuario de prueba, no un acceso de administrador reutilizado. No use credenciales reales ni anote contraseñas. Conserve el usuario: la prueba de grupos posterior lo reutiliza.

### Conceda Viewer sobre una VM {#grant-viewer}

1. Como administrador, abra **Settings → ACLs** (`/#/settings/acls`).
2. Seleccione solo al usuario de prueba como sujeto, solo la VM desechable como objeto y **Viewer** como rol. Seleccione **Create**.
3. Compruebe sujeto, objeto y rol en la fila nueva.

No seleccione todos los objetos ni todo el pool. El formulario acepta varios sujetos y objetos y crea una regla por cada pareja. Compruebe las identidades, no nombres similares. Los filtros de objetos y etiquetas seleccionan objetos existentes ahora; no establecen reglas para objetos futuros.

### Compruebe qué puede hacer el usuario {#check-what-the-user-can-do}

1. En la sesión del usuario, actualice la página o acceda de nuevo.
2. Compruebe que la VM es visible y se pueden leer sus datos básicos.
3. Compruebe que no están disponibles las acciones de arranque, apagado y administración. Si aún puede solicitar una acción, debe rechazarse y la VM no debe cambiar.

Ejecute esta prueba solo sobre la VM desechable. Un botón oculto no demuestra por sí solo que el servidor rechace la acción.

Si una acción tiene éxito inesperadamente, deténgase. Como administrador, compruebe el permiso global, los grupos y cualquier otra regla sobre VM, host o pool. No amplíe permisos para corregir un error de acceso que no entiende. Si falta la página ACL, anote versiones y error y [comuníquelo](/docs/xoa-hl/troubleshooting/). No suponga que necesita un plan de pago de otra edición.

### Revoque y compruebe de nuevo {#revoke-and-check-again}

1. Como administrador, quite la regla de prueba exacta.
2. En la sesión del usuario, actualice o acceda otra vez. Compruebe que perdió el acceso a la VM.
3. Compruebe que su administrador sigue accediendo y administrando los objetos previstos.

Si persiste el acceso, busque otras reglas directas, de grupo y heredadas: quitar una fila no elimina todas las concesiones.

**Comprobación:** el usuario pudo leer la VM pero no modificarla, y perdió acceso al quitar la regla. Anote tipo de cuenta, ámbito de la regla y resultados esperados y reales, sin credenciales.

Conserve el usuario hasta terminar todas las pruebas de esta página. La delegación de tareas de copia y el ámbito de tokens API quedan fuera. Antes de cambios más amplios, consulte [Hosts y pools](/docs/xoa-hl/hosts-pools/) y [exporte su configuración](/docs/xoa-hl/configuration-backup/).

## Conceda acceso mediante grupos locales {#group-access}

Un grupo aplica sus reglas de objeto a todos sus miembros. Añadir un usuario a un grupo no cambia su permiso global.

**Antes de empezar**

- Termine [Dar acceso a una VM a un usuario de prueba](#vm-access). Su regla directa debe estar eliminada y no debe recibir acceso a la VM de otro grupo ni de un objeto padre.
- Use el mismo usuario normal y la misma VM desechable.
- Mantenga una segunda cuenta normal de prueba fuera del grupo para comparar.
- Mantenga abierta la sesión de administrador.

### Cree el grupo y su regla {#create-the-group-and-its-rule}

1. Abra **Settings → Groups** (`/#/settings/groups`). Introduzca un nombre distinto, como `lab-vm-viewers`, en **New group name** y seleccione **Create**.
2. Compruebe que el nuevo grupo no tiene usuarios. Si ya existe el nombre, elija otro: no reutilice un grupo desconocido con sus permisos.
3. En **Settings → ACLs**, seleccione solo este grupo como sujeto, la VM de prueba como objeto y **Viewer** como rol. Seleccione **Create** y compruebe grupo, VM y rol exactos en la fila nueva.
4. Compruebe que ambas cuentas normales siguen viendo solo lo anterior. Un grupo vacío no concede acceso.

### Añada el usuario y compruebe el acceso {#add-the-user-and-check-access}

1. En **Groups**, en **Add user** de este grupo, seleccione solo al usuario de prueba. El cambio se envía inmediatamente; no hay botón de guardado separado.
2. Expanda el recuento **Users** con el icono más y compruebe el identificador.
3. En **Settings → Users**, compruebe que los grupos del usuario incluyen este y que la cuenta sigue como **User**. Tras cualquier error, actualice ambas vistas: los dos registros de pertenencia se escriben por separado, por lo que no basta con que una lista parezca correcta.
4. En la sesión del miembro, actualice o acceda de nuevo. Compruebe que lee la VM y que arranque, apagado y administración están ausentes o se rechazan sin modificarla.
5. Compruebe que la segunda cuenta sigue sin acceso a la VM.

Si difieren los resultados, deténgase. Compruebe identidad real, permiso global, grupos y todas las reglas directas y de padres. No añada concesiones más amplias para superar la prueba.

### Quite al miembro {#remove-the-member}

1. En **Groups**, expanda los miembros y seleccione el icono de quitar junto al identificador exacto. La eliminación se envía inmediatamente, sin confirmación.
2. Compruebe que el identificador ha salido del grupo y que el grupo ha desaparecido de los datos del usuario.
3. En la sesión del antiguo miembro, actualice o acceda de nuevo. Compruebe que perdió el acceso a la VM por el grupo.

La regla del grupo permanece: cualquier otro miembro conserva el acceso.

### Compruebe que las concesiones se suman {#check-that-grants-add-up}

1. Vuelva a añadir al usuario y compruebe que recupera Viewer.
2. Añada una regla directa **Viewer** independiente para este usuario sobre la misma VM.
3. Quite solo la regla del grupo sobre la VM. El usuario aún puede leerla mediante la regla directa.
4. Quite la regla directa y compruebe otra vez. Sin otra concesión, el acceso desaparece aunque siga siendo miembro.

La ausencia de una regla de grupo no deniega nada y un **Admin** global omite todas las reglas de objeto.

### Limpie la prueba de grupos {#clean-up-the-group-test}

1. Quite las reglas de prueba mientras sus usuarios y grupos aún existen.
2. Quite las pertenencias de prueba y compruebe los resultados para ambas cuentas normales.
3. Compruebe fila y nombre del grupo de prueba vacío. Seleccione **Delete group** en esa fila y confirme. La confirmación no nombra el grupo: identifíquelo antes de abrirla.
4. Actualice Groups, ACLs y Users. Conserve el administrador independiente.

XO elimina en segundo plano las reglas y pertenencias de un grupo borrado. Que desaparezca el grupo no demuestra que se hayan eliminado todos sus registros. La tabla ACL puede ocultar filas cuyo sujeto ya no existe. Si falló una solicitud o los registros discrepan, deténgase. Anote identidades y errores sin secretos y [comunique la incoherencia](/docs/xoa-hl/troubleshooting/) antes de repetir o borrar algo más.

No se cubren grupos sincronizados desde proveedores de autenticación, grupos anidados, cambios de nombre ni delegación más amplia. Sus controles locales de nombre y miembros están restringidos. No use **Synchronize LDAP groups** ni desconecte un proveedor para eludir esos límites.

## Pruebe la cuota de un conjunto de recursos delegado {#resource-set-delegation}

Un conjunto de recursos permite a un usuario normal crear VM desde plantillas, SR y redes elegidos dentro de límites (cuotas) de CPU, RAM y disco. Aquí prueba un conjunto para un usuario sobre un pool desechable.

**Antes de empezar**

- Use solo un pool desechable y un usuario normal dedicado sin reglas amplias sobre el pool.
- Mantenga una sesión de administrador independiente y una copia independiente de todo lo que quiera conservar.
- No añada usuarios de producción ni comparta almacenamiento o redes de producción.
- Use dos sesiones: administrador XOA-HL y usuario normal en sesión separada.

### Cree el conjunto de recursos {#create-the-resource-set}

1. Como administrador, elija un pool desechable, una plantilla conocida detenida, un SR de prueba con escritura y espacio suficiente y una red de laboratorio aislada accesible por los hosts elegibles.
2. Anote sus UUID exactos y valores predeterminados de CPU, RAM y disco de la plantilla. Si sus discos o red no pueden ubicarse en esos recursos, deténgase.
3. Compruebe que el usuario es **User**, no **Admin** global, y aún no puede crear VM en este pool.
4. Abra **Self service → Resource sets** (`/#/self`) y seleccione **New**. Asigne un nombre de laboratorio único. Seleccione solo ese usuario y pool y después únicamente las **Templates**, **SRs** y **Networks** elegidas.
5. Compruebe la lista de hosts. El editor muestra elegibles y excluidos según acceso a SR y red. Al menos un host previsto debe ser elegible.
6. Establezca valores finitos en **Maximum CPUs**, **Maximum RAM** y **Maximum disk space**. Deben permitir una VM pequeña de la plantilla, pero quedar por debajo de la solicitud excesiva que probará después.
7. Deje **Share VMs by default** desactivado, no añada pool IP y seleccione **Save**. El editor crea el conjunto y después lo edita: tras un error de guardado, actualice y busque conjuntos vacíos o parciales antes de repetir.
8. Recargue el conjunto. Compruebe ID, usuario, plantillas, SR, redes, hosts y los tres límites. Anote el uso actual, normalmente cero.

Si la página muestra una petición de actualizar el plan o falta el conjunto, anote la versión y deténgase. No suponga que necesita un plan Vates ni omita la interfaz mediante una llamada API sin revisar.

### Compruebe la cuota {#check-the-quota}

1. En la sesión normal, abra **New VM** (`/#/vms/new`) y seleccione el conjunto exacto.
2. Solicite una VM que supere el límite de CPU. Mantenga válidos plantilla, SR, red, RAM y disco. El servidor debe rechazarla sin crear VM ni discos inesperados.
3. Como administrador, compruebe inventario y uso de cuota. Un control oculto no demuestra que se aplique el límite. Si hay VM o disco parcial, deténgase y enumérelos antes de limpiar.
4. Como usuario normal, solicite una VM dentro de todos los límites y usando solo los objetos seleccionados. Déjela detenida. Quite o desconecte VIF heredadas antes de arrancar de forma aislada.
5. Compruebe UUID de VM nueva, SR de discos, red, conjunto y valores **Used** y **Total** de cuota.
6. Compruebe que el usuario puede ver y administrar esta VM y que otra cuenta normal sin el conjunto no puede.

Nunca pruebe el límite con una VM de producción. Por defecto, XO da al creador el rol de objeto **Admin** sobre su VM. Activar **Share VMs by default** lo amplía a los usuarios del conjunto. El usuario de prueba no necesita una regla administradora sobre todo el pool.

**Comprobación:** la solicitud excesiva se rechazó sin restos y la VM dentro de límites figura en el uso de cuota.

### Quite al usuario del conjunto {#remove-the-user-from-the-set}

1. Como administrador, quite al usuario de prueba del conjunto. Actualice su sesión normal.
2. Compruebe que ya no puede seleccionar el conjunto ni crear otra VM mediante él.
3. Compruebe por separado las reglas directas o heredadas que quedan sobre la VM existente. Quitar al usuario elimina las reglas de VM del conjunto, pero otra concesión puede conservar el acceso.

Si acceso o uso no coinciden, deténgase y anote ID de conjunto y VM y el error sin secretos. No use **Recompute all limits** como reparación que no puede explicar.

### Limpie la prueba del conjunto {#clean-up-the-resource-set-test}

1. Detenga la VM nueva y confirme sus ID exactos de VM y VDI. Quite sus VIF.
2. Elimine **solo** esa VM desechable. Compruebe que discos e instantáneas se trataron como pretendía.
3. Actualice uso de cuota y recuento de VM del conjunto. Compruebe que no queda ninguna.
4. Seleccione **Delete resource set** en el conjunto exacto. Eliminarlo solo desvincula sus VM; no las borra.
5. Compruebe de nuevo usuario normal, administrador independiente e inventario del pool.

Anote ID esperados/reales, rechazos, cifras de cuota y limpieza, sin credenciales. Quedan fuera sujetos de grupo, pools IP, uso compartido por defecto, varias VM a la vez, limpieza tras creación fallida y delegación de producción.

## Pruebe el acceso externo LDAP {#ldap-sign-in}

Un acceso LDAP puede crear una cuenta XO o vincular una existente. Use un directorio desechable y una identidad de prueba dedicada sin administración.

{{< callout type="warning" >}}
Los valores predeterminados son `createUserOnFirstSignin = true` y `mergeProvidersUsers = true`. Por tanto, un usuario de directorio que coincida con uno local de XO puede vincularse a esa cuenta y borrar su contraseña local. Use un nombre de prueba que no coincida con **ninguna** cuenta XO existente.
{{< /callout >}}

**Antes de empezar**

- Mantenga una sesión local de administrador independiente y una vía de recuperación.
- Como administrador, anote versiones de imagen, paquete y XO y ajustes efectivos de autenticación. Conserve una [exportación de configuración](/docs/xoa-hl/configuration-backup/) privada.
- En **Settings → Plugins** (`/#/settings/plugins`), compruebe que aparece `auth-ldap` con versión. Anote su configuración y estados cargado y autocarga sin secretos. Si falta o ya sirve a usuarios reales, deténgase.
- Prepare con el responsable del directorio un destino LDAPS o StartTLS aislado con CA de confianza, atributo de ID único y estable, base y filtro de usuarios acotados e identidad dedicada de búsqueda si es necesaria.
- No cambie el último administrador local ni un proveedor existente para hacer funcionar esta prueba.

### Configure y cargue el complemento {#configure-and-load-the-plugin}

1. En una ventana autorizada de laboratorio, introduzca en el formulario solo los valores del responsable: URI, ruta CA, comprobación de certificado activada, elección StartTLS, base, filtro, atributo ID y credenciales de búsqueda.
2. Deje **Synchronize groups** sin configurar. Puede importar pertenencias y cambiar quién accede a qué.
3. Compruebe por separado identidad TLS y accesibilidad. Nunca desactive la verificación de certificado para ocultar un error.
4. Guarde la configuración. Cargue después el complemento y lea de nuevo sus estados cargado y autocarga. Cargarlo desde esta página también activa la autocarga.

Guardar por sí solo no demuestra que funcione el acceso. Mantenga los secretos fuera de capturas, registros e incidencias.

### Acceda una vez y compruebe la cuenta {#sign-in-once-and-check-the-account}

**No** use **Test** como comprobación inocua de conexión. Ejecuta el acceso real, que puede crear una cuenta XO y, si está configurado, sincronizar grupos.

1. En una sesión nueva e independiente, acceda una vez con la identidad de directorio única de prueba.
2. Desde la sesión administradora, compruebe el ID nuevo de usuario XO, proveedor, permiso global (**User**), grupos y visibilidad. Un acceso correcto no concede por sí solo acceso a objetos.
3. Dé a esta cuenta **Viewer** sobre una sola VM desechable, como en [Conceder Viewer sobre una VM](#grant-viewer). En su sesión, compruebe que puede leer y que operar/administrar están ausentes o se rechazan sin cambios.
4. Quite esa regla exacta. En una sesión actualizada, compruebe que perdió el acceso.
5. Pruebe una contraseña de directorio incorrecta sin revelarla. Compruebe que el administrador local independiente sigue accediendo.

Si se vincula una cuenta XO existente, aparece administración o grupos inesperados o no está claro el proveedor o resultado del certificado, deténgase, guarde pruebas saneadas y siga el plan del responsable. No vuelva a acceder ni amplíe permisos.

### Limpie la prueba LDAP {#clean-up-the-ldap-test}

1. Quite solo reglas y pertenencias de prueba. Cierre la sesión externa.
2. Descargue `auth-ldap` y lea de nuevo estados cargado y autocarga. El administrador local debe seguir funcionando.
3. Antes de borrar la cuenta, identifique usuario exacto, tokens y reglas. Borrar cuenta y purgar configuración del complemento son acciones separadas. Nunca purgue un proveedor que sirva a otros usuarios.

Si falla carga, acceso o descarga, guarde errores saneados y estados reales de usuario y proveedor antes de repetir. Nunca relaje TLS ni combine cuentas para evitar un fallo. Anote proveedor, versión, confianza TLS, asignación de identidad, ID de usuario/reglas anteriores y posteriores, resultados permitidos/rechazados y acceso local conservado. Quedan fuera sincronización de grupos, caídas del directorio, rotación de credenciales, cambios de identidad, tokens, OTP y conmutación.

## Pruebe el acceso externo SAML {#saml-sign-in}

Necesita una aplicación aislada de proveedor de identidad (IdP), una identidad de prueba sin administración y con nombre único y un administrador XO local independiente. El complemento toma el nombre de usuario XO del atributo de perfil indicado en `usernameField`.

{{< callout type="warning" >}}
Con los valores predeterminados de `createUserOnFirstSignin` y `mergeProvidersUsers`, un nombre que coincida con una cuenta XO existente puede vincularse a ella y borrar su contraseña local. Nunca pruebe con un nombre XO existente ni una aplicación de inicio de sesión único (SSO) de producción.
{{< /callout >}}

**Antes de empezar**

- Con el responsable del IdP, anote versiones de imagen, paquete, XO y complemento, ajustes de autenticación efectivos y dirección HTTPS pública. Conserve una [exportación privada de configuración](/docs/xoa-hl/configuration-backup/).
- Compruebe que `auth-saml` aparece en **Settings → Plugins** (`/#/settings/plugins`) y no sirve a usuarios reales.
- Acuerde un atributo de perfil único y estable para `usernameField`. Antes de cargar, compare su valor de prueba con **todos** los nombres de usuario XO.
- Mantenga una sesión administradora local funcional y una vía separada de recuperación por consola.
- Si dirección pública, proxy o asignación de cuentas no están claros, deténgase.

### Registre el appliance en el IdP {#register-the-appliance-with-the-idp}

1. Registre solo este proveedor de servicio de laboratorio en el IdP. Su URL de retorno debe coincidir con `https://<appliance-name>/signin/saml/callback`, accesible desde fuera. Compruebe nombre DNS exacto, confianza del certificado y redirección mediante cualquier proxy.
2. Obtenga el **certificado de firma**, punto de entrada y emisor acordado del IdP mediante el canal privado del responsable. No es el certificado HTTPS del appliance.
3. Exija respuesta o aserción SAML firmada según lo acordado. Los valores predeterminados `wantAssertionsSigned` y `wantAuthnResponseSigned` son ambos `false`, pero eso **no** hace aceptables los mensajes sin firma.

Revise estas opciones con el responsable. Nunca debilite comprobaciones de firma ni TLS para ocultar diferencias.

### Configure, cargue y acceda {#configure-load-and-sign-in}

1. Introduzca solo certificado, punto de entrada, emisor y campo de usuario del laboratorio y las opciones de retorno o rigor aprobadas por el responsable.
2. Guarde la configuración. Cargue el complemento y lea los estados cargado y autocarga. Guardarlo no lo activa; cargarlo desde esta página activa también la autocarga.
3. En una sesión nueva e independiente, inicie SAML desde la página de acceso XO. Autentíquese una vez con la identidad asignada.
4. Pida al responsable del IdP confirmar respuesta firmada y atributo elegido sin publicar la aserción.

Nunca pegue certificados, aserciones, datos de perfil ni tokens de sesión en incidencias públicas.

### Compruebe la cuenta nueva {#check-the-new-account}

1. Desde la sesión administradora, compruebe ID **nuevo** de usuario XO, proveedor `saml`, permiso global (**User**), grupos y visibilidad.
2. Dé **Viewer** sobre una sola VM desechable como en [Conceder Viewer sobre una VM](#grant-viewer). Compruebe lectura y una operación rechazada.
3. Quite la regla exacta. En sesión actualizada, compruebe que perdió acceso.
4. Pida al responsable del IdP rechazar una identidad de control de laboratorio no asignada en sesión nueva. Prueba un acceso nuevo, no revoca tokens XO existentes.
5. Compruebe que el administrador local sigue accediendo.

Si se vincula un usuario existente, aparece un rol privilegiado, falta el atributo o no está claro el resultado de firma o retorno, deténgase y conserve solo pruebas saneadas. Cuando falta el campo de usuario, el complemento registra el perfil completo: trate los registros de fallo como sensibles.

### Limpie la prueba SAML {#clean-up-the-saml-test}

1. Cierre la sesión SAML de prueba y quite sus reglas.
2. Descargue solo el complemento aislado `auth-saml`. Compruebe estados cargado y autocarga y acceso local.
3. Antes de borrar la cuenta, enumere el usuario exacto y sus tokens. Cerrar sesión o desactivar el proveedor no demuestra que los tokens XO existentes sean inválidos. Nunca purgue un proveedor que sirva a usuarios reales.

Ante un fallo, anote retorno y error redactados y estados reales de usuario, proveedor y tokens antes de repetir. Anote dirección de retorno, identidad y caducidad del certificado IdP, política de firma, atributo asignado, estado del complemento, ID anteriores/posteriores de usuario y reglas, resultados y acceso local conservado, sin secretos. Quedan fuera caídas del IdP, rotación de claves de firma, desfase horario, cambios de atributos, revocación de tokens/sesiones, OTP y federación de producción.

{{< details title="Fuentes" closed="true" >}}
- **Usuarios, ACL y plan de compilación**: [interfaz de usuarios](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/users/index.js), [interfaz ACL](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/acls/index.js), [plan de compilación predeterminado](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js), [roles y omisión del administrador global](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs), [herencia de permisos de objetos](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-acl-resolver/index.js), [script de compilación xoa-hl](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
- **Grupos**: [interfaz de grupos](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/groups/index.js), [API de grupos](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/group.mjs), [pertenencia y eliminación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [ACL combinadas de usuario y grupo](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/acls.mjs), [selector de sujetos](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-objects.js).
- **Conjuntos de recursos**: [editor de conjuntos y control de plan](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/self/index.js), [API de conjuntos de recursos](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/resource-set.mjs), [restricciones, cómputo de cuotas y eliminación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/resource-sets.mjs), [creación de VM y ACL](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [selección de conjunto en VM nueva](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js).
- **LDAP**: [esquema, TLS, prueba, registro y sincronización opcional de grupos](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server-auth-ldap/src/index.js), [página de complementos: configuración, carga y prueba](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/plugins/index.js), [registro de usuarios y colisiones de nombres](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [ajustes predeterminados de autenticación](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [espacios de compilación XOA-HL](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [contenido RPM](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec).
- **SAML**: [esquema del complemento, asignación de perfil y registro](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server-auth-saml/src/index.js), [retorno web, acceso y creación de tokens](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [página de carga de complementos](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/plugins/index.js), [comportamiento ante colisiones de usuarios](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [guía SAML de XO 5 original](https://docs.xen-orchestra.com/users-and-access/users#saml).
{{< /details >}}
