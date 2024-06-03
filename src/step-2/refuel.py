from microbit import *
import radio

LOW_LEVEL = 600
HIGH_LEVEL = 700

POLL_INTERVAL = 300

radio.config(group=42, power = 4)
radio.on()

correct_count = 0

while True:
    level = pin0.read_analog()

    if level > HIGH_LEVEL:
        display.show(Image.CONFUSED)
        correct_count = 0
    elif level > LOW_LEVEL:
        display.show(Image.HAPPY)
        correct_count += 1

        if correct_count > 9:
            radio.send("Fuel_GO")
            correct_count = 0
    else:
        display.show(Image.SAD)
        correct_count = 0
    
    sleep(POLL_INTERVAL)