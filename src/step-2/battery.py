from microbit import *
import radio

# This code checks for the shake gesture, and increases the battery charge
# whenever this occurs.  When the charge level reaches the maximum, the code
# sends a message to the control unit to move on to the next step.

# This controls how quickly the charging will occur.  Increase this number
# to make the battery charge quicker.
CHARGE_RATE = 3

# Images showing the charge level as it increases
LEVEL_DISPLAY = [Image('00000:00000:00000:00000:00900:'),
        Image('00000:00000:00000:00000:99999:'),
        Image('00000:00000:00000:99999:99999:'),
        Image('00000:00000:99999:99999:99999:'),
        Image('00000:99999:99999:99999:99999:'),
        Image.HAPPY]

# How frequently to check for input (milliseconds)
POLL_INTERVAL = 50

# This variable keeps track of the current charge level
charge_level = 0

while True:
    if accelerometer.was_gesture('shake'):
        charge_level += CHARGE_RATE

    if charge_level > 50:
        display.show(LEVEL_DISPLAY[5])
        # The battery is fully charged, so break out of the while loop
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

# The battery is now charged, so signal the control unit to move on to the 
# next step.

# Turn the radio on, and send the message until we get a response
radio.config(group=42, power = 4)
radio.on()
while radio.receive() != "Battery ACK":
    radio.send("Battery GO")
    sleep(1000)

# The control unit has got our message, so shut down
display.show(Image.YES)
radio.off()