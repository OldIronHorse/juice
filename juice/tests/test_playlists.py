from unittest import TestCase
from unittest.mock import MagicMock
from telnetlib import Telnet

from juice import get_playing_title

class TestNowPlaying(TestCase):
  def setUp(self):
    self.tn = Telnet()
    self.tn.write = MagicMock('write')
    self.tn.read_until = MagicMock('read')

  #def test_valid_player_full_track(self):
    #self.assertEqual(Track('Hook, Line & Sinker',
                           #'Tales From Terra Firma',
                           #'Stornoway'),
                     #get_now_playing(None,2))

  def test_playing_title(self):
    self.tn.read_until.return_value = \
      b'02:blah:blah title Tales%20From%20Terra%20Firma'
    self.assertEqual('Tales From Terra Firma',
                     get_playing_title(self.tn,'02:blah:blah'))
    self.tn.write.assert_called_once_with(b'02:blah:blah title ?\n')
    self.tn.read_until.assert_called_once_with(b'\n')
