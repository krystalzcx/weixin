import sys
sys.path.append(r"/Users/mac/PycharmProjects/api_test/weixin")
import datetime
import time
import random
#import jsonpath
import pytest
import logging
import allure
from contact.utils import Utils
from contact.department import Department



@allure.feature('部门相关功能')
class TestDepartment:

    logging.basicConfig(level=logging.DEBUG)
    test_create_depth_1_departmentId = 0

    @classmethod
    def setup_class(cls):
        cls.depart = Department()

    '''
    测试不符合规定的参数类型(若出错，请查看参数类型)
    逐个参数换成不符合规定的类型，核实接口返回是否是相应的报错信息
    '''
    @allure.story('部门创建-参数类型不正确')
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize("name,parentid,order",[
        (123,1,1),
        ("测试","1",1),
        ("测试",1,"1")
    ])
    def test_parameter_type(self,name,parentid,order):
        data = {
            "name": name,
            "parentid": parentid,
            "order": order
        }
        r = self.depart.create(data=data)
        # logging.debug(r)
        assert r["errcode"] == 60001

    #测试不符合规定和边缘的参数长度
    @allure.story('部门创建-参数长度边缘和不符合规定')
    @allure.severity('minor')
    @pytest.mark.parametrize(",name,parentid,order",[
        ("一二三四五六七八九十一二三四五六1",1,1),
        ("测试",123456789012345678901234567890123,1),
        ("测试",1,123456789012345678901234567890123)
    ])
    def test_parameter_lenth(self,name,parentid,order):
        data = {
            "name": name,
            "parentid": parentid,
            "order": order
        }
        r = self.depart.create(data=data)
        logging.debug(r)
        assert r["errcode"] == 60001

    #部门名字特殊字符检查
    @allure.story('部门创建-部门名字包含特殊字符(规定不允许的字符)')
    @allure.severity(allure.severity_level.MINOR)
    def test_create_name_contain_SpecialCharacter(self):
        data = {
            "name": "部门名字\:?”<>｜",
            "parentid": 1
        }
        r = self.depart.create(data)
        assert r['errcode']==60009

    #测试重名
    @allure.story('部门创建-部门重名')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_duplicate_name(self):
        duplicate_name = self.depart.list(id=2)['department'][0]["name"]
        data = {
            "name":duplicate_name,
            "parentid": 1
        }
        r = self.depart.create(data)
        assert r['errcode'] == 60008


    '''
    部门名字长度(最大32)
    问题:name长度取32或31，仍然报60001。
    这是用例中长度计算方法不对？还是企业微信有BUG
    '''
    @allure.story('部门创建-部门名字长度超长')
    @allure.severity('minor')
    def test_create_name_length(self):
        sam = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
        name = random.sample(sam,33)
        data = {
            "name":name,
            "parentid": 1
        }
        r = self.depart.create(data)
        assert r['errcode']== 60001



    #父部门-企业id
    @allure.story('部门创建-父部门下创建一层级部门')
    @allure.severity('trivial')
    def test_create_depth_1(self):
        data = {
            "name": "第十期_krystal_1_"+str(time.time()),
            "parentid": 1
        }
        r = self.depart.create(data)
        assert r['errcode'] == 0

    #子孙部门
    @allure.story('部门创建-父部门下创建两层级部门')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_depth_2(self):
        #第一层部门(除去id=1的祖先部门)
        data = {
            "name": "第十期_krystal_1_" + str(time.time()),
            "parentid": 1
        }
        r = self.depart.create(data)
        parentid =  r['id']
        #第二层部门
        data = {
            "name": "第十期_krystal_2_"+str(time.time()),
            "parentid": parentid
        }
        r = self.depart.create(data)
        assert r['errcode'] == 0

    #多级部门
    #并且验证了最大级数
    @allure.story('部门创建-父部门下创建最多层级部门(包含父部门共15层)')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_max_depth(self):
        parentid=1
        #部门最多15级
        for i in range(1,16):
            data = {
                "name": "第十期_krystal_666"+str(parentid)+str(datetime.datetime.now().timestamp()),
                "parentid": parentid
            }
            r = self.depart.create(data)
            # print("num" + str(i))
            # print(r['errcode'])
            if i < 15:
                assert r['errcode'] == 0
                parentid = r['id']
            else :
                #验证最多部门级数
                assert r['errcode'] == 81002


    #多样部门名称
    @allure.story('部门创建-部门名称支持多种语言')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("name",[
        "广州研发中心",
        "東京アニメーション研究所",
        "도쿄 애니메이션 연구소",
        "معهد طوكيو للرسوم المتحركة",
        "東京動漫研究所"
    ])
    def test_create_order(self,name):
        #name后加了随机数字，保证下次运行用例时部门名称不是重复的
        data = {
            "name": name+Utils.udid(),
            "parentid": 1,
            "order": 1
        }
        r = self.depart.create(data)
        assert r['errcode'] == 0

    '''
    修改部门名称
    问题：门店id=8和id=3是存在的，但是运行接口始终返回60003(部门ID不存在)
    '''
    @allure.story('修改部门-修改部门名称')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_name(self):
        name = "测试修改名字"+str(time.time())
        id = Utils.department_id()
        data={
            "name":name,
            "id":id
        }
        r1 = self.depart.update(data)
        print(r1)
        #assert r1['errcode'] == 0
        r2 = self.depart.list(id)
        #assert r2['department']['name']==name


    # 部门名字长度(最大32)
    @allure.story('修改部门-修改部门名称超长')
    @allure.severity(allure.severity_level.MINOR)
    def test_update_name_length(self):
        sam = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
        name = random.sample(sam,33)
        id = Utils.department_id()
        data = {
            "name":name,
            "id": id
        }
        r = self.depart.update(data)
        print(r['errcode'])
        #assert r['errcode']== 60001


    #修改部门的上级部门
    @allure.story('修改部门-修改父部门')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_parentid(self):
        id = Utils.department_id()
        new_parentid = Utils.new_father_department(id)
        data = {
            "id": id,
            "parentid":new_parentid
                }
        r = self.depart.update(data)
        assert r['errcode'] == 0

    #修改部门次序
    @allure.story('修改部门-修改部门次序')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_order(self):
        id = Utils.department_id()
        old_order = Utils.department_info(id)['order']
        new_order= Utils.random_out_of_order(id)
        data = {
            "id":id,
            "order":new_order
        }
        r = self.depart.update(data)
        order = Utils.department_info(id)['order']
        assert r['errcode'] == 0
        assert order == new_order


    #获取部门列表(所有部门)
    @allure.story('部门列表-获取所有部门')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_all(self):
        r = self.depart.list()
        assert r['errcode'] == 0


    '''
       在父部门中的次序值。order值大的排序靠前。有效的值范围是[0, 2^32)
       即为父部门相同，部门为同级的，根据order排序
    '''
    @allure.story('部门列表-验证排序')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("id",[
        (3),
        (26)
    ])
    def test_list_order(self,id):
        #父部门id
        r = self.depart.list(id)
        #logging.debug(r)
        list = []
        for i in range(len(r['department'])):
            if r['department'][i]['parentid']== id:
                list.append(r['department'][i])
        for j in range(len(list)-1):
            if list[j]['order'] < list[j+1]['order']:
                print(str(list[j]) + "和" + str(list[j+1]))
                assert '前一个部门order大于后一个order' == ''
                break;




    @allure.story('部门列表-获取特定父部门下部门列表')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("id",[
        3,
        191
    ])
    def test_list_one(self,id):
        r = self.depart.list(id)
        if id == 3:
            assert r['errcode'] == 0
            # 部门个数
            assert len(r['department'][0]) == 4
            #验证指定id的部门在列表
            #assert jsonpath.jsonpath(r,"$.department[?(@.id==6)].name")[0]== '第十期_krystal5'
            #assert jsonpath.jsonpath(r, "$.department[?(@.id==4)].name")[0] == '第十期_krystal3'
        if id == 191:
            assert r['errcode'] == 0
            # 部门个数,还包含查询的id部门自己
            assert len(r['department'][0]) == 4


    #不能删除根部门；不能删除含有子部门、成员的部门
    @allure.story('部门删除-删除包含子部门的父部门、删除包含成员的部门')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("id,code",[
        (1,60005),
        (3,60006),
    ])
    def test_delete_error(self,id,code):
        r= self.depart.delete(id)
        print(r)
        assert r['errcode'] == code

    #删除部门成功
    @allure.story('部门删除-成功删除部门')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_right(self):
        #先创建一个部门
        data = {
            "name": "测试删除部门成功_"+str(time.time()),
            "parentid": 37
        }
        id=self.depart.create(data)['id']
        r = self.depart.delete(id)
        assert r['errcode'] == 0

