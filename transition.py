import docx2txt
import xlsxwriter

from monosyllable import *


class Word:
    original_word = ''
    word = ''

    def __init__(self, word: str):
        self.original_word = word
        self.word = word
        self.clean()

    def clean(self):
        global aksharas
        cleaned_word = ''.join([c for c in self.word if c in aksharas.keys()])
        self.word = cleaned_word


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
        self.clean()

    def __str__(self):
        return self.cleaned_text_string

    def read_text(self, path: str):
        file = open(path + '.txt', 'r', encoding='utf8')
        self.text_string = file.readlines()[0]
        file.close()

    def clean(self):
        global aksharas
        cleaned = ''.join([c for c in self.text_string if c in aksharas.keys()])
        self.cleaned_text_string = cleaned

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
        workbook = xlsxwriter.Workbook('mapped/first_order.xlsx')
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

    def write_second_order(self):
        count_second_order()
        self.count_cv2()
        self.total_second_order = sum(self.second_transition_map.values())
        self.second_transition_map = dict(sorted(self.second_transition_map.items(), key=lambda x: x[1], reverse=True))
        workbook = xlsxwriter.Workbook('mapped/second_order.xlsx')
        wk = workbook.add_worksheet('second_order')
        wk.write_row(0, 0, ('CV1', 'CV2', 'CV3', 'Freq', 'Prob', 'CV1 + CV2 | CV3'))
        row = 1
        for each in self.second_transition_map:
            wk.write_row(row, 0, (each[0], each[1], each[2], self.second_transition_map[each],
                                  self.second_transition_map[each] / self.total_second_order,
                                  self.second_transition_map[each] / self.cv2_count[(each[0], each[1])]))
            row += 1
        workbook.close()


def hi_syllables(word):
    signs = [u'\u0901', u'\u0902', u'\u0903', u'\u093c', u'\u093e', u'\u093f', u'\u0940',
             u'\u0941', u'\u0942', u'\u0943', u'\u0944', u'\u0946',
             u'\u0947', u'\u0948', u'\u094a', u'\u094b', u'\u094c',
             u'\u094d']
    syllables = []
    for char in word:
        if char in signs and len(syllables) != 0:
            syllables[-1] = syllables[-1] + char
        else:
            try:
                if '्' == syllables[-1][-1]:
                    syllables[-1] = syllables[-1] + char
                else:
                    syllables.append(char)
            except IndexError:
                syllables.append(char)
    return syllables


def count_first_order():
    spl = text.cleaned_text_string.split(" ")
    for i in spl:
        syllablify = hi_syllables(i)
        if len(syllablify) == 1:
            # text.insert_in_first_map((syllablify[0], ''))
            pass
        else:
            for k in range(len(syllablify) - 1):
                curr_char = syllablify[k]
                next_char = syllablify[k + 1]
                text.insert_in_first_map((curr_char, next_char))


def count_second_order():
    spl = text.cleaned_text_string.split(" ")
    for i in spl:
        syllablify = hi_syllables(i)
        if len(syllablify) == 1:
            # text.insert_in_second_map((syllablify[0], '', ''))
            pass
        elif len(syllablify) == 2:
            # text.insert_in_second_map((syllablify[0], syllablify[1], ''))
            pass
        else:
            for k in range(len(syllablify) - 2):
                curr_char = syllablify[k]
                next_char = syllablify[k + 1]
                next_next_char = syllablify[k + 2]
                text.insert_in_second_map((curr_char, next_char, next_next_char))


def convert_docx_txt(path: str):
    text = docx2txt.process(path + '.docx')
    with open(path + '.txt', 'w', encoding='utf8') as f:
        f.write(text)


def clean_non_hindi_words(hindi_path: str, string_path: str):
    # hindi_words = []
    # file = open(hindi_path + '.txt', 'r', encoding='utf8')
    # for line in file:
    #     word = Word(line)
    #     hindi_words.append(word.word)
    # file.close()
    # print(hindi_words)
    # print(len(hindi_words))

    string_words = []
    cleaned_words = []
    removed = []
    file = open(string_path + '.txt', 'r', encoding='utf8')
    for line in file:
        for word in line.split(' '):
            word = Word(word)
            string_words.append(word.word)
            # if word.word in hindi_words:
            with open(string_path + '_cleaned_chars.txt', 'a', encoding='utf8') as f:
                f.write(word.word + ' ')
            cleaned_words.append(word.word)
            # else:
            #     removed.append(word.word)
            #     with open('mapped/removed.txt', 'a', encoding='utf8') as f:
            #         f.write(word.word + ' ')
    file.close()
    print(len(string_words), len(cleaned_words), len(removed))


def freq_analysis(path: str):
    freq_map = {}
    file = open(path + '.txt', 'r', encoding='utf8')
    for line in file:
        for word in line.split(' '):
            if word in freq_map:
                freq_map[word] += 1
            else:
                freq_map[word] = 1
    file.close()
    workbook = xlsxwriter.Workbook('mapped/freq_analysis.xlsx')
    wk = workbook.add_worksheet('freq_analysis')
    wk.write_row(0, 0, ('Word', 'Frequency'))
    row = 1
    for each in freq_map:
        wk.write_row(row, 0, (each, freq_map[each]))
        row += 1
    workbook.close()


if __name__ == '__main__':
    aksharas = read_aksharas('tamil_script_phonetic_data')
    aksharas.update({'ँ': Akshara('ँ', '901', '', 'anusvar', True)})
    aksharas.update({'ं': Akshara('ं', '902', '', 'anusvar', True)})

    # convert_docx_txt('corpus_string_final'
    # clean_non_hindi_words('corpus', 'corpus_string_final')

    # freq_analysis('corpus_string_final')

    text = Text('corpus_string_final_cleaned_chars')
    text.write_first_order()
    text.write_second_order()

    # print(hi_syllables('उसी'))
