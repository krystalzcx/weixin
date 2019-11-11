import requests
import yaml
import logging

class Weixin:
    #logging.basicConfig(level=logging.DEBUG)
    #类变量，默认值
    _token=''
    @classmethod
    def get_token(cls):
        if len(cls._token)== 0:
            cls._token=cls.get_token_new()
        return cls._token

    @classmethod
    def get_token_new(cls):
        conf = yaml.safe_load(open("../contact/weixin.yml"))
        #logging.debug(conf["env"])
        r = requests.get("https://qyapi.weixin.qq.com/cgi-bin/gettoken",
                         params={"corpid": conf["env"]["corpid"], "corpsecret": conf["env"]["secret"]}).json()
        print(r["access_token"])
        return r["access_token"]








