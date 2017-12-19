from unittest import TestCase
from unittest.mock import MagicMock, patch
from telnetlib import Telnet

from juice import get_playing_title, get_playing_album, get_playing_artist, \
  get_playing_track, Track, get_current_playlist

class TestCurrentPlaylist(TestCase):
  def setUp(self):
    self.tn = Telnet()
    self.tn.write = MagicMock('write')
    self.tn.read_until = MagicMock('read')

  def test_partially_played(self):
    self.maxDiff=None
    self.tn.read_until.return_value = \
      b"00%3A0f%3A55%3Aa6%3A65%3Ae5 status 0 9999 tags%3Ala player_name%3ADining%20Room player_connected%3A1 player_ip%3A192.168.1.114%3A40788 power%3A1 signalstrength%3A0 mode%3Astop time%3A0 rate%3A1 duration%3A361.853 can_seek%3A1 mixer%20volume%3A49 playlist%20repeat%3A0 playlist%20shuffle%3A0 playlist%20mode%3Aoff seq_no%3A0 playlist_cur_index%3A25 playlist_timestamp%3A1513650517.74163 playlist_tracks%3A31 digital_volume_control%3A1 playlist%20index%3A0 id%3A8204 title%3AAin't%20Got%20You album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A1 id%3A8205 title%3ATougher%20Than%20the%20Rest album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A2 id%3A8206 title%3AAll%20That%20Heaven%20Will%20Allow album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A3 id%3A8207 title%3ASpare%20Parts album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A4 id%3A8208 title%3ACautious%20Man album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A5 id%3A8209 title%3AWalk%20Like%20A%20Man album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A6 id%3A8210 title%3ATunnel%20of%20Love album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A7 id%3A8211 title%3ATwo%20Faces album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A8 id%3A8212 title%3ABrilliant%20Disguise album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A9 id%3A8213 title%3AOne%20Step%20Up album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A10 id%3A8214 title%3AWhen%20You're%20Alone album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A11 id%3A8215 title%3AValentine's%20Day album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A12 id%3A1253 title%3ABetter%20Days album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A13 id%3A1255 title%3ALucky%20Town album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A14 id%3A1256 title%3ALocal%20Hero album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A15 id%3A1257 title%3AIf%20I%20Should%20Fall%20Behind album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A16 id%3A1258 title%3ALeap%20of%20Faith album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A17 id%3A1259 title%3AThe%20Big%20Muddy album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A18 id%3A1260 title%3ALiving%20Proof album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A19 id%3A1261 title%3ABook%20of%20Dreams album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A20 id%3A1262 title%3ASouls%20of%20the%20Departed album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A21 id%3A1254 title%3AMy%20Beautiful%20Reward album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A22 id%3A5642 title%3AYou%20Take%20Me%20as%20I%20Am album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A23 id%3A5643 title%3AFarewell%20Appalachia album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A24 id%3A5644 title%3AThe%20Bigger%20Picture album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A25 id%3A5645 title%3A(A%20Belated)%20Invite%20to%20Eternity album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A26 id%3A5646 title%3AHook%2C%20Line%2C%20Sinker album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A27 id%3A5647 title%3AKnock%20Me%20on%20the%20Head album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A28 id%3A5648 title%3AThe%20Great%20Procrastinator album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A29 id%3A5649 title%3AThe%20Ones%20We%20Hurt%20the%20Most album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A30 id%3A5650 title%3ANovember%20Song album%3ATales%20From%20Terra%20Firma artist%3AStornoway\n"
    self.assertEqual([Track("Ain't Got You", "Tunnel Of Love", "Bruce Springsteen"),
      Track("Tougher Than the Rest", "Tunnel Of Love", "Bruce Springsteen"),
      Track("All That Heaven Will Allow", "Tunnel Of Love", "Bruce Springsteen"),
      Track("Spare Parts", "Tunnel Of Love", "Bruce Springsteen"),
      Track("Cautious Man", "Tunnel Of Love", "Bruce Springsteen"),
      Track("Walk Like A Man", "Tunnel Of Love", "Bruce Springsteen"),
      Track("Tunnel of Love", "Tunnel Of Love", "Bruce Springsteen"),
      Track("Two Faces", "Tunnel Of Love", "Bruce Springsteen"),
      Track("Brilliant Disguise", "Tunnel Of Love", "Bruce Springsteen"),
      Track("One Step Up", "Tunnel Of Love", "Bruce Springsteen"),
      Track("When You're Alone", "Tunnel Of Love", "Bruce Springsteen"),
      Track("Valentine's Day", "Tunnel Of Love", "Bruce Springsteen"),
      Track("Better Days", "Lucky Town", "Bruce Springsteen"),
      Track("Lucky Town", "Lucky Town", "Bruce Springsteen"),
      Track("Local Hero", "Lucky Town", "Bruce Springsteen"),
      Track("If I Should Fall Behind", "Lucky Town", "Bruce Springsteen"),
      Track("Leap of Faith", "Lucky Town", "Bruce Springsteen"),
      Track("The Big Muddy", "Lucky Town", "Bruce Springsteen"),
      Track("Living Proof", "Lucky Town", "Bruce Springsteen"),
      Track("Book of Dreams", "Lucky Town", "Bruce Springsteen"),
      Track("Souls of the Departed", "Lucky Town", "Bruce Springsteen"),
      Track("My Beautiful Reward", "Lucky Town", "Bruce Springsteen"),
      Track("You Take Me as I Am", "Tales From Terra Firma", "Stornoway"),
      Track("Farewell Appalachia", "Tales From Terra Firma", "Stornoway"),
      Track("The Bigger Picture", "Tales From Terra Firma", "Stornoway"),
      Track("(A Belated) Invite to Eternity", "Tales From Terra Firma", "Stornoway"),
      Track("Hook, Line, Sinker", "Tales From Terra Firma", "Stornoway"),
      Track("Knock Me on the Head", "Tales From Terra Firma", "Stornoway"),
      Track("The Great Procrastinator", "Tales From Terra Firma", "Stornoway"),
      Track("The Ones We Hurt the Most", "Tales From Terra Firma", "Stornoway"),
      Track("November Song", "Tales From Terra Firma", "Stornoway")],
                     get_current_playlist(self.tn,'00:0f:55:a6:65:e5'))
    self.tn.write.assert_called_once_with(b'00:0f:55:a6:65:e5 status 0 9999 tags:la\n')
    self.tn.read_until.assert_called_once_with(b'\n')


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

    
