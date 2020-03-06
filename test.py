import unittest
from schema import schema


class TestFindSongsByArtist(unittest.TestCase):
    def setUp(self):
        self.expected_titles = [
            'My Sweet Lord',
            'Hark! The Herald Angels Sing',
            'Silent Night',
            'O Come All Ye Faithful (Album Version)'
        ]
        query_string = '''{
          filterSongByArtist(artistId: "ARXJJSN1187B98CB37") {
            msdTrackId
            title
          }
        }'''
        self.queried_titles = []
        for f in schema.execute(query_string).data['filterSongByArtist']:
            self.queried_titles.append(f['title'])
        self.expected_msd_track_id = [
            'TRPYNNL12903CAF506',
            'TRFMJLM12903CAF4FB',
            'TRSKGOU12903CAF4FD',
            'TRQSEJD12903CAF4F9'
        ]
        self.queried_msd_track_id = []
        for f in schema.execute(query_string).data['filterSongByArtist']:
            self.queried_msd_track_id.append(f['msdTrackId'])

    def test_title_counts(self):
        self.assertCountEqual(self.queried_titles, self.expected_titles)

    def test_msd_track_id_counts(self):
        self.assertCountEqual(self.queried_msd_track_id, self.expected_msd_track_id)


if __name__ == '__main__':
    unittest.main()
