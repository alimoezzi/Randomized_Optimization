from functools import reduce
from random import sample, shuffle, randrange, choices

fs = lambda x: 1 / (1 + (36 - x) ** 2)
fm = lambda x: 1 / (1 + (360 - x) ** 2)


def GA(k, fs, fm):
    p = []
    for i in range(k):
        acards = list(range(1, 11))
        pile1 = sample(range(1, 11), 5)
        pile2 = [i for i in acards if i not in pile1]
        a, b = fs(sum(pile1)), fm(reduce(lambda x, y: x * y, pile2, 1))
        p.append((a, b, pile1, pile2))
    while round(p[0][0]) != 1 or round(p[0][1]) != 1:
        # crossover the worst
        t = randrange(start=1, stop=4)
        temp1 = p.pop()
        c1 = sample(temp1[2], t)
        c2 = sample(temp1[3], t)
        c1s = [i for i in temp1[2] if i not in c1]
        c2s = [i for i in temp1[3] if i not in c2]
        a1 = [*c1, *c2s]
        a2 = [*c2, *c1s]
        p.insert(0, (
            fs(sum(a1)),
            fm(reduce(lambda x, y: x * y, a2, 1)),
            a1,
            a2
        ))
        # mutate the best
        p.sort(key=lambda x: 1 / (1 + (2 - (x[0] + x[1])) ** 2), reverse=True)
    return p[0]

if __name__ == '__main__':
    import time
    a = time.time()
    s = GA(10, fs, fm)
    b = time.time()
    print(s,sum(s[2]), reduce(lambda x, y: x * y, s[3], 1), b-a)
