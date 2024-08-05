import os

from selenium import webdriver


def syllabify_kn(text):
    signs = [u'\u0c82', u'\u0c83', u'\u0cbd', u'\u0cbe', u'\u0cbf', u'\u0cc0', u'\u0cc1', u'\u0cc2', u'\u0cc3',
             u'\u0cc4', u'\u0cc6', u'\u0cc7', u'\u0cc8', u'\u0cca', u'\u0ccb', u'\u0ccc', u'\u0ccd']
    limiters = ['.', '\"', '\'', '`', '!', ';', ',', '?']

    halant = u'\u0ccd'
    lst_chars = []
    for char in text:
        if char in limiters:
            lst_chars.append(char)
        elif char in signs:
            try:
                lst_chars[-1] = lst_chars[-1] + char
            except IndexError:
                pass
                # print(text)
        else:
            try:
                if lst_chars[-1][-1] == halant:
                    lst_chars[-1] = lst_chars[-1] + char
                else:
                    lst_chars.append(char)
            except IndexError:
                lst_chars.append(char)

    return lst_chars


import unicodedata


def clean_non_kannada_chars(file):
    cleaned_words = []
    with open(file, 'r') as f:
        lines = f.readlines()
        removed_chars = {}
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            else:
                new_line = []
                for char in line:
                    if 'KANNADA' in unicodedata.name(char):
                        new_line.append(char)
                    else:
                        if char in removed_chars:
                            removed_chars[char] += 1
                        else:
                            removed_chars[char] = 1
                new_line = ''.join(new_line)
                cleaned_words.append(new_line)

    with open('kn_words_separated_cleaned.txt', 'w') as f:
        for word in cleaned_words:
            f.write(word + '\n')

    return removed_chars


def get_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable_gpu")
    return chrome_options


def clean_non_dict_words(file):
    non_words = []
    words = []

    if os.path.exists('kn_non_dict_words.txt'):
        with open('kn_non_dict_words.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                non_words.append(line.strip())

    if os.path.exists('kn_dict_words.txt'):
        with open('kn_dict_words.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                words.append(line.strip())

    url = "https://alar.ink/dictionary/kannada/english/"
    driver = webdriver.Chrome(options=get_chrome_options())
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                line = lines[i]
                line = line.strip()
                if len(line) == 0:
                    continue
                elif line not in non_words and line not in words:
                    driver.get(url + line)
                    try:
                        if "No results found" in driver.page_source:
                            non_words.append(line)
                        else:
                            words.append(line)
                    except:
                        print(f"Error: {line}")
                print(f"Processed: {i} / {len(lines)} ({i * 100 / len(lines):.4}%), "
                      f"Non-words: {len(non_words)} ({len(non_words) * 100 / len(lines):.4}%)", end='\r')

        with open('kn_non_dict_words.txt', 'w') as f:
            for word in non_words:
                f.write(word + '\n')

        with open('kn_dict_words.txt', 'w') as f:
            for word in words:
                f.write(word + '\n')
    except:
        with open('kn_non_dict_words.txt', 'w') as f:
            for word in non_words:
                f.write(word + '\n')

        with open('kn_dict_words.txt', 'w') as f:
            for word in words:
                f.write(word + '\n')


if __name__ == '__main__':
    # print(clean_corpus('kn_words_separated.txt'))
    # clean_non_dict_words('kn_words_separated_cleaned.txt')
    print(syllabify_kn("ರೊಟ್ಟಿತಿಂಡಿಪಾನೀಯಢೋಕ್ಲಾಮಜ್ಜಿಗೆಹುರಿದಕಾಳುಪಾಪ್"))
