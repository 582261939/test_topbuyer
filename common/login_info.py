import os
import logging
from common.get_path import BASIC_PATH
from common.get_config import config_data


def login_info(name, level, log_name, lf_level, ls_level):
    log = logging.getLogger(name)
    log.setLevel(level)

    formats = "%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s"
    log_format = logging.Formatter(formats)

    lf = logging.FileHandler(os.path.join(BASIC_PATH, log_name), encoding="utf-8")
    lf.setLevel(lf_level)
    log.addHandler(lf)
    lf.setFormatter(log_format)

    ls = logging.StreamHandler()
    ls.setLevel(ls_level)
    log.addHandler(ls)
    ls.setFormatter(log_format)

    return log


log = login_info(name=config_data.get("login", "name"),
    level=config_data.get("login", "level"),
    log_name=config_data.get("login", "log_name"),
    lf_level=config_data.get("login", "fh_level"),
    ls_level=config_data.get("login", "sh_level"))


