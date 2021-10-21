def foo(a, b):
    print(f'z funkcji {a + b}')


def 최대찾기(w):
    mx = -1000
    for i in w:
        print(f'sprawdzam {i}')
        mx = max(mx, i)
    return mx


def give_me_2():
    return 2, 'kadabra'


# foo(1, 2)
# foo(0, 5)
# foo(2, 2)

# m = 최대찾기([2, 9, 1, 2])
# print(m)

x, y = give_me_2()
print(x)
print(y)
