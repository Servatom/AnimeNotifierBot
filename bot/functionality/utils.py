from database import Base, SessionLocal, engine
import models

# add anime


def addAnime(anime_id, latest_episode, guild_id, anime_name):
    # check if anime is there
    db = SessionLocal()
    anime = db.query(models.Anime).filter(
        models.Anime.anime_id == anime_id).first()
    if anime is None:
        # add anime
        anime = models.Anime(anime_id, latest_episode, guild_id, anime_name)
        db.add(anime)
        db.commit()
    else:
        # add guild
        guilds = list(anime.server_list)
        if guild_id not in guilds:
            # server_list append
            guilds.append(guild_id)
            anime.server_list = guilds
            db.commit()
        else:
            return
    db.close()
