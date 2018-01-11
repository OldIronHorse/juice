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

