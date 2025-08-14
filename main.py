from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

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
            print(member.id)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
