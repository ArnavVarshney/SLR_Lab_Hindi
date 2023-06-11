def syllabify_kn(text):
    signs = [
        u'\u0c82', u'\u0c83', u'\u0cbd', u'\u0cbe', u'\u0cbf', u'\u0cc0', u'\u0cc1',
        u'\u0cc2', u'\u0cc3', u'\u0cc4', u'\u0cc6', u'\u0cc7', u'\u0cc8',
        u'\u0cca', u'\u0ccb', u'\u0ccc', u'\u0ccd']
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
                print(text)
        else:
            try:
                if lst_chars[-1][-1] == halant:
                    lst_chars[-1] = lst_chars[-1] + char
                else:
                    lst_chars.append(char)
            except IndexError:
                lst_chars.append(char)

    return lst_chars

# print(syllabify_kn("ಅಷ್ಟೊಂದು"))
