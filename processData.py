#coding=utf-8

#import jieba.posseg as peg #带词性
import jieba

# data = '木质后盖蛮喜欢的'
path = r'file/tmp/stopwords.txt'     #停用词表
# file_path = r'file/tmp/test1.txt'    #原始数据
# seg_path = r'file/tmp/seg_file.txt'  #分词结果
# res_path = r'file/tmp/res.txt'       #相似度
# distinct_path = r'file/tmp/distinct.txt'       #最终结果

file_path = r'file/resource/huaweimaimang.txt'    #原始数据
seg_path = r'file/seg/seg_huaweimaimang.txt'  #分词结果
res_path = r'file/sim/sim_huaweimaimang.txt'       #相似度
distinct_path = r'file/res/distinct_huaweimaimang.txt'       #最终结果

#seg = peg.cut(data)   #精确模式
# seg = jieba.cut(data)

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

def process():
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

def model():
    Corp = MyCorpus()
    dictionary = corpora.Dictionary(Corp)
    corpus = [dictionary.doc2bow(text) for text in Corp]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    #把评论做成索引

    index = similarities.MatrixSimilarity(corpus_tfidf)
    content = getFileContent(file_path)
    seg_content = getFileContent(seg_path)
    i = 0
    res_tmp = []
    for seg_item in seg_content:
        vec_bow = dictionary.doc2bow(seg_item.split())
        vec_tfidf = tfidf[vec_bow]
        sims = index[vec_tfidf]
        similarity = list(sims)
        j = 0
        flag = True
        for sim in similarity:
            if j <= i:   #后边的不和前边的进行比较
                j = j + 1
                continue
            if sim >= 0.95:
                flag = False
                break
            j = j + 1
        if flag:
            res_tmp.append(content[i])
        i = i + 1
    distinct_file = open(distinct_path, 'w', encoding='utf-8')
    for item in res_tmp:
        distinct_file.write(item + "\n")
    distinct_file.close()
process()
model()
