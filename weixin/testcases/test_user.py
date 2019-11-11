import json
import logging
import time
from jsonschema import validate
import pystache
import requests
import pytest
#from contact.weixin_token import Weixin
from contact.user import User
from contact.utils import Utils


class TestUser:
    depart_id = 1

    def setup_class(self):
        print("setup_class(self)：每个类之前执行一次")


    def teardown_class(self):
        print("teardown_class(self)：每个类之后执行一次")

    @classmethod
    def setup_class(cls):
        # todo: create depart
        cls.user = User()

    #方法1：字段由少递增测试
    def test_create(self):
        uid = "seveniruby_" + str(time.time())
        data = {
            "userid": uid,
            "name": uid,
            "department": [self.depart_id],
            "email": uid + "@testerhome.com"
        }
        r = self.user.create(data)
        logging.debug(r)
        assert r['errcode'] == 0

    #方法2：模版测试
    #测试创建
    def test_create_by_template(self):
        uid="seveniruby_" + str(time.time())
        mobile = str(time.time()).replace(".","")[0:11]
        data=str(Utils.parse("../contact/user_create.json",{
            "name":uid,
            "title":"校长",
            "email":mobile+"@qq.com",
            "mobile":mobile
        }))
        data = data.encode("UTF-8")
        r = self.user.create(data=data)
        #logging.debug(r)
        assert r["errcode"] == 0

    def test_create_base(self):
        sch = json.load(open("../contact/list_schema.json"))
        ins = json.load(open("../contact/user_create_sh.json"))
        # 两部分做对比，参数：实际返回结果，schema文件
        validate(instance=ins, schema=sch)

    #更新用户信息
    def test_update_by_template(self):
        uid = 'seveniruby_1565665944.295618'
        mobile = str(time.time()).replace('.','')[0:11]
        data = str(Utils.parse('../contact/user_create.json',{
            "name":uid,
            "title":"副校长",
            "email":mobile+"@qq.com",
            "mobile":mobile
        }))
        data=data.encode("UTF-8")
        r=self.user.update(data=data)
        assert r["errcode"] == 0

    def test_list(self):
        r = self.user.list()
        print(r)
        #logging.debug(r)

    @pytest.mark.parametrize("userid",[
        'ZhuCuiXue',
        'seveniruby_1565665944.295618'
    ])
    def test_get_user(self,userid):
        r = self.user.get_user(userid)
        assert r["errcode"] == 0


    def test_delete(self):
        userid = "ceshi_" + str(time.time())
        mobile = str(time.time()).replace(".", "")[0:11]
        data = str(Utils.parse("../contact/user_create.json", {
            "name": userid,
            "title": "测试删除",
            "email": mobile + "@qq.com",
            "mobile": mobile
        }))
        data = data.encode("UTF-8")
        r = self.user.create(data=data)
        r = self.user.delete(userid)
        assert r["errcode"] == 0
        assert r["errmsg"] == 'deleted'

    def test_batchdelete(self):
        # userlist = []
        # for i in range(3):
        #     userid = "batchdelete_" + str(i)
        #     mobile = str(time.time()).replace(".", "")[0:11]
        #     data = str(Utils.parse("../contact/user_create.json", {
        #         "name": userid,
        #         "title": "测试批量删除",
        #         "email": mobile + "@qq.com",
        #         "mobile": mobile
        #     }))
        #     data = data.encode("UTF-8")
        #     self.user.create(data=data)
        #     userlist.append(userid)
        # userlist = ['batchdelete_2','batchdelete_1']
        # data= {"useridlist":userlist}
        # r = self.user.batchdelete(userlist)
        # print(r)
        # assert r["errcode"] == 0
        # assert r["errmsg"] == 'deleted'
        self.user.batchdelete()













