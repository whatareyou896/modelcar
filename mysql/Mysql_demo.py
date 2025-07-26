import pymysql
from pymysql.cursors import DictCursor
from typing import List, Dict, Optional, Any


class MySQLCRUD:
    """
    MySQL数据库增删查改基类
    设计为可继承结构，方便后续扩展特定表的操作
    """

    def __init__(self, host: str, user: str, password: str, database: str, table_name: str):
        """
        初始化数据库连接
        :param host: 数据库地址
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名
        :param table_name: 表名
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table_name = table_name
        self.connection = None

    def connect(self):
        """建立数据库连接"""
        if not self.connection or not self.connection.open:
            try:
                # 尝试使用新版本参数
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    charset='utf8mb4',
                    cursorclass=DictCursor,
                    auth_plugin='mysql_native_password'
                )
            except TypeError:
                # 如果报错，使用旧版本连接方式
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    charset='utf8mb4',
                    cursorclass=DictCursor
                )
        return self.connection

    def close(self):
        """关闭数据库连接"""
        if self.connection and self.connection.open:
            self.connection.close()
            self.connection = None

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """
        执行查询语句
        :param query: SQL查询语句
        :param params: 参数元组
        :return: 结果列表
        """
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()
        finally:
            # 这里不关闭连接，保持连接开启
            pass

    def execute_update(self, query: str, params: tuple = None) -> int:
        """
        执行更新/插入/删除语句
        :param query: SQL语句
        :param params: 参数元组
        :return: 影响的行数
        """
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(query, params or ())
                conn.commit()
                return affected_rows
        except Exception as e:
            conn.rollback()
            raise e

    def create(self, data: Dict) -> int:
        """
        创建记录
        :param data: 包含字段和值的字典
        :return: 插入的行ID
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        print(query)
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, tuple(data.values()))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e

    def read(self, conditions: Dict = None, fields: List[str] = None) -> List[Dict]:
        """
        读取记录
        :param conditions: 查询条件字典
        :param fields: 要查询的字段列表
        :return: 结果字典列表
        """
        if not fields:
            fields = ['*']

        field_list = ', '.join(fields)
        query = f"SELECT {field_list} FROM {self.table_name}"
        params = []
        if conditions:
            where_clause = ' AND '.join([f"{k}=%s" for k in conditions.keys()])
            query += f" WHERE {where_clause}"
            params.extend(conditions.values())
        print(params)
        return self.execute_query(query, tuple(params))

    def update(self, updates: Dict, conditions: Dict) -> int:
        """
        更新记录
        :param updates: 要更新的字段和值
        :param conditions: 更新条件
        :return: 影响的行数
        """
        set_clause = ', '.join([f"{k}=%s" for k in updates.keys()])
        where_clause = ' AND '.join([f"{k}=%s" for k in conditions.keys()])

        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {where_clause}"
        params = tuple(list(updates.values()) + list(conditions.values()))

        return self.execute_update(query, params)

    def delete(self, conditions: Dict) -> int:
        """
        删除记录
        :param conditions: 删除条件
        :return: 影响的行数
        """
        where_clause = ' AND '.join([f"{k}=%s" for k in conditions.keys()])
        query = f"DELETE FROM {self.table_name} WHERE {where_clause}"

        return self.execute_update(query, tuple(conditions.values()))

    def get_by_id(self, id_value: Any, id_field: str = 'id') -> Optional[Dict]:
        """
        根据ID获取单条记录
        :param id_value: ID值
        :param id_field: ID字段名，默认为'id'
        :return: 单条记录或None
        """
        results = self.read({id_field: id_value})
        return results[0] if results else None



