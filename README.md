# discord-access-sync

Aplicación que utiliza discord.py y SQLite para agregar y eliminar roles a usuarios que no cumplan los requisitos para ser miembro en el servidor de Discord de la academia. Los usuarios en la base de datos están manualmente agregados para que coincidan con los del servidor de Discord.

**Cómo ejecutar la aplicación**

La aplicación se ejecuta, valida y asigna roles con un solo comando.

Primero, instala las dependencias necesarias:
`pip install discord.py dotenv`.

Corre la aplicacion con
`python main.py`.

**Variables de entorno**

Dentro del archivo `.env.example` se encuentran todas las variables de entorno necesarias.  

`DISCORD_BOT_TOKEN` hace referencia al ID del bot dentro del servidor que se utilizará.  

`GUILD_ID` es el ID del servidor de Discord desde el que el bot funcionará. Para efectos prácticos, uitlizar el servidor de prueba "Academy Server" en el que se encuentra el bot, cuyo ID es 1386815148777406588.  

`ROLE_ID` es el ID del rol que se le quiere asignar o eliminar a los usuarios. El servidor de prueba ya tiene un rol "Member" creado, su ID es 1405645722396917812.  

`ACADEMY_ID` es el ID de la academia a la que el usuario debe pertenecer para mantener su rol de miembro. Los usuarios ya registrados en la base de datos tienen un ID de 42, así que para efectos prácticos colocar ese.  

`GRACE_DAYS` son los días adicionales que se le quiere dar al usuario para renovar su pago después de la fecha de expiración, una vez acabados se le eliminará el rol.  

`DRY_RUN` refiere a la intención de hacer una run de prueba en el código. Si se declara como "true" , se ejecuta la aplicación a manera de test, consultando los usuarios en la base de datos pero sin realizar las acciones de agregar y eliminar sus roles en Discord, solo se imprime un mensaje simulando la acción. Si se declara como "false", la aplicación se ejecuta como normalmente lo haría.
