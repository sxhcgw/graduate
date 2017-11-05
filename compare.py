

pair_path = r'file/pairs/pairs.txt'     #标注
ext_path = r'file/pairs/r_iphone6.txt' #提取

#获取文件内容
def getFileContent(filePath):
    content = [line.strip() for line in open(filePath, 'r', encoding='utf-8').readlines()]
    return content

def caculate():
    pairs = getFileContent(pair_path)
    exts = getFileContent(ext_path)
    dict = {}
    correct = 0
    for pair in pairs:
        if pair == '':
            continue
        val = dict.setdefault(pair, 0)
        dict[pair] = val + 1
    for ext in exts:
        if ext in dict.keys():
            val = dict.get(ext)
            if val > 0:
                correct = correct + 1
                dict[ext] = val - 1
    corr_ratio = correct / exts.__len__()
    recall_ration = correct / pairs.__len__()
    print("正确率: ", corr_ratio)
    print("召回率: ", recall_ration)

caculate()
