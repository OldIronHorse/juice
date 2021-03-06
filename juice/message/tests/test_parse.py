from unittest import TestCase
from unittest.mock import MagicMock,patch

from juice.message import parse_msg, InvalidMsgException

class TestLogin(TestCase):
  def test_valid(self):
    self.assertEqual({
        'command': 'login',
        'user': 'myusername'
      },
      parse_msg('login myusername ******'))

  def test_missing_field(self):
    with self.assertRaises(InvalidMsgException):
      parse_msg('login myusername')

  def test_wrong_value(self):
    with self.assertRaises(InvalidMsgException):
      parse_msg('login myusername an_unexpected_value')


class TestListen(TestCase):
  def test_valid_0(self):
    self.assertEqual({
        'command': 'listen',
        'value' : 0,
      },
      parse_msg('listen 0'))

  def test_valid_1(self):
    self.assertEqual({
        'command': 'listen',
        'value' : 1,
      },
      parse_msg('listen 1'))

  def test_invalid_value(self):
    with self.assertRaises(InvalidMsgException):
      parse_msg('listen 2')

  def test_invalid_value_type(self):
    with self.assertRaises(InvalidMsgException):
      parse_msg('listen not_listening')

  def test_missing_field(self):
    with self.assertRaises(InvalidMsgException):
      parse_msg('listen')


class TestSubscribe(TestCase):
  def test_valid_single(self):
    self.assertEqual({
        'command': 'subscribe',
        'notifications': ['mixer'],
      },
      parse_msg('subscribe mixer'))

  def test_valid_multiple(self):
    self.assertEqual({
        'command': 'subscribe',
        'notifications': ['mixer', 'pause', 'play'],
      },
      parse_msg('subscribe mixer,pause,play'))


class TestPlayer(TestCase):
  def test_count_valid(self):
    self.assertEqual({
        'command': 'player',
        'count': 4
      },
      parse_msg('player count 4'))

  def test_id_valid(self):
    self.assertEqual({
      'command': 'player',
      'index': 1,
      'id': '00:0f:55:a6:65:e5',
    },
    parse_msg('player id 1 00%3A0f%3A55%3Aa6%3A65%3Ae5'))

  def test_uuid_valid(self):
    self.assertEqual({
      'command': 'player',
      'index': 0,
      'uuid': '012345678901234567890123456789012',
    },
    parse_msg('player uuid 0 012345678901234567890123456789012'))

  def test_name_valid(self):
    self.assertEqual({
      'command': 'player',
      'index': 2,
      'name': 'Dining Room',
    },
    parse_msg('player name 2 Dining%20Room'))
    
  def test_ip_valid(self):
    self.assertEqual({
      'command': 'player',
      'index': 0,
      'ip': '192.168.1.22:3483',
    },
    parse_msg('player ip 0 192.168.1.22:3483'))

  def test_ip_id(self):
    self.assertEqual({
      'command': 'player',
      'id': '00:0f:55:a6:65:e5',
      'ip': '192.168.1.22:3483',
    },
    parse_msg('player ip 00%3A0f%3A55%3Aa6%3A65%3Ae5 192.168.1.22:3483'))
    
  def test_model_valid(self):
    self.assertEqual({
      'command': 'player',
      'index': 0,
      'model': 'squeezelite',
    },
    parse_msg('player model 0 squeezelite'))

  def test_isplayer(self):
    self.assertEqual({
      'command': 'player',
      'index': 1,
      'isplayer': 0,
    },
    parse_msg('player isplayer 1 0'))

