import os
import unittest
import requests
from unittestreport import ddt, list_data
from common.get_path import EXECL_PATH
from common.open_excel import OpenExcel
from common.get_config import config_data
from common.tools_re import replace_data, assertDictIn
from common.login_info import log


@ddt
class TestLogin(unittest.TestCase):
    oe = OpenExcel(os.path.join(EXECL_PATH, "test_case.xlsx"), "login")
    case = oe.red_data()
    headers = eval(config_data.get("api", "headers"))

    @list_data(case)
    def test_login(self, item):
        url = config_data.get("api", "basic_path") + item["url"]
        if "#mobile_phone#" or "#pwd#" in item["data"]:
            setattr(self, "mobile_phone", config_data.get("test_user", "user_phone"))
            setattr(self, "pwd", config_data.get("test_user", "pwd"))
            item["data"] = replace_data(item["data"], self)
        data = eval(item["data"])
        rep = requests.request(item["method"], url=url, json=data, headers=self.headers).json()
        expected = eval(item["expected"])
        try:
            assertDictIn(rep, expected)
        except AssertionError as e:
          log.error("用例--【{}】--执行失败 : {}".format(item["title"], e))
          raise e
        else:
            log.info("用例--【{}】--执行成功 : ".format(item["title"]))

