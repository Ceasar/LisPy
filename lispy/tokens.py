

class OpenParens(object):
    pass


class CloseParens(object):
    pass


# Atoms

class Symbol(object):
    def __init__(self, value):
        self.value = value


class Number(object):
    def __init__(self, value):
        self.value = value
