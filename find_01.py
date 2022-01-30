###############################################################################
# Longest line is <= 99 characters
#
# find_01.py
#
# Helper program to
# CS-043-T001 Part 2 - Unit 6 - Final Collaborative Project: 3-3
# to find faster the hidden treasure chests.
#
# Updated to Python 3.10.
#
# The sonar game itself was copied fom: Sweigart, Al.
# https://inventwithpython.com/invent4thed/chapter13.html
# Sonar Treasure Hunt
#
###############################################################################

import math as m
import random as ran
import re
import itertools as it

import inspect  # Prints location in the program
def ln() -> str:
    fi = inspect.getframeinfo(inspect.currentframe().f_back)
    return f'{fi.lineno:3d}'
def fl() -> str:
    fi = inspect.getframeinfo(inspect.currentframe().f_back)
    return f'{fi.function} {fi.lineno:3d}'  # fi.filename if needed

""" This works, e.g. c.D can be used as 9
class _c:  # Gather the constants here
    X = 60  # The board width
    Y = 15  # its high
    D =  9  # Max sensibility of the sonar
c = _c()  # Simpler?
"""
class c:  # Gather the constants here
    X = 60  # The board width
    Y = 15  # its high
    D =  9  # Max sensibility of the sonar


def distance(dx, dy) -> int:
    return round(m.sqrt(dx**2 + dy**2))


def removeFrom_poss():
    global c  # The constants
    global farPoints, poss  # possible locations
    # For farPoints delete the points from its neighbourhood in poss
    ls = list(farPoints)
    for X, Y in ls:
        possCopy = poss.copy()
        lposs = len(poss)
        for x, y in possCopy:
            if distance((X-x), (Y-y)) <= c.D:
                if (x, y) in poss:
                    poss.remove((x, y))

        if lposs - len(poss) > 0:
            print(f'For ({X:2d}, {Y:2d}) {lposs-len(poss):3d} points deleted '
                  f'from the possible points set')


mainQuestion = 'Add/delete/list points or quit this game (y/n/q)? : '

def manipulatePoints() -> bool:
    global c  # The constants
    global points, circles, farPoints, poss  # ible locations
    printed = False
    while True:
        while True:
            r = input(mainQuestion).lower()
            if r in {'y', 'n', 'q'}:
                break

        if r[0] == 'q':
            return False

        if r[0] != 'y':
            break  # and update circles

        if not printed:
            printed = True
            print("'L' - list the points")
            print("Any negative number, -n means: delete the nth point;")
            print("Can be the point just entered, e.g. '15 5': '15 5 4' or '15 5 X'")
            print("All points printed by Sonar, e.g.: '(14,8)=X (17,8)=9 (26,7)=1 (26,8)=2'")

        a = input('Enter one of the four kinds of input: ')
        a = a.split()  # At spaces
        if len(a) == 0:
            print('Please enter valid value.')
            printed = False
            continue

        if a[0].find('=') >= 0:
            points = []
            for p in a:
                e = re.search('\(([0-9]+),([0-9]+)\)=([0-9]+|X)', p)
                x = int(e.group(1))
                y = int(e.group(2))
                if e.group(3) == 'X':
                    farPoints.add((x, y))  # Duplicates will be ignored
                else:
                    d = int(e.group(3))
                    points.append((x, y, d))
            continue

        X = a[0]
        if X[0] == '-':  # Delete a point from p
            i = int(X[1:])
            del points[i-1]
            continue

        if X.lower().startswith('l'):
            if len(points) == 0:
                print("No points")
            else:
                for i in range(len(points)):
                    _x, _y, _d = points[i]
                    print(f"{i+1}. point = ({_x:2d}, {_y:2d}, {_d})")
            if len(farPoints) == 0:
                print("No farPoints, with distance X")
            else:
                ls = list(farPoints); ls.sort()
                for _x, _y in ls:
                    print(f"farPoint ({_x:2d}, {_y:2d})")
            print(f'{len(poss) = }, the number of possible places')
            continue

        if len(a) != 3:
            print('Please enter valid values for x, y, and distance.')
            continue
        Y = a[1]
        D = a[2]

        if D.lower().startswith('x'):  # Add the point to farPoints and delete all the points
            # from poss, which are closer or equal than c.D
            if not X.isdecimal():
                print(f"'{X=}' is not decimal"); continue
            if not Y.isdecimal():
                print(f"'{Y=}' is not decimal"); continue
            X = int(X); Y = int(Y)
            farPoints.add((X, Y))  # Points from poss will be deleted at the end of this function
            continue

        # Add the point to points, if all are decimals, >= 0
        if not X.isdecimal():
            print(f"'{X=}' is not decimal"); continue
        if not Y.isdecimal():
            print(f"'{Y=}' is not decimal"); continue
        if not D.isdecimal():
            print(f"'{D=}' is not decimal"); continue

        points.append((int(X), int(Y), int(D)))

    # After 'while True' loop ---------------------

    # Populate circles, for each point build a set of (x,y) tuples
    circles = []
    for X, Y, D in points:
        s = set()  # Points, which are D distance from (X,Y)
        # print(f'{X=} {Y=} {D=}')
        for x in range(max(0, X - D), min(c.X, X + D + 1)):
            for y in range(max(0, Y - D), min(c.Y, Y + D + 1)):
                if distance((X - x), (Y - y)) == D:
                    s.add((x, y))

        # This point is done, add to the circle points
        circles.append(s.copy())

    removeFrom_poss()

    return True

