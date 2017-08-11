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
# Подсчет количества одинаковых элементов в списке
# \result   dict(el1:cnt1, el2:cnt2, ...)
def count_same_elements(all):
    lst = list(all)
    els = set(lst)
    for o in els:
        yield o, lst.count(o)



