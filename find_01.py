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

import math
import re
import copy  # To make deepcopy
import itertools as it
import inspect as ins  # Location in the program, members of a class


def ln() -> str:
    fi = ins.getframeinfo(ins.currentframe().f_back)
    return f'{fi.lineno:3d}'
def fl() -> str:
    fi = ins.getframeinfo(ins.currentframe().f_back)
    return f'{fi.function} {fi.lineno:3d}'  # fi.filename if needed


class c:  # Gather the main parameters here, the variables not starting with '_' can be
    # overwritten at the beginning
    # Using only class variables
    BOARD_WIDTH = 60  # The board width
    BOARD_HIGH  = 15  # its high
    _D = 9  # Max sensibility of the sonar, you can't mofify this


def distance(dx, dy) -> int:
    return round(math.sqrt(dx**2 + dy**2))


# Removing the possible locations has 2 steps:
# 1) those, which are <= c._D to a farPoint;
# 2) those, which are < d to a tried point.
def removeFrom_poss():
    global c  # The main parameters
    global points, farPoints, poss  # possible locations

    # For farPoints delete the points from its neighbourhood in poss
    ls = list(farPoints)
    for X, Y in ls:
        possCopy = copy.deepcopy(poss)  # Perhaps poss.copy() would be enough
        lposs = len(poss)
        for x, y in possCopy:
            if distance((X-x), (Y-y)) <= c._D:
                if (x, y) in poss:
                    poss.remove((x, y))

        if lposs - len(poss) > 0:
            print(f'For ({X:2d}, {Y:2d}) {lposs-len(poss):3d} points deleted '
                  f'from the possible points set')

    # For points delete the possible points which are < d, the closest chest
    for X, Y, D in points:  # List of tuples in (x,y,d) form
        possCopy = copy.deepcopy(poss)  # Perhaps poss.copy() would be enough
        lposs = len(poss)
        for x, y in possCopy:
            if distance((X - x), (Y - y)) < D:
                if (x, y) in poss:
                    poss.remove((x, y))

        if lposs - len(poss) > 0:
            print(f'For ({X:2d}, {Y:2d}) {lposs - len(poss):3d} points deleted '
                  f'from the possible points set')


mainQuestion = 'Add/delete/list points (y), get hint (h), or quit (q): '

def manipulatePoints() -> bool:
    global c  # The main parameters
    global points, circles, farPoints, poss  # ...ible locations
    printed = False
    while True:
        while True:
            r = input(mainQuestion).lower()
            if r in {'y', 'h', 'q'}:
                break

        if r[0] == 'q':
            return False

        if r[0] != 'y':
            break  # and update circles

        if not printed:
            printed = True
            print("'L' - list the points")
            print("Any negative number, -n means: delete the nth point;")
            print("Can be the point just entered, e.g. '25 5': '25 5 4' or '25 5 X'")
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
        for x in range(max(0, X - D), min(c.BOARD_WIDTH, X + D + 1)):
            for y in range(max(0, Y - D), min(c.BOARD_HIGH, Y + D + 1)):
                if distance((X - x), (Y - y)) == D:
                    s.add((x, y))

        # This point is done, add to the circle points
        circles.append(copy.deepcopy(s))

    removeFrom_poss()

    return True

# manipulatePoints()


def getGuess():
    global c  # The main parameters
    global points, farPoints, poss
    # Get the point from poss, which has the most points from poss closer or equal to c._D.
    ls = []
    for X, Y in poss:
        n = 0
        for x, y in poss:
            if distance((X-x), (Y-y)) <= c._D:
                n += 1
        ls.append((n, (X, Y)))

    ls.sort(key=lambda a: a[0], reverse=True)  # Give it some randomness (exclude a[1])
    print(f'Try: {ls[0]}')  # Print out the first one


