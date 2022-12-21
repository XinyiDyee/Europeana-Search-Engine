from flask import Flask, redirect, url_for, request, render_template, session, escape,  Response
import pymysql
import json

app = Flask(__name__,static_folder='static',static_url_path='/static')


@app.route('/homepage/',methods=['POST','GET'])
def homepage():
	return render_template('homepage.html')

@app.route('/details/<id>/<page>/',methods = ['POST','GET'])
def details(id,page):
	conn = pymysql.connect(host='localhost', user='root', password='', db='newspaper_info_content_all', charset='utf8')
	cur1 = conn.cursor()
	cur2 = conn.cursor()
	sql1 = "select a.image_url, a.year, a.month, b.grammar_check_text_line \
	from newspaper_info_content_all as a \
	left join newspaper_grammar_check_text as b \
	on (a.year = b.year and a.month = b.month and a.page = b.page) \
	where a.identifier = '%s' and a.page = '%s'" %(id, page)
	sql2 = "select a.entity, a.url_wikidata \
	from newspaper_ner_freq_label_url as a \
	left join newspaper_info_content_all as b \
	on (a.year=b.year and a.month=b.month and a.page=b.page) \
	where b.identifier = '%s' and b.page = '%s'" %(id, page)
	cur1.execute(sql1)
	u1 = cur1.fetchall()
	cur2.execute(sql2)
	u2 = cur2.fetchall()
	conn.close()
	return render_template('details.html',u1=u1,u2=u2,identifier=id,page_next=str(int(page)+1),page_previous=str(int(page)-1))


@app.route('/searchall/',methods = ['POST','GET'])
def searchall():
	category = request.form.get('category')
	keyword = request.form['input']
	conn = pymysql.connect(host='localhost', user='root', password='', db='newspaper_info_content_all', charset='utf8')
	cur = conn.cursor()
	print(category)
	if category == None:
		sql = "select tabel1.identifier, tabel1.page, tabel1.image_url, tabel1.grammar_check_text_line \
		from (select a.year, a.month, a.page, a.identifier, a.image_url, a.text, b.grammar_check_text_line from newspaper_info_content_all AS a LEFT JOIN newspaper_grammar_check_text as b on a.year = b.year and a.month = b.month and a.page = b.page) as tabel1 \
		where tabel1.grammar_check_text_line LIKE '%" + keyword + "%' limit 100"
	else:
		sql = "select b.identifier, a.page, b.image_url, c.grammar_check_text_line, a.frequency \
		from (select * from newspaper_ner_freq_label_url where entity like '%" + keyword + "%' and label= '" + category +"') as a \
		left join (select * from newspaper_info_content_all) as b \
		on a.page=b.page and a.year=b.year and a.month=b.month \
		left join (select * from newspaper_grammar_check_text) as c \
		on a.page = c.page and a.year = c.year and a.month = c.month \
		order by a.frequency DESC limit 100"
		print(sql)

	cur.execute(sql)
	u = cur.fetchall()
	conn.close()
	return render_template('search_results.html',u=u)

@app.route('/search/',methods = ['POST','GET'])
def search():
	keyword = request.form['input']
	conn = pymysql.connect(host='localhost', user='root', password='', db='newspaper_info_content_all', charset='utf8')
	cur = conn.cursor()
	sql = "select tabel1.identifier, tabel1.page, tabel1.image_url, tabel1.grammar_check_text_line \
	from (select a.year, a.month, a.page, a.identifier, a.image_url, a.text, b.grammar_check_text_line from newspaper_info_content_all AS a LEFT JOIN newspaper_grammar_check_text as b on a.year = b.year and a.month = b.month and a.page = b.page) as tabel1 \
	where tabel1.grammar_check_text_line LIKE '%" + keyword + "%' limit 100"

	cur.execute(sql)
	u = cur.fetchall()
	conn.close()
	return render_template('search_results.html',u=u)

@app.route('/ngram/',methods = ['POST','GET'])
def ngram():
	keyword = request.form['input_ngram']
	conn = pymysql.connect(host='localhost', user='root', password='', db='newspaper_info_content_all', charset='utf8')
	cur = conn.cursor()
	sql = "select entity, year, month, sum(frequency) as frequency \
	from newspaper_ner_freq_label_url \
	where entity = '%s' \
	group by entity, year, month \
	order by year, month" %(keyword)
	cur.execute(sql)
	u = cur.fetchall()
	data = []
	for ocur in u:
		year = ocur[1]
		month = ocur[2]
		time = str(year) + "-" + str(month)
		frequency = int(ocur[3])
		data.append([time,frequency])
	conn.close()
	data = json.dumps(data,ensure_ascii=False)
	return render_template('ngram.html',data=data,word=keyword)

if __name__ == '__main__':
	app.run('localhost',debug = True)
