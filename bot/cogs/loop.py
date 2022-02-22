from discord.ext import commands, tasks
import database as db
from functionality import datascrape
import models


class Loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        task = self.loop.start()

    @tasks.loop(seconds=60)
    async def loop(self):
        print('running loop')
        session = db.SessionLocal()
        animes = session.query(models.Anime).all()
        for anime in animes:
            print(anime.anime_id)
            data = datascrape.getAnime(anime.anime_id)
            if int(data['episode_number']) > anime.latest_episode:
                self.bot.dispatch('new_episode', data)
        session.close()


def setup(bot):
    bot.add_cog(Loop(bot))
