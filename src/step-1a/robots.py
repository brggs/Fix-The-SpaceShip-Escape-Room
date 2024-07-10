from microbit import *

# This code runs on each of the four robots used in step 1.  Each one has a 
# secret letter, which the players must find to put the robots in order, and
# find the code to unlock the fuel for step 2. 

# Each robot requires a different input to get it to reveal it's letter.
# When this code first runs, the person setting up the challenge chooses which 
# input is required on each robot, by pressing the A button.  Press B when the 
# number of the robot is shown (1-4).  The robot is now ready for the game.

# To make it easy to identify the different robots, each one displays a 
# different icon on its LEDs.
ROBOT_ICONS = {
    1: Image.HEART,
    2: Image.ANGRY,
    3: Image.HAPPY,
    4: Image.SAD,
}

# The amount of time to wait when displaying the letter
SHOW_LETTER_INTERVAL = 3000

# How frequently to check for input (milliseconds)
POLL_INTERVAL = 50

# Start by choosing which number robot we are.
choosing_role = True
role = 1

while choosing_role:
    display.show(role)

    if button_a.was_pressed():
        role += 1
        if role == 5: role = 1
    if button_b.was_pressed():
        choosing_role = False

# The robot is now ready for the game.  

# Wait for the correct input, then display the letter.
while True:
    display.show(ROBOT_ICONS[role])

    if role == 1 and button_a.is_pressed() and button_b.is_pressed():
        display.show('E')
        sleep(SHOW_LETTER_INTERVAL)
    elif role == 2 and accelerometer.was_gesture('down'):
        display.show('B')
        sleep(SHOW_LETTER_INTERVAL)
    elif role == 3 and accelerometer.was_gesture('shake'):
        display.show('H')
        sleep(SHOW_LETTER_INTERVAL)
    elif role == 4 and display.read_light_level() < 20:
        display.show('G')
        sleep(SHOW_LETTER_INTERVAL)
    
    sleep(POLL_INTERVAL)