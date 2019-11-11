from unittest import TestCase

from contact.weixin_token import Weixin


class TestWeixin(TestCase):
    def test_get_token(self):
        print(Weixin.get_token())
        assert Weixin.get_token() != ""
        #self.fail()
