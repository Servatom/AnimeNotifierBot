from discord.ext import commands
import discord
from functionality import utils


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setprefix')
    async def setprefix(self, ctx, prefix):
        utils.setPrefix(ctx.guild.id, prefix)
        await ctx.send(f'Prefix set to {prefix}')
