import os
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.ext.mutable import MutableList
from database import Base

try:
    PREFIX = os.environ["PREFIX"]
except:
    PREFIX = "*"


class Server(Base):
    __tablename__ = 'servers'
    guild_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    prefix = Column(String(5), nullable=False, default=PREFIX)
    channel_id = Column(Integer, nullable=False)

    def __init__(self, guild_id, prefix, channel_id):
        self.guild_id = guild_id
        self.prefix = prefix
        self.channel_id = channel_id


class Anime(Base):
    __tablename__ = 'anime'
    anime_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    latest_episode = Column(Integer, nullable=False, default=null())
    server_list = MutableList.as_mutable(
        Column(JSON, nullable=False, default=[]))

    def __init__(self, anime_id, latest_episode, server_list):
        self.anime_id = anime_id
        self.latest_episode = latest_episode
        self.server_list = server_list


class NewEpisode(Base):
    __tablename__ = 'new_episodes'
    anime_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    anime_name = Column(String, nullable=False)
    episode_name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)

    def __init__(self, anime_id, anime_name, episode_name, image_url):
        self.anime_id = anime_id
        self.anime_name = anime_name
        self.episode_name = episode_name
        self.image_url = image_url
