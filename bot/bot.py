import discord
from discord.ext import commands
from database import SessionLocal, engine
import models
import os

bot = commands.Bot(command_prefix='!')
models.Base.create_all(bind=engine)
db = SessionLocal()


def getToken():
    return os.environ.get('TOKEN')


cogs = []


def load_cogs():
    for cog in cogs:
        bot.load_extension(cog)


if __name__ == '__main__':
    load_cogs()
    bot.run(getToken())
