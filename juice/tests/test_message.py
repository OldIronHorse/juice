from unittest import TestCase
from unittest.mock import MagicMock,patch

from juice.message import parse_msg, InvalidMsgException,\
  parse_login, parse_listen, parse_subscribe, parse_player, parse_id

class TestLogin(TestCase):
  def test_valid(self):
    self.assertEqual({
        'command': 'login',
        'user': 'myusername'
      },
      parse_login('login myusername ******'))

  def test_missing_field(self):
    with self.assertRaises(InvalidMsgException):
      parse_login('login myusername')

  def test_wrong_value(self):
    with self.assertRaises(InvalidMsgException):
      parse_login('login myusername an_unexpected_value')


class TestListen(TestCase):
  def test_valid_0(self):
    self.assertEqual({
        'command': 'listen',
        'value' : 0,
      },
      parse_listen('listen 0'))

  def test_valid_1(self):
    self.assertEqual({
        'command': 'listen',
        'value' : 1,
      },
      parse_listen('listen 1'))

  def test_invalid_value(self):
    with self.assertRaises(InvalidMsgException):
      parse_listen('listen 2')

  def test_invalid_value_type(self):
    with self.assertRaises(InvalidMsgException):
      parse_listen('listen not_listening')

  def test_missing_field(self):
    with self.assertRaises(InvalidMsgException):
      parse_listen('listen')

class TestSubscribe(TestCase):
  def test_valid_single(self):
    self.assertEqual({
        'command': 'subscribe',
        'notifications': ['mixer'],
      },
      parse_subscribe('subscribe mixer'))

  def test_valid_multiple(self):
    self.assertEqual({
        'command': 'subscribe',
        'notifications': ['mixer', 'pause', 'play'],
      },
      parse_subscribe('subscribe mixer,pause,play'))

class TestPlayer(TestCase):
  def test_count_valid(self):
    self.assertEqual({
        'command': 'player',
        'count': 4
      },
      parse_player('player count 4'))

  def test_id_valid(self):
    self.assertEqual({
      'command': 'player',
      'index': 1,
      'id': '00:0f:55:a6:65:e5',
    },
    parse_player('player id 1 00%3A0f%3A55%3Aa6%3A65%3Ae5'))

  def test_uuid_valid(self):
    self.assertEqual({
      'command': 'player',
      'index': 0,
      'uuid': '012345678901234567890123456789012',
    },
    parse_player('player uuid 0 012345678901234567890123456789012'))

  def test_name_valid(self):
    self.assertEqual({
      'command': 'player',
      'index': 2,
      'name': 'Dining Room',
    },
    parse_player('player name 2 Dining%20Room'))
    
  def test_ip_valid(self):
    self.assertEqual({
      'command': 'player',
      'index': 0,
      'ip': '192.168.1.22:3483',
    },
    parse_player('player ip 0 192.168.1.22:3483'))

  def test_ip_id(self):
    self.assertEqual({
      'command': 'player',
      'id': '00:0f:55:a6:65:e5',
      'ip': '192.168.1.22:3483',
    },
    parse_player('player ip 00%3A0f%3A55%3Aa6%3A65%3Ae5 192.168.1.22:3483'))
    
  def test_model_valid(self):
    self.assertEqual({
      'command': 'player',
      'index': 0,
      'model': 'squeezelite',
    },
    parse_player('player model 0 squeezelite'))

  def test_isplayer(self):
    self.assertEqual({
      'command': 'player',
      'index': 1,
      'isplayer': 0,
    },
    parse_player('player isplayer 1 0'))

class TestPlayerId(TestCase):
  def test_signalstrength(self):
    self.assertEqual({
      'id': '00:04:20:23:30:7f',
      'signalstrength': 62,
    },
    parse_id('00%3A04%3A20%3A23%3A30%3A7f signalstrength 62'))

  def test_name(self):
    self.assertEqual({
      'id': '00:04:20:23:30:7f',
      'name': 'Dining Room',
    },
    parse_id('00%3A04%3A20%3A23%3A30%3A7f name Dining%20Room'))



class TestParseMsg(TestCase):
  def test_unknown_cmd(self):
    with self.assertRaises(InvalidMsgException):
      parse_msg('not_a_cmd some more stuff')

  def test_valid_login(self):
    self.assertEqual({
        'command': 'login',
        'user': 'myusername'
      },
      parse_msg('login myusername ******'))
  
  def test_valid_listen(self):
    self.assertEqual({
        'command': 'listen',
        'value' : 0,
      },
      parse_msg('listen 0'))

  def test_valid_subscribe(self):
    self.assertEqual({
        'command': 'subscribe',
        'notifications': ['mixer', 'pause', 'play'],
      },
      parse_msg('subscribe mixer,pause,play'))

  def test_valid_player_count(self):
    self.assertEqual({
        'command': 'player',
        'count': 4
      },
      parse_msg('player count 4'))

  def test_signalstrength(self):
    self.assertEqual({
      'id': '00:04:20:23:30:7f',
      'signalstrength': 62,
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f signalstrength 62'))

  def test_connected(self):
    self.assertEqual({
      'id': '00:04:20:23:30:7f',
      'connected': 1,
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f connected 1'))

  def test_sleep(self):
    self.assertEqual({
      'id': '00:04:20:23:30:7f',
      'sleep': 100.5,
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f sleep 100.5'))

  def test_sync_index(self):
    self.assertEqual({
      'id': '00:04:20:23:30:7f',
      'sync': 1,
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f sync 1'))

  def test_sync_id(self):
    self.assertEqual({
      'id': '00:04:20:23:30:7f',
      'sync': '00:04:20:23:30:70',
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f sync 00%3A04%3A20%3A23%3A30%3A70'))

  def test_sync_none(self):
    self.assertEqual({
      'id': '00:04:20:23:30:7f',
      'sync': '-',
    },
    parse_msg('00%3A04%3A20%3A23%3A30%3A7f sync -'))

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
