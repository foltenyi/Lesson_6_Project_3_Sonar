"""
         1         2         3         4         5         6         7         8         9
123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
"""
###########################################################################
# Line length <= 99
#
# sonar_02.py
#
# CS-043-T001 Part 2 - Unit 6 - Final Collaborative Project: 3-3
#
# Added that two or more players can play against each other, or, as before,
# one player can play against the computer.
# The main parameters are collected in class c. Their values can be overwritten at the
# beginning if their name doesn't start with '_'.
#
# Updated to Python 3.10.
#
# The base copied fom: Sweigart, Al.
# https://inventwithpython.com/invent4thed/chapter13.html
#
###########################################################################
#
# Sonar Treasure Hunt

import random
import sys
import math
import copy  # To make deep copy
import inspect

def ln() -> str:
    fi = inspect.getframeinfo(inspect.currentframe().f_back)
    return f'{fi.lineno:3d}'
def fl() -> str:
    fi = inspect.getframeinfo(inspect.currentframe().f_back)
    return f'{fi.function} {fi.lineno:3d}'  # fi.filename if needed

class c:  # Gather the main parameters here, the variables not starting with '_' can be
    # overwritten at the very beginning
    # Using only class variables
    BOARD_WIDTH = 60  # The board width
    BOARD_HIGH  = 15  # its high
    _D = 9  # Max sensibility of the sonar, can't be overwritten
    SONAR_DEVICES = 20
    CHESTS = 3


######################### F U N C T I O N S   S T A R T ########################


def getNewBoard():
    # breakpoint() # ???? DO NOT FORGET TO COMMENT OUT ????
    # Create a new c.BOARD_WIDTH x c.BOARD_HIGH board data structure.
    board = []
    for x in range(c.BOARD_WIDTH):  # The main list is a list of c.BOARD_WIDTH lists.
        board.append([])
        # Each list in the main list has c.BOARD_HIGH single-character strings.
        for y in range(c.BOARD_HIGH):
            # Use different characters for the ocean to make it more readable.
            char = '~' if random.randint(0, 1) == 0 else '`'
            board[x].append(char)

    return board


def getRandomChests(n, numChests):  # For the (n+1)th player
    global numberOfPlayers
    # Create a list of chest data structures (two-item lists of x, y int coordinates).
    # If there is only one player, let the computer generate the locations.
    # Otherwise let an other player to hide the chests.
    chests = set()  # Make chests a set
    if numberOfPlayers == 1:
        while len(chests) < numChests:
            newChest = (random.randint(0, c.BOARD_WIDTH-1), random.randint(0, c.BOARD_HIGH-1))
            chests.add(newChest)  # If duplicate, just ignored
    else:
        # Pick up another player, m
        while (m := random.randint(0, numberOfPlayers-1)) == n:
            pass
        print(f'Player{n+1}, please turn away')
        print(f'Player{m+1}, please hide {c.CHESTS} chests, enter their coordinates, x y')
        print(f'x [0 - {c.BOARD_WIDTH-1}], y [0 - {c.BOARD_HIGH-1}]')
        while len(chests) < numChests:
            a = input('Please enter x y: ')
            a = a.split()  # At the spaces
            if len(a) == 2 and a[0].isdecimal() and a[1].isdecimal():
                newChest = (int(a[0]), int(a[1]))
                if 0 <= newChest[0] <= c.BOARD_WIDTH-1 and 0 <= newChest[1] <= c.BOARD_HIGH-1:
                    chests.add(newChest)
                else:
                    print('Please observe the limits.')
            else:
                print('Please enter two numbers.')
        print('Please, clan the screen')
        while True:
            a = input('How many lines to scroll?: ')
            if a.isdecimal():
                for _ in range(int(a)):
                    print()
                break

        print('Push enter to continue...', end='')
        input()

    return chests  # One set for player n


def drawBoard(board):
    global c  # The constants
    # Draw the board data structure.
    tensDigitsLine = ' '*5  # Initial space for the numbers the left side of the board
    for i in range(1, int(c.BOARD_WIDTH/10)):
        tensDigitsLine += (' ' * (10-len(str(i))) + str(i))

    # Print the numbers across the top of the board.
    print(tensDigitsLine)
    digitsLine = ''
    for i in range(c.BOARD_WIDTH):
        digitsLine += str(i % 10)
    print(' '*4 + digitsLine)

    # Print each of the c.BOARD_HIGH rows.
    for row in range(c.BOARD_HIGH):
        # Create the string for this row on the board.
        boardRow = ''
        for column in range(c.BOARD_WIDTH):
            boardRow += board[column][row]

        print(f'{row:3d} {boardRow} {row}')

    # Print the numbers across the bottom of the board.
    print(' '*4 + digitsLine)
    print(tensDigitsLine)

    # Added: print the points, if any
    first = True
    # breakpoint()  # ???? DON'T FORGET TO COMMENT OUT ????
    for x in range(c.BOARD_WIDTH):
        for y in range(c.BOARD_HIGH):
            ch = board[x][y]
            if ch.isdigit() or ch == 'X':
                print(('' if first else ' ') + f'({x},{y})={ch}', end='')
                first = False
    if not first:
        print('\n')


