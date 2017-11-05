#coding=utf-8

import jieba

data = '木质后盖,蛮喜欢的'
seg = jieba.cut(data)
for word in seg:
    print(word)
