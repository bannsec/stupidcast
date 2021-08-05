
class Config:
    def __init__(self):
        self._dict = {}
        self.cast = None

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

def __init__():
    global config, __done_init
    config = Config()

    __done_init = True

try:
    __done_init
except:
    __init__()
