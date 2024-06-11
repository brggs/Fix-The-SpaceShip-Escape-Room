from microbit import *
import radio

LOW_LEVEL = 600
HIGH_LEVEL = 700
POLL_INTERVAL = 50
CHECK_COUNT = 50

radio.config(group=42, power = 4)
correct_count = 0

while True:
    level = pin0.read_analog()

    if level > HIGH_LEVEL:
        display.show(Image.CONFUSED)
        correct_count = 0
    elif level > LOW_LEVEL:
        display.show(Image.HAPPY)
        correct_count += 1
        if correct_count > CHECK_COUNT:
            break
    else:
        display.show(Image.SAD)
        correct_count = 0
    
    sleep(POLL_INTERVAL)

radio.on()
while radio.receive() != "Fuel_Ack":
    radio.send("Fuel_GO")
    sleep(1000)

display.show(Image.YES)
radio.off()
