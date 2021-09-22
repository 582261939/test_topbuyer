import os
import unittest
import requests
from unittestreport import ddt, list_data
from common.open_excel import OpenExcel
from common.get_path import EXECL_PATH
from common.get_config import config_data
from common.tools_re import replace_data, random_phone, assertDictIn
from common.connect_mysql import ConnectMysql
from common.login_info import log


@ddt
class TestRegister(unittest.TestCase):
    ex = OpenExcel(os.path.join(EXECL_PATH, "test_case.xlsx"), "register")
    case_data = ex.red_data()

    @classmethod
    def setUpClass(cls):
        cls.headers = eval(config_data.get("api", "headers"))
        cls.con = ConnectMysql(
            host=config_data.get("mysql", "host"),
            port=config_data.getint("mysql", "port"),
            user=config_data.get("mysql", "user"),
            password=config_data.get("mysql", "password"),
            charset=config_data.get("mysql", "charset"))

    @list_data(case_data)
    def test_register(self, item):
        url = config_data.get("api", "basic_path") + item["url"]
        if "#mobile_phone#" in item["data"]:
            setattr(self, "mobile_phone", random_phone())
            item["data"] = replace_data(item["data"], self)
        data = eval(item["data"])
        expected = eval(item["expected"])
        count01 = None
        count02 = None
        flag = item["sql"]
        sql = "select id from futureloan.member"
        if flag:
            count01 = self.con.get_count_data(sql)
        rep = requests.request(item["method"], json=data, headers=self.headers, url=url).json()
        if flag:
            count02 = self.con.get_count_data(sql)
        try:
            assertDictIn(rep, expected)
            if flag:
                self.assertEqual(count01, count02)
        except AssertionError as e:
            log.error("用例--【{}】--执行失败 : {}".format(item["title"], e))
            raise e
        else:
            log.info("用例--【{}】--执行成功 : ".format(item["title"]))


