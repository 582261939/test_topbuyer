import unittest
from unittestreport import TestRunner
from common.get_path import TEST_CASE, REPORTS
from common.get_config import config_data


def test_run():
    test_case = unittest.defaultTestLoader.discover(TEST_CASE)
    tr = TestRunner(test_case, tester="张振伟", desc="小蚁买手项目测试生成的报告", report_dir=REPORTS, templates=2)
    tr.run()
    sen_list = eval(config_data.get("Email", "sen_list"))
    tr.send_email(host=config_data.get("Email", "host"),
                  port=int(config_data.get("Email", "port")),
                  user=config_data.get("Email", "user"),
                  password=config_data.get("Email", "password"),
                  to_addrs=sen_list,
                  is_file=True)
