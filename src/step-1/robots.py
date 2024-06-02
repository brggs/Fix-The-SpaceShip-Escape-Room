from microbit import *
import radio

POLL_INTERVAL = 300

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

display.show(ROBOT_ICONS[role])

radio.config(group=1, power = 3)
radio.on()

while True:

    if role == 1 and button_a.was_pressed():
        radio.send("0")
    elif role == 2 and button_a.was_pressed():
        radio.send("0")
    elif role == 3 and button_a.was_pressed():
        radio.send("0")
    elif role == 4 and button_a.was_pressed():
        radio.send("0")
    elif role == 5 and button_a.was_pressed():
        radio.send("1")
    
    sleep(POLL_INTERVAL)