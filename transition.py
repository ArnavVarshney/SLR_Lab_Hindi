from monosyllable import *


class Text:
    text_string = ""
    cleaned_text_string = ""
    length = 0
    first_transition_map = {}
    second_transition_map = {}

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

    def insert_in_second_map(self, char):
        if char in self.second_transition_map:
            self.second_transition_map[char] += 1
        else:
            self.second_transition_map[char] = 1


def hi_syllables(word):
    signs = [u'\u0901', u'\u0902', u'\u0903', u'\u093c', u'\u093e', u'\u093f', u'\u0940',
             u'\u0941', u'\u0942', u'\u0943', u'\u0944', u'\u0946',
             u'\u0947', u'\u0948', u'\u094a', u'\u094b', u'\u094c',
             u'\u094d']
    syllables = []
    for char in word:
        if char in signs:
            syllables[-1] = syllables[-1] + char
        else:
            try:
                if '्' == syllables[-1][-1]:
                    syllables[-1] = syllables[-1] + char
                else:
                    syllables.append(char)
            except IndexError:
                syllables.append(char)
    # new_syllables = []
    # for j in syllables:
    #     try:
    #         if aksharas[j].type == 'C':
    #             new_syllables.append(j)
    #             new_syllables.append('अ')
    #         else:
    #             new_syllables.append(j)
    #     except KeyError:
    #         new_syllables.append(j)
    return syllables


def count_first_order():
    spl = text.cleaned_text_string.split(" ")
    for i in spl:
        syll = hi_syllables(i)
        if len(syll) == 1:
            text.insert_in_first_map(syll[0])
        else:
            for k in range(len(syll) - 1):
                curr = syll[k]
                next = syll[k + 1]
                text.insert_in_first_map(curr + '|' + next)


def count_second_order():
    spl = text.cleaned_text_string.split(" ")
    for i in spl:
        syll = hi_syllables(i)
        if len(syll) == 1:
            text.insert_in_second_map(syll[0])
        elif len(syll) == 2:
            text.insert_in_second_map(syll[1])
        for k in range(len(syll) - 2):
            curr = syll[k]
            next = syll[k + 1]
            next_2 = syll[k + 2]
            text.insert_in_second_map(curr + '|' + next_2)


if __name__ == '__main__':
    aksharas = read_aksharas('tamil_script_phonetic_data')
    aksharas.update({'ँ': Akshara('ँ', '901', '', 'anusvar', True)})
    aksharas.update({'ं': Akshara('ं', '902', '', 'anusvar', True)})
    text = Text('hi')
    val = dict(sorted(text.first_transition_map.items(), key=lambda x: x[1], reverse=True))
    print(val)
    # print(hi_syllables('उसी'))
