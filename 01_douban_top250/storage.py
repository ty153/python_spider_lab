import pymysql
from config import CONFIG_MYSQL

def database_init():
    '''
    初始化数据库和表(如果不存在)
    '''
    # 建立连接
    config_without_db = CONFIG_MYSQL.copy()
    config_without_db.pop('database', None)
    conn = pymysql.connect(**config_without_db)
    cursor = conn.cursor()
    
    # 建立库如果不存在
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {CONFIG_MYSQL["database"]} DEFAULT CHARSET utf8mb4')
    cursor.close()
    conn.close()

    # 连接到指定数据库，创建表
    conn = pymysql.connect(**CONFIG_MYSQL)
    cursor = conn.cursor()
    '''
    UNIQUE 的作用：告诉 MySQL,“title 这一列的值不能重复”。
    如果你尝试插入一个已经存在的 title,MySQL 会拒绝并报错。
    '''
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movie_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) UNIQUE,
            credits VARCHAR(255),
            rating_count VARCHAR(20),
            rating_num VARCHAR(20),
            con VARCHAR(255),
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) DEFAULT CHARSET=utf8mb4
    """)
    conn.commit()
    conn.close()
    print("数据库和表初始化完成")


def save_to_mysql(data_list):
    '''
    接受一个字典列表插入数据库
    '''
    conn = pymysql.connect(**CONFIG_MYSQL)
    cursor = conn.cursor()
    success_count = 0
    '''
    INSERT IGNORE 的作用：当遇到 UNIQUE 约束冲突时，静默跳过，不报错、不中断程序，继续执行下一条。
    '''
    for data in data_list:
        sql = "INSERT IGNORE INTO movie_info (title, credits, rating_count, rating_num, con) VALUES (%s, %s, %s, %s, %s)"
        try:
            affected_rows = cursor.execute(sql, (data['title'], data['credits'], data['rating_count'], data['rating_num'], data['con']))
            if affected_rows == 1:
                success_count += 1
        except Exception as e:
            print(f'插入失败：{e}')
    
    conn.commit()
    conn.close()
    print(f'成功存入 {success_count} 条数据，跳过 {len(data_list) - success_count} 条重复数据')