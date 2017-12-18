from unittest import TestCase
from unittest.mock import MagicMock,patch

from telnetlib import Telnet

from juice import Player, get_players, get_player_name, get_player_id

class TestGetPlayers(TestCase):
  def test_no_players(self):
    with patch('juice.players.get_player_count', return_value=0):
      self.assertEqual([], get_players(None))

  def test_multiple_players(self):
    with patch('juice.players.get_player_count', return_value=3), \
         patch('juice.players.get_player_name',
               side_effect=['Lounge','Kitchen','Dining Room']), \
         patch('juice.players.get_player_id',
               side_effect=['00:12:34:56:78:90','01:12:34:56:78:90',
                            '02:12:34:56:78:90']):
      self.assertEqual([Player(0,'Lounge','00:12:34:56:78:90'),
                       Player(1,'Kitchen','01:12:34:56:78:90'),
                       Player(2,'Dining Room','02:12:34:56:78:90')],
                      get_players(None))

    
class TestGetPlayerInfo(TestCase):
  def setUp(self):
    self.tn = Telnet()
    self.tn.write = MagicMock('write')
    self.tn.read_until = MagicMock('read')

  def test_name_valid_index(self):
    self.tn.read_until.return_value = b'player name 1 Lounge\n'
    self.assertEqual('Lounge', get_player_name(self.tn,1))
    self.tn.write.assert_called_once_with(b'player name 1 ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')

  def test_name_invalid_index(self):
    self.tn.read_until.return_value = b'player name 99\n'
    with self.assertRaises(IndexError):
      get_player_name(self.tn,99)
    self.tn.write.assert_called_once_with(b'player name 99 ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')

  def test_id(self):
    self.tn.read_until.return_value = b'player id 2 00:12:34:56:78:90\n'
    self.assertEqual('00:12:34:56:78:90', get_player_id(self.tn,2))
    self.tn.write.assert_called_once_with(b'player id 2 ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')
