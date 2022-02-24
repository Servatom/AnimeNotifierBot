import discord
from discord.ext import commands
from functionality.datascrape import getAnimeName
from functionality import datascrape, utils
import models
from database import SessionLocal, engine


class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='remove <anime id>', description='Remove an anime')
    async def add(self, ctx, id):
        # check if anime id is in the db
        db = SessionLocal()
        anime = db.query(models.Anime).filter(
            models.Anime.anime_id == id).first()
        if anime is None:
            # anime id is invalid
            embed = discord.Embed(
                title="Error",
                description="Anime ID is invalid",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        else:
            server_list = list(anime.server_list)
            if ctx.guild.id in server_list:
                # remove guild from server_list
                server_list.remove(ctx.guild.id)
                anime.server_list = server_list
                db.commit()
                anime_name = getAnimeName(anime.anime_id)
                embed = discord.Embed(
                    title="Success!",
                    description=f'Removed {anime_name} from your list',
                    color=0x00ff00
                )
                await ctx.send(embed=embed)
            else:
                # client
                guild = db.query(models.Server).filter(
                    guild_id=ctx.guild.id
                ).first()
                prefix = guild.prefix
                await ctx.send("You are not subscribed to this anime please use ```{}add```".format(prefix))


def setup(bot):
    bot.add_cog(Remove(bot))
