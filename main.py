from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from datetime import datetime, date, timedelta
from database import cur

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def add_role(guild, member_id, dry_run='false'):
    if guild:
        member = guild.get_member(member_id)
        if member and member.bot == False:
            member_role = discord.utils.get(guild.roles, id=int(os.getenv("ROLE_ID")))
            if member_role:
                if dry_run != 'true':
                    return member.add_roles(member_role)
                else:
                    print(f'[DRY RUN] Added role with ID {os.getenv('ROLE_ID')} to member {member.name}')
            else:
                print(f'Role with ID {os.getenv('ROLE_ID')} was not found')
        elif not member:
            print(f'User with ID {member_id} was not found')
    else:
        print("Servidor no encontrado")
        return
                
async def remove_role(guild, member_id, dry_run=False):
    if guild:
        member = guild.get_member(member_id)
        if member and member.bot == False:
            member_role = discord.utils.get(guild.roles, id=int(os.getenv("ROLE_ID")))
            if member_role:
                if dry_run != 'true':
                    return member.remove_roles(member_role)
                else:
                    print(f'[DRY RUN] Removed role with ID {os.getenv('ROLE_ID')} from member {member.name}')
            else:
                print(f'Role with ID {os.getenv('ROLE_ID')} was not found')
        elif not member:
            print(f'User with ID {member_id} was not found')
    else:
        print("Servidor no encontrado")
        return
@bot.event
async def on_ready():
    print("ready to go")
    
    guild = bot.get_guild(int(os.getenv("GUILD_ID")))

    res = cur.execute(f'''SELECT user.discord_user_id, user.first_name, sub.status AS sub_status FROM User AS user
    INNER JOIN ProfileAcademy AS profile ON user.id = profile.user_id
    INNER JOIN CohortUser AS cohort ON profile.user_id = cohort.user_id
    INNER JOIN Subscription AS sub ON cohort.user_id = sub.user_id
    WHERE academy_id = {os.getenv("ACADEMY_ID")} AND
    (educational_status != 'postponed' OR educational_status != 'dropped' OR educational_status != 'graduated_blocked') AND
    (financial_status != 'financial_hold' OR financial_status != 'collections')
    ''')

    users_info = []

    for user in res.fetchall():
        user_info = {}
        for i in range(len(res.description)):
            user_info[res.description[i][0]] = user[i]
        users_info.append(user_info)
   
    for user in users_info:
        if user["sub_status"] == "active" or user["sub_status"] == "trialing":
            await add_role(guild, int(user['discord_user_id']), os.getenv('DRY_RUN'))

        elif user["sub_status"] == "past_due":
            res = cur.execute(f'''SELECT user.discord_user_id, invoice.status AS invoice_status, invoice.paid_at, invoice.due_date FROM User AS user
            INNER JOIN Invoice AS invoice ON user.id = invoice.user_id
            WHERE user.discord_user_id = {user["discord_user_id"]}
            ''')

            invoices = []

            for user_invoice in res.fetchall():
                invoices.append({"id": user_invoice[0], "due_date": user_invoice[3], "invoice_status": user_invoice[1]})

            most_recent_invoice = max(invoices, key=lambda item: datetime.fromisoformat(item["due_date"]))
            date_most_recent_invoice = datetime.strptime(most_recent_invoice["due_date"], '%Y-%m-%d').date()
            expiring_day = date_most_recent_invoice + timedelta(days=int(os.getenv("GRACE_DAYS")))

            if date.today() > date_most_recent_invoice and most_recent_invoice["invoice_status"] != "paid" and expiring_day > date.today():
                await add_role(guild, int(user['discord_user_id']), os.getenv('DRY_RUN'))

            elif date.today() > date_most_recent_invoice and most_recent_invoice["invoice_status"] != "paid" and expiring_day < date.today():
                await remove_role(guild, int(user['discord_user_id']), os.getenv('DRY_RUN'))

    res = cur.execute(f'''SELECT user.discord_user_id, user.first_name FROM User AS user
    INNER JOIN CohortUser AS cohort ON user.id = cohort.user_id
    WHERE (educational_status == 'postponed' OR educational_status == 'dropped' OR educational_status == 'graduated_blocked') OR
    (financial_status == 'financial_hold' OR financial_status == 'collections') OR
    cohort.cohort_id == null
    ''')

    for user in res.fetchall():
        await remove_role(guild, int(user[0]), os.getenv('DRY_RUN'))

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
