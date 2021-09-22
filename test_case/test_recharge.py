import os
import unittest
import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.get_path import EXECL_PATH
from common.open_excel import OpenExcel
from common.get_config import config_data
from common.tools_re import replace_data, assertDictIn, lv3
from common.connect_mysql import ConnectMysql
from common.login_info import log


@ddt
class TestRecharge(unittest.TestCase):
    oe = OpenExcel(os.path.join(EXECL_PATH, "test_case.xlsx"), "recharge")
    case = oe.red_data()

    @classmethod
    def setUpClass(cls):
        url = config_data.get("api", "basic_path") + config_data.get("api", "login")
        cls.headers = eval(config_data.get("api", "headers"))
        data = {
            "mobile_phone": config_data.get("test_user", "user_phone"),
            "pwd": config_data.get("test_user", "pwd")
        }
        rep = requests.request("post", url=url, json=data, headers=cls.headers).json()
        cls.token = jsonpath(rep, "$..token")[0]
        cls.member_id = jsonpath(rep, "$..id")[0]
        cls.con = ConnectMysql(
            host=config_data.get("mysql", "host"),
            port=config_data.getint("mysql", "port"),
            user=config_data.get("mysql", "user"),
            password=config_data.get("mysql", "password"),
            charset=config_data.get("mysql", "charset"))

    @list_data(case)
    def test_recharge(self, item):
        sgin = lv3(self.token)
        url = config_data.get("api", "basic_path") + item["url"]
        self.headers["Authorization"] = "Bearer " + self.token
        if "#member_id#" in item["data"]:
            item["data"] = replace_data(item["data"], self)
        params = eval(item["data"])
        params.update(sgin)
        sql = "select leave_amount from futureloan.member where mobile_phone = {}".format(config_data.get("test_user", "user_phone"))
        amount01 = None
        amount02 = None
        if item["sql"]:
            amount01 = self.con.get_one_data(sql)[0]
        rep = requests.request("post", url=url, headers=self.headers, json=params).json()
        if item["sql"]:
            amount02 = self.con.get_one_data(sql)[0]
        expected = eval(item["expected"])
        try:
            assertDictIn(rep, expected)
            if item["sql"]:
                self.assertEqual(float(amount02-amount01), float(params["amount"]))
        except AssertionError as e:
            log.error("用例--【{}】--执行失败 : {}".format(item["title"], e))
            raise e
        else:
            log.info("用例--【{}】--执行成功 : ".format(item["title"]))







