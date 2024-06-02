from microbit import *
import radio

radio.config(group = 1)
radio.on()

while True:
    received = radio.receive()
    if received == "1":
        display.show(Image.YES, delay=1000)
    elif received != None:
        display.show(Image.NO, delay=1000)
    else:
        display.show(Image.HAPPY)
    sleep(500)