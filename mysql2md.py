# -*- coding: utf-8 -*-

import pymysql
_author_ = 'zhibin'
_date_ = '2019/10/15 23:21'

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='information_schema', charset='utf8')
# 表名
table_name = 'mytable'

cursor = conn.cursor()
cursor.execute("select table_name,table_comment from information_schema.tables where table_schema='%s' and table_type='BASE TABLE'" % table_name)

tables = cursor.fetchall()

markdown_table_header = """### %s %s
字段名 | 字段类型 | 默认值 | 注解
---- | ---- | ---- | ---- 
"""
markdown_table_row = """%s | %s | %s | %s
"""

# 保存输出结果
file = "%s.md" % table_name
f = open(file, 'w')
for table in tables:
    cursor.execute(
        "select COLUMN_NAME,COLUMN_TYPE,COLUMN_DEFAULT,COLUMN_COMMENT from information_schema.COLUMNS where table_schema='%s' and table_name='%s' order by ORDINAL_POSITION asc" % (
            table_name, table[0]))
    tmp_table = cursor.fetchall()
    p = markdown_table_header % (table[0], table[1]);
    for col in tmp_table:
        p += markdown_table_row % col
    f.writelines(p)
f.close()
