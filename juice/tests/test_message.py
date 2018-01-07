from unittest import TestCase
from unittest.mock import MagicMock,patch

from juice.message import parse_msg, InvalidMsgException,\
  parse_login, parse_listen, parse_subscribe

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