# manipulatePoints()


def getGuess():
    global c  # The constants
    global points, farPoints, poss
    # Get the point from poss, which has the most points from poss closer or equal c.D.
    # From the farthest points pick the first one, which was not used, yet.
    ls = []
    for X, Y in poss:
        n = 0
        for x, y in poss:
            if distance((X-x), (Y-y)) <= c.D:
                n += 1
        ls.append((n, (X, Y)))

    ls.sort(key=lambda a: a[0], reverse=True)  # Give it some randomness
    ps = set(points) | farPoints
    if len(ps) > 0:
        for n, xy in ls:
            if xy not in ps:
                break
    else:
        n, xy = ran.choice(ls[:(c.X-2*c.D)])

    print(f'Try: {xy}')

    pass  # To set breakpoint


def getSuggestions():
    # breakpoint()  # ???? DO NOT FORGET TO COMMENT OUT ????
    global c  # class with constants
    global points, circles, farPoints, poss
    if len(points) != len(circles):
        breakpoint()  # ???? Internal error

    somethingPrinted = False
    if len(points) > 0:
        # Create an index list, from which the combinations will be picked up
        np = []
        for i in range(len(points)):
            np.append(i)

        # If we have more than one point, don't give individual circles
        for r in range(1 if len(np) > 1 else 0, len(np)):
            lc = list(it.combinations(np, r + 1))  # List of tuples r+1 size
            for cs in lc:
                # print(f'{fl()} {cs=}')  # ???? Debug
                s = circles[cs[0]]  # set of tuples, points, around cs[0] point
                # print(f'{fl()} {s=}')  # ???? Debug
                x, y, d = points[cs[0]]  # Pick up the first point
                print(f'{cs[0] + 1:2d}. Point ({x:2d}, {y:2d}), {d=}')
                # print(f'{fl()} {s=}')  # ???? Debug
                for ipt in cs[1:]:  # Pick up the remaining points
                    x, y, d = points[ipt]
                    print(f'{ipt + 1:2d}. Point ({x:2d}, {y:2d}), {d=}')
                    s = s & circles[ipt]  # and - tuples in both places
                    # print(f'{fl()} {s=}')  # ???? Debug

                # Take out the points, if any, not in poss set
                s = s & poss
                # If any point in s is closer to any given point, delete it
                sCopy = s.copy()
                # print(f'{fl()} {s=}')  # ???? Debug
                for x1, y1 in sCopy:
                    for x2, y2, d in points:
                        if distance((x1-x2), (y1-y2)) < d:
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
                        if distance((x1 - x2), (y1 - y2)) <= c.D:
                            n += 1
                    res.append((n, (x1, y1)))

                res.sort(reverse=True)
                print(str(res)[1:-1])  # Delete the '[]' around it
                if len(res) > 0:
                    somethingPrinted = True

    if not somethingPrinted:
        getGuess()


def instructions():
    print(f"""Instructions:
This program will help to locate the treasure chests. The program can be mistake,
i.e. two close points say the chest is close by, the program assumes that they
both refer to the same chest, but it could be two chests in an opposite directions.
Picking up a wrong point is not a waste, it gives a lot of information for future guessing.
The distance between two points calculated this way, like in Sonar, everything is integer:
    distance = round(math.sqrt((x2-x1)**2 + (y2-y1)**2))

The main question is:
    {mainQuestion}
y - you want to add a new point(s), delete one point, or list the points
n - give me a hint which point to try
q - quit this game

If the answer was 'y' you can give a point in this way:
    x y d - e.g. 32 9 5 meaning that there is a chest from (32,9) distance 5
            or 43 5 X - there is no chest in the vicinity of point (43,5)
    L     - list the points already tried
    -n    - delete the nth point
    After a hit almost all the points have changed, it would be too tedious to delete
    and add many points. The current version of the Sonar game not only shows the
    points, but prints them out, too, e.g.:
        (1,2)=3 (44,14)=9 (46,7)=X (53,4)=X
    Just copy the whole line to the program, the points will be processed.

Press enter to continue...""")
    input()

# instructions() function end


############################## F U N C T I O N S  E N D ##################################

print('H E L P  to find the chests\n')

while True:
    # breakpoint()  # ???? DEBUG, to set other breakpoints

    print('Would you like to view the instructions? (yes/no): ', end='')
    if input().lower().startswith('y'):
        instructions()

    # points and circles are indexed together
    points = []  # List of points (X,Y,D) 1<=D<=9
    circles = []  # Each element is a set of points (x,y), which are D distance from a points[]

    farPoints = set()  # Points where no chest is close by
    poss = set()  # All possible points, minus the points, which are <= c.D distance from farPoints

    for y in range(c.Y):
        for x in range(c.X):
            poss.add((x, y))  # All points are candidates

    while True:
        ret = manipulatePoints()  # False means quit this game
        if ret:
            getSuggestions()
        else:
            break

    if not input('Do you want another game? (y/n): ').lower().startswith('n'):
        continue
    else:
        print('\nThanks for using this program, any suggestion is welcomed.')
        break
