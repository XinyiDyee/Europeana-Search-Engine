import os
import json
import spacy
import pandas as pd
from collections import Counter
from insert_reocr_data import process_bar, connect, table_exists
from sqlalchemy import create_engine


def create_table(cursor, opt = 1):
    if opt == 1:
        sql_createTb = """CREATE TABLE newspaper_page_ner (
                 year  INT,
                 month INT,
                 page INT,
                 ents_info VARCHAR(5000),
                 ents_freq VARCHAR(5000),
                 PRIMARY KEY(year, month, page))
                 """
    else:
        sql_createTb = """CREATE TABLE newspaper_ner_freq_label_url (
                 entity CHAR(500),
                 year  INT,
                 month INT,
                 page INT,
                 frequency INT,
                 label CHAR(10),
                 url CHAR(500),
                 PRIMARY KEY(entity, year, month, page))
                 """
    cursor.execute(sql_createTb)


def insert_mysql(df, table_name):
    engine = create_engine("mysql+pymysql://root:mysql123456@localhost:3306/europeana?charset=utf8")
    con = engine.connect()
    df.to_sql(table_name, con=con, if_exists='replace', index=False)
    con.close()


def named_entity_info_freq(text_fr):
    nlp_model_fr = spacy.load("fr_core_news_lg")
    nlp_model_fr.add_pipe("entityfishing", config={"language": "fr"})
    doc_fr = nlp_model_fr(text_fr)

    ents = []
    ents_info = {}
    for ent in doc_fr.ents:
        ents.append(ent.text)
        ents_info[ent.text] = {'label': ent.label_,
                               'kb_qid': ent._.kb_qid,
                               'url_wikidata': ent._.url_wikidata}

    return ents_info, ents


def get_info_freq(path):
    g = os.walk(path)
    year = []
    month = []
    page = []
    ents_info = []
    ents_freq = []
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
            info, ents = named_entity_info_freq(text_fr)
            ents_info.append(info)
            freq = dict(Counter(ents))
            ents_freq.append(freq)

            x += 1
            process_bar(x+1, n)

            data = {'ents_info': info, 'ents_freq': freq, 'year': ymp[0], 'month': ymp[1], 'page': ymp[2]}
            json_data = json.dumps(data)
            f2 = open('/Users/DXY/Documents/Project/entity_json/'+ str(ymp[0]) + '-' + str(ymp[1]) + '-' + str(ymp[2]) + '.json', 'w')
            f2.write(json_data)
            f2.close()

    return ents_info, ents_freq, year, month, page


def get_info_freq_from_json(path):
    year = []
    month = []
    page = []
    ents_info = []
    ents_freq = []
    g = os.walk(path)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            with open(os.path.join(path,file_name), 'r') as f:
                data = json.load(f)

            ents_info.append(data['ents_info'])
            ents_freq.append(data['ents_freq'])
            year.append(int(data['year']))
            month.append(int(data['month']))
            page.append(int(data['page']))

    return ents_info, ents_freq, year, month, page


def table4pageNer(ents_info, ents_freq, year, month, page):
    ents_info_str = [str(e) for e in ents_info]
    ents_freq_str = [str(e) for e in ents_freq]

    df = pd.DataFrame({"year": year,
                       "month": month,
                       "page": page,
                       "ents_info": ents_info_str,
                       "ents_freq": ents_freq_str})

    return df


def table4Ner(ents_info, ents_freq, year, month, page):
    lenth_entity = len(ents_freq)
    lst_entity = list()
    x = 0
    for i in range(lenth_entity):
        for k,v in ents_freq[i].items():
            lst_entity.append([k,  # entity
                               year[i],
                               month[i],
                               page[i],
                               v,  # frequency
                               ents_info[i][k]['label'],
                               ents_info[i][k]['url_wikidata']])
        x += 1
        process_bar(x + 1, lenth_entity)

    df = pd.DataFrame(lst_entity)
    df.columns = ['entity', 'year', 'month', 'page', 'frequency', 'label', 'url_wikidata']

    return df


def main():
    # path = '/Users/DXY/Documents/Project/modified_text'
    # ents_info, ents_freq, year, month, page = get_info_freq(path)

    # load data
    path = '/Users/DXY/Documents/Project/entity_json/'
    ents_info, ents_freq, year, month, page = get_info_freq_from_json(path)

    # # save data
    # data = {'ents_info': ents_info, 'ents_freq': ents_freq, 'year': year, 'month': month, 'page': page}
    # json_data = json.dumps(data)
    # f2 = open('json_entity_data.json', 'w')
    # f2.write(json_data)
    # f2.close()
    # print('\nSaved data!')

    # table newspaper_reocr_text
    df1 = table4pageNer(ents_info, ents_freq, year, month, page)
    table_name1 = 'newspaper_page_ner'
    conn = connect()
    cursor = conn.cursor()
    if table_exists(cursor, table_name1) == 0:
        create_table(cursor, 1)
        conn.commit()
    conn.close()
    cursor.close()
    print('Created table newspaper_page_ner')

    insert_mysql(df1, table_name1)
    print('Inserted data for table newspaper_page_ner')

    # table newspaper_ner_freq_label_url
    df2 = table4Ner(ents_info, ents_freq, year, month, page)
    table_name2 = 'newspaper_ner_freq_label_url'
    conn = connect()
    cursor = conn.cursor()
    if table_exists(cursor, table_name1) == 0:
        create_table(cursor, 2)
        conn.commit()
    conn.close()
    cursor.close()
    print('\nCreated table newspaper_ner_freq_label_url')

    insert_mysql(df2, table_name2)
    print('Inserted data for table')


if __name__ == '__main__':
    main()
