from copy import copy
from dataclasses import dataclass

d = dict()
d['kadabra'] = 12
d['chairman'] = 1

print(d)
print(d['chairman'])

for k,v in d.items():
    print(k,v)

s = set()
s.add(3)
s.add(10)
s.add(14)
print(s)
print(s.__contains__(10))
print(s.__contains__(11))

@dataclass
class Car:
    vin: str
    price: int
    model: str

c = Car('abc', 12, 'gg111')
dd = c.__dict__
print(dd)
gg = copy(dd)
c2 = Car(**gg)
print(c2)