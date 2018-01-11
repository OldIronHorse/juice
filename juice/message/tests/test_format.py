from unittest import TestCase

import juice.message.format as msg_format

class TestLogin(TestCase):
  def test_kwarg(self):
    self.assertEqual('login myname mypassword\n',
      msg_format.login(user='myname', password='mypassword'))

  def test_positional(self):
    self.assertEqual('login myname mypassword\n',
      msg_format.login('myname', 'mypassword'))

