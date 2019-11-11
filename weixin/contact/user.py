import requests
from contact.weixin_token import Weixin


class User():
    #创建用户
    def create(self,dict=None,data=None):
        #同时有dict和data两种参数，是因为入参数类型不一定，有可能是字典或者是字符串
        #例如：以模版转化过来的数据就是字符串/json
        return requests.post("https://qyapi.weixin.qq.com/cgi-bin/user/create",
                          params={"access_token": Weixin.get_token()},
                          json=dict,
                          data=data
                          ).json()

    def update(self,dict=None,data=None):
        return requests.post("https://qyapi.weixin.qq.com/cgi-bin/user/update",
                             params={"access_token": Weixin.get_token()},
                             json=dict,
                             data=data
                             ).json()


    #获取部门用户列表
    def list(self, department_id=1, fetch_child=0, **kwards):
        return requests.get("https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?",
                            params={"access_token": Weixin.get_token(),
                                    "department_id": department_id,
                                    "fetch_child": fetch_child
                                 }).json()

    #读取成员
    def get_user(self, userid):
        return requests.get("https://qyapi.weixin.qq.com/cgi-bin/user/get",
                            params={"access_token": Weixin.get_token(),
                                    "userid":userid}).json()
    #单个删除
    def delete( self, userid):
        return requests.get("https://qyapi.weixin.qq.com/cgi-bin/user/delete",
                            params={"access_token": Weixin.get_token(),
                                    "userid": userid}).json()

    #批量删除
    def batchdelete(self):
        # return requests.post("https://qyapi.weixin.qq.com/cgi-bin/user/batchdelete",
        #                     params={"access_token": Weixin.get_token()},
        #                     data=data).json()
        r = requests.post("https://qyapi.weixin.qq.com/cgi-bin/user/batchdelete",
                             params={"access_token": Weixin.get_token()},
                             data={"userlist":['batchdelete_2','batchdelete_1']}
                             ).json()
        print(r)