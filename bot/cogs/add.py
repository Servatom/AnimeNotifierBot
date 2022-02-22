import discord
from discord.ext import commands
from functionality import datascrape, utils


class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send("lol")
    @commands.command(name='add')
    async def add(self, ctx, id):
        data = datascrape.getAnime(id)
        if data is None:
            # anime id is invalid
            embed = discord.Embed(
                title="Error",
                description="Anime ID is invalid",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        # data is valid
        utils.addAnime(data['anime_id'], data['episode_number'], ctx.guild.id, data["anime_name"])
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
