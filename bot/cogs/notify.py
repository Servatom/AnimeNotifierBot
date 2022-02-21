from discord.ext import commands
import discord


class Notify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener
    async def on_new_episode(self, data):
        embed = discord.Embed(title='New Episode',
                              description='New Episode', color=0x00ff00)
