import discord
from discord.ext import commands

class Add(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = 'add')
    def add(self,id):
        embed = discord.Embed(title = 'Add Anime', description = 'Adding ', color = 0x00ff00)

