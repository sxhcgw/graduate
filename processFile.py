

file_path = r'file/crf/resource/final_data.txt'
res_path = r'file/crf/result/res_final.data'
dic_path = r'file/crf/dic/dictionary.txt'
predict_path = r'file/crf/predict/res_output_final.txt'

#获取文件内容
def getFileContent(filePath):
    content = [line.strip() for line in open(filePath, 'r', encoding='utf-8').readlines()]
    return content

def trans():
    content = getFileContent(file_path)
    res = ''
    for item in content:
        tmp = list(item)
        for ch in tmp:
            if ch != ' ':
                res = res + ch + '\n'
        res = res + '\n'
    res_file = open(res_path, 'w', encoding='utf-8')
    res_file.write(res)
    res_file.close()

def extract():
    res = set()
    chs = getFileContent(predict_path)
    word = ''
    for ch in chs:
        if ch == '':
            continue
        tmp = ch.split()
        if tmp.__len__() < 2:
            continue
        if tmp[1] == 'I':
            word = word + tmp[0]
        elif tmp[1] == 'B':
            if word != '':
                res.add(word)
                word = ''
            word = word + tmp[0]
        elif tmp[1] == 'O':
            if word != '':
                res.add(word)
                word = ''
    dic_file = open(dic_path, 'w', encoding='utf-8')
    str = ''
    for item in res:
        str =str + item + '\n'
    dic_file.write(str)
    dic_file.close()

#将文本变为crf格式
#trans()
#crf进行预测
#...
#提取特征并构造词典
extract()