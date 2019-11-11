import time
import pystache
import random
from contact.department import Department

class Utils:


    #解析模版(创建用户，data数据部分)
    #dict是传参
    @classmethod
    def parse(cls,template_path,dict):
        # 把user_create.json里内容存为字符串
        template = "".join(open(template_path).readlines())
        return pystache.render(template, dict)

    @classmethod
    def udid(self):
        return str(time.time()).replace(".","")[0:11]

    #随机选择部门id(除了祖先部门1)
    @classmethod
    def department_id(cls):
        depart = Department()
        r = depart.list()
        list = []
        for i in range(len(r['department'])):
            if r['department'][i]['id'] != 1:
                list.append(r['department'][i]['id'])
        #在列表里随机选择元素
        depart_id = random.choice(list)
        return depart_id

    #获取部门自己的信息
    @classmethod
    def department_info(cls,id):
        depart = Department()
        #返回类型是字典:{'id': 26, 'name': '東京動漫研究所', 'parentid': 1, 'order': 1}
        r = depart.list(id)['department'][0]
        return r

    #为部门更新一个新的父亲部门
    @classmethod
    def new_father_department(cls,id):
        # 需要获取一个和原来部门的父部门不同的id
        old_parentid = Utils.department_info(id)['parentid']
        print(old_parentid)
        #new_parentid = 0
        for new_parentid in [id,old_parentid]:
            new_parentid = Utils.department_id()
        return  new_parentid

    #产生除了固定数字外的其他随机数
    #为一个部门更新排序order
    @classmethod
    def random_out_of_order(cls,id):
        depart = Department()
        #当前部门的父部门的id
        parentid=Utils.department_info(id)['parentid']
        r = depart.list(parentid)['department']
        order_list = []
        #把父部门下所有部门的order放在列表中
        for i in range(len(r)):
            if r[i]['parentid'] == parentid:
                #print(r[i])
                order_list.append(r[i]['order'])
        #新的order要把旧的order都排除掉
        for new_order in order_list:
            new_order = random.randint(100,10000)
        return new_order



if __name__=='__main__':
    # print(Utils.department_id())
    # print(Utils.department_info(26))
    # print(type(Utils.department_info(26)))
    #print(Utils.new_father_department(145))
    print(Utils.random_out_of_order(3))






