class Triangle:
    def __init__(self):
        self._a = None
        self._b = None
        self._c = None

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def c(self):
        return self._c

    @a.setter
    def a(self, aIn):
        try:
            aTemp = int (aIn)
            if aTemp <= 0:
                return False
            else:
                self._a = aTemp
                return True
        except ValueError:
            print(f"Invalid value for a: {aIn}")
            return False

    @b.setter
    def b(self, bIn):
        try:
            bTemp = int (bIn)
            if bTemp <= 0:
                return False
            else:
                self._b = bTemp
                return True
        except ValueError:
            print(f"Invalid value for b: {bIn}")
            return False

    @c.setter
    def c(self, cIn):
        try:
            cTemp = int (cIn)
            if cTemp <= 0:
                return False
            else:
                self._c = cTemp
                return True
        except ValueError:
            print(f"Invalid value for c: {cIn}")
            return False

    def checkTriangleIneq(self):
        sortedSides = sorted[self.a, self.b, self.c]
        return sum(sortedSides[:2]) > sortedSides[-1]