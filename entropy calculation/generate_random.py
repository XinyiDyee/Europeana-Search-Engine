import random

charset = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","z","à","â","ç","é","è","ê","ë","î","ï","ô","û","ù","ü","ÿ","ñ","æ","œ"]

random_list = [random.choice(charset) for i in range(12500000)]
random_str = ''.join(random_list)
print(random_str)

with open('random.txt','w',encoding="utf-8") as f:
    f.write(random_str)