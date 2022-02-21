from database import Base, SessionLocal, engine
import models

db = SessionLocal()


# add anime
def add_anime(anime_id, latest_episode, guild_id):
    # check if anime is there
    anime = db.query(models.Anime).filter(models.Anime.anime_id == anime_id).first()
    if anime is None:
        anime = models.Anime(anime_id, latest_episode)
        db.add(anime)
        db.commit()
        guilds = anime.server_list
        guilds.append(guild_id)
        anime.server_list = guilds
        db.commit()
    else:
        guilds = anime.server_list
        if guild_id not in guilds:
            guilds.append(guild_id)
            anime.server_list = guilds
            db.commit()
