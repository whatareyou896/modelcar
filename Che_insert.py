from Mysql_demo import *

# 示例：用户表操作类（继承基类）
class UserDAO(MySQLCRUD):
    """用户表数据访问对象"""

    def __init__(self, host: str, user: str, password: str, database: str ,table_name: str):
        super().__init__(host, user, password, database, table_name)

def Che_insert_main(a):
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'test',
        'password': '123456',
        'database': 'chehang',
        "table_name": "che",
    }
    # 创建DAO实例
    user_dao = UserDAO(**DB_CONFIG)
    try:
        user_dao.create(a)
    except pymysql.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"General error: {e}")
    finally:
        # 确保关闭连接
        user_dao.close()

if __name__ == '__main__':
    Che_insert_main()
    # 配置数据库连接
