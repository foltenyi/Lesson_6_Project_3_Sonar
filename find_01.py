import math as m
import random as ran
import itertools as it

import inspect
def ln() -> str:
    fi = inspect.getframeinfo(inspect.currentframe().f_back)
    return f'{fi.lineno:3d}'
def fl() -> str:
    fi = inspect.getframeinfo(inspect.currentframe().f_back)
    return f'{fi.function} {fi.lineno:3d}'  # fi.filename if needed


def manipulatePoints():
    global points, circles
    while True:
        if not input('Add/delete/list points (y/n)? : ').lower().startswith('y'):
            break  # and update circles

        print("Any negative number in 'X' means: delete |n|th point; 'L' - list the points")
        a = input('X {-n|L|(0-59)} [ Y (0-14) D {X|(1-9)} ]: ')
        a = a.split()  # At spaces
        if len(a) == 0:
            print('Please enter valid value.')
            continue

        X = a[0]
        if X[0] == '-':  # Delete a point from p
            i = int(X[1:])
            del points[i-1]
            continue
        if X.lower().startswith('l'):
            if len(points) == 0:
                print("No points[]")
            else:
                for i in range(len(points)):
                    print(f"{i+1}. point = {points[i]}")
            print()
            if len(farPoints) == 0:
                print("No farPoints, with distance X")
            else:
                for p in farPoints:
                    print(f"farPoint {p}")
            print()
            print(f'{len(poss) = }, the number of possible places')
            print()
            continue

        if len(a) < 3:
            print('Please enter valid values for x, y, and distance.')
            continue
        Y = a[1]
        D = a[2]

        if D.lower().startswith('x'):  # Add the point to farPoints and delete all the points
            # from poss, which are closer than 10 (<=9)
            if not X.isdecimal():
                print(f"'{X=}' is not decimal"); continue
            if not Y.isdecimal():
                print(f"'{Y=}' is not decimal"); continue
            X = int(X); Y = int(Y)
            farPoints.add((X, Y))
            lposs = len(poss)
            # And now delete the points from its neighbourhood in poss
            possCopy = poss.copy()
            for x, y in possCopy:
                # if round(m.sqrt((X-x)**2 + (Y-y)**2)) <= 9:
                if (X-x)**2 + (Y-y)**2 < 94:
                    poss.remove((x, y))
            print(f'{lposs - len(poss)} points deleted from the possible points set')
            continue

        # Add the point to points, if all are decimals, >= 0
        if not X.isdecimal():
            print(f"'{X=}' is not decimal"); continue
        if not Y.isdecimal():
            print(f"'{Y=}' is not decimal"); continue
        if not D.isdecimal():
            print(f"'{D=}' is not decimal"); continue

        points.append((int(X), int(Y), int(D)))

    # Populate circles, for each point build a set of (x,y) tuples
    circles = []
    for X, Y, D in points:
        s = set()
        # print(f'{X=} {Y=} {D=}')
        for x in range(max(0, X - D), min(60, X + D + 1)):
            for y in range(max(0, Y - D), min(15, Y + D + 1)):
                if round(m.sqrt((X - x) ** 2 + (Y - y) ** 2)) == D:
                    s.add((x, y))

        # This point is done, add the circle points
        circles.append(s.copy())


def getGuess():
    # Get the point from poss, which has the most points from poss closer or equal 9
    # which means ((X-x)**2 + (Y-y)**2) < 94, no need for sqrt. There is no number
    # between [90, 97] in the form i*i + j*j
    # From the farthest points pick one randomly.
    N = 0
    for X, Y in poss:
        n = 0
        for x, y in poss:  # Simpler than get a square around (X,Y)
            if (X-x)**2 + (Y-y)**2 < 94:
                n += 1
        if N < n:  # The order in set poss gives some randomness
            xy = []
        if N <= n:
            N = n; xy.append((X, Y))

    print(f'Try: {ran.choice(xy)}')


def getSuggestions():
    # breakpoint()
    global points, circles
    if len(points) != len(circles):
        breakpoint()
    if len(points) > 0:
        # Create an index list, from which the combinations will be picked up
        np = []
        for i in range(len(points)):
            np.append(i)

        # If we have more than one point, don't give individual circles
        somethingPrinted = False
        for r in range(1 if len(np) > 1 else 0, len(np)):
            lc = list(it.combinations(np, r + 1))  # List of tuples r+1 size
            for cs in lc:
                # print(f'{fl()} {cs=}')  # ???? Debug
                s = circles[cs[0]]
                # print(f'{fl()} {s=}')  # ???? Debug
                x, y, d = points[cs[0]]
                print(f'{cs[0] + 1:2d}. Point ({x}, {y}), {d=}')
                # print(f'{fl()} {s=}')  # ???? Debug
                for c in cs[1:]:
                    x, y, d = points[c]
                    print(f'{c + 1:2d}. Point ({x}, {y}), {d=}')
                    s = s & circles[c]
                    # print(f'{fl()} {s=}')  # ???? Debug

                # Take out the points, if any, not in poss set
                s = s & poss
                # If any point in s is closer to any given point, delete it
                sCopy = s.copy()
                # print(f'{fl()} {s=}')  # ???? Debug
                for x1, y1 in sCopy:
                    for x2, y2, d in points:
                        if round(m.sqrt((x1-x2)**2 + (y1-y2)**2)) < d:
                            # print(f'{fl()} {sCopy=}  {s=}  ({x1},{y1})')  # ???? Debug
                            s.remove((x1, y1))
                            break  # Get the next point to check
                # Probably doesn't help, wrote it as an exercise
                # For each remaining points in s associate with the number in poss,
                # which are close enough.
                res = []
                for x1, y1 in s:
                    n = 0
                    for x2, y2 in poss:
                        if (x1 - x2)**2 + (y1 - y2)**2 < 94:
                            n += 1
                    res.append((n, (x1, y1)))
                res.sort(reverse=True)
                print(res)
                if len(res) > 0:
                    somethingPrinted = True

    else:
        somethingPrinted = True
        getGuess()

    if not somethingPrinted:
        getGuess()


while True:
    # breakpoint()  # ???? DEBUG, to set other breakpoints
    # points and circles are indexed together
    points = []  # List of points (X,Y,D) 1<=D<=9
    circles = []  # Each element is a set of points (x,y), which are D distance from a points[]

    farPoints = set()  # Points where no chest is close by
    poss = set()  # All possible points, minus the points, which are <= 9 distance from farPoints

    for y in range(15):
        for x in range(60):
            poss.add((x, y))

    while True:
        manipulatePoints()

        getSuggestions()

        if input('Continue this game? (y/n): ').lower().startswith('y'):
            continue
        else:
            break

    if input('Do you want another game? (y/n): ').lower().startswith('y'):
        continue
    else:
        print('\nThanks for using this program, any suggestion is welcomed.')
        break
