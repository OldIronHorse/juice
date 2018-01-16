from unittest import TestCase

import juice.message.format as msg_format

class TestLogin(TestCase):
  def test_kwarg(self):
    self.assertEqual('login myname mypassword\n',
      msg_format.login(user='myname', password='mypassword'))

  def test_positional(self):
    self.assertEqual('login myname mypassword\n',
      msg_format.login('myname', 'mypassword'))


class TestListen(TestCase):
  def test_query(self):
    self.assertEqual('listen ?\n',
      msg_format.listen())

  def test_set(self):
    self.assertEqual('listen 1\n',
      msg_format.listen(True))

  def test_clear(self):
    self.assertEqual('listen 0\n',
      msg_format.listen(False))


class TestSubscribe(TestCase):
  def test_empty(self):
    self.assertEqual('subscribe\n',
      msg_format.subscribe())

  def test_single(self):
    self.assertEqual('subscribe mixer\n',
      msg_format.subscribe(['mixer']))

  def test_multiple(self):
    self.assertEqual('subscribe mixer,pause\n',
      msg_format.subscribe(['mixer', 'pause']))


class TestPlayer(TestCase):
  def test_count(self):
    self.assertEqual('player count ?\n',
      msg_format.player('count'))

  def test_id(self):
    self.assertEqual('player id 1 ?\n',
      msg_format.player('id', 1))


class TestPlayerById(TestCase):
  def test_signalstrength(self):
    self.assertEqual('00:12:34:56:78:90 signalstrength ?\n',
      msg_format.player_by_id('00:12:34:56:78:90', 'signalstrength'))

  def test_name_get(self):
    self.assertEqual('00:12:34:56:78:90 name ?\n',
      msg_format.player_by_id('00:12:34:56:78:90', 'name'))

  def test_name_set(self):
    self.assertEqual('00:12:34:56:78:90 name Some%20New%20Name\n',
      msg_format.player_by_id('00:12:34:56:78:90', 'name', 'Some New Name'))


class TestSyncgroups(TestCase):
  def test_get(self):
    self.assertEqual('syncgroups ?\n',
      msg_format.syncgroups())


class TestPlayerVolume(TestCase):
  def test_get(self):
    self.assertEqual('00:12:34:56:78:90 mixer volume ?\n',
      msg_format.player_by_id('00:12:34:56:78:90', 'volume'))

  def test_set(self):
    self.assertEqual('00:12:34:56:78:90 mixer volume 75\n',
      msg_format.player_by_id('00:12:34:56:78:90', 'volume', 75))

  def test_increment(self):
    self.assertEqual('00:12:34:56:78:90 mixer volume +5\n',
      msg_format.player_by_id('00:12:34:56:78:90', 'volume', '+5'))

  def test_decrement(self):
    self.assertEqual('00:12:34:56:78:90 mixer volume -5\n',
      msg_format.player_by_id('00:12:34:56:78:90', 'volume', -5))


class TestPlayerMuting(TestCase):
  def test_get(self):
    self.assertEqual('00:12:34:56:78:90 mixer muting ?\n',
      msg_format.player_by_id('00:12:34:56:78:90', 'muting'))

  def test_set(self):
    self.assertEqual('00:12:34:56:78:90 mixer muting 75\n',
      msg_format.player_by_id('00:12:34:56:78:90', 'muting', 75))

  def test_toggle(self):
    self.assertEqual('00:12:34:56:78:90 mixer muting toggle\n',
      msg_format.player_by_id('00:12:34:56:78:90', 'muting', 'toggle'))


class TestPlayers(TestCase):
  def test_defaults(self):
    self.assertEqual('players 0 10\n',
      msg_format.players())

  def test_override(self):
    self.assertEqual('players 5 3\n',
      msg_format.players(5, 3))


