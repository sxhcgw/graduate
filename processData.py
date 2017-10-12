#coding=utf-8

#import jieba.posseg as peg #带词性
import jieba

data = '木质后盖蛮喜欢的'
path = r'file/resource/stopwords.txt'
file_path = r'file/resource/test1.txt'
seg_path = r'file/resource/seg_file.txt'
res_path = r'file/resource/res.txt'
#seg = peg.cut(data)   #精确模式
seg = jieba.cut(data)

#获取文件内容
def getFileContent(filePath):
    content = [line.strip() for line in open(filePath, 'r', encoding='utf-8').readlines()]
    return content

#去停用词
def seg_sentence(seg, stopWords):
    outstr = ''
    for word in seg:
        if word not in stopWords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr
#获得停用词
stopWords = getFileContent(path)
#保存最后结果
res = ''
#获取用户评论
fileContent = getFileContent(file_path)
#分词并去除停用词
for line in fileContent:
    line = line.strip()
    if line == '':
        continue
    tmp = jieba.cut(line)
    res += seg_sentence(tmp, stopWords)
    res += '\n'
#写入文件
seg_file = open(seg_path, 'w', encoding='utf-8')
seg_file.write(res)
seg_file.close()


#计算tf-idf值
class MyCorpus(object):
    def __iter__(self):
        for line in open(seg_path, 'r', encoding='utf-8'):
            yield line.split()

from gensim import corpora, models, similarities
Corp = MyCorpus()
dictionary = corpora.Dictionary(Corp)
corpus = [dictionary.doc2bow(text) for text in Corp]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
#把评论做成索引
query = '打电话 时有 回音 ， 买 父亲 、 十天 ， 、 '
vec_bow = dictionary.doc2bow(query.split())
vec_tfidf = tfidf[vec_bow]
# for item in corpus_tfidf:
#     print(item)
index = similarities.MatrixSimilarity(corpus_tfidf)
sims = index[vec_tfidf]
similarity = list(sims)
sim_file = open(res_path, 'w')
for i in similarity:
    sim_file.write(str(i) + "\n")
sim_file.close()


