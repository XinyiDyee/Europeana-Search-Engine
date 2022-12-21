from sklearn.feature_extraction.text import CountVectorizer
import os


def n_gram(txt,dic):
    content_list = [txt]

    vectorizer = CountVectorizer(ngram_range=(1, 1), min_df=1)
    X = vectorizer.fit_transform(content_list)

    vocab_list = vectorizer.get_feature_names_out()
    for word in vocab_list:
        dic[word]=dic.get(word, 0) + 1
    return dic

def main():
    path_in = 'C:\\Users\\86136\\Desktop\\fdh\\modified_text'
    path_out = 'C:\\Users\\86136\\Desktop\\fdh\\modified_text'
    g = os.walk(path_in)
    dic={}
    for path, dir_list, file_list in g:
        for file_name in file_list:
            with open(os.path.join(path_in, file_name),"r", encoding="utf-8") as f:
                txt=f.read()
            dic=n_gram(txt,dic)
    with open(path_out, "w", encoding="utf-8") as ff:
        ff.write(dic)


if __name__ == '__main__':
    main()