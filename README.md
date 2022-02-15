# Lesson_6_Project_3_Sonar

sonar_01.py
The base copied fom: Sweigart, Al.
https://inventwithpython.com/invent4thed/chapter13.html
One player against the computer to find 3 chests on a 60x15 board.

sonar_02.py
It was made more flexible, at the start you can modify :
BOARD_WIDTH   - the default is 60
BOARD_HIGH    - the default is 15
SONAR_DEVICES - the default is 20
CHESTS        - the default is  3
Number Of Players:
If 1, it is similar to sonar_01, the player plays against the computer.
More than 1, then the players play against each othe. For each player an
other player hides the Chests.

find_01.py
It gives hints which locations to try. If it used against sonar_01,
it needs about 10 guests to find the 3 hidden chests.
You can ask for a hint at the very beginning, when no location was tried, yet.
You enter the locations as they were given to the sonar program, with the answer
and ask for a hint. The hint usually contains many locations, you pick one.
After a hit there are many changes. It would be tedious manually enter the
changes. The current version of the sonar programs print out all entered
locations with the distance to the nearest chest. You just copy this and
give to this program and after ask for a hint.
