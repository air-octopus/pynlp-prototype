# Утилиты для списков


# ----------------------------------------------------------------------------------------------------------------------
# Класс для автоматического подсчета количества объектов
class ObjectCounter:
    def __init__(self):
        self.objs = dict()

    def add(self, obj):
        self.objs[obj] = self.objs.get(obj, 0) + 1

    def get(self):
        return self.objs


# ----------------------------------------------------------------------------------------------------------------------
# Класс для автоматического подсчета количества объектов,
# при этом объектам приписывается некоторый тег
class ObjectCounterTagged:
    def __init__(self, default_tag_gen):
        self.objs = dict()
        self.default_tag_gen = default_tag_gen

    def _obj_val_internal(self, obj):
        return self.objs.get(obj, [0, self.default_tag_gen()])

    def clear(self):
        self.objs.clear()

    def add(self, obj):
        o_val = self._obj_val_internal(obj)
        o_val[0] += 1
        self.objs[obj] = o_val
        return o_val[1]

    def get(self):
        return self.objs

    def get_count(self, obj):
        o_val = self._obj_val_internal(obj)
        return o_val[0]

    def get_tag(self, obj):
        o_val = self._obj_val_internal(obj)
        return o_val[1]

    def elements(self):
        for k, o in self.objs.items():
            yield (k, o[0], o[1])

# ----------------------------------------------------------------------------------------------------------------------
# Подсчет количества одинаковых элементов в списке
# \result   dict(el1:cnt1, el2:cnt2, ...)
def count_same_elements(all):
    lst = list(all)
    els = set(lst)
    for o in els:
        yield o, lst.count(o)



