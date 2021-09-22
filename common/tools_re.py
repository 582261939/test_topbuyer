import re
import os
import rsa
import random
import base64
import time
from common.get_config import config_data
from common.get_path import POUBLIC

with open(os.path.join(POUBLIC, "public.pem"), "r") as f:
    publics = f.read()
publics1 = """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQENQujkLfZfc5Tu9Z1LprzedE
O3F7gs+7bzrgPsMl29LX8UoPYvIG8C604CprBQ4FkfnJpnhWu2lvUB0WZyLq6sBr
tuPorOc42+gLnFfyhJAwdZB6SqWfDg7bW+jNe5Ki1DtU7z8uF6Gx+blEMGo8Dg+S
kKlZFc8Br7SHtbL2tQIDAQAB
-----END PUBLIC KEY-----
"""

def replace_data(data, cls):
    while re.search("#(.+?)#", data):
        re2 = re.search("#(.+?)#", data)
        passive = re2.group()
        reality = re2.group(1)
        try:
            value = getattr(cls, reality)
        except AttributeError:
            value = config_data.get("test_data", "user_phone")
        data = data.replace(passive, str(value))

    return data


def random_phone():
    phone = "152"
    for i in range(8):
        phone += str(random.randint(0, 9))
    return phone


def assertDictIn(rep, expected):
    for k, v in expected.items():
        if rep[k] == v:
            continue
        else:
            raise AssertionError("{} ont in {}".format(rep, expected))


def rsa_encryption(msg):
    msg = msg.encode("utf-8")
    public = publics.encode("utf-8")
    key01 = rsa.PublicKey.load_pkcs1_openssl_pem(public)
    key02 = rsa.encrypt(msg, key01)
    key03 = base64.b64encode(key02).decode()
    return key03


def lv3(msg):
    msg = msg[:50]
    timestamp = int(time.time())
    m = msg + str(timestamp)
    sgin = rsa_encryption(m)
    return {"timestamp": timestamp, "sign": sgin}



