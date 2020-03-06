from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String


class SongModel(Base):
    """
    A model for songs
    """
    __tablename__ = 'song'
    msd_track_id = Column('msd_track_id', String, primary_key=True)
    artist_id = Column('artist_id', String, ForeignKey('artist.artist_id'))
    performance = Column('performance', Integer)
    title = Column('title', String)


class ArtistModel(Base):
    """
    A model for artists
    """
    __tablename__ = 'artist'
    artist_id = Column('artist_id', String, primary_key=True)
    artist_name = Column('artist_name', Integer)
    song_list = relationship(SongModel, backref='artist')
