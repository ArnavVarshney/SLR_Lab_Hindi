import string

import docx2txt
import xlsxwriter


class Word:
    original_word = ''
    word = ''

    def __init__(self, word: str):
        self.original_word = word
        self.word = word
        self.clean()

    def clean(self):
        cleaned_word = ''.join([c.lower() for c in self.word if c in list(string.ascii_lowercase)])
        self.word = cleaned_word


class Text:
    text_string = ""
    cleaned_text_string = ""
    length = 0

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
        cleaned = ''.join([c.lower() for c in self.word if c in list(string.ascii_lowercase)])
        self.cleaned_text_string = cleaned


def convert_docx_txt(path: str):
    text = docx2txt.process(path + '.docx')
    with open(path + '.txt', 'w', encoding='utf8') as f:
        f.write(text)


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
    workbook = xlsxwriter.Workbook('mapped/eng_freq_analysis.xlsx')
    wk = workbook.add_worksheet('freq_analysis')
    wk.write_row(0, 0, ('Word', 'Frequency'))
    row = 1
    for each in freq_map:
        wk.write_row(row, 0, (each, freq_map[each]))
        row += 1
    workbook.close()


if __name__ == '__main__':
    convert_docx_txt('engcorpus')

    freq_analysis('engcorpus')
    # print(hi_syllables('उसी'))
