from unittest import TestCase
from unittest.mock import MagicMock, patch
from telnetlib import Telnet

from juice import get_playing_track, get_current_playlist

class TestCurrentPlaylist(TestCase):
  def setUp(self):
    self.tn = Telnet()
    self.tn.write = MagicMock('write')
    self.tn.read_until = MagicMock('read')

  def test_radio(self):
    self.tn.read_until.return_value = \
     b"00%3A04%3A20%3A17%3A4b%3A3b status 0 9999 tags%3Ala player_name%3AKitchen player_connected%3A1 player_ip%3A192.168.1.75%3A25329 power%3A1 signalstrength%3A68 mode%3Astop remote%3A1 current_title%3Acapital%20UK time%3A0 rate%3A1 mixer%20volume%3A25 playlist%20repeat%3A0 playlist%20shuffle%3A0 playlist%20mode%3Aoff seq_no%3A0 playlist_cur_index%3A0 playlist_timestamp%3A1513669016.13007 playlist_tracks%3A1 digital_volume_control%3A1 remoteMeta%3AHASH(0x62e0cb8) playlist%20index%3A0 id%3A-103741560 title%3ANew%20Rules artist%3ADua%20Lipa"
    self.assertEqual([{'title': "New Rules", 'artist': "Dua Lipa"}],
                     get_current_playlist(self.tn,'00:04:20:17:4b:3b'))
    self.tn.write.assert_called_once_with(b"00:04:20:17:4b:3b status 0 9999 tags:al\n")
    self.tn.read_until.assert_called_once_with(b'\n')

  def test_partially_played(self):
    self.maxDiff=None
    self.tn.read_until.return_value = \
      b"00%3A0f%3A55%3Aa6%3A65%3Ae5 status 0 9999 tags%3Ala player_name%3ADining%20Room player_connected%3A1 player_ip%3A192.168.1.114%3A40788 power%3A1 signalstrength%3A0 mode%3Astop time%3A0 rate%3A1 duration%3A361.853 can_seek%3A1 mixer%20volume%3A49 playlist%20repeat%3A0 playlist%20shuffle%3A0 playlist%20mode%3Aoff seq_no%3A0 playlist_cur_index%3A25 playlist_timestamp%3A1513650517.74163 playlist_tracks%3A31 digital_volume_control%3A1 playlist%20index%3A0 id%3A8204 title%3AAin't%20Got%20You album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A1 id%3A8205 title%3ATougher%20Than%20the%20Rest album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A2 id%3A8206 title%3AAll%20That%20Heaven%20Will%20Allow album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A3 id%3A8207 title%3ASpare%20Parts album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A4 id%3A8208 title%3ACautious%20Man album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A5 id%3A8209 title%3AWalk%20Like%20A%20Man album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A6 id%3A8210 title%3ATunnel%20of%20Love album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A7 id%3A8211 title%3ATwo%20Faces album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A8 id%3A8212 title%3ABrilliant%20Disguise album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A9 id%3A8213 title%3AOne%20Step%20Up album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A10 id%3A8214 title%3AWhen%20You're%20Alone album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A11 id%3A8215 title%3AValentine's%20Day album%3ATunnel%20Of%20Love artist%3ABruce%20Springsteen playlist%20index%3A12 id%3A1253 title%3ABetter%20Days album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A13 id%3A1255 title%3ALucky%20Town album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A14 id%3A1256 title%3ALocal%20Hero album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A15 id%3A1257 title%3AIf%20I%20Should%20Fall%20Behind album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A16 id%3A1258 title%3ALeap%20of%20Faith album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A17 id%3A1259 title%3AThe%20Big%20Muddy album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A18 id%3A1260 title%3ALiving%20Proof album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A19 id%3A1261 title%3ABook%20of%20Dreams album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A20 id%3A1262 title%3ASouls%20of%20the%20Departed album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A21 id%3A1254 title%3AMy%20Beautiful%20Reward album%3ALucky%20Town artist%3ABruce%20Springsteen playlist%20index%3A22 id%3A5642 title%3AYou%20Take%20Me%20as%20I%20Am album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A23 id%3A5643 title%3AFarewell%20Appalachia album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A24 id%3A5644 title%3AThe%20Bigger%20Picture album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A25 id%3A5645 title%3A(A%20Belated)%20Invite%20to%20Eternity album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A26 id%3A5646 title%3AHook%2C%20Line%2C%20Sinker album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A27 id%3A5647 title%3AKnock%20Me%20on%20the%20Head album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A28 id%3A5648 title%3AThe%20Great%20Procrastinator album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A29 id%3A5649 title%3AThe%20Ones%20We%20Hurt%20the%20Most album%3ATales%20From%20Terra%20Firma artist%3AStornoway playlist%20index%3A30 id%3A5650 title%3ANovember%20Song album%3ATales%20From%20Terra%20Firma artist%3AStornoway\n"
    self.assertEqual([{'title': "Ain't Got You", 'album': "Tunnel Of Love", 'artist': "Bruce Springsteen"},
      {'title': "Tougher Than the Rest", 'album': "Tunnel Of Love", 'artist': "Bruce Springsteen"},
      {'title': "All That Heaven Will Allow", 'album': "Tunnel Of Love", 'artist': "Bruce Springsteen"},
      {'title': "Spare Parts", 'album': "Tunnel Of Love", 'artist': "Bruce Springsteen"},
      {'title': "Cautious Man", 'album': "Tunnel Of Love", 'artist': "Bruce Springsteen"},
      {'title': "Walk Like A Man", 'album': "Tunnel Of Love", 'artist': "Bruce Springsteen"},
      {'title': "Tunnel of Love", 'album': "Tunnel Of Love", 'artist': "Bruce Springsteen"},
      {'title': "Two Faces", 'album': "Tunnel Of Love", 'artist': "Bruce Springsteen"},
      {'title': "Brilliant Disguise", 'album': "Tunnel Of Love", 'artist': "Bruce Springsteen"},
      {'title': "One Step Up", 'album': "Tunnel Of Love", 'artist': "Bruce Springsteen"},
      {'title': "When You're Alone", 'album': "Tunnel Of Love", 'artist': "Bruce Springsteen"},
      {'title': "Valentine's Day", 'album': "Tunnel Of Love", 'artist': "Bruce Springsteen"},
      {'title': "Better Days", 'album': "Lucky Town", 'artist': "Bruce Springsteen"},
      {'title': "Lucky Town", 'album': "Lucky Town", 'artist': "Bruce Springsteen"},
      {'title': "Local Hero", 'album': "Lucky Town", 'artist': "Bruce Springsteen"},
      {'title': "If I Should Fall Behind", 'album': "Lucky Town", 'artist': "Bruce Springsteen"},
      {'title': "Leap of Faith", 'album': "Lucky Town", 'artist': "Bruce Springsteen"},
      {'title': "The Big Muddy", 'album': "Lucky Town", 'artist': "Bruce Springsteen"},
      {'title': "Living Proof", 'album': "Lucky Town", 'artist': "Bruce Springsteen"},
      {'title': "Book of Dreams", 'album': "Lucky Town", 'artist': "Bruce Springsteen"},
      {'title': "Souls of the Departed", 'album': "Lucky Town", 'artist': "Bruce Springsteen"},
      {'title': "My Beautiful Reward", 'album': "Lucky Town", 'artist': "Bruce Springsteen"},
      {'title': "You Take Me as I Am", 'album': "Tales From Terra Firma", 'artist': "Stornoway"},
      {'title': "Farewell Appalachia", 'album': "Tales From Terra Firma", 'artist': "Stornoway"},
      {'title': "The Bigger Picture", 'album': "Tales From Terra Firma", 'artist': "Stornoway"},
      {'title': "(A Belated) Invite to Eternity", 'album': "Tales From Terra Firma", 'artist': "Stornoway"},
      {'title': "Hook, Line, Sinker", 'album': "Tales From Terra Firma", 'artist': "Stornoway"},
      {'title': "Knock Me on the Head", 'album': "Tales From Terra Firma", 'artist': "Stornoway"},
      {'title': "The Great Procrastinator", 'album': "Tales From Terra Firma", 'artist': "Stornoway"},
      {'title': "The Ones We Hurt the Most", 'album': "Tales From Terra Firma", 'artist': "Stornoway"},
      {'title': "November Song", 'album': "Tales From Terra Firma", 'artist': "Stornoway"}],
                     get_current_playlist(self.tn,'00:0f:55:a6:65:e5'))
    self.tn.write.assert_called_once_with(b'00:0f:55:a6:65:e5 status 0 9999 tags:al\n')
    self.tn.read_until.assert_called_once_with(b'\n')

