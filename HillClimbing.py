import math
from random import uniform
import altair as alt
import numpy as np
import pandas as pd
from altair import Chart

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


def randomized_hill_climbing(n, minMax, mark=False):
    market = {'x': [], 'y': []}
    m = (0, 0)
    for i in range(n):
        if mark:
            market['x'].append(m[0])
            market['y'].append(f(m[1]))
        a = uniform(minMax[0], minMax[1])
        res = Hill_Climbing(f, near, a)
        if m[1] < res[1]:
            m = res
    return m, market


def annealing(fx, fxt, t):
    if fxt >= fx:
        return 1
    else:
        print(fx, fxt, t, math.e ** ((fxt - fx) / t))
        return round(math.e ** ((fxt - fx) / t))


def simulated_annealing(f, fn, g: float, t, mark=False):
    market = {'x': [], 'y': []}
    temp = t
    current = g
    while round(temp) > 0:
        near = fn(current)
        a = list(map(f, near))
        if mark:
            market['x'].append(current)
            market['y'].append(f(current))
        for i in range(2):
            p = annealing(f(current), a[i], temp)
            if p == 1:
                current = near[i]
                break
            temp -= 0.1
    return current, market


if __name__ == '__main__':
    alt.renderers.enable('altair_viewer')
    x = np.linspace(0.5, 2.5)
    source = pd.DataFrame({
        'x': x,
        'f(x)': ((np.sin(10. * np.pi * x) / 2. * x) + ((x - 1.) ** 4.))
    })
    chart: Chart = alt.Chart(source).mark_line().encode(
        x='x',
        y='f(x)'
    ).interactive()

    v = Hill_Climbing(f, near, 2)
    vr, m1 = randomized_hill_climbing(10, (0.5, 2.5), mark=True)
    vsa, m = simulated_annealing(f, near, 0, 3, mark=True)
    print(vsa, m)
    chart2 = alt.Chart(pd.DataFrame(m)).mark_point(filled=True, size=50).encode(
        x='x',
        y='y',
        color=alt.value('red')
    )
    (chart + chart2).show()