class TestInfo(TestCase):
  def test_genres(self):
    self.assertEqual('info total genres ?\n',
      msg_format.total('genres'))

  def test_artists(self):
    self.assertEqual('info total artists ?\n',
      msg_format.total('artists'))

  def test_albums(self):
    self.assertEqual('info total albums ?\n',
      msg_format.total('albums'))

  def test_songs(self):
    self.assertEqual('info total songs ?\n',
      msg_format.total('songs'))

  def test_duration(self):
    self.assertEqual('info total duration ?\n',
      msg_format.total('duration'))


class TestGenres(TestCase):
  def test_no_filtres_defaults(self):
    self.assertEqual('genres 0 100 tags:lytiqwaSes\n',
      msg_format.genres())

  def test_no_filtres_override(self):
    self.assertEqual('genres 5 11 tags:lytiqwaSes\n',
      msg_format.genres(5, 11))

  def test_artist_filtre(self):
    self.assertEqual('genres 0 100 tags:lytiqwaSes artist_id:4\n',
      msg_format.genres(artist_id=4))

  def test_album_filtre(self):
    self.assertEqual('genres 0 100 tags:lytiqwaSes album_id:4\n',
      msg_format.genres(album_id=4))

  def test_track_filtre(self):
    self.assertEqual('genres 0 100 tags:lytiqwaSes track_id:4\n',
      msg_format.genres(track_id=4))

  def test_genre_filtre(self):
    self.assertEqual('genres 0 100 tags:lytiqwaSes genre_id:4\n',
      msg_format.genres(genre_id=4))

  def test_year_filtre(self):
    self.assertEqual('genres 0 100 tags:lytiqwaSes year:1994\n',
      msg_format.genres(year=1994))

  def test_multiple_filtres(self):
    self.assertEqual('genres 0 100 tags:lytiqwaSes artist_id:4 year:1994\n',
      msg_format.genres(artist_id=4, year=1994))


class TestArtists(TestCase):
  def test_no_filtres_defaults(self):
    self.assertEqual('artists 0 100 tags:lytiqwaSes\n',
      msg_format.artists())

  def test_no_filtres_override(self):
    self.assertEqual('artists 5 11 tags:lytiqwaSes\n',
      msg_format.artists(5, 11))

  def test_artist_filtre(self):
    self.assertEqual('artists 0 100 tags:lytiqwaSes artist_id:4\n',
      msg_format.artists(artist_id=4))

  def test_album_filtre(self):
    self.assertEqual('artists 0 100 tags:lytiqwaSes album_id:4\n',
      msg_format.artists(album_id=4))

  def test_track_filtre(self):
    self.assertEqual('artists 0 100 tags:lytiqwaSes track_id:4\n',
      msg_format.artists(track_id=4))

  def test_genre_filtre(self):
    self.assertEqual('artists 0 100 tags:lytiqwaSes genre_id:4\n',
      msg_format.artists(genre_id=4))

  def test_year_filtre(self):
    self.assertEqual('artists 0 100 tags:lytiqwaSes year:1994\n',
      msg_format.artists(year=1994))

  def test_multiple_filtres(self):
    self.assertEqual('artists 0 100 tags:lytiqwaSes artist_id:4 year:1994\n',
      msg_format.artists(artist_id=4, year=1994))


class TestPlayerStatus(TestCase):
  def test_defaults(self):
    self.assertEqual('00:12:34:56:78:90 status - 100 tags:al\n',
      msg_format.player_status('00:12:34:56:78:90'))

  def test_subscribe_defaults(self):
    self.assertEqual('00:12:34:56:78:90 status - 100 tags:al subscribe:0\n',
      msg_format.player_status('00:12:34:56:78:90', subscribe=0))


class TestPlayerCommands(TestCase):
  def test_next_track(self):
    self.assertEqual('00:12:34:56:78:90 playlist index %2B1\n',
      msg_format.next_track('00:12:34:56:78:90'))

  def test_previous_track(self):
    self.assertEqual('00:12:34:56:78:90 playlist index -1\n',
      msg_format.previous_track('00:12:34:56:78:90'))
