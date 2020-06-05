import xlrd
import numpy as np

dic_path = './data/综合类中文词库.xlsx'
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

for key, value in word_prob.items():
    dic_words[key] = value


def create_graph(input_str):
    N = len(input_str)
    graph = {}
    for idx_end in range(1, N + 1):
        temp_list = []
        max_split = min(idx_end, max_len_word)
        for idx_start in range(idx_end - max_split, idx_end):
            word = input_str[idx_start:idx_end]
            if word in dic_words:
                temp_list.append(idx_start)
        graph[idx_end] = temp_list
    return graph


def word_segment_viterbi(input_str):
    graph = create_graph(input_str)
    N = len(input_str)
    m = [np.inf] * (N + 1)
    m[0] = 0
    last_index = [0] * (N + 1)
    for idx_end in range(1, N + 1):
        for idx_start in graph[idx_end]:
            log_prob = round(-1 * np.log(dic_words[input_str[idx_start:idx_end]])) + m[idx_start]
            if log_prob < m[idx_end]:
                m[idx_end] = log_prob
                last_index[idx_end] = idx_start
    best_segment = []
    i = N
    while True:
        best_segment.insert(0, input_str[last_index[i]:i])
        i = last_index[i]
        if i == 0:
            break
    return best_segment


print(word_segment_viterbi("北京的天气真好啊"))
print(word_segment_viterbi("今天的课程内容很有意思"))
print(word_segment_viterbi("经常有意见分歧"))
