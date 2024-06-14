from microbit import *
import radio

CHARGE_RATE = 3
LEVEL_DISPLAY = [Image('00000:00000:00000:00000:00900:'),
        Image('00000:00000:00000:00000:99999:'),
        Image('00000:00000:00000:99999:99999:'),
        Image('00000:00000:99999:99999:99999:'),
        Image('00000:99999:99999:99999:99999:'),
        Image.HAPPY]
POLL_INTERVAL = 50

charge_level = 0

while True:
    if accelerometer.was_gesture('shake'):
        charge_level += CHARGE_RATE

    if charge_level > 50:
        display.show(LEVEL_DISPLAY[5])
        break
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
    
    sleep(POLL_INTERVAL)

radio.on()
while radio.receive() != "Battery ACK":
    radio.send("Battery GO")
    sleep(1000)

display.show(Image.YES)
radio.off()