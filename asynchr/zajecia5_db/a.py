"""
Rozwiązujemy równanie y'' = - y     (**)

Zmienne
y
yp
(yp to y prim -- odpowiada pochodnej y)

Równania:
y' = yp
(yp)' = y'' = -y            (zgodnie z **)

Numeryczne rozwiązanie:
zaczynamy od t=0
przechodzimy o dt do przodu ... gdzie delta_t=0.001 (krok czasowy)

delta_y = delta_t * yp
delta_ypp = delta_t * (-y)

"""

y = 10
yp = 0

t = 0
delta_t = 0.001
dane = []
while t < 100:
    delta_y = delta_t * yp
    delta_yp = delta_t * (-y)
    print(f'y={y:.3f}, yp={yp:.3f}')
    dane.append(y)
    y += delta_y
    yp += delta_yp
    t += delta_t

import matplotlib.pyplot as plt
plt.plot(dane)
plt.ylabel('some numbers')
plt.show()