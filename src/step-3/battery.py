from microbit import *

POLL_INTERVAL = 200
charge_level = 0

LEVEL_DISPLAY = [Image('00000:00000:00000:00000:00900:'),
        Image('00000:00000:00000:00000:99999:'),
        Image('00000:00000:00000:99999:99999:'),
        Image('00000:00000:99999:99999:99999:'),
        Image('00000:99999:99999:99999:99999:'),
        Image.SMILE]

while True:
    if accelerometer.was_gesture('shake'):
        charge_level += 1

    if charge_level > 50:
        display.show(LEVEL_DISPLAY[5])
    elif charge_level > 40:
        display.show(LEVEL_DISPLAY[4])
    elif charge_level > 30:
        display.show(LEVEL_DISPLAY[3])
    elif charge_level > 20:
        display.show(LEVEL_DISPLAY[2])
    elif charge_level > 10:
        display.show(LEVEL_DISPLAY[1])
    else:
        display.show(LEVEL_DISPLAY[0])
        break
    
    sleep(50)

while True:
    pin0.write_digital(1)
    sleep(POLL_INTERVAL)
