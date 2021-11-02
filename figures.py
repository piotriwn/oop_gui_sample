import math

class Triangle:
    def __init__(self):
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
        except ValueError as e:
            print(f"{e}. Invalid value for a: {aIn}")

    @b.setter
    def b(self, bIn):
        try:
            bTemp = float (bIn)
            if bTemp <= 0:
                raise ValueError(f"{bTemp} is smaller or equal to 0")
            else:
                self._b = bTemp
        except ValueError as e:
            print(f"{e}. Invalid value for b: {bIn}")

    @c.setter
    def c(self, cIn):
        try:
            cTemp = float (cIn)
            if cTemp <= 0:
                raise ValueError(f"{cTemp} is smaller or equal to 0")
            else:
                self._c = cTemp
        except ValueError as e:
            print(f"{e}. Invalid value for c: {cIn}")

    @a.deleter
    def a(self):
        del self._a

    @b.deleter
    def b(self):
        del self._b

    @c.deleter
    def c(self):
        del self._c

    @property
    def circumference(self):
        return self.a + self.b + self.c

    @property
    def area(self):
        s = 0.5*self.circumference
        return math.sqrt( s* (s-self.a) * (s - self.b ) * (s - self.c)  )

    @property
    def rInscribed(self):
        return (2 * self.area) / (self.circumference)

    @property
    def RCircum(self):
        return   (self.a * self.b * self.c) / (4 * self.area) 

    def checkTriangleIneq(self):
        sortedSides = sorted([self.a, self.b, self.c])
        return sum(sortedSides[:2]) > sortedSides[-1]

class Square:
    def __init__(self):
        pass

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, aIn):
        try:
            aTemp = float (aIn)
            if aTemp <= 0:
                raise ValueError(f'{aTemp} is smaller or equal to 0')
            else:
                self._a = aTemp
        except ValueError as e:
            print(f"{e}. Invalid value for a: {aIn}")

    @a.deleter
    def a(self):
        del self._a

    @property
    def circumference(self):
        return 4* self.a

    @property
    def area(self):
        return self.a ** 2

    @property
    def rInscribed(self):
        return (0.5 * self.a)

    @property
    def RCircum(self):
        return 0.5 * math.sqrt(self.a)

class Hexagon:
    def __init__(self):
        pass

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, aIn):
        try:
            aTemp = float (aIn)
            if aTemp <= 0:
                raise ValueError(f'{aTemp} is smaller or equal to 0')
            else:
                self._a = aTemp
        except ValueError as e:
            print(f"{e}. Invalid value for a: {aIn}")

    @a.deleter
    def a(self):
        del self._a

    @property
    def circumference(self):
        return 6* self.a

    @property
    def area(self):
        return math.sqrt(3) * 3 * self.a **2 / 2

    @property
    def rInscribed(self):
        return math.sqrt(3) * self.a / 2

    @property
    def RCircum(self):
        return self.a