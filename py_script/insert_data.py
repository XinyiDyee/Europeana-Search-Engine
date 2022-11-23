# conding=utf-8

import pymysql
import json
import os
import pandas as pd
from sqlalchemy import create_engine

def connect():
    """
    connet to mysql database
    :return:
    """
    conn = pymysql.connect(host="127.0.0.1", port=3306,
                           user="root", password="mysql123456",
                           database="europeana", charset="utf8")
    return conn


def create_table():
    conn = connect()
    cursor = conn.cursor()
    sql_createTb = """CREATE TABLE newspaper_info_content_all (
                 title CHAR(100),
                 year  INT,
                 month INT,
                 page INT,
                 identifier CHAR(100),
                 image_url VARCHAR(500),
                 text VARCHAR(5000),
                 PRIMARY KEY(year, month, page))
                 """
    cursor.execute(sql_createTb)
    conn.commit()
    conn.close()
    cursor.close()

    return cursor


def df4Issue(k, v):
    l = len(v['img'])
    pages = []
    urls = []
    for p, u in v['img'].items():
        pages.append(int(p))
        urls.append(u)

    text = []
    for p, t in v['text'].items():
        text.append(t)
    
    identifiers = [k]*l
    titles = [v['title']]*l
    years = [v['year']]*l
    months = [v['month']]*l
    df = pd.DataFrame({"title": titles,
                       "year": years, 
                       "month": months, 
                       "page": pages, 
                       "identifier": identifiers,
                       "image_url": urls,
                       "text": text})
    
    return df
 
 
def insert_mysql(df):
    engine = create_engine("mysql+pymysql://root:mysql123456@localhost:3306/europeana?charset=utf8")
    con = engine.connect()
    df.to_sql("newspaper_info_content_all",con=con,if_exists='replace',index=False)

 
def main():
    # create_table()

    path = "/Users/DXY/Documents/Project/Europeana/data/img_url_and_text"
    file_p = os.path.join(path, '10.json')
    with open(file_p,'r') as load_f:
        load_dict = json.load(load_f)
    df_list = []
    for k,v in load_dict.items():
        df_list.append(df4Issue(k,v))
    data = pd.concat(df_list)

    insert_mysql(data)


if __name__ == '__main__':
    main()