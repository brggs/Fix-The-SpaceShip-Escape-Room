from microbit import *
import radio

# This code runs on the micro:bit attached to the fuel container.  It checks
# the water level via the moisture sensor attached to pin0. 
#
# When the level has been just right (not too low, or too high) for long
# enough, the code sends a message to the control micro bit, then ends.

# The water level reading must be between these values to complete the 
# objective.
LOW_LEVEL = 600
HIGH_LEVEL = 700

# This controls how long to wait before signalling success.  The amount of 
# time will be this value multiplied by POLL_INTERVAL.
CHECK_COUNT = 50

# How frequently to check for input (milliseconds)
POLL_INTERVAL = 50

# This variable keeps track of how long the water has been at the correct
# level for.
correct_count = 0

while True:
    # Read the water level
    level = pin0.read_analog()

    if level > HIGH_LEVEL:
        # The water is too high
        display.show(Image.CONFUSED)
        correct_count = 0
    elif level > LOW_LEVEL:
        # The water level is just right
        display.show(Image.HAPPY)
        correct_count += 1
        if correct_count > CHECK_COUNT:
            # The water level has been right for long enough
            # Break out of the While loop
            break
    else:
        # The water is too low  
        display.show(Image.SAD)
        correct_count = 0
    
    sleep(POLL_INTERVAL)

# The level has been at the right level for long enough, so signal the 
# control unit to move on to the next step.

# Turn the radio on, and send the message until we get a response
radio.config(group=42, power = 4)
radio.on()
while radio.receive() != "Fuel ACK":
    radio.send("Fuel GO")
    sleep(1000)

# The control unit has got our message, so shut down
display.show(Image.YES)
radio.off()
