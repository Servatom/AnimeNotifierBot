from discord.ext import commands, tasks
from database import SessionLocal, engine
from functionality import datascrape
import models
import discord

class Scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        task = self.loop.start()

    @tasks.loop(seconds=60)
    async def loop(self):
        print('running loop')
        db = SessionLocal()
        animes = db.query(models.Anime).all()
        for anime in animes:
            # get anime data
            data = datascrape.getAnime(anime.anime_id)
            if data is None:
                continue
            # check if latest episode is new
            if anime.latest_episode == data['episode_number']:
                continue
            # update latest episode
            anime.latest_episode = data['episode_number']
            db.commit()
            # send message to server
            guilds = list(anime.server_list)
            for guild_id in guilds:
                guild = db.query(models.Server).filter(
                    models.Server.guild_id == guild_id).first()
                embed = discord.Embed(
                        title=f'{anime.anime_name}',
                        url='https://myanimelist.net/anime/{id}/',
                        description=f'New episode of {anime.anime_name} is now airing!',
                        color=0x00ff00
                    )
                embed.set_thumbnail(url=data['image_url'])
                try:
                    channel = self.bot.fetch_channel(guild.channel_id)
                    await channel.send(embed=embed)
                except:
                    print("Could not send message to channel")
                    continue
        db.close()

def setup(bot):
    bot.add_cog(Scraper(bot))
