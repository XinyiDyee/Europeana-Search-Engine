import os
import pandas as pd
import sys
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
    df.to_sql(table_name, con=con, if_exists='replace', index=False)
    con.close()


def create_table(cursor):
    sql_createTb = """CREATE TABLE newspaper_reocr_text (
             year  INT,
             month INT,
             page INT,
             ocr_text VARCHAR(5000),
             ocr_text_line VARCHAR(5000),
             PRIMARY KEY(year, month, page))
             """
    cursor.execute(sql_createTb)


def text2df(path):
    g = os.walk(path)
    year = []
    month = []
    page = []
    ocr_text = []
    ocr_text_line = []
    x = 0
    for path, dir_list, file_list in g:
        n = len(file_list)
        for file_name in file_list:
            f = file_name.split('.')[0]
            ymp = f.split('-')
            if ymp[0] == '':
                continue
            year.append(int(ymp[0]))
            month.append(int(ymp[1]))
            page.append(int(ymp[2]))

            with open(os.path.join(path, file_name)) as text:
                ocr_lines = text.readlines()
            ocr_text.append(''.join(ocr_lines))

            for i in range(len(ocr_lines)):
                s = ocr_lines[i]
                if s.endswith('¬\n'):
                    ocr_lines[i] = s.replace('¬\n', '')
                else:
                    ocr_lines[i] = s.replace('\n', ' ')
            ocr_text_line.append(''.join(ocr_lines))

            x += 1
            process_bar(x+1, n)

    df = pd.DataFrame({"year": year,
                       "month": month,
                       "page": page,
                       "ocr_text": ocr_text,
                       "ocr_text_line": ocr_text_line})

    return df


def main():
    table_name = 'newspaper_reocr_text'
    conn = connect()
    cursor = conn.cursor()
    if table_exists(cursor, table_name) == 0:
        create_table(cursor)
        conn.commit()
    conn.close()
    cursor.close()
    print('Created a table')

    path = '/Users/DXY/Documents/Project/text'
    print('Start insert data')
    df = text2df(path)
    insert_mysql(df, table_name)


if __name__ == '__main__':
    main()