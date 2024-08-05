import xlsxwriter
from matplotlib import pyplot as plt

from kannada import syllabify_kn


class Text:
    text_string = ""
    cleaned_text_string = ""
    length = 0

    first_transition_map = {}
    cv1_count = {}
    total_first_order = 0

    second_transition_map = {}
    cv2_count = {}
    total_second_order = 0

    def __init__(self, path: str):
        self.read_text(path)
        self.cleaned_text_string = self.text_string

    def __str__(self):
        return self.cleaned_text_string

    def read_text(self, path: str):
        file = open(path + '.txt', 'r', encoding='utf8')
        for line in file.readlines():
            self.text_string += line
        file.close()

    def insert_in_first_map(self, char):
        if char in self.first_transition_map:
            self.first_transition_map[char] += 1
        else:
            self.first_transition_map[char] = 1

    def count_cv1(self):
        for char, nxt in self.first_transition_map.keys():
            if char not in self.cv1_count.keys():
                val = 0
                for cv1, cv2 in self.first_transition_map.keys():
                    if cv1 == char:
                        val += self.first_transition_map[(cv1, cv2)]
                self.cv1_count[char] = val

    def write_first_order(self):
        count_first_order()
        self.count_cv1()
        self.total_first_order = sum(self.first_transition_map.values())
        self.first_transition_map = dict(sorted(self.first_transition_map.items(), key=lambda x: x[1], reverse=True))
        workbook = xlsxwriter.Workbook('mapped/first_order_kn.xlsx')
        wk = workbook.add_worksheet('first_order')
        wk.write_row(0, 0, ('CV1', 'CV2', 'Freq', 'Prob', 'CV1 | CV2'))
        row = 1
        for each in self.first_transition_map:
            wk.write_row(row, 0, (each[0], each[1], self.first_transition_map[each],
                                  self.first_transition_map[each] / self.total_first_order,
                                  self.first_transition_map[each] / self.cv1_count[each[0]]))
            row += 1
        workbook.close()

    def insert_in_second_map(self, char):
        if char in self.second_transition_map:
            self.second_transition_map[char] += 1
        else:
            self.second_transition_map[char] = 1

    def count_cv2(self):
        for char, nxt, nxt_nxt in self.second_transition_map.keys():
            if (char, nxt) not in self.cv2_count.keys():
                val = 0
                for cv1, cv2, cv3 in self.second_transition_map.keys():
                    if (cv1, cv2) == (char, nxt):
                        val += self.second_transition_map[(cv1, cv2, cv3)]
                self.cv2_count[(char, nxt)] = val

    def sort_second_order(self):
        sorted_dict = {}
        count_second_order()
        self.count_cv2()
        self.second_transition_map = dict(
            sorted(self.second_transition_map.items(), key=lambda x: x[1], reverse=True))
        self.total_second_order = sum(self.second_transition_map.values())
        for pair in self.cv2_count.keys():
            sorted_dict[pair] = []
            for each in self.second_transition_map.keys():
                if pair == (each[0], each[1]):
                    if each not in sorted_dict[pair]:
                        sorted_dict[pair].append(each)
        workbook = xlsxwriter.Workbook('mapped/second_order_filtered_kn.xlsx')
        wk = workbook.add_worksheet('second_order')
        wk.write_row(0, 0, ('CV1', 'CV2', 'CV3', 'Freq', 'Prob', 'CV1 + CV2 | CV3'))
        row = 1
        for key in sorted_dict.keys():
            ls = sorted_dict[key]
            if 3 >= len(ls) > 1:
                for each in ls:
                    wk.write_row(row, 0, (each[0], each[1], each[2], self.second_transition_map[each],
                                          self.second_transition_map[each] / self.total_second_order,
                                          self.second_transition_map[each] / self.cv2_count[(each[0], each[1])]))
                    row += 1
        workbook.close()

    def write_second_order(self):
        count_second_order()
        self.count_cv2()
        self.total_second_order = sum(self.second_transition_map.values())
        self.second_transition_map = dict(
            sorted(self.second_transition_map.items(), key=lambda x: x[1], reverse=True))
        workbook = xlsxwriter.Workbook('mapped/second_order_kn.xlsx')
        wk = workbook.add_worksheet('second_order')
        wk.write_row(0, 0, ('CV1', 'CV2', 'CV3', 'Freq', 'Prob', 'CV1 + CV2 | CV3'))
        row = 1
        for each in self.second_transition_map:
            wk.write_row(row, 0, (each[0], each[1], each[2], self.second_transition_map[each],
                                  self.second_transition_map[each] / self.total_second_order,
                                  self.second_transition_map[each] / self.cv2_count[(each[0], each[1])]))
            row += 1
        workbook.close()


def count_first_order():
    spl = text.cleaned_text_string.split(" ")
    for i in spl:
        syllablify = syllabify_kn(i)
        if len(syllablify) == 1:
            pass
        else:
            for k in range(len(syllablify) - 1):
                curr_char = syllablify[k]
                next_char = syllablify[k + 1]
                text.insert_in_first_map((curr_char, next_char))


def count_second_order():
    spl = text.cleaned_text_string.split(" ")
    for i in spl:
        syllablify = syllabify_kn(i)
        if len(syllablify) == 1:
            pass
        elif len(syllablify) == 2:
            pass
        else:
            for k in range(len(syllablify) - 2):
                curr_char = syllablify[k]
                next_char = syllablify[k + 1]
                next_next_char = syllablify[k + 2]
                text.insert_in_second_map((curr_char, next_char, next_next_char))


def freq_analysis(path: str):
    freq_map = {}
    file = open(path + '.txt', 'r', encoding='utf8')
    for line in file:
        for word in line.split(' '):
            word = word.strip()
            if word in freq_map:
                freq_map[word] += 1
            else:
                freq_map[word] = 1
    file.close()
    workbook = xlsxwriter.Workbook('mapped/freq_analysis_kn.xlsx')
    wk = workbook.add_worksheet('freq_analysis')
    wk.write_row(0, 0, ('Word', 'Frequency'))
    row = 1
    for each in freq_map:
        wk.write_row(row, 0, (each, freq_map[each]))
        row += 1
    workbook.close()


def plot_first_order():
    count_first_order()
    chosen_cv1 = input('Enter CV1: ')
    cv1_transitions = [text.first_transition_map[i] for i in text.first_transition_map.keys() if i[0] == chosen_cv1]
    cv1_transitions.sort(reverse=True)
    plt.figure(figsize=(10, 5))
    plt.plot(cv1_transitions)
    plt.xlabel('CV2')
    plt.ylabel('Frequency')
    plt.title('Frequency of CV1 transitions')
    plt.show()


if __name__ == '__main__':
    # freq_analysis('final Kannada corpus text.11.06.23')

    text = Text('final Kannada corpus text.11.06.23')
    plot_first_order()  # text.write_first_order()  # text.write_second_order()

# plotting freq column * freq(cv1)
# python - plotting freq column per cv1
