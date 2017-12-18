from unittest import TestCase
from unittest.mock import MagicMock, patch
from telnetlib import Telnet

from juice import get_playing_title, get_playing_album, get_playing_artist, \
  get_playing_track, Track

class TestNowPlaying(TestCase):
  def setUp(self):
    self.tn = Telnet()
    self.tn.write = MagicMock('write')
    self.tn.read_until = MagicMock('read')

  def test_valid_player_full_track(self):
    with patch('juice.playlists.get_playing_title', 
               return_value='Hook, Line, Sinker') as title, \
         patch('juice.playlists.get_playing_artist',
               return_value='Stornoway') as artist, \
         patch('juice.playlists.get_playing_album',
               return_value='Tales From Terra Firma') as album:
      self.assertEqual(Track('Hook, Line, Sinker',
                             'Tales From Terra Firma',
                             'Stornoway'),
                       get_playing_track(None,'02:blah:blah'))
      title.assert_called_once_with(None,'02:blah:blah')
      album.assert_called_once_with(None,'02:blah:blah')
      artist.assert_called_once_with(None,'02:blah:blah')

  def test_valid_player_no_album(self):
    with patch('juice.playlists.get_playing_title', 
               return_value='Hook, Line, Sinker') as title, \
         patch('juice.playlists.get_playing_artist',
               return_value='Stornoway') as artist, \
         patch('juice.playlists.get_playing_album',
               return_value=None) as album:
      self.assertEqual(Track('Hook, Line, Sinker',
                             None,
                             'Stornoway'),
                       get_playing_track(None,'02:blah:blah'))
      title.assert_called_once_with(None,'02:blah:blah')
      album.assert_called_once_with(None,'02:blah:blah')
      artist.assert_called_once_with(None,'02:blah:blah')

  def test_playing_album(self):
    self.tn.read_until.return_value = \
      b'02:blah:blah album Tales%20From%20Terra%20Firma\n'
    self.assertEqual('Tales From Terra Firma',
                     get_playing_album(self.tn,'02:blah:blah'))
    self.tn.write.assert_called_once_with(b'02:blah:blah album ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')

  def test_playing_no_album(self):
    self.tn.read_until.return_value = b'02:blah:blah album\n'
    self.assertIsNone(get_playing_album(self.tn,'02:blah:blah'))
    self.tn.write.assert_called_once_with(b'02:blah:blah album ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')

  def test_playing_title(self):
    self.tn.read_until.return_value = \
      b'02:blah:blah title Hook%2C%20Line%2C%20Sinker\n'
    self.assertEqual('Hook, Line, Sinker',
                     get_playing_title(self.tn,'02:blah:blah'))
    self.tn.write.assert_called_once_with(b'02:blah:blah title ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')

  def test_playing_artist(self):
    self.tn.read_until.return_value = \
      b'02:blah:blah arist Stornoway'
    self.assertEqual('Stornoway',
                     get_playing_artist(self.tn,'02:blah:blah'))
    self.tn.write.assert_called_once_with(b'02:blah:blah artist ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')

    
