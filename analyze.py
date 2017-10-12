#coding=utf-8

#    1. 正确率 = 提取出的正确信息条数 /  提取出的信息条数
#    2. 召回率 = 提取出的正确信息条数 /  样本中的信息条数
path = r'file/output05.txt'


def read_data(path):
    file = open(path, 'r', encoding='utf-8')
    lines = file.readlines()
    # print(len(lines))
    # print(lines[0].split())
    sentences = []  #保存评论
    reals = []      #保存实际标注
    predicts = []    #预测结果
    sentence = ""
    real = ""
    predict = ""
    for line in lines:
        if line.rstrip() == '':
            sentences.append(sentence)
            reals.append(real)
            predicts.append(predict)
            sentence = ""
            real = ""
            predict = ""
        else:
            origin = line.split()
            sentence = sentence + origin[0]
            real = real + origin[1]
            predict = predict + origin[2]

    print("评论内容: ", sentences)
    print("标注: ", reals)
    print("预测: ", predicts)
    print("评论数: ", len(sentences))
    print("标注数: ", len(reals))
    print("预测数: ", len(predicts))
    return reals, predicts


def test(reals, predicts):
    real_num = 0
    pre_num = 0
    for real in reals:
        real_num += real.count('B')
    for predict in predicts:
        pre_num += predict.count('B')
    print("实际命名实体数目: ", real_num)
    print("预测命名实体数目: ", pre_num)


def caculate(reals, predicts):
    correct_info = 0   #正确信息条数
    extract_info = 0   #提取信息条数
    sample_info = 0     #样本中的信息条数
    is_entity = False
    for i in range(len(reals)):
        is_entity = False
        real = reals[i]
        predict = predicts[i]
        real_list = list(real)
        predict_list = list(predict)
        for j in range(len(real_list)):
            if is_entity:
                if real_list[j] == predict_list[j]:
                    if j == len(real_list)-1:
                        correct_info = correct_info + 1
                        is_entity = False
                    elif real_list[j] == 'O':
                        correct_info = correct_info + 1
                        is_entity = False
                    elif real_list[j] == 'B':
                        correct_info = correct_info + 1
                        extract_info = extract_info + 1
                        sample_info = sample_info + 1
                else:
                    is_entity = False
                    if real_list[j] == 'B':
                        sample_info = sample_info + 1
                        if predict_list[j] == 'O':
                            correct_info = correct_info + 1
                    if real_list[j] == 'I':
                        if predict_list[j] == 'B':
                            extract_info = extract_info + 1
                    if real_list[j] == 'O':
                        if predict_list[j] == 'B':
                            extract_info = extract_info + 1
                            correct_info = correct_info + 1
            else:
                if real_list[j] == predict_list[j]:
                    if real_list[j] == 'B':
                        sample_info = sample_info + 1
                        extract_info = extract_info + 1
                        is_entity = True
                else:
                    if predict_list[j] == 'B':
                        extract_info = extract_info + 1
                    if real_list[j] == 'B':
                        sample_info = sample_info + 1

    print("样例数目: ", sample_info)
    print("提取数目: ", extract_info)
    print("正确标注数目: ", correct_info)
    print("准确率: ", correct_info/extract_info)
    print("召回率:", correct_info/sample_info)




if __name__ == "__main__":
    reals, predicts = read_data(path)
    test(reals, predicts)
    caculate(reals, predicts)

# if __name__ == "__main__":
#     reals = ['OOOOBIBIIOBI']
#     predicts = ['OOOOOOOOOOBI']
#     caculate(reals, predicts)