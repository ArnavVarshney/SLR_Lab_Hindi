import csv
import glob
import os


class Akshara:
    char = ''
    unicode = ''
    special = False
    type = ''
    remark = ''

    def __init__(self, char: str, unicode: str, type: str, remark: str = '', special: bool = False):
        self.char = char
        self.unicode = unicode
        self.type = type
        self.remark = remark
        self.special = special

    def __str__(self) -> str:
        return self.char


class Word:
    original_word = ''
    tokenized = []
    word = ''
    struct = ''
    length = 0

    def __init__(self, word: str):
        self.original_word = word
        self.word = word
        self.clean()
        self.tokenized = self.tokenize()
        self.length = len(self.tokenized)

    def __str__(self) -> str:
        return f'{self.original_word[:-1]:<10} {self.tokenized.__str__():<30} ' \
               f'{self.word:<9} {self.length:<8} {self.struct:<11}'

    def clean(self):
        global aksharas
        cleaned_word = ''.join([c for c in self.word if c in aksharas.keys()])
        self.word = cleaned_word

    def tokenize(self) -> list:
        return [i for i in self.word]

    def structify(self, debug: bool = False):
        global aksharas
        temp_word = self.word + ' '
        for i in range(self.length):
            curr_char = aksharas[temp_word[i]]
            next_char = aksharas[temp_word[i + 1]]
            self.struct += curr_char.type
            print(curr_char.char + ' ' if debug else '', end='')
            print(curr_char.type + ' ' if debug else '', end='')

            if curr_char.remark != 'halanta':
                if curr_char.type != 'V':
                    if next_char.type != 'V':
                        if next_char.remark != 'halanta':
                            if next_char.remark != 'nukta':
                                if next_char.remark != 'space':
                                    print('V ' if debug else '', end='')
                                    self.struct += 'V'

                    if self.length == 1:
                        print('V ' if debug else '', end='')
                        self.struct += 'V'

            # if next_char == '़':
            #     print('V', end=' ')
            #     struct += 'V'

        print('\n' + self.struct + '\n' if debug else '', end='')


class Corpus:
    path = ''
    words = []
    total_words = 0
    duplicates = []

    def __init__(self, path: str):
        self.path = path

    def convert_csv_to_txt(self):
        corpus = set({})
        with open(self.path + '.csv', 'r', encoding='utf8') as ph_file:
            read = csv.reader(ph_file)
            for row in read:
                for i in row:
                    if i in corpus:
                        self.duplicates.append(i)
                    corpus.add(i)
            ph_file.close()

        mono_syl_sorted = sorted(corpus)
        with open(self.path + '.txt', 'w', encoding='utf8') as file:
            for i in mono_syl_sorted:
                file.write(i + '\n')
            file.close()

    def read_corpus(self):
        file = open(self.path + '.txt', 'r', encoding='utf8')
        for each in file:
            word = Word(each)
            self.words.append(word)
        file.close()

    def generate_struct(self):
        for each in self.words:
            each.structify()

    def write_struct_files(self, debug: bool = False):
        if len(self.words) == 0:
            return
        for each in self.words:
            file = open('mapped/' + each.struct + '.txt', 'a', encoding='utf8')
            file.write(each.original_word)
            file.close()
        if debug:
            with open('debug_mapped/output.csv', 'w', newline='', encoding='utf8') as file:
                writer = csv.writer(file)
                writer.writerow(['Original', 'Tokenized', 'Cleaned', 'Length', 'Structure'])
                for each in self.words:
                    writer.writerow([each.original_word[:-1], each.tokenized, each.word, each.length, each.struct])
            file.close()

    def struct_stats(self):
        if len(self.words) == 0:
            return
        files = sorted(glob.glob('mapped/*'))
        total_elems = 0
        index = 1
        file = open('mapped/stats.txt', 'w')
        for each in files:
            with open(each, 'r', encoding='utf8') as fp:
                for count, _ in enumerate(fp):
                    pass
            count += 1
            total_elems += count
            print(f"{str(index) + '.':<4}{each[7:-4]:<8}{count:<4}")
            print(f"{str(index) + '.':<4}{each[7:-4]:<8}{count:<4}", file=file)
            index += 1
        print(f"{'Total':<12}{total_elems:<4}")
        print(f"{'Total':<12}{total_elems:<4}", file=file)
        file.close()


"""Reads Consonant/Vowel type assignment from the CSV database"""


def read_aksharas(path: str):
    global aksharas
    with open(path + '.csv', 'r', encoding='utf8') as ph_file:
        read = csv.reader(ph_file)
        for row in read:
            akshara = None
            if row[6] == '1' and row[10] == '0':
                akshara = Akshara(row[2], row[0], 'V')
            elif row[7] == '1' and row[10] == '0':
                akshara = Akshara(row[2], row[0], 'C')
            elif row[8] == '1':
                akshara = Akshara(row[2], row[0], '', 'nukta', True)
            elif row[9] == '1':
                akshara = Akshara(row[2], row[0], '', 'halanta', True)
            # elif row[10] == '1':
            #     akshara = Akshara(row[2], row[0], '', 'anusvar', True)
            if akshara:
                aksharas.update({akshara.char: akshara})
        ph_file.close()


def clean_mapped():
    files = glob.glob('mapped/*')
    for f in files:
        os.remove(f)
    files = glob.glob('debug_mapped/*')
    for f in files:
        os.remove(f)


"""Prints out the structure-wise distribution of the corpus"""

if __name__ == "__main__":
    aksharas = {' ': Akshara(' ', '0020', '', 'space', True)}
    read_aksharas('tamil_script_phonetic_data')

    clean_mapped()

    corpus = Corpus('monosyl_complete')
    corpus.convert_csv_to_txt()
    corpus.read_corpus()
    corpus.generate_struct()
    corpus.write_struct_files(debug=True)
    corpus.struct_stats()

    w = Word('भाैंह')
    w.structify(debug=True)
    print(w)
