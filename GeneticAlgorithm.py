from functools import reduce
from random import sample, shuffle, randrange, choices
import altair as alt
import numpy as np
import pandas as pd
from altair import Chart

fs = lambda x: 1 / (1 + (36 - x) ** 2)
fm = lambda x: 1 / (1 + (360 - x) ** 2)


def GA(k, fs, fm, mark=False):
    market = {'x': [], 'y': []}
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
        if mark:
            market['x'].append(p[0][0] + p[0][1])
            market['y'].append(1 / (1 + (2 - (p[0][0] + p[0][1])) ** 2))
    return p[0], market


if __name__ == '__main__':
    import time

    alt.renderers.enable('altair_viewer')
    x = np.linspace(-3, 6)
    source = pd.DataFrame({
        'x': x,
        'f(x)': 1 / (1 + (2 - (x)) ** 2)
    })
    chart: Chart = alt.Chart(source).mark_line().encode(
        x='x',
        y='f(x)'
    ).interactive()
    a = time.time()
    s, m = GA(10, fs, fm, mark=True)
    b = time.time()
    chart2 = alt.Chart(pd.DataFrame(m)).mark_point(filled=True, size=50).encode(
        x='x',
        y='y',
        color=alt.value('red')
    )
    print(s, sum(s[2]), reduce(lambda x, y: x * y, s[3], 1), b - a)
    (chart + chart2).show()
