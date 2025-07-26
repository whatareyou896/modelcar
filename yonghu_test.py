from Mysql_demo import *

# 示例：用户表操作类（继承基类）
class UserDAO(MySQLCRUD):
    """用户表数据访问对象"""

    def __init__(self, host: str, user: str, password: str, database: str ,table_name: str):
        super().__init__(host, user, password, database, table_name)

    def get_by_username(self, username: str) -> Optional[Dict]:
        """根据用户名获取用户"""
        results = self.read({'username': username})
        print(results)
        return results[0] if results else None

    def get_active_users(self) -> List[Dict]:
        """获取所有活跃用户"""

        return self.read({'status': 'active'})

    def update_password(self, user_id: int, new_password: str) -> bool:
        """更新用户密码"""
        affected_rows = self.update(
            {'password': new_password},
            {'id': user_id}
        )
        return affected_rows > 0

    def delete_inactive_users(self) -> int:
        """删除所有不活跃用户"""
        return self.delete({'status': 'inactive'})


# 使用示例
if __name__ == '__main__':
    # 配置数据库连接
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'test',
        'password': '123456',
        'database': 'chehang',
        "table_name" : "yonghu",
    }

    # 创建DAO实例
    user_dao = UserDAO(**DB_CONFIG)

    try:
        # 创建用户
        new_user = {
            'username': '123',
            'password': 'secure123',
            'email': 'john@example.com',
            'status': 'active'
        }
        user_dao.create(new_user)
        user_dao.get_by_id(12)
        user_dao.get_by_username("123")
        user_id = 12
        update_data = {'email': 'john.doe@.com'}
        user_dao.update(update_data, {'id': 12})
        updated_user = user_dao.get_by_id(user_id)
        print(f"Updated user: {updated_user}")
        '''
        user_id = user_dao.create(new_user)
        print(f"Created user with ID: {user_id}")

        # 查询用户
        user = user_dao.get_by_id(user_id)
        print(f"User by ID: {user}")

        # 根据用户名查询
        same_user = user_dao.get_by_username('john_doe')
        print(f"User by username: {same_user}")

        # 更新用户
        update_data = {'email': 'john.doe@example.com'}
        user_dao.update(update_data, {'id': user_id})
        updated_user = user_dao.get_by_id(user_id)
        print(f"Updated user: {updated_user}")

        # 删除用户
        user_dao.delete({'id': user_id})
        deleted_user = user_dao.get_by_id(user_id)
        print(f"User after deletion: {deleted_user}")
    '''
    except pymysql.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"General error: {e}")
    finally:
        # 确保关闭连接
        user_dao.close()