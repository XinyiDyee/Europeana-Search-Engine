import requests
import json
import os


def grammar_checker(file_in_list, file_out_list):
    i=0
    for file in file_in_list:
        with open(file, "r", encoding="utf-8") as f:  # to read the original txt
            t = f.read()
        if (i==0):
            txt=t
        else:
            txt=txt+'asdfghjkl'+t
        i=i+1

    txt = txt.replace('ſ', 's')
    txt = txt.replace('’', "'")
    txt = txt.replace('é̂', 'ê')
    txt = txt.replace('ê', 'ê')
    txt = txt.replace('à', 'à')
    txt = txt.replace('é', 'é')
    txt = txt.replace('ù', 'ù')
    txt = txt.replace('\n', ' ')
    txt = txt.replace('asdfghjkl', '\n\n\n')
    txt = txt.replace('¬ ', '')
    txt = txt.replace('  ', ' ')

    api_key = "866e7cafd65bbf48"
    endpoint = "https://api.languagetoolplus.com/v2/check"

    data = {'text': txt}
    params = {
        'text': txt,
        'language': 'fr',
        'username': 'xingchen.li@epfl.ch',
        'apiKey': api_key,
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(endpoint, headers=headers, data=data, params=params)
    print(response)
    json_response = response.json()
    modi_dic = json.dumps(json_response, indent=4, ensure_ascii=False)
    modi_dic = json.loads(modi_dic)
    un_modified = txt

    modified = un_modified
    matches = modi_dic['matches']
    sub = 0  # record the difference of part1's length before modification and after modification
    for i in range(len(matches)):
        message = matches[i]
        rep = message["replacements"]  # a list with all possible replacements
        if (len(rep)==0):
          continue
        ans = rep[0]
        anwser = ans['value']
        offsets = message["offset"]
        lengths = message["length"]
        old_word = un_modified[offsets:(offsets + lengths)]

        part1 = modified[:offsets + sub]
        part2 = un_modified[offsets:]
        new_part2 = part2.replace(old_word, anwser, 1)
        sub = sub + len(anwser) - len(old_word)

        modified = part1 + new_part2

    modified_list=modified.split('\n\n\n')
    j=0
    for out in file_out_list:
        with open(out, "w", encoding='utf-8') as fm:
            fm.write(modified_list[j])
        j=j+1


def main():
    path_in = 'C:\\Users\\86136\\Desktop\\fdh\\text'
    path_out = 'C:\\Users\\86136\\Desktop\\fdh\\modified_text'
    g = os.walk(path_in)
    for path, dir_list, file_list in g:
        i=0
        file_in_list = []
        file_out_list = []
        for file_name in file_list:
            if(i==0):
                file_in_list = []
                file_out_list = []
            if(i<1):
                file_in_list.append(os.path.join(path_in, file_name))
                file_out_list.append(os.path.join(path_out, file_name))
                i=i+1
            if(i==1):
                grammar_checker(file_in_list, file_out_list)
                i=0


if __name__ == '__main__':
    main()
