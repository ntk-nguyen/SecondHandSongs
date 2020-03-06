from schema import schema

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Find songs that have been played by an artist")
    parser.add_argument('-a', metavar='Artist ID', help='Artist ID from the Second Hands Dataset',
                        dest='artist_id')
    args = parser.parse_args()
    query_string = '''{
      filterSongByArtist(artistId: "%s") {
        msdTrackId
        title
      }
    }''' % args.artist_id
    result = schema.execute(query_string)
    print('Artist %s has played the following songs' % args.artist_id)
    for f in result.data['filterSongByArtist']:
        print('\t%s (MSD Track ID: %s)' % (f['title'], f['msdTrackId']))
