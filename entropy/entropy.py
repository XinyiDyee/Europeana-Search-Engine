import re
import numpy as np
from collections import Counter


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
    text = text.replace('\n', '')
    text = text.replace('¬ ', '')
    text = text.replace(' ', '')
    text = text.replace('-','')
    return re.compile('[^a-zàâçéèêëîïôûùüÿñæœ .-]+').sub('', text)

def gram_1(text):
    length_1_substrings = [text[i:i + 1] for i in range(len(text) - 1)]
    length_1_substring_counts = Counter(length_1_substrings)
    normalizer_1 = sum(length_1_substring_counts.values())
    length_1_probabilities = dict((k, float(v) / normalizer_1) for k, v in length_1_substring_counts.items())
    entropy_1 = -sum(p * np.log2(p) for p in length_1_probabilities.values())
    return entropy_1

def gram_2(text):
    length_2_substrings = [text[i: i + 2] for i in range(len(text) - 2)]
    length_2_substring_counts = Counter(length_2_substrings)
    normalizer_2 = sum(length_2_substring_counts.values())
    length_2_probabilities = dict((k, float(v) / normalizer_2) for k, v in length_2_substring_counts.items())
    entropy_2 = -sum(p * np.log2(p) for p in length_2_probabilities.values())
    return entropy_2

if __name__ == '__main__':
    fList = ['french','origin', 'reocr', 'grammar','random']
    for fname in fList:
        # Read and normalise input text
        with open( fname+'.txt', "r",encoding="utf-8") as f:
            text = f.read()[:12500000]
        text = clean(text)
        entropy_1 = gram_1(text)
        entropy_2 = gram_2(text)

        print(fname,'\n1-gram entropy:%.2f \n2-gram entropy:%.2f' %(entropy_1,entropy_2))