class TestPlayerId(TestCase):
  def test_signalstrength(self):
    self.assertEqual({
      'player': {
        'id': '00:04:20:23:30:7f',
        'signalstrength': 62,
      }
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f signalstrength 62'))

  def test_name(self):
    self.assertEqual({
      'player': {
        'id': '00:04:20:23:30:7f',
        'name': 'Dining Room',
      }
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f name Dining%20Room'))

  def test_connected(self):
    self.assertEqual({
      'player': {
        'id': '00:04:20:23:30:7f',
        'connected': 1,
      }
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f connected 1'))

  def test_sleep(self):
    self.assertEqual({
      'player': {
        'id': '00:04:20:23:30:7f',
        'sleep': 100.5,
      }
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f sleep 100.5'))

  def test_sync_index(self):
    self.assertEqual({
      'player': {
        'id': '00:04:20:23:30:7f',
        'sync': 1,
      }
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f sync 1'))

  def test_sync_id(self):
    self.assertEqual({
      'player': {
        'id': '00:04:20:23:30:7f',
        'sync': '00:04:20:23:30:70',
      }
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f sync 00%3A04%3A20%3A23%3A30%3A70'))

  def test_sync_none(self):
    self.assertEqual({
      'player': {
        'id': '00:04:20:23:30:7f',
        'sync': '-',
      }
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f sync -'))


class TestSyncGroups(TestCase):
  def test_syncgroups_none(self):
    self.assertEqual({
      'ids': [],
      'names': [],
    },
    parse_msg('syncgroups'))

  def test_syncgroups(self):
    self.assertEqual({
      'ids': ['00:04:20:17:4b:3b','00:0f:55:a6:65:e5'],
      'names': ['Kitchen', 'Dining Room'],
    },
    parse_msg('syncgroups sync_members%3A00%3A04%3A20%3A17%3A4b%3A3b%2C00%3A0f%3A55%3Aa6%3A65%3Ae5 sync_member_names%3AKitchen%2CDining%20Room'))


class TestMixer(TestCase):
  def test_volume_set(self):
    self.assertEqual({
      'player': {
        'id': '00:04:20:23:30:7f',
        'volume': 25,
      }
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f mixer volume 25'))

  def test_volume_inc(self):
    self.assertEqual({
      'player': {
        'id': '00:04:20:23:30:7f',
        'volume_change': 5,
      }
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f mixer volume +5'))

  def test_volume_dec(self):
    self.assertEqual({
      'player': {
        'id': '00:04:20:23:30:7f',
        'volume_change': -5,
      }
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f mixer volume -5'))

class TestPlayers(TestCase):
  def test_2_of_3(self):
    self.maxDiff = None
    self.assertEqual({
      'player_count': 3,
      'players': [{
        'index': 0,
        'id': '00:04:20:17:4b:3b',
        'uuid': '39c8dbb3bf7d756d013348f4eca8e130',
        'ip': '192.168.1.75:28225',
        'name': 'Kitchen',
        'seq_no': 0,
        'model': 'receiver',
        'modelname': 'Squeezebox Receiver',
        'power': 1,
        'isplaying': 0,
        'displaytype': 'none',
        'isplayer': 1,
        'canpoweroff': 1,
        'connected': 1,
        'firmware': '77'
      },{
        'index': 1,
        'id': '00:0f:55:a6:65:e5',
        'uuid': '',
        'ip': '192.168.1.82:57600',
        'name': 'Dining Room',
        'seq_no': 0,
        'model': 'squeezelite',
        'modelname': 'SqueezeLite',
        'power': 1,
        'isplaying': 0,
        'displaytype': 'none',
        'isplayer': 1,
        'canpoweroff': 1,
        'connected': 1,
        'firmware': 'v1.8.7-999'
      }]},
    parse_msg('players 0 2 count%3A3 playerindex%3A0 playerid%3A00%3A04%3A20%3A17%3A4b%3A3b uuid%3A39c8dbb3bf7d756d013348f4eca8e130 ip%3A192.168.1.75%3A28225 name%3AKitchen seq_no%3A0 model%3Areceiver modelname%3ASqueezebox%20Receiver power%3A1 isplaying%3A0 displaytype%3Anone isplayer%3A1 canpoweroff%3A1 connected%3A1 firmware%3A77 playerindex%3A1 playerid%3A00%3A0f%3A55%3Aa6%3A65%3Ae5 uuid%3A ip%3A192.168.1.82%3A57600 name%3ADining%20Room seq_no%3A0 model%3Asqueezelite modelname%3ASqueezeLite power%3A1 isplaying%3A0 displaytype%3Anone isplayer%3A1 canpoweroff%3A1 connected%3A1 firmware%3Av1.8.7-999'))

  def test_3rd_of_3(self):
    self.maxDiff = None
    self.assertEqual({
      'player_count': 3,
      'players': [{
        'index': 2,
        'id': '00:04:20:23:30:7f',
        'uuid': 'b0ff501bdcff1d6a18e0965b23844c94',
        'ip': '192.168.1.69:36472',
        'name': 'Lounge',
        'seq_no': 4,
        'model': 'fab4',
        'modelname': 'Squeezebox Touch',
        'power': 1,
        'isplaying': 0,
        'displaytype': 'none',
        'isplayer': 1,
        'canpoweroff': 1,
        'connected': 1,
        'firmware': '7.8.0-r16754'
      }]},
    parse_msg('players 2 2 count%3A3 playerindex%3A2 playerid%3A00%3A04%3A20%3A23%3A30%3A7f uuid%3Ab0ff501bdcff1d6a18e0965b23844c94 ip%3A192.168.1.69%3A36472 name%3ALounge seq_no%3A4 model%3Afab4 modelname%3ASqueezebox%20Touch power%3A1 isplaying%3A0 displaytype%3Anone isplayer%3A1 canpoweroff%3A1 connected%3A1 firmware%3A7.8.0-r16754'))


class TestInfo(TestCase):
  def test_total_genres(self):
    self.assertEqual({'genre_count': 18},
      parse_msg('info total genres 18'))

  def test_total_artists(self):
    self.assertEqual({'artist_count': 18},
      parse_msg('info total artists 18'))

  def test_total_albums(self):
    self.assertEqual({'album_count': 18},
      parse_msg('info total albums 18'))

  def test_total_songs(self):
    self.assertEqual({'song_count': 18},
      parse_msg('info total songs 18'))

  def test_total_duration(self):
    self.assertEqual({'total_duration': 181234},
      parse_msg('info total duration 181234'))

class TestGenres(TestCase):
  def setUp(self):
    self.maxDiff = None

  def test_no_filtre(self):
    self.assertEqual({
      'count': 6,
      'start': 0,
      'page_size': 5,
      'genres': [
        {'id': 3, 'name': 'Acid Jazz'},
        {'id': 4, 'name': 'Alternative & Punk'},
        {'id': 5, 'name': 'French'},
        {'id': 6, 'name': 'No Genre'},
        {'id': 7, 'name': 'Pop'},
      ]},
      parse_msg('genres 0 5 count:6 id:3 genre:Acid%20Jazz id:4 genre:Alternative%20&%20Punk id:5 genre:French id:6 genre:No%20Genre id:7 genre:Pop'))

  def test_no_filtre_rescan(self):
    self.maxDiff = None
    self.assertEqual({
      'rescan': 1,
      'count': 6,
      'start': 0,
      'page_size': 5,
      'genres': [
        {'id': 3, 'name': 'Acid Jazz'},
        {'id': 4, 'name': 'Alternative & Punk'},
        {'id': 5, 'name': 'French'},
        {'id': 6, 'name': 'No Genre'},
        {'id': 7, 'name': 'Pop'},
      ]},
      parse_msg('genres 0 5 rescan%3A1 count:6 id:3 genre:Acid%20Jazz id:4 genre:Alternative%20&%20Punk id:5 genre:French id:6 genre:No%20Genre id:7 genre:Pop'))

  def test_search(self):
    self.assertEqual({
      'count': 1,
      'start': 0,
      'page_size': 5,
      'search': 'unk',
      'genres': [
        {'id': 4, 'name': 'Alternative & Punk'},
      ]},
      parse_msg('genres 0 5 search%3Aunk count%3A1 id%3A4 genre%3AAlternative%20&%20Punk'))


class TestArtists(TestCase):
  def setUp(self):
    self.maxDiff = None

  def test_no_filtre(self):
    self.assertEqual({
      'count': 7,
      'start': 0,
      'page_size': 5,
      'artists': [
        {'id': 2, 'name': 'Anastacia'},
        {'id': 3, 'name': 'Calogero'},
        {'id': 4, 'name': 'Evanescence'},
        {'id': 5, 'name': 'Leftfield & Lydon'},
        {'id': 18, 'name': 'Llorca'},
      ]},
      parse_msg('artists 0 5 count:7 id:2 artist:Anastacia id:3 artist:Calogero id:4 artist:Evanescence id:5 artist:Leftfield%20%26%20Lydon id:18 artist:Llorca'))

  def test_genre_filtre(self):
    self.assertEqual({
      'genre_id': 7,
      'count': 2,
      'start': 0,
      'page_size': 5,
      'artists': [
        {'id': 2, 'name': 'Anastacia'},
        {'id': 19, 'name': 'Sarah Connor'},
      ]},
      parse_msg('artists 0 5 genre_id:7 count:2 id:2 artist:Anastacia id:19 artist:Sarah%20Connor'))


class TestAlbums(TestCase):
  def setUp(self):
    self.maxDiff = None

  def test_no_filtre_no_tags(self):
    self.assertEqual({
      'count': 14,
      'start': 0,
      'page_size': 4,
      'albums': [
        {'id': 1, 'name': 'Amadeus (Disc 1 of 2)'},
        {'id': 4, 'name': 'Anastacia'},
        {'id': 5, 'name': 'Bounce [Single]'},
        {'id': 6, 'name': 'Fallen'},
      ]},
      parse_msg('albums 0 4 count:14 id:1 album:Amadeus%20(Disc%201%20of%202) id:4 album:Anastacia id:5 album:Bounce%20[Single] id:6 album:Fallen'))

  def test_artist_filter_no_tags(self):
    self.assertEqual({
      'artist_id': 19,
      'count': 1,
      'start': 0,
      'page_size': 5,
      'albums': [
        {'id': 5, 'name': 'Bounce [Single]'},
      ]},
      parse_msg('albums 0 5 artist_id:19 count:1 id:5 album:Bounce%20[Single]'))

  def test_no_filter_all_tags(self):
    self.assertEqual({
      'tags': 'lytiqwaS',
      'count': 597,
      'start': 102,
      'page_size': 1,
      'albums': [
        {'id': 558,
         'name': 'Classics for Children',
         'year': 1999,
         'title': 'Classics for Children',
         'disc': 2,
         'disccount': 2,
         'compilation': 1,
         'artist': 'Various Artists',
         'artist_id': 3,
        },
      ]},
      parse_msg('albums 102 1 tags%3AlytiqwaS id%3A558 album%3AClassics%20for%20Children year%3A1999 title%3AClassics%20for%20Children disc%3A2 disccount%3A2 compilation%3A1 artist_id%3A3 artist%3AVarious%20Artists count%3A597'))


class TestYears(TestCase):
  def setUp(self):
    self.maxDiff = None

  def test_years(self):
    self.assertEqual({
      'count': 44,
      'start': 0,
      'page_size': 2,
      'years': [2017,2016],
      },
      parse_msg('years 0 2 year%3A2017 year%3A2016 count%3A44'))


class TestTracks(TestCase):
  def setUp(self):
    self.maxDiff = None

  def test_by_album_id(self):
    self.assertEqual({
      'start': 0,
      'page_size': 3,
      'count': 14,
      'album_id': 432,
      'tracks':[
        {'id': 5417, 'title': '-', 'genre': 'Rock/Pop', 'artist': 'Snow Patrol', 'album': 'Eyes Open', 'duration': 235.373},
        {'id': 5421, 'title': 'Chasing Cars', 'genre': 'Rock/Pop', 'artist': 'Snow Patrol', 'album': 'Eyes Open', 'duration': 268},
        {'id': 5416, 'title': 'The Finish Line', 'genre': 'Rock/Pop', 'artist': 'Snow Patrol', 'album': 'Eyes Open', 'duration': 208.133},
      ]},
      parse_msg('tracks 0 3 album_id%3A432 id%3A5417 title%3A- genre%3ARock%2FPop artist%3ASnow%20Patrol album%3AEyes%20Open duration%3A235.373 id%3A5421 title%3AChasing%20Cars genre%3ARock%2FPop artist%3ASnow%20Patrol album%3AEyes%20Open duration%3A268 id%3A5416 title%3AThe%20Finish%20Line genre%3ARock%2FPop artist%3ASnow%20Patrol album%3AEyes%20Open duration%3A208.133 count%3A14'))


class TestSearch(TestCase):
  def setUp(self):
    self.maxDiff = None

  def test_simple_term(self):
    self.assertEqual({
      'count': 393,
      'start': 0,
      'page_size': 2,
      'term': 'al',
      'contributors_count': 41,
      'contributors': [
        {'id':95, 'name': 'Alanis Morissette'},
        {'id':96, 'name': 'Alex Bailey'},
      ],
      'albums_count': 13,
      'albums': [
        {'id': 24, 'name': 'No Album'},
        {'id': 64, 'name': 'All About Eve'},
      ],
      'tracks_count': 339,
      'tracks': [
        {'id': 56, 'name': 'Totem Pole (alternate take)'},
        {'id': 63, 'name': 'All of Me'},
      ]},
      parse_msg('search 0 2 term%3Aal contributors_count%3A41 contributor_id%3A95 contributor%3AAlanis%20Morissette contributor_id%3A96 contributor%3AAlex%20Bailey albums_count%3A13 album_id%3A24 album%3ANo%20Album album_id%3A64 album%3AAll%20About%20Eve tracks_count%3A339 track_id%3A56 track%3ATotem%20Pole%20(alternate%20take) track_id%3A63 track%3AAll%20of%20Me count%3A393'))


class TestPlay(TestCase):
  def test_no_fade(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'action': 'play'
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 play'))
    
  def test_with_fade(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'action': 'play',
        'fade': 15
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 play 15'))


class TestStop(TestCase):
  def test_stop(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'action': 'stop'
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 stop'))
    

class TestPause(TestCase):
  def test_toggle(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'action': 'toggle_pause'
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 pause'))
    
  def test_force_pause(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'action': 'pause'
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 pause 1'))
    
  def test_force_unpause(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'action': 'unpause'
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 pause 0'))
    
  def test_force_unpause_with_fade(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'action': 'unpause',
        'fade': 15
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 pause 0 15'))


class TestMode(TestCase):
  def test_play(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'mode': 'play'
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 mode play'))
    
  def test_pause(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'mode': 'pause'
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 mode pause'))
    
  def test_stop(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'mode': 'stop'
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 mode stop'))
    

class TestTime(TestCase):
  def test_float(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'time': 12.55
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 time 12.55'))
    
  def test_int(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'time': 5
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 time 5'))
    
  def test_plus(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'time_change': 5
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 time +5'))
    
  def test_minus(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'time_change': -5
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 time -5'))
    

class TestPlayerCurrent(TestCase):
  def test_genre(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'genre': 'Acoustic',
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 genre Acoustic'))
    
  def test_artist(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'artist': 'Dua Lipa',
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 artist Dua%20Lipa'))
    
  def test_album(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'album': 'Greatest Hits',
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 album Greatest%20Hits'))
    
  def test_title(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'title': 'Voulez Vous',
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 title Voulez%20Vous'))
    
  def test_duration(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'duration': 103.2,
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 duration 103.2'))
    
  def test_remote_true(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'remote': True,
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 remote 1'))
    
  def test_remote_fase(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'remote': False,
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 remote 0'))
    
  def test_current_title(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'current_title': '1-Voulez Vous (ABBA)',
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 current_title 1-Voulez%20Vous%20(ABBA)'))
    

class TestPlaylist(TestCase):
  def test_play(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'playlist': {
          'action': 'play',
          'item': '/music/abba/01-voulez vous.mp3'
        },
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 playlist play /music/abba/01-voulez%20vous.mp3'))
    
  def test_play_with_title(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'playlist': {
          'action': 'play',
          'item': '/music/abba/01-voulez vous.mp3',
          'title': 'Voulez Vous!',
        },
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 playlist play /music/abba/01-voulez%20vous.mp3 Voulez%20Vous!'))
    
  def test_add(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'playlist': {
          'action': 'add',
          'item': '/music/abba/01-voulez vous.mp3'
        },
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 playlist add /music/abba/01-voulez%20vous.mp3'))
    
  def test_add_with_title(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'playlist': {
          'action': 'add',
          'item': '/music/abba/01-voulez vous.mp3',
          'title': 'Voulez Vous!',
        },
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 playlist add /music/abba/01-voulez%20vous.mp3 Voulez%20Vous!'))
    
  def test_insert(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'playlist': {
          'action': 'insert',
          'item': '/music/abba/01-voulez vous.mp3'
        },
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 playlist insert /music/abba/01-voulez%20vous.mp3'))
    
  def test_insert_with_title(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'playlist': {
          'action': 'insert',
          'item': '/music/abba/01-voulez vous.mp3',
          'title': 'Voulez Vous!',
        },
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 playlist insert /music/abba/01-voulez%20vous.mp3 Voulez%20Vous!'))
    
  def test_deleteitem(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'playlist': {
          'action': 'deleteitem',
          'item': '/music/abba/01-voulez vous.mp3'
        },
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 playlist deleteitem /music/abba/01-voulez%20vous.mp3'))
    
  def test_delete(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'playlist': {
          'action': 'delete',
          'index': 4,
        },
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 playlist delete 4'))
    
  def test_move(self):
    self.assertEqual({
      'player': {
        'id': '00:0f:55:a6:65:e5',
        'playlist': {
          'action': 'move',
          'from': 4,
          'to': 6,
        },
      }
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 playlist move 4 6'))
    

class TestCompound(TestCase):
  def setUp(self):
    self.maxDiff = None

  def test_serverstatus(self):
    self.assertEqual({
      'serverstatus': {
        'start': 0,
        'page_size': 2,
        'lastscan': 1514208396,
        'version': '7.9.0',
        'uuid': '2a5700ff-aec8-4676-b524-f69f925fcd6b',
        'totals': {
          'artists': 1490,
          'albums': 597,
          'genres': 52,
          'songs': 8578,
          'duration': 2036617.432,
        },
        'player count': 3,
        'players': [{
            'index': 0,
            'id': '00:0f:55:a6:65:e5',
            'uuid': '',
            'ip': '192.168.1.82:55016',
            'name': 'Dining Room',
            'seq_no': 0,
            'model': 'squeezelite',
            'modelname': 'SqueezeLite',
            'power': 1,
            'isplaying': 1,
            'displaytype': 'none',
            'isplayer': 1,
            'canpoweroff': 1,
            'connected': 1,
            'firmware': 'v1.8.7-999',
          },{
            'index': 1,
            'id': '00:04:20:23:30:7f',
            'uuid': 'b0ff501bdcff1d6a18e0965b23844c94',
            'ip': '192.168.1.69:46707',
            'name': 'Lounge',
            'seq_no': 6,
            'model': 'fab4',
            'modelname': 'Squeezebox Touch',
            'power': 1,
            'isplaying': 0,
            'displaytype': 'none',
            'isplayer': 1,
            'canpoweroff': 1,
            'connected': 1,
            'firmware': '7.8.0-r16754',
        }],
        'sn player count': 0, 
        'other player count': 0,
      }},
      parse_msg('serverstatus 0 2 lastscan%3A1514208396 version%3A7.9.0 uuid%3A2a5700ff-aec8-4676-b524-f69f925fcd6b info%20total%20albums%3A597 info%20total%20artists%3A1490 info%20total%20genres%3A52 info%20total%20songs%3A8578 info%20total%20duration%3A2036617.432 player%20count%3A3 playerindex%3A0 playerid%3A00%3A0f%3A55%3Aa6%3A65%3Ae5 uuid%3A ip%3A192.168.1.82%3A55016 name%3ADining%20Room seq_no%3A0 model%3Asqueezelite modelname%3ASqueezeLite power%3A1 isplaying%3A1 displaytype%3Anone isplayer%3A1 canpoweroff%3A1 connected%3A1 firmware%3Av1.8.7-999 playerindex%3A1 playerid%3A00%3A04%3A20%3A23%3A30%3A7f uuid%3Ab0ff501bdcff1d6a18e0965b23844c94 ip%3A192.168.1.69%3A46707 name%3ALounge seq_no%3A6 model%3Afab4 modelname%3ASqueezebox%20Touch power%3A1 isplaying%3A0 displaytype%3Anone isplayer%3A1 canpoweroff%3A1 connected%3A1 firmware%3A7.8.0-r16754 sn%20player%20count%3A0 other%20player%20count%3A0'))

  def test_player_status(self):
    self.assertEqual({
      'player': {
        'cmd': 'status',
        'start': '-',
        'page_size': 2,
        'tags': '',
        'subscribe': 0,
        'id': '00:0f:55:a6:65:e5',
        'name': 'Dining Room',
        'connected': 1,
        'ip': '192.168.1.82:57702',
        'power': 1,
        'signalstrength': 0,
        'mode': 'play',
        'time': 19.4145948696136,
        'rate': 1,
        'duration': 228.106,
        'can_seek': 1,
        'volume':32,
        'playlist repeat': 0,
        'playlist shuffle': 0,
        'playlist mode': 'off',
        'seq_no': 0,
        'playlist_cur_index': 8,
        'playlist_timestamp': 1515551291.82482,
        'playlist_tracks': 11,
        'digital_volume_control': 1,
        'playlist': [
          {'index': 8, 'id': 8691, 'title': 'Cryin\' In Your Beer'},
          {'index': 9, 'id': 8692, 'title': 'Boy On A Bike'},
        ],
      },
    },
    parse_msg('00%3A0f%3A55%3Aa6%3A65%3Ae5 status - 2 tags%3A subscribe%3A0 player_name%3ADining%20Room player_connected%3A1 player_ip%3A192.168.1.82%3A57702 power%3A1 signalstrength%3A0 mode%3Aplay time%3A19.4145948696136 rate%3A1 duration%3A228.106 can_seek%3A1 mixer%20volume%3A32 playlist%20repeat%3A0 playlist%20shuffle%3A0 playlist%20mode%3Aoff seq_no%3A0 playlist_cur_index%3A8 playlist_timestamp%3A1515551291.82482 playlist_tracks%3A11 digital_volume_control%3A1 playlist%20index%3A8 id%3A8691 title%3ACryin\'%20In%20Your%20Beer playlist%20index%3A9 id%3A8692 title%3ABoy%20On%20A%20Bike'))
