import pymysql

# 本地数据库
MYSQL = {
    'HOSTNAME': '127.0.0.1',
    'PORT': 3306,
    'DATABASE': 'best-seller',
    'USERNAME': "root",
    'PASSWORD': "123"
}


class DBMysql:
    def __init__(self):
        self.db = pymysql.connect(host=MYSQL['HOSTNAME'], user=MYSQL['USERNAME'],
                                  password=MYSQL['PASSWORD'],
                                  database=MYSQL['DATABASE'],
                                  charset='utf8mb4', port=MYSQL['PORT'])

    def save_category(self, item, table='department'):
        try:
            cursor = self.db.cursor()
            # 取出keys为字段
            item_keys = ', '.join('`{}`'.format(k) for k in item.keys())
            # 取出values为插入的值
            item_values = ', '.join('"{}"'.format(k) for k in item.values())
            product_sql = "insert into `{}`({}) values({})".format(table, item_keys, item_values)
            cursor.execute(product_sql)
            self.db.commit()
        except Exception as e:
            print("product_sql insert err:{},sql statement:{}".format(e, product_sql))
            self.db.rollback()

    def truncate_table(self, db_table='department'):
        self.db = pymysql.connect(host=MYSQL['HOSTNAME'], user=MYSQL['USERNAME'],
                                  password=MYSQL['PASSWORD'],
                                  database=MYSQL['DATABASE'],
                                  charset='utf8mb4', port=MYSQL['PORT'])
        cursor = self.db.cursor()
        try:
            cursor.execute("truncate table {}".format(db_table))
            self.db.commit()
            print("truncate_table success!")
        except Exception as e:
            print('truncate_table, err: ', e)