def isOnBoard(x, y):
    # Return True if the coordinates are on the board; otherwise, return False.
    return 0 <= x < c.BOARD_WIDTH and 0 <= y < c.BOARD_HIGH


def enterPlayerMove(previousMoves):  # Returns a tuple (x,y)
    # Let the player enter their move. Return a two-item tuple of int x, y coordinates.
    print(
        f'Where to drop the next sonar device? [0,{c.BOARD_WIDTH-1}] [0,{c.BOARD_HIGH-1}] (or quit): ',
        end='')
    while True:
        move = input()
        if move.lower()[0] == 'q':
            print('Thanks for playing!')
            sys.exit()

        move = move.split()
        if (len(move) == 2 and move[0].isdecimal() and move[1].isdecimal() and
                                isOnBoard(int(move[0]), int(move[1]))):
            if (int(move[0]), int(move[1])) in previousMoves:
                print('You already moved there.')
                continue
            return (int(move[0]), int(move[1]))

        print(
            f'Enter a number [0,{c.BOARD_WIDTH-1}], a space, then a number [0,{c.BOARD_HIGH-1}]: ',
            end='')

    # breakpoint()  # ???? TO BE COMMENTED OUT ????


def makeMove(board, chests, x, y):
    global c  # The constants
    # breakpoint()  # ???? DO NOT FORGET TO COMMENT OUT ????
    # Change the board data structure with a sonar device character. Remove treasure chests
    # from the chests list as they are found.
    # Return False if this is an invalid move.
    # Otherwise, return the string of the result of this move.
    smallestDistance = c.BOARD_WIDTH**2 + c.BOARD_HIGH**2  # Any chest will be closer than that.
    for cx, cy in chests:
        distance = round(math.sqrt((cx - x)**2 + (cy - y)**2))
        if distance < smallestDistance:  # We want the closest treasure chest.
            smallestDistance = distance

    if smallestDistance == 0:
        # xy is directly on a treasure chest!
        chests.remove((x, y))
        return 'You have found a sunken treasure chest!'
    else:
        if smallestDistance <= c._D:
            board[x][y] = str(smallestDistance)
            return f'Treasure detected at a distance of {smallestDistance} from the sonar device.'
        else:
            board[x][y] = 'X'
            return 'Sonar did not detect anything. All treasure chests are out of range.'


def showInstructions():
    global c  # The class with the constants
    print("""Instructions:
You are the captain of the Simon, a treasure-hunting ship. Your current mission
is to use sonar devices to find three sunken treasure chests at the bottom of
the ocean. But you only have cheap sonar that finds distance, not direction.

Enter the coordinates to drop a sonar device. The ocean map will be marked with
how far away the nearest chest is, or an X if it is beyond the sonar device's
range. For example, the C marks are where chests are. The sonar device shows a
3 because the closest chest is 3 spaces away.

              1         2         3
    012345678901234567890123456789012
  0 ~~~~`~```~`~``~~~``~`~~``~~~``~`~ 0
  1 ~`~`~``~~`~```~~~```~~`~`~~~`~~~~ 1
  2 `~`C``3`~~~~`C`~~~~`````~~``~~~`` 2
  3 ````````~~~`````~~~`~`````~`~``~` 3
  4 ~`~~~~`~~`~~`C`~``~~`~~~`~```~``~ 4
    012345678901234567890123456789012
              1         2         3
In the real game, the chests are not visible in the ocean.

Press enter to continue...""")
    input()

    print(f"""When you drop a sonar device directly on a chest, you retrieve it and the other
sonar devices update to show how far away the next nearest chest is. The chests
are beyond the range of the sonar device on the left, so it shows an X.

              1         2         3
    012345678901234567890123456789012
  0 ~~~~`~```~`~``~~~``~`~~``~~~``~`~ 0
  1 ~`~`~``~~`~```~~~```~~`~`~~~`~~~~ 1
  2 `~`X``7`~~~~`C`~~~~`````~~``~~~`` 2
  3 ````````~~~`````~~~`~`````~`~``~` 3
  4 ~`~~~~`~~`~~`C`~``~~`~~~`~```~``~ 4
    012345678901234567890123456789012
              1         2         3

The treasure chests don't move around. Sonar devices can detect treasure chests
up to a distance of {c._D} spaces. Try to collect all {c.CHESTS} chests before running out
of the {c.SONAR_DEVICES} sonar devices. Good luck!

One player can play against the computer, or more players against each other.

Press enter to continue...""")
    input()

