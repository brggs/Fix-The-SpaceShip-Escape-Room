from microbit import *

POLL_INTERVAL = 50

ROBOT_ICONS = {
    1: Image.STICKFIGURE,
    2: Image.HEART,
    3: Image.ANGRY,
    4: Image.HAPPY,
    5: Image.SAD,
}

choosing_role = True
role = 1

while choosing_role:
    display.show(role)

    if button_a.was_pressed():
        role += 1
        if role == 6: role = 1
    if button_b.was_pressed():
        choosing_role = False

# The robot is now ready for the game.  
# Wait for the correct input send a message.
# This input is different for each robot.

while True:
    display.show(ROBOT_ICONS[role])

    if role == 1 and button_a.was_pressed():
        display.show(4)
        sleep(1000)
    elif role == 2 and button_a.is_pressed() and button_b.is_pressed():
        display.show(5)
        sleep(1000)
    elif role == 3 and accelerometer.was_gesture('down'):
        display.show(2)
        sleep(1000)
    elif role == 4 and accelerometer.was_gesture('shake'):
        display.show(8)
        sleep(1000)
    elif role == 5 and display.read_light_level() < 20:
        display.show(7)
        sleep(1000)
    
    sleep(POLL_INTERVAL)