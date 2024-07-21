from math import sqrt as sqrt


def translate_points(points, i, j):

    for x in range(0,len(points), 2):
        points[x] += i

    for y in range(1,len(points), 2):
        points[y] += j

def scale_points(points, i, j):

    for x in range(0,len(points), 2):  # scale x coords by factor i
        points[x] *= i

    for y in range(1,len(points), 2):  # scale y coords by factor j
        points[y] *= j

    print(points)


def area_trapizium(w1, w2, h):
    "w1, w2 are half width of a, b respectively where a & b are top and bottom of trapizium"

    area = ((2*w1)+w2)*h
    return area


def quadratic_formula(a, b, c):

    x = (-b + sqrt((b**2) - (4*a*c))) / (2*a)

    return x


def binary_searchii(value, slist):
    # 1: Check if value within slist range
    if value < slist[0]:
        return 0
    elif value > slist[-1]:
        return len(slist) - 1

    n_prev = len(slist)
    n = len(slist) // 2
    d = n_prev-n

    while (abs(n-n_prev) > 1) or not (slist[n_prev-1] <= value <= slist[n-1]):

        n_prev = n
        if slist[n-1] - value > 0:
            n = n - abs(d) // 2
            d = n_prev - n
        elif slist[n-1] - value < 0:
            n = n + abs(d) // 2
            d = n_prev - n
        if d <= 1:
            d = 2

    # print(" %s: is between %s and %s" %(value, slist[n_prev-1], slist[n-1]))
    return n_prev-1



