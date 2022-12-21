import pymysql
import pandas as pd
import numpy as np

conn = pymysql.connect(host='localhost', user='root', password='', db='newspaper_info_content_all', charset='utf8')

sql1 = "SELECT text FROM newspaper_info_content_all WHERE 1"
sql2 = "SELECT ocr_text_line FROM `newspaper_reocr_text` WHERE 1"
sql3 = "SELECT grammar_check_text_line FROM `newspaper_grammar_check_text` WHERE 1"

df1 = pd.read_sql(sql1, con=conn)
df2 = pd.read_sql(sql2, con=conn)
df3 = pd.read_sql(sql3, con=conn)

df1 = np.array(df1) #先使用array()将DataFrame转换一下
l1 = df1.tolist()#再将转换后的数据用tolist()转成列表
l1 = [t[0] for t in l1]
print(l1)
origin = ''.join(l1)
with open('origin.txt','w',encoding="utf-8") as f:
    f.write(origin)

df2 = np.array(df2) #先使用array()将DataFrame转换一下
l2 = df2.tolist()#再将转换后的数据用tolist()转成列表
l2 = [t[0] for t in l2]
reocr = ''.join(l2)
with open('reocr.txt','w',encoding="utf-8") as f:
    f.write(reocr)

df3 = np.array(df3) #先使用array()将DataFrame转换一下
l3 = df3.tolist()#再将转换后的数据用tolist()转成列表
l3 = [t[0] for t in l3]
grammar = ''.join(l3)
with open('grammar.txt','w',encoding="utf-8") as f:
    f.write(grammar)