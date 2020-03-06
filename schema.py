from graphene_sqlalchemy import SQLAlchemyObjectType
from database.models import SongModel, ArtistModel
from graphene_sqlalchemy import SQLAlchemyConnectionField
import graphene


# Initialize description of song attributes for queries
class SongAttribute:
    artist_id = graphene.ID(description='ID of the artists who have played this song')
    performance = graphene.String(description='SHS performance')
    title = graphene.String(description='Title')


class Song(SQLAlchemyObjectType, SongAttribute):
    """
    Create a node for song
    """
    class Meta:
        model = SongModel
        interfaces = (graphene.relay.Node, )


class ArtistAttribute:
    artist_name = graphene.String(description='Artist name')


class Artist(SQLAlchemyObjectType, ArtistAttribute):
    """
    Create a node for artist
    """
    class Meta:
        model = ArtistModel
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    """
    Query objects for GraphQL API
    """
    node = graphene.relay.Node.Field()
    song = graphene.relay.Node.Field(Song)
    song_list = SQLAlchemyConnectionField(Song)
    artist = graphene.relay.Node.Field(Artist)
    artist_list = SQLAlchemyConnectionField(Artist)

    # Create a filter to query what songs an artist has played
    filter_song_by_artist = graphene.List(
        Song,
        artist_id=graphene.String(),
    )

    def resolve_filter_song_by_artist(self, info, **args):
        artist_id = args.get("artist_id")
        query = Song.get_query(info)
        songs = query.filter(SongModel.artist_id == artist_id).all()
        return songs


schema = graphene.Schema(query=Query)
