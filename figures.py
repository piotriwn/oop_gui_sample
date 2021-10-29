class Triangle:
    def __init__(self):
        # self._a = None
        # self._b = None
        # self._c = None
        pass

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
            aTemp = float (aIn)
            if aTemp <= 0:
                raise ValueError(f'{aTemp} is smaller or equal to 0')
            else:
                self._a = aTemp
                return True
        except ValueError as e:
            print(f"{e}. Invalid value for a: {aIn}")
            return False

    @b.setter
    def b(self, bIn):
        try:
            bTemp = float (bIn)
            if bTemp <= 0:
                raise ValueError(f"{bTemp} is smaller or equal to 0")
            else:
                self._b = bTemp
                return True
        except ValueError as e:
            print(f"{e}. Invalid value for b: {bIn}")
            return False

    @c.setter
    def c(self, cIn):
        try:
            cTemp = float (cIn)
            if cTemp <= 0:
                raise ValueError(f"{cTemp} is smaller or equal to 0")
            else:
                self._c = cTemp
                return True
        except ValueError as e:
            print(f"{e}. Invalid value for c: {cIn}")
            return False

    def checkTriangleIneq(self):
        sortedSides = sorted([self.a, self.b, self.c])
        return sum(sortedSides[:2]) > sortedSides[-1]