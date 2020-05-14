import math

f = lambda x: ((math.sin(10 * math.pi * x) / 2 * x) + (x - 1) ** 4) if 0.5 < x < 2.5 else 0


def near(n):
    return [n + 0.1, n - 0.1]


def Hill_Climbing(f, fn, g: float) -> float:
    current = g
    while True:
        near = fn(current)
        a = list(map(f, near))
        if max(map(f, fn(current))) > f(current):
            if a[0] > a[1]:
                current = near[0]
            else:
                current = near[0]
        else:
            return current


if __name__ == '__main__':
    v = Hill_Climbing(f, near, 2)
    print(v)
