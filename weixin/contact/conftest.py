#pytest的功能，一些特性功能放在这个文件里
import  pytest


from contact.weixin_token import Weixin



#只执行一次
@pytest.fixture(scope="session")
def token():

    return Weixin.get_token_new()


