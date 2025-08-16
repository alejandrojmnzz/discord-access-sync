from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from datetime import datetime, date, timedelta

# Se importa de la base de datos un cursor que permite ejecutar comandos SQL para SQLite
from database import cur

# Se carga la librería dotenv para obtener las variables de entorno
load_dotenv()

# Se especifica que de la libreía discord.py, se va a hacer uso de intents y se da el permiso de manipular miembros
intents = discord.Intents.default()
intents.members = True

# Se configura el bot con los intents establecidos
bot = commands.Bot(command_prefix="!", intents=intents)

# Función global para agregar un rol a un miembro
async def add_role(guild, member_id, user_name, dry_run='false'):
    if guild:
        member = guild.get_member(member_id)
        if member and member.bot == False:
            # De la librería discord.py, se obtiene el rol especificado del guild (servidor) especificado
            member_role = discord.utils.get(guild.roles, id=int(os.getenv("ROLE_ID")))
            if member_role:
                # Si no se quiere hacer un dry run, se ejecuta el comando para agregar roles para el miembro con ID especificado (si el usuario ya tiene el rol se mantiene igual)
                if dry_run != 'true':
                    print(f'Added role with ID {os.getenv('ROLE_ID')} to member {member.name} ({user_name})')
                    return await member.add_roles(member_role)
                # Si se quiere hacer un dry run, solo se imprime la información del miembro al que se agregaría el miembro
                else:
                    print(f'[DRY RUN] Added role with ID {os.getenv('ROLE_ID')} to member {member.name} ({user_name})')
            else:
                print(f'Role with ID {os.getenv('ROLE_ID')} was not found')
        elif not member:
            print(f'User with ID {member_id} was not found')
    else:
        print("Servidor no encontrado")
        return

# Función global para eliminar un rol a un miembro
async def remove_role(guild, member_id, user_name, dry_run='false'):
    if guild:
        member = guild.get_member(member_id)
        if member and member.bot == False:
            member_role = discord.utils.get(guild.roles, id=int(os.getenv("ROLE_ID")))
            if member_role:
                if dry_run != 'true':
                    print(f'Removed role with ID {os.getenv('ROLE_ID')} from member {member.name} ({user_name})')
                    return await member.remove_roles(member_role)
                else:
                    print(f'[DRY RUN] Removed role with ID {os.getenv('ROLE_ID')} from member {member.name} ({user_name})')
            else:
                print(f'Role with ID {os.getenv('ROLE_ID')} was not found')
        elif not member:
            print(f'User with ID {member_id} was not found')
    else:
        print("Servidor no encontrado")
        return

# Se declara el evento de bot on_ready, el cual escucha al momento en que el bot está listo para usarse en el servidor de Discord
@bot.event
async def on_ready():
    print("ready to go")
    
    # Se busca el servidor de Discord especificado (el bot tiene que estar dentro del mismo)
    guild = bot.get_guild(int(os.getenv("GUILD_ID")))

    # Se ejecuta una consulta SQL a la base de datos SQLite
    # La consulta devuelve todos los usuarios que cumplan ciertas condiciones respecto a su estadod educativo y financiero, así como si tiene el ID de academia correcto
    # Se establece una relación de las tablas de perfil académico, cohorte del usuario y estado de suscripción con la tabla usuario, para obtener todos esos datos para cada usuario obtenido
    res = cur.execute(f'''SELECT user.discord_user_id, user.first_name, sub.status AS sub_status FROM User AS user
    INNER JOIN ProfileAcademy AS profile ON user.id = profile.user_id
    INNER JOIN CohortUser AS cohort ON profile.user_id = cohort.user_id
    INNER JOIN Subscription AS sub ON cohort.user_id = sub.user_id
    WHERE academy_id = {os.getenv("ACADEMY_ID")} AND
    (educational_status != 'postponed' OR educational_status != 'dropped' OR educational_status != 'graduated_blocked') AND
    (financial_status != 'financial_hold' OR financial_status != 'collections')
    ''')

    users_info = []

    # Con la respuesta de la consulta SQL, se crea una lista con cada dato de usuario para un procesamiento más eficiente de los mismos
    for user in res.fetchall():
        user_info = {}
        for i in range(len(res.description)):
            # res.description otorga una lista de tuplas cuyo primer elemento es el nombre de cada key
            # Se asigna ese nombre como una nueva key de un diccionario user_info y se iguala al valor de la key en el usuario iterado
            user_info[res.description[i][0]] = user[i]
        users_info.append(user_info)


    # Se itera en la lista de diccionarios creada y primero se comprueba si el estado de la suscripción del usuario está activo, y si es así se llama a la función global add_role()
    for user in users_info:
        if user["sub_status"] == "active" or user["sub_status"] == "trialing":
            await add_role(guild, int(user['discord_user_id']), user['first_name'], os.getenv('DRY_RUN'))

        elif user["sub_status"] == "past_due":

            # Si el estado en suscripción del usuario está vencido, se consulta en la base de datos información adicional sobre el mismo (sus facturas)
            res = cur.execute(f'''SELECT user.discord_user_id, invoice.status AS invoice_status, invoice.paid_at, invoice.due_date FROM User AS user
            INNER JOIN Invoice AS invoice ON user.id = invoice.user_id
            WHERE user.discord_user_id = {user["discord_user_id"]}
            ''')

            invoices = []

            # Se itera en la respuesta y se crea una lista para guardar eficientemente las facturas del usuario
            for user_invoice in res.fetchall():
                invoices.append({"id": user_invoice[0], "due_date": user_invoice[3], "invoice_status": user_invoice[1]})

            # Con esa información, se crean tres variables para almacenar la factura más reciente, su versión con solo el día de expiración convertido a formato "date" 
            # y el día de expiración según el de la última factura sumado a los días de gracia
            most_recent_invoice = max(invoices, key=lambda item: datetime.fromisoformat(item["due_date"]))
            most_recent_invoice_due_date = datetime.strptime(most_recent_invoice["due_date"], '%Y-%m-%d').date()
            expiring_day = most_recent_invoice_due_date + timedelta(days=int(os.getenv("GRACE_DAYS")))

            # Se verifica que el tiempo de pago junto a los días de gracia ya expiró, para saber si agregar/mantener el rol o eliminarlo
            if date.today() > most_recent_invoice_due_date and most_recent_invoice["invoice_status"]:
                if expiring_day > date.today():
                    await add_role(guild, int(user['discord_user_id']), user['first_name'], os.getenv('DRY_RUN'))
                elif expiring_day < date.today():
                    await remove_role(guild, int(user['discord_user_id']), user['first_name'], os.getenv('DRY_RUN'))

    # Se obtienen los usuarios que no cumplen con los estados necesarios en educativa o financialmente
    res = cur.execute(f'''SELECT user.discord_user_id, user.first_name FROM User AS user
    INNER JOIN CohortUser AS cohort ON user.id = cohort.user_id
    WHERE (educational_status == 'postponed' OR educational_status == 'dropped' OR educational_status == 'graduated_blocked') OR
    (financial_status == 'financial_hold' OR financial_status == 'collections') OR
    cohort.cohort_id == null
    ''')

    # Se itera en el resultado y se le elimina el rol a todos los usuarios (esta vez no es necesario almacenarlos en una lista debido a la simplicidad del procesamiento)
    for user in res.fetchall():
        await remove_role(guild, int(user[0]), user[1], os.getenv('DRY_RUN'))

# Se ejecuta el comando para activar el bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
