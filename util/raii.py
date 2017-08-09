# Класс для поддержки идиомы RAII
class Raii:
    def __init__(self, exit_proc):
        self.exit_proc = exit_proc

    def __enter__(self): pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.exit_proc()
