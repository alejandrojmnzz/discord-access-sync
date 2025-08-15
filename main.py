from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

import sqlite3

connection = sqlite3.connect("academy.db")
cur = connection.cursor()

def createDB():
    connection = sqlite3.connect("academy.db")

def createInvoiceTable():
    connection = sqlite3.connect("academy.db")
    cur.execute(
        """
        CREATE TABLE Invoice(
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        status TEXT NOT NULL, 
        paid_at DATE NULLABLE,
        due_date DATE NOT NULL,
        FOREIGN KEY (status) REFERENCES InvoiceStatus(status)

        )
        """
        )

def createUserTable():
    connection = sqlite3.connect("academy.db")
    cur.execute(
        """
        CREATE TABLE User(
        id INT PRIMARY KEY,
        email TEXT NOT NULL,
        first_name TEXT NOT NULL, 
        last_name TEXT NOT NULL,
        discord_user_id TEXT DATE NOT NULL

        )
        """
        )
def createProfileTable():
    connection = sqlite3.connect("academy.db")
    cur.execute(
        """
        CREATE TABLE ProfileAcademy(
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        academy_id INT NOT NULL, 
        FOREIGN KEY (user_id) REFERENCES User(id)
        )
        """
        )

        
def deleteTable():
    cur.execute("DROP TABLE Invoice")

def insertUserRow():
    cur.execute("""INSERT INTO User VALUES 
    (1, 'alejandro@gmail.com', 'Alejandro', 'Jiménez', 1379943138247839985),
    (2, 'miguel@gmail.com', 'Miguel', 'Gonzáles', 1390720076671357112),
    (3, 'javier@gmail.com', 'Javier', 'García', 1350129598943465513)
    """)
    connection.commit() 

def insertProfileRow():
    cur.execute("""INSERT INTO ProfileAcademy VALUES
    (1, 1, 30), (2, 2, 42), (3, 3, 42)
    """)
    connection.commit() 


def insertCohortRow():
    cur.execute("""INSERT INTO CohortUser VALUES 
    (1, 1, 36, 'postponed', 'financial_hold'),
    (2, 2, 48, 'higher_education', 'income_statement'),
    (3, 3, 23, 'secondary', 'balance_sheet')
    """)
    connection.commit() 

def insertSubscriptionRow():
    cur.execute("""INSERT INTO Subscription VALUES 
    (1, 1, 'canceled'),
    (2, 2, 'active'),
    (3, 3, 'past_due')
    """)
    connection.commit() 

def insertInvoiceRow():
    cur.execute("""INSERT INTO Invoice VALUES 
    (1, 1, 'uncollectible', null, '2025-07-30'),
    (2, 2, 'paid', '2025-07-12', '2025-07-30'), (3, 2, 'paid', '2025-08-04', '2025-08-30'), 
    (4, 3, 'paid', '2025-08-04', '2025-08-20'), (5, 3, 'open', null, '2025-08-13')
    """)
    connection.commit() 



# cur.execute("DROP TABLE SubscriptionStatus")
res = cur.execute("SELECT discord_user_id FROM User")


all_discord_ids = res.fetchall()


for id in all_discord_ids:
    print(id[0])


load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("ready to go")
    # role = discord.utils.get(discord.guild.roles, id=1)
    for guild in bot.guilds:
        for member in guild.members:
            if member.bot == False:
                pass
                # member_role = discord.utils.get(guild.roles, name="Member")
                # await member.add_roles(member_role)
            
    res = cur.execute(f'''SELECT user.discord_user_id, user.first_name, sub.status AS sub_status, invoice.status AS invoice_status, invoice.due_date FROM User AS user
    INNER JOIN ProfileAcademy AS profile ON user.id = profile.user_id
    INNER JOIN CohortUser AS cohort ON profile.user_id = cohort.user_id
    INNER JOIN Subscription AS sub ON cohort.user_id = sub.user_id
    INNER JOIN Invoice AS invoice ON sub.user_id = invoice.user_id


    WHERE academy_id = {os.getenv("ACADEMY_ID")} AND
    (educational_status != 'postponed' OR educational_status != 'dropped' OR educational_status != 'graduated_blocked') AND
    (financial_status != 'financial_hold' OR financial_status != 'collections')
    ''')

    users_info = []

    for user in res.fetchall():
        user_info = {}
        index = 0
        for key in res.description:
            user_info[key[0]] = user[index]
            index += 1
        users_info.append(user_info)

   

    for user in users_info:
        print(user)
        if user["sub_status"] == "active" or user["sub_status"] == "trialing":
            print(True)
        else:
            print(False)


bot.run(os.getenv("DISCORD_BOT_TOKEN"))
