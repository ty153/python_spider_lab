import pymysql
from config import CONFIG_MYSQL,TABLE_NAME,TABLE_COLUMNS

def database_init():
    '''
    初始化数据库和表(如果不存在)
    '''
    # 建立连接
    config_without_db = CONFIG_MYSQL.copy()
    config_without_db.pop('database', None)
    try:
        conn = pymysql.connect(**config_without_db)
        cursor = conn.cursor()
        
        # 建立库如果不存在
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {CONFIG_MYSQL["database"]} DEFAULT CHARSET utf8mb4')
        cursor.close()
        conn.close()
    except Exception as e:
         print(f'数据库连接失败：{e}')
    
    # 根据配置动态生成建表的sql
    columns_def = ['id INT AUTO_INCREMENT PRIMARY KEY']
    for col_name,col_type in TABLE_COLUMNS.items():
        columns_def.append(f'{col_name} {col_type}')
    columns_def.append('create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    creat_sql =f'''
         CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
            {','.join(columns_def)}
         ) DEFAULT CHARSET=utf8mb4
        '''
    # 执行建表
    conn = pymysql.connect(**CONFIG_MYSQL)
    try:
        cursor = conn.cursor()
        cursor.execute(creat_sql)
        conn.commit()
        conn.close()
        print(f"数据库 [{CONFIG_MYSQL['database']}] 和表 [{TABLE_NAME}] 初始化完成")
    except Exception as e:
        print('失败或已经存在',e)
            

   


def save_to_mysql(data_list):
    '''
    接受一个字典列表插入数据库
    '''
    # 从配置中解析出需要存储的字段
    fields = list(TABLE_COLUMNS.keys())
    placeholders = ','.join(['%s']*len(fields))
    fields_str = ','.join(fields)

    conn = pymysql.connect(**CONFIG_MYSQL)
    cursor = conn.cursor()
    success_count = 0
    '''
    INSERT IGNORE 的作用：当遇到 UNIQUE 约束冲突时，静默跳过，不报错、不中断程序，继续执行下一条。
    '''
    for data in data_list:
        sql = f"INSERT IGNORE INTO {TABLE_NAME} ({fields_str}) VALUES ({placeholders})"
        values = tuple(data.get(field, '') for field in fields)  
        try:
            affected_rows = cursor.execute(sql,values)
            if affected_rows == 1:
                success_count += 1
        except Exception as e:
            print(f'插入失败：{e}')
    
    conn.commit()
    conn.close()
    print(f'成功存入 {success_count} 条数据，跳过 {len(data_list) - success_count} 条重复数据')