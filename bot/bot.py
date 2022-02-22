from discord.ext import commands
import os
import models
from database import engine

bot = commands.Bot(command_prefix='*')


def getToken():
    return os.environ.get('TOKEN')


cogs = ['cogs.add', 'cogs.remove']


def load_cogs():
    for cog in cogs:
        bot.load_extension(cog)


@bot.event
async def on_ready():
    print('AnimeNotifier is connected to Discord!')

if __name__ == '__main__':
    models.Base.metadata.create_all(bind=engine)
    load_cogs()
    bot.run(getToken())
