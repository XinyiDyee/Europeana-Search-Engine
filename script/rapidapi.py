import requests
import json
import os


def grammar_checker(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:  # to read the original txt
        txt = f.read()

    txt = txt.replace('ſ', 's')
    txt = txt.replace('’', "'")
    txt = txt.replace('é̂', 'ê')
    txt = txt.replace('ê', 'ê')
    txt = txt.replace('à', 'à')
    txt = txt.replace('é', 'é')
    txt = txt.replace('ù', 'ù')
    txt = txt.replace('¬ ', '')
    txt = txt.replace('  ', ' ')

    url = "https://textgears-textgears-v1.p.rapidapi.com/spelling"

    data = {'text': txt, 'language': 'fr-FR'}
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "265d49cb0cmsh5598c5df0b98834p15068ajsn25409b7f642c",
        "X-RapidAPI-Host": "textgears-textgears-v1.p.rapidapi.com"
    }
    params = {
        'text': txt,
        'lang': 'fr_FR',
    }
    response = requests.request("POST", url, data=data, headers=headers, params=params)
    json_response = response.json()
    modi_dic = json.dumps(json_response, indent=4, ensure_ascii=False)
    modi_dic = json.loads(modi_dic)
    modi_dic = modi_dic['response']
    errors = modi_dic['errors']
    un_modified = txt

    modified = un_modified
    sub = 0  # record the difference of part1's length before modification and after modification

    for i in range(len(errors)):
        message = errors[i]
        offsets = message["offset"]
        lengths = message["length"]
        rep = message["better"]  # a list with all possible replacements
        if (len(rep) == 0):
            continue
        anwser = rep[0]
        old_word = un_modified[offsets:(offsets + lengths)]

        part1 = modified[:offsets + sub]
        part2 = un_modified[offsets:]
        new_part2 = part2.replace(old_word, anwser, 1)
        sub = sub + len(anwser) - len(old_word)

        modified = part1 + new_part2

    with open(output_file, "w", encoding='utf-8') as fm:
        fm.write(modified)


def main():
    path_in = 'C:\\Users\\86136\\Desktop\\fdh\\text'
    path_out = 'C:\\Users\\86136\\Desktop\\fdh\\modified_text'
    g = os.walk(path_in)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            grammar_checker(os.path.join(path_in, file_name),os.path.join(path_out, file_name))


if __name__ == '__main__':
    main()



