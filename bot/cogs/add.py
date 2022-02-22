import discord
from discord.ext import commands
from functionality import datascrape, utils


class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add')
    async def add(self, ctx, id):
        data = datascrape.getAnime(id)
        utils.addAnime(data['anime_id'], data['episode_number'], ctx.guild.id)
        anime_name = data['anime_name']
        embed = discord.Embed(
            title=f'{anime_name}', url='https://myanimelist.net/anime/{id}/', description=f'Adding {anime_name}', color=0x00ff00)
        embed.set_thumbnail(url=data['image_url'])
        embed.add_field(
            name='Episode', value=data['episode_name'], inline=False)
        embed.add_field(name='Episode Number',
                        value=data['episode_number'], inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Add(bot))
