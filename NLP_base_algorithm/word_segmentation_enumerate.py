import numpy as np
import xlrd

dic_path = 'data/综合类中文词库.xlsx'


def create_dic(file_path):
    workbook = xlrd.open_workbook(file_path)
    booksheet = workbook.sheet_by_index(0)
    col_values = booksheet.col_values(0)
    dic_words = {}
    max_len_word = 0
    for word in col_values:
        dic_words[word] = 0.00001
        len_word = len(word)
        if len_word > max_len_word:
            max_len_word = len_word

    print(len(dic_words))
    print(max_len_word)
    return dic_words, max_len_word


dic_words, max_len_word = create_dic(dic_path)

word_prob = {"北京": 0.03, "的": 0.08, "天": 0.005, "气": 0.005, "天气": 0.06, "真": 0.04, "好": 0.05, "真好": 0.04, "啊": 0.01,
             "真好啊": 0.02,
             "今": 0.01, "今天": 0.07, "课程": 0.06, "内容": 0.06, "有": 0.05, "很": 0.03, "很有": 0.04, "意思": 0.06, "有意思": 0.005,
             "课": 0.01,
             "程": 0.005, "经常": 0.08, "意见": 0.08, "意": 0.01, "见": 0.005, "有意见": 0.02, "分歧": 0.04, "分": 0.02, "歧": 0.005}
# 更新字典的值
for key, value in word_prob.items():
    dic_words[key] = value

# 枚举出所有可能的分词结果
def word_segmentation(input_str):
    segments = []
    if len(input_str) == 0:
        return segments
    max_split = min(len(input_str), max_len_word) + 1
    for idx in range(1, max_split):
        word = input_str[0:idx]
        if word in dic_words:
            segments_substr = word_segmentation(input_str[idx:])
            if (segments_substr == []) and (len(input_str[idx:]) == 0):
                segments.append([word])
            else:
                for seg in segments_substr:
                    seg = [word] + seg
                    segments.append(seg)
    return segments


def word_segment_naive(input_str):
    segments = word_segmentation(input_str)
    best_segment = []
    best_score = np.inf
    for seg in segments:
        log_prob = -1 * np.sum(np.log([dic_words[word] for word in seg]))
        if log_prob < best_score:
            best_segment = seg
            best_score = log_prob

    return best_segment


# 测试
print(word_segment_naive("北京的天气真好啊"))
print(word_segment_naive("今天的课程内容很有意思"))
print(word_segment_naive("经常有意见分歧"))
