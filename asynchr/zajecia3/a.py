from dataclasses import dataclass


@dataclass
class A:
    x: int
    y: int


def strip(d: dict):
    return {k: d[k] for k in ['x', 'y']}


d = {'x': 5, 'y': 10, 'z': 12}
a = A(**strip(d))
print(a)
