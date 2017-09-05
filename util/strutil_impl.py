import itertools


# ----------------------------------------------------------------------------------------------------------------------
# посимвольная свертка двух строк
def str_convolution_by_chars(s1, s2):

    def char_cmp(c1, c2):
        return 1 if c1 == c2 else 0

    for x in map(char_cmp, s1, s2):
        yield x


# ----------------------------------------------------------------------------------------------------------------------
# посимвольная свертка двух строк
def str_convolution_by_chars_shifted(s1, s2, shift, only_middle=True):
    sh1 =  shift if shift > 0 else 0
    sh2 = -shift if shift < 0 else 0

    if not only_middle:
        for x in range(0, sh1): yield 0
        for x in range(0, sh2): yield 0

    yield from str_convolution_by_chars(s1[sh1:], s2[sh2:])

    if not only_middle:
        cnt = abs(len(s1) - len(s2) - shift)
        for x in range(0, cnt): yield 0


# ----------------------------------------------------------------------------------------------------------------------
# Свертка двух строк
# shift -- сдвиг второй строки относительно первой
def str_convolution(s1, s2, shift=0):
    return sum(str_convolution_by_chars_shifted(s1, s2, shift))


# ----------------------------------------------------------------------------------------------------------------------
# набор всевозможных сверток двух строк
# результат: генератор кортежей (shift, convval)
def str_convolutions(s1, s2):
    sh1 = -len(s2) + 1  # начальный сдвиг второй строки
    sh2 =  len(s1)      # конечный сдвиг второй строки

    for sh in range(sh1, sh2):
        yield (sh, str_convolution(s1, s2, sh))


# ----------------------------------------------------------------------------------------------------------------------
# максимальное значение свертки и соответствующее смещение в виде кортежа (shift, convolution)
def str_convolution_max(s1, s2):
    return max(str_convolutions(s1, s2), key=lambda x: x[1])


# ----------------------------------------------------------------------------------------------------------------------
# Выделить общую начальную часть двух слов.
# Например:
#   str_extract_same_beg('abcdopq', 'abcdxy') --> ('abcd', 'opq', 'xy')
# Возвращается кортеж из трех строк (общая часть и отличающиеся части из первого и второго) слова
def str_extract_same_beg(s1, s2):
    pos = 0
    for t in str_convolution_by_chars(s1, s2):
        if t == 0: break
        pos += 1
    return s1[:pos], s1[pos:], s2[pos:]

# ----------------------------------------------------------------------------------------------------------------------
def str_split_by_equal1(s1, s2):
    len1, len2 = len(s1), len(s2)
    if len2 > len1:
        (ss1, ss2) = str_split_by_equal1(s2, s1)
        return ss2, ss1

    # список кортежей, содержащих пары символов из первой и второй строки
    charPairs = map(lambda c1, c2: (c1, c2), s1, s2)
    # группируем пары символов по принципу их одинаковости или различности
    ss = [list(o) for k, o in itertools.groupby(charPairs, lambda o: o[0] == o[1])]

    # выделяем и собираем строки (подстроки исходных строк)
    ss1 = [''.join([c[0] for c in seq]) for seq in ss]
    ss2 = [''.join([c[1] for c in seq]) for seq in ss]

    if len1 != len2:
        ss1.append(s1[len2 - len1:]), ss2.append('')
        #s1_tail = s1[len2-len1:]
        #if ss1[-1] != ss2[-1]:
        #    ss1[-1] = ss1[-1] + s1[len2-len1:]
        #else:
        #    ss1.append(s1[len2-len1:]), ss2.append('')

    return ss1, ss2


# ----------------------------------------------------------------------------------------------------------------------
def str_split_by_equal2(s1, s2, shift):
    s1_front = False
    s2_front = False
    if shift > 0:
        s1_front = s1[: shift]
        s1 = s1[ shift:]
    if shift < 0:
        s2_front = s2[:-shift]
        s2 = s2[-shift:]

    (ss1, ss2) = str_split_by_equal1(s1, s2)

    if s1_front: ss1.insert(0, s1_front), ss2.insert(0, '')
    if s2_front: ss2.insert(0, s2_front), ss1.insert(0, '')

    return ss1, ss2


# ----------------------------------------------------------------------------------------------------------------------
# находим в строках общие части и выделяем их разбивая таким образом строки на несколько кусков
def str_split_by_equal(s1, s2, shift=0):
    return str_split_by_equal1(s1, s2) if shift == 0 else str_split_by_equal2(s1, s2, shift)


# ----------------------------------------------------------------------------------------------------------------------
# конструируем N-граммы из слова
def str_build_n_gramms_fix_len(str, ngramm_len):
    str_len = len(str)
    return [str[i : i + ngramm_len] for i in range(str_len - ngramm_len + 1)]


# ----------------------------------------------------------------------------------------------------------------------
# конструируем все N-граммы из слова с длинами от len/2..len
def str_build_n_gramms(str):
    def gen(str):
        str_len = len(str)
        for ngramm_len in range(str_len // 2 if str_len > 1 else 1, str_len + 1):
            yield from str_build_n_gramms_fix_len(str, ngramm_len)

    return [ngramm for ngramm in gen(str)]


# ----------------------------------------------------------------------------------------------------------------------
# сохранить строки в словарь с подсчетом количества их использования
def str_store_to_dict(str_dict, str):
    #cnt = str_dict.get(str, 0)
    str_dict[str] = str_dict.get(str, 0) + 1


# ----------------------------------------------------------------------------------------------------------------------
# Расстояние-по-максимальной-общей-части.
# Фактически это количество символов, отличающихся в строках.
# Предполагаем, что строки одной длины. Если это не так,
# то считаем, что короткая срока дополнена отличающимися символами.
def str_dist_by_max_same_parts(s1, s2):
    pass


# ----------------------------------------------------------------------------------------------------------------------
# Представить строку (если это возможно) в виде последовательности более коротких строк
# из набора components
# Если возможно несколько вариантов разбиения -- возвращаем все возможные
def str_decompose(s, components):
    c = {}
    # c.
    lst = []
    str_len = len(s)
    for i in range(1, str_len):
        beg = s[:i]
        end = s[i:]
        if components.get(beg, '') != '':
            lst.append()


