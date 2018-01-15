from unittest import TestCase
from unittest.mock import MagicMock
from telnetlib import Telnet

from juice import Artist, get_artists

class TestWithCLI(TestCase):
  def setUp(self):
    self.tn = Telnet();
    self.tn.write = MagicMock('write')
    self.tn.read_until = MagicMock('read_until')


class TestGetArtists(TestWithCLI):
  def test_all_artists(self):
    self.maxDiff=None
    self.tn.read_until.return_value = \
      b"artists 0 9999 id%3A1024 artist%3A5%20Seconds%20of%20Summer id%3A92 artist%3A6%20Notes id%3A725 artist%3A702 id%3A954 artist%3A98%20Degrees id%3A732 artist%3AAaliyah id%3A660 artist%3AABBA id%3A89 artist%3AAbigail%20Washburn id%3A1283 artist%3AColonel%20Abrams id%3A189 artist%3AAceface id%3A1326 artist%3AOleta%20Adams count%3A10\n"
    self.assertEqual([Artist(id=1024, name="5 Seconds of Summer"),
                      Artist(id=92, name="6 Notes"),
                      Artist(id=725, name="702"),
                      Artist(id=954, name="98 Degrees"),
                      Artist(id=732, name="Aaliyah"),
                      Artist(id=660, name="ABBA"),
                      Artist(id=89, name="Abigail Washburn"),
                      Artist(id=1283, name="Colonel Abrams"),
                      Artist(id=189, name="Aceface"),
                      Artist(id=1326, name="Oleta Adams")],
                     get_artists(self.tn))
    self.tn.read_until.assert_called_once_with(b'\n')
    self.tn.write.assert_called_once_with(b'artists 0 9999\n')


