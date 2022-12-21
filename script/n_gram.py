import os
import sys
import pandas as pd
from collections import Counter
from insert_reocr_data import process_bar, connect, table_exists
from sqlalchemy import create_engine


def create_table(cursor):
    sql_createTb = """CREATE TABLE newspaper_n_gram (
                     word CHAR(100),
                     year  INT,
                     month INT,
                     page INT,
                     frequency INT,
                     PRIMARY KEY(word, year, month, page))
                     """

    cursor.execute(sql_createTb)


def insert_mysql(df, table_name):
    engine = create_engine("mysql+pymysql://root:mysql123456@localhost:3306/europeana?charset=utf8")
    con = engine.connect()
    df.to_sql(table_name, con=con, if_exists='replace', index=False)
    con.close()


def get_n_gram(path):
    g = os.walk(path)
    year = []
    month = []
    page = []
    words = []
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

            with open(os.path.join(path, file_name)) as f:
                text_fr = f.read()
            words.append(dict(Counter(text_fr.split())))

            x += 1
            process_bar(x+1, n)

    return words, year, month, page


def table4Ngram(words_freq, year, month, page):
    lenth_n_gram = len(words_freq)
    lst_n_gram = list()
    x = 0
    for i in range(lenth_n_gram):
        for k,v in words_freq[i].items():
            lst_n_gram.append([k,  # words
                               year[i],
                               month[i],
                               page[i],
                               v])  # frequency
        x += 1
        process_bar(x + 1, lenth_n_gram)

    df = pd.DataFrame(lst_n_gram)
    df.columns = ['word', 'year', 'month', 'page', 'frequency']

    return df


def main():
    words, year, month, page = get_n_gram('/Users/DXY/Documents/Project/modified_text')
    df = table4Ngram(words, year, month, page)

    table_name = 'newspaper_n_gram'
    conn = connect()
    cursor = conn.cursor()
    if table_exists(cursor, table_name) == 0:
        create_table(cursor)
        conn.commit()
    conn.close()
    cursor.close()

    insert_mysql(df, table_name)

if __name__ == '__main__':
    main()