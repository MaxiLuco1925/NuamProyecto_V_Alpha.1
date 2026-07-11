# Azure Cosmos DB: sesiones y auditoría

La aplicación guarda una copia de cada inicio de sesión exitoso en el contenedor `sesiones` y los eventos de autenticación en `auditoria_seguridad`.

1. En Azure Portal, cree una cuenta **Azure Cosmos DB for NoSQL** y una base de datos llamada `nuam`.
2. Cree los contenedores `sesiones` y `auditoria_seguridad`, ambos con clave de partición `/documento`.
3. Copie la *Primary connection string* de **Keys** a `COSMOS_DB_CONNECTION_STRING` en el archivo `.env` del servidor y configure `COSMOS_DB_ENABLED=True`.
4. Instale las dependencias con `pip install -r requirements.txt` y reinicie la aplicación.

Para desarrollo se puede usar `COSMOS_AUTO_CREATE_CONTAINERS=True`; la identidad usada debe tener permisos de creación. Manténgalo en `False` en producción.

El acceso de usuarios no se bloquea si Cosmos DB no está disponible: el error se registra en el log de Django y la autenticación continúa.
