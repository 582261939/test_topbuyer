import pymysql
from common.get_config import config_data

class ConnectMysql:
    def __init__(self, host, port, user, password, charset):
        # 连接数据库
        self.con = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset=charset)

    def get_all_data(self, sql):
        with self.con as cur:
            cur.execute(sql)
            all_data = cur.fetchall()
            cur.close()
            return all_data

    def get_one_data(self, sql):
        with self.con as cur:
            cur.execute(sql)
            one_data = cur.fetchone()
            cur.close()
            return one_data

    def get_count_data(self, sql):
        with self.con as cur:
            count_data = cur.execute(sql)
            cur.close()
            return count_data

    def __del__(self):
        self.con.close()


if __name__ == '__main__':
    con = ConnectMysql(
        host=config_data.get("mysql", "host"),
        port=config_data.getint("mysql", "port"),
        user=config_data.get("mysql", "user"),
        password=config_data.get("mysql", "password"),
        charset=config_data.get("mysql", "charset"))
    sql = "select id from futureloan.member"
    print(con.get_count_data(sql))
