import requests
from contact.weixin_token  import Weixin

class Department():


    def create(self,dict=None,data=None):
        return requests.post("https://qyapi.weixin.qq.com/cgi-bin/department/create",
                          params={"access_token": Weixin.get_token()},
                          json=dict,
                          data=data
                          ).json()

    def update(self,data=None):
        return requests.post("https://qyapi.weixin.qq.com/cgi-bin/department/update",
                            params={"access_token": Weixin.get_token()},
                            data=data).json()

    def list(self,id=None):
        return requests.get("https://qyapi.weixin.qq.com/cgi-bin/department/list",
                     params={"access_token": Weixin.get_token(),
                             "id": id}).json()

    def delete(self,id=None):
        return requests.get("https://qyapi.weixin.qq.com/cgi-bin/department/delete",
                            params={"access_token": Weixin.get_token(),
                                    "id": id}).json()

