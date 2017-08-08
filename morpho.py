# функция определяет предполагаемые основы слов (общие части) и (прото)аффиксы -- то,
# что осталось после удаления предполагаемых основ
def extract_proto_morphemes(s1, s2):
    from strutil import str_convolution_max, str_split_by_equal

    sh, conv = str_convolution_max(s1, s2)
    components = str_split_by_equal(s1, s2, sh)

    assert len(components[0]) == len(components[1]), "Unexpected str_split_by_equal(...) result"
    if len(components[0]) <= 0:
        return ('', [])

    global i
    i = 0

    def map_func(ss1, ss2):
        global i
        v = (len(ss1), i) if ss1 == ss2 else (0, 0)
        i += 1
        return v

    proto_root_pos = max(map(map_func, components[0], components[1]), key=lambda x: x[0])

    proto_affixes = \
        [
              ''.join(components[0][:proto_root_pos[1]])
            , ''.join(components[0][proto_root_pos[1] + 1:])
            , ''.join(components[1][:proto_root_pos[1]])
            , ''.join(components[1][proto_root_pos[1] + 1:])
        ]
    proto_affixes = [o for o in proto_affixes if o != '']

    return \
        (
            # предполагаемый корень
            components[0][proto_root_pos[1]],
            # прото-аффиксы
            proto_affixes
        )