def getSuggestions():
    # breakpoint()  # ???? DO NOT FORGET TO COMMENT OUT ????
    global c  # class with constants
    global points, circles, farPoints, poss
    if len(points) != len(circles):
        breakpoint()  # ???? Internal error

    somethingPrinted = False
    if len(points) > 0:
        # Create an index list, from which the combinations will be picked up
        indexList = []  # 0,1,2,...
        for i in range(len(points)):
            indexList.append(i)

        startFrom0 = False
        while True:
            # If we have more than one point, don't give individual circles
            strt = 0 if startFrom0 else (1 if len(indexList) > 1 else 0)
            for r in range(strt, len(indexList)):
                lc = list(it.combinations(indexList, r + 1))  # List of tuples r+1 size

                for cs in lc:
                    # print(f'{ln()} {cs=} {circles[cs[0]]=}')  # ???? Debug
                    intersec = circles[cs[0]].copy()  # set of tuples, points, around cs[0] point
                    for ipt in cs[1:]:  # Pick up the remaining points, if any
                        # print(f'{ln()} {ipt=} {circles[ipt]=}')  # ???? Debug
                        intersec &= circles[ipt]  # and - tuples in both places
                        # print(f'{ln()} {cs[0]=} {circles[cs[0]]=}')  # ???? Debug
                        # print(f'{fl()} {intersec=}')  # ???? Debug

                    # Take out the points, if any, not in poss set
                    intersec &= poss

                    # For each remaining points in intersec associate with the number in poss,
                    # which are close enough.
                    res = []
                    for x1, y1 in intersec:
                        n = 0
                        for x2, y2 in poss:
                            if distance((x1 - x2), (y1 - y2)) <= c._D:
                                n += 1
                        res.append((n, (x1, y1)))

                    res.sort(reverse=True)
                    if len(res) > 0:
                        somethingPrinted = True
                        for ipt in cs:  # There was some intersection for these points
                            x, y, d = points[ipt]
                            print(f'{ipt + 1:2d}. Point ({x:2d}, {y:2d}), {d=}')
                        print(str(res)[1:-1])  # Delete the '[]' around it

            # for r in range
            if somethingPrinted:
                break  # from while true
            # There was no intersection among the points
            startFrom0 = True  # ... and repeat the while True loop

    if not somethingPrinted:
        getGuess()


def instructions():
    print(f"""\nInstructions:
This program will help to locate the treasure chests. The program can be mistaken,
i.e. two close points say the chest is close by, the program assumes that they
both refer to the same chest, but it could be two chests in an opposite directions.
Picking up a wrong point is not a waste, it gives a lot of information for future guessing.
The distance between two points calculated this way, like in Sonar, everything is integer:
    distance = round(math.sqrt((x2-x1)**2 + (y2-y1)**2))

The main question is:
    {mainQuestion}
y - you want to add a new point(s), delete one point, or list the points
h - give me a hint which point to try. The hints are printed out this way:
    (p,(x,y)) - from point (x,y) p possible locations can be seen.
q - quit this game

If the answer was 'y' you can give a point in this way:
    x y d - e.g. 32 9 5 meaning that there is a chest from (32,9) distance 5
            or 43 5 X - there is no chest in the vicinity of point (43,5)
            or in the form the current Sonar prints out, e.g.:
            (15,7)=7 (15,8)=6 (20,7)=9 (22,2)=X (22,7)=X (22,12)=7 (34,7)=X
    L     - list the points already tried
    -n    - delete the nth point
    After a hit almost all the points have changed, it would be too tedious to delete
    and add many points. The current version of the Sonar game not only shows the
    points, but prints them out, too, see an example above.
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

    print('You can modify the Board size')
    for m in ins.getmembers(c):  # type(m)=tuple (name as string, value as it is)
        if m[0][0] != '_':
            p = f'{m[0]} = {m[1]} ... Keep it? (y/n): '  # Make a prompt
            if input(p).lower().startswith('y'):
                continue  # for m
            # Get a new value
            while True:  # To allow to correct a bad answer
                v = input('Enter its new value: ')
                if v.isdecimal():
                    # Construct the statement
                    exec(f'c.{m[0]}={v}')
                    break  # Out from while True
                else:  # Entered not decimal
                    print('Please enter a decimal number.')

    # points and circles are indexed together
    points = []  # List of points (X,Y,D) 1<=D<=c._D
    circles = []  # Each element is a set of points (x,y), which are D distance from a points[]

    farPoints = set()  # Points where no chest is close by
    poss = set()  # All possible points, minus the points,
                  #     which are <= c._D distance from farPoints, and
                  #     point closer than d, reported by Sonar (px, py, d)

    for y in range(c.BOARD_HIGH):
        for x in range(c.BOARD_WIDTH):
            poss.add((x, y))  # All points are candidates

    ret = True
    while ret:
        ret = manipulatePoints()  # False means quit this game
        if ret:
            getSuggestions()

    if not input('Do you want another game? (y/n): ').lower().startswith('n'):
        continue  # From asking whether to see the instructions
    else:
        print('\nThanks for using this program, any suggestion is welcomed.')
        break
