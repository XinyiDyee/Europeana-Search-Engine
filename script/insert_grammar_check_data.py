import os
import sys
import pandas as pd
from insert_origin_data import connect, table_exists
from sqlalchemy import create_engine


def process_bar(num, total):
    rate = float(num)/total
    ratenum = int(100*rate)
    r = '\r[{}{}]{}%'.format('*'*ratenum,' '*(100-ratenum), ratenum)
    sys.stdout.write(r)
    sys.stdout.flush()


def insert_mysql(df, table_name):
    engine = create_engine("mysql+pymysql://root:mysql123456@localhost:3306/europeana?charset=utf8")
    con = engine.connect()
    df.to_sql(table_name, con=con, if_exists='append', index=False)
    con.close()


def create_table(cursor):
    sql_createTb = """CREATE TABLE newspaper_grammar_check_text (
             year  INT,
             month INT,
             page INT,
             grammar_check_text_line VARCHAR(5000),
             PRIMARY KEY(year, month, page))
             """
    cursor.execute(sql_createTb)


def text2df(path):
    g = os.walk(path)
    year = []
    month = []
    page = []
    grammar_check_text_line = []
    for path, dir_list, file_list in g:
        for file_name in file_list:
            f = file_name.split('.')[0]
            ymp = f.split('-')
            year.append(int(ymp[0]))
            month.append(int(ymp[1]))
            page.append(int(ymp[2]))

            with open(os.path.join(path, file_name)) as text:
                lines = text.read()
            grammar_check_text_line.append(lines)

    df = pd.DataFrame({"year": year,
                       "month": month,
                       "page": page,
                       "grammar_check_text_line": grammar_check_text_line})

    return df


def main():
    table_name = 'newspaper_grammar_check_text'
    conn = connect()
    cursor = conn.cursor()
    if table_exists(cursor, table_name) == 0:
        create_table(cursor)
        conn.commit()
    conn.close()
    cursor.close()

    path = '/Users/DXY/Documents/Project/modified_text'
    df = text2df(path)
    insert_mysql(df, table_name)


if __name__ == '__main__':
    main()