import pandas as pd
import numpy as np
import re


# Function to normalise the text.
# remove characters like numbers
def clean(text):
    text = text.replace('ſ', 's')
    text = text.replace('’', "'")
    text = text.replace('é̂', 'ê')
    text = text.replace('ê', 'ê')
    text = text.replace('à', 'à')
    text = text.replace('é', 'é')
    text = text.replace('ù', 'ù')
    text = text.replace('\n', ' ')
    text = text.replace('¬ ', '')
    return re.compile('[^a-zàâçéèêëîïôûùüÿñæœ .-]+').sub('', text)

if __name__ == '__main__':

    # Dictionary for letter counts
    dic = pd.read_csv('dictionary.csv')
    dic['word'] = dic['word'].str.lower()
    fr_dic = dic['word'].tolist()
    print(fr_dic)
    in_dic = 0
    out_dic = 0
    fList = ['origin','reocr','grammar']
    for fname in fList:
        # Read and normalise input text
        with open(fname+'.txt', "r",encoding="utf-8") as f:
            text = f.read()
            text = clean(text)
        words = text.lower().split(' ')
        words_dic = {}
        for word in words:
            if word in words_dic:
                words_dic[word] += 1
            else:
                words_dic[word] = 1
        for word in words_dic.keys():
            if word in fr_dic:
                in_dic += words_dic[word]
            else:
                out_dic += words_dic[word]
        ratio = in_dic / (in_dic + out_dic)
        print(fname,ratio)