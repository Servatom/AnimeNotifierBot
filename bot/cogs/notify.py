from discord.ext import commands
import discord
import models
import database as db


class Notify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name='on_new_episode')
    async def on_new_episode(self, data):
        session = db.SessionLocal()
        anime_id = data['anime_id']
        anime = session.query(models.Anime).filter(
            models.Anime.anime_id == anime_id).first()
        guilds = list(anime.server_list)
        anime_name = data['anime_name']
        embed = discord.Embed(
            title=f'{anime_name}', url='https://myanimelist.net/anime/{id}/', description=f'New episode of {anime_name} is now airing!', color=0x00ff00)
        embed.set_thumbnail(url=data['image_url'])
        for guild_id in guilds:
            guild = session.query(models.Server).filter(
                models.Server.guild_id == guild_id).first()
            print(guild.guild_id, guild.channel_id)
            try:
                channel = self.bot.fetch_channel(guild.channel_id)
                await channel.send(embed=embed)
            except:
                print("Could not send message to channel")
                continue
        session.close()

def setup(bot):
    bot.add_cog(Notify(bot))
