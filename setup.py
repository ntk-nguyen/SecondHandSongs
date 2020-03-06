from database.models import SongModel, ArtistModel
from database import base
import logging
import sys
import re

# Load logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    log.info('Create database {}'.format(base.db_name))
    base.Base.metadata.create_all(base.engine)

    log.info('Insert artist data in database')
    with open('database/data/unique_artists.txt', 'r', encoding='utf-8') as file:
        for line in file:
            artist_id = line.rstrip().split('<SEP>')[0]
            artist_name = line.rstrip().split('<SEP>')[-1]
            artist = ArtistModel(**{'artist_id': artist_id, 'artist_name': artist_name})
            base.db_session.add(artist)
        base.db_session.commit()

    log.info('Insert song data in database')
    with open('database/data/shs_dataset_train.txt', 'r', encoding='utf-8') as file:
        title = ''
        for line in file:
            if re.search('^#', line):
                # Ignore comments
                continue
            elif re.search('^%', line):
                title = line.rstrip().split(', ')[-1]
            else:
                msd_track_id, artist_id, performance = line.rstrip().split('<SEP>')
                song = SongModel(**{
                    'msd_track_id': msd_track_id,
                    'artist_id': artist_id,
                    'performance': performance,
                    'title': title
                })
                base.db_session.add(song)
        base.db_session.commit()
