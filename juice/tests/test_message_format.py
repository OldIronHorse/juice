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


