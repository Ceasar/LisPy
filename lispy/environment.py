"""
"""


class Environment(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        if var in self:
            return self
        elif self.outer:
            return self.outer.find(var)
        else:
            raise NameError("Name '%s' is not defined" % var)
