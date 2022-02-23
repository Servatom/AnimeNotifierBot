import discord
from discord.ext import commands
from functionality import datascrape, utils
from database import SessionLocal, engine
import models
class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send("lol")

    @commands.command(name='add')
    async def add(self, ctx, *args):
        if len(args) == 0:
            embed = discord.Embed(
                title="Error",
                description="Anime ID is invalid",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        anime_id = None
        try:
            print(args[0])
            anime_id = int(args[0])
            print("herE")
        except:
            embed = discord.Embed(
                title="Error",
                description="Anime ID is invalid",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        db = SessionLocal()
        id = anime_id
        data = datascrape.getAnime(id)
        print(data)
        guild = db.query(models.Server).filter(
            models.Server.guild_id == ctx.guild.id
        ).first()
        if guild is None:
            # send error
            # get channel 
            channel = ctx.channel
            channel_id = channel.id
            # add server in database
            server = models.Server(
                guild_id=ctx.guild.id,
                prefix="*",
                channel_id=channel_id,
            )
            db.add(server)
            db.commit()
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
        utils.addAnime(data['anime_id'], data['episode_number'],
                       ctx.guild.id, data["anime_name"])
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