# showInstructions() function end


print('\nS O N A R   G A M E!\n')

while True:  # Start a new game
    # Game setup
    print('Would you like to view the instructions? (y/n): ', end='')
    if input().lower().startswith('y'):
        showInstructions()

    print('You can modify the parameters of the Game. Do you want it? (y/n): ', end='')
    if input().lower().startswith('y'):
        for m in inspect.getmembers(c):  # type(m)=tuple (name as string, value as it is)
            if m[0][0] == '_':  # Skip system and fix members
                continue
            p = f'{m[0]} = {m[1]} ... Keep it? (y/n): '  # Make a prompt
            if input(p).lower().startswith('y'):
                continue  # for m
            # Get a new value
            while True:  # To allow to correct a bad answer
                v = input('Enter its new value: ')
                if v.isdecimal():
                    exec(f'c.{m[0]}={v}')  # Execute the statement
                    break  # Out from while True
                else:  # Entered not decimal
                    print('Please enter a decimal number.')

    # Get number of players, one or more
    # breakpoint()  # ???? DO NOT FORGET TO COMMENT OUT ????
    while True:  # Break out when got the number
        _n = input('Enter the number of players (1 or more): ')
        if _n.isdecimal():
            numberOfPlayers = int(_n)
            break

    sonarDevices = []  # How many left for each player
    theBoards = []  # The board of the ith player
    theChests = []  # A set of tuples (x,y) for each player
    chestsBackup = []  # To keep the original
    previousMoves = []  # set()
    for i in range(numberOfPlayers):
        sonarDevices.append(c.SONAR_DEVICES)
        theBoards.append(getNewBoard())  # one board is theBoard[x][y]
        chests = getRandomChests(i, c.CHESTS)  # Set of tuples (x,y) for the (i+1)th player
        theChests.append(chests)
        chestsBackup.append(copy.deepcopy(chests))
        previousMoves.append(set())

    while True:  # It is too complicated to put here if any player left
        # A player is in the game if s/he has sonar device and hidden chest
        for cp in range(numberOfPlayers):
            if sonarDevices[cp] > 0 and len(theChests[cp]) > 0:
                break
        else:
            break  # Executed if the break above was not executed

        for currPlayer in range(numberOfPlayers):
            # If currPlayer has Chest(s) AND Sonar Device(s), make a move
            if len(theChests[currPlayer]) > 0 and sonarDevices[currPlayer] > 0:
                if numberOfPlayers > 1:
                    print(f'\nThe board of Player{currPlayer+1}')
                drawBoard(theBoards[currPlayer])
            else:  # The currPlayer has finished this game, try the next player
                continue

            # Show sonar device and chest statuses.
            print(f'You have {sonarDevices[currPlayer]} sonar device(s) left. '
                  f'{len(theChests[currPlayer])} treasure chest(s) remaining.')

            x, y = enterPlayerMove(previousMoves[currPlayer])
            # We must track all moves so that sonar devices can be updated.
            previousMoves[currPlayer].add((x, y))  # To the set as a tuple

            moveResult = makeMove(theBoards[currPlayer], theChests[currPlayer], x, y)
            sonarDevices[currPlayer] -= 1
            print(moveResult)
            if moveResult == 'You have found a sunken treasure chest!':
                # Update all the sonar devices currently on the map.
                for x, y in previousMoves[currPlayer]:
                    makeMove(theBoards[currPlayer], theChests[currPlayer], x, y)

            if len(theChests[currPlayer]) == 0:  # Found the LAST one
                # breakpoint()  # ???? DO NOT FORGET TO COMMENT OUT ????
                # Show where the chests were
                for x, y in chestsBackup[currPlayer]:
                    theBoards[currPlayer][x][y] = 'C'

                drawBoard(theBoards[currPlayer])
                print(f'{sonarDevices[currPlayer]} sonar device(s) left')
                print('Congratulations and good game!')
                continue  # Any player left

            if sonarDevices[currPlayer] == 0 and len(theChests[currPlayer]) > 0:
                print(f'Player{currPlayer+1} run out of sonar devices!')
                print('The remaining chests were here:', end='')
                for x, y in theChests[currPlayer]:
                    print(f' ({x}, {y})', end='')
                print()

            # continue next player

        # continue next round

    print('No player left. Does anybody want to play again? (yes or no): ', end='')
    if not input().lower().startswith('y'):
        sys.exit()
