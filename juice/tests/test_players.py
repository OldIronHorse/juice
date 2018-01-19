from unittest import TestCase
from unittest.mock import MagicMock,patch

from telnetlib import Telnet

from juice import get_players, get_player_name, get_player_id, \
  play, pause, state, get_player_volume, set_player_volume

class TestWithServer(TestCase):
  def setUp(self):
    self.tn = Telnet()
    self.tn.write = MagicMock('write')
    self.tn.read_until = MagicMock('read')

class TestVolume(TestWithServer):
  def test_get_volume(self):
    self.tn.read_until.return_value=b'00:12:34:56:78:90 mixer volume 75\n'
    self.assertEqual(75,get_player_volume(self.tn,'00:12:34:56:78:90'))
    self.tn.write.assert_called_once_with(b'00:12:34:56:78:90 mixer volume ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')

  def test_set_volume_set(self):
    self.tn.read_until.return_value=b'00:12:34:56:78:90 mixer volume 75\n'
    set_player_volume(self.tn,'00:12:34:56:78:90', 75)
    self.tn.write.assert_called_once_with(b'00:12:34:56:78:90 mixer volume 75\n')
    self.tn.read_until.assert_called_once_with(b'\n')
    
  def test_set_volume_inc(self):
    self.tn.read_until.return_value=b'00:12:34:56:78:90 mixer volume +15\n'
    set_player_volume(self.tn,'00:12:34:56:78:90', '+15')
    self.tn.write.assert_called_once_with(b'00:12:34:56:78:90 mixer volume +15\n')
    self.tn.read_until.assert_called_once_with(b'\n')
    
  def test_set_volume_dec(self):
    self.tn.read_until.return_value=b'00:12:34:56:78:90 mixer volume -15\n'
    set_player_volume(self.tn,'00:12:34:56:78:90', '-15')
    self.tn.write.assert_called_once_with(b'00:12:34:56:78:90 mixer volume -15\n')
    self.tn.read_until.assert_called_once_with(b'\n')
    


class TestState(TestWithServer):
  def test_invalid_id(self):
    self.tn.read_until.return_value = b'00:12:34:56:78:90 mode \0x3f\n'
    with self.assertRaises(ValueError):
      state(self.tn,'00:12:34:56:78:90')
    self.tn.write.assert_called_once_with(b'00:12:34:56:78:90 mode ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')

  def test_play(self):
    self.tn.read_until.return_value = b'00:12:34:56:78:90 mode play\n'
    self.assertEqual('play', state(self.tn,'00:12:34:56:78:90'))
    self.tn.write.assert_called_once_with(b'00:12:34:56:78:90 mode ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')

  def test_pause(self):
    self.tn.read_until.return_value = b'00:12:34:56:78:90 mode pause\n'
    self.assertEqual('pause', state(self.tn,'00:12:34:56:78:90'))
    self.tn.write.assert_called_once_with(b'00:12:34:56:78:90 mode ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')

  def test_stop(self):
    self.tn.read_until.return_value = b'00:12:34:56:78:90 mode stop\n'
    self.assertEqual('stop', state(self.tn,'00:12:34:56:78:90'))
    self.tn.write.assert_called_once_with(b'00:12:34:56:78:90 mode ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')


class TestControl(TestWithServer):
  def test_play(self):
    self.tn.read_until.return_value = b'00:12:34:56:78:90 play\n'
    play(self.tn,'00:12:34:56:78:90')
    self.tn.write.assert_called_once_with(b'00:12:34:56:78:90 play\n')
    self.tn.read_until.assert_called_once_with(b'\n')

  def test_pause(self):
    self.tn.read_until.return_value = b'00:12:34:56:78:90 pause\n'
    pause(self.tn,'00:12:34:56:78:90')
    self.tn.write.assert_called_once_with(b'00:12:34:56:78:90 pause\n')
    self.tn.read_until.assert_called_once_with(b'\n')
    

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
      self.assertEqual([{'index': 0, 'name': 'Lounge',
                         'id': '00:12:34:56:78:90'},
                        {'index': 1, 'name': 'Kitchen', 
                         'id': '01:12:34:56:78:90'},
                        {'index': 2, 'name': 'Dining Room', 
                         'id': '02:12:34:56:78:90'}],
                      get_players(None))

    
class TestGetPlayerInfo(TestWithServer):
  def test_name_valid_index(self):
    self.tn.read_until.return_value = b'player name 1 Lounge\n'
    self.assertEqual('Lounge', get_player_name(self.tn,1))
    self.tn.write.assert_called_once_with(b'player name 1 ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')

  def test_name_valid_index_space(self):
    self.tn.read_until.return_value = b'player name 1 Dining%20Room\n'
    self.assertEqual('Dining Room', get_player_name(self.tn,1))
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


