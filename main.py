import asyncio
import discord
from discord.ext.commands import CommandNotFound, NoPrivateMessage, Bot, ExpectedClosingQuoteError
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.reactions = True
intents.members = True

if not os.path.exists("data/temp"):
    os.makedirs("data/temp")

bot = Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        pass
    elif isinstance(error, NoPrivateMessage):
        await ctx.send("Cannot run this command in DMs")
    elif isinstance(error, ExpectedClosingQuoteError):
        await ctx.send(f"Mismatching quotes, {str(error)}")
    elif hasattr(error, "original"):
        raise error.original
    else: raise error


# Load poll functionality

async def load_extensions():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())

