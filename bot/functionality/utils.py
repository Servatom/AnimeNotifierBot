from database import Base, SessionLocal, engine
import models

db = SessionLocal()


# add anime
def addAnime(anime_id, latest_episode, guild_id):
    # check if anime is there
    anime = db.query(models.Anime).filter(
        models.Anime.anime_id == anime_id).first()
    if anime is None:
        anime = models.Anime(anime_id, latest_episode, [guild_id])
        db.add(anime)
        db.commit()
        guilds = anime.server_list
        guilds.append(guild_id)
        anime.server_list = guilds
        db.commit()
    else:
        print('already exists')
        guilds = anime.server_list
        print(guilds)
        if guild_id not in guilds:
            guilds.append(guild_id)
            print(guilds)
            anime.server_list = guilds
            print(anime.server_list)
            db.commit()
