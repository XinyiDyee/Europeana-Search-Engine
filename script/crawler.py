import requests
import json


if __name__ == '__main__':
    results_dic = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }

    identifier_url = 'https://newspapers.eanadev.org/api/v2/search.json?wskey=api2demo&qf=LANGUAGE%3A%22fr%22&qf=proxy_dcterms_issued%3A%5B1704-06-01+TO+1794-08-31%5D&qf=collection%3Anewspaper&qf=contentTier%3A%282+OR+3+OR+4%29&query=*&rows=0&profile=facets&facet=europeana_id&f.europeana_id.facet.limit=2000'
    response = requests.get(identifier_url, headers=headers)
    html = response.text
    html = json.loads(html)

    for count,journal in enumerate(html['facets'][0]['fields']):
		try:
			journal_identifier = journal['label']
			results_dic[journal_identifier] = {}

			manifest_url = 'https://iiif.europeana.eu/presentation' + journal_identifier + '/manifest'
			journal_manifest = requests.get(manifest_url, headers=headers).text
			journal_manifest = json.loads(journal_manifest)

			journal_title = journal_manifest['label'][0]['@value']
			results_dic[journal_identifier]['title'] = journal_title

			journal_time = journal_title.split(' ')[-1]
			journal_year = journal_time.split('-')[0]
			journal_month = journal_time.split('-')[1]
			results_dic[journal_identifier]['year'] = journal_year
			results_dic[journal_identifier]['month'] = journal_month

			results_dic[journal_identifier]['img'] = {}
			results_dic[journal_identifier]['text'] = {}

			for i,page in enumerate(journal_manifest['sequences'][0]['canvases']):
				img_url = page['images'][0]['resource']['@id']
				text_url_previous = page['otherContent'][0]
				text_url_previous_content = json.loads(requests.get(text_url_previous, headers=headers).text)
				text_url_final = text_url_previous_content['resources'][0]['resource']['@id']
				page_text = json.loads(requests.get(text_url_final, headers=headers).text)['value']
				results_dic[journal_identifier]['img'][i] = img_url
				results_dic[journal_identifier]['text'][i] = page_text
		except:
			pass

        if (count+1)%10 == 0:
            with open(str(count+1)+'.json', 'w') as fp:
                json.dump(results_dic, fp)
            results_dic = {}
            print('?????????',str(count+1),'/1200')
