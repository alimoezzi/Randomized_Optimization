import math
from random import uniform

f = lambda x: ((math.sin(10 * math.pi * x) / 2 * x) + (x - 1) ** 4) if 0.5 < x < 2.5 else 0


def near(n):
    return [n + 0.1, n - 0.1]


def Hill_Climbing(f, fn, g: float) -> (float, float):
    current = g
    while True:
        near = fn(current)
        a = list(map(f, near))
        if max(map(f, fn(current))) > f(current):
            if a[0] > a[1]:
                current = near[0]
            else:
                current = near[1]
        else:
            return (current, f(current))


def randomized_hill_climbing(n, minMax):
    m = (0, 0)
    for i in range(n):
        a = uniform(minMax[0], minMax[1])
        res = Hill_Climbing(f, near, a)
        if m[1] < res[1]:
            m = res
    return m


def annealing(fx, fxt, t):
    if fxt >= fx:
        return 1
    else:
        print(fx, fxt, t, math.e ** ((fxt - fx) / t))
        return round(math.e ** ((fxt - fx) / t))


def simulated_annealing(f, fn, g: float, t):
    temp = t
    current = g
    while round(temp) > 0:
        near = fn(current)
        a = list(map(f, near))
        for i in range(2):
            p = annealing(f(current), a[i], temp)
            if p == 1:
                current = near[i]
                break
            temp -= 0.1
    return current


if __name__ == '__main__':
    v = Hill_Climbing(f, near, 2)
    vr = randomized_hill_climbing(10, (0.5, 2.5))
    vsa = simulated_annealing(f, near, 0, 3)
    print(vsa)
