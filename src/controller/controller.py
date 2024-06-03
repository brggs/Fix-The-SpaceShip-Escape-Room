from microbit import *
import radio

POLL_INTERVAL = 200

time = 0
start = 0
running = False

radio.config(group=42, power = 4)
radio.on()

while True:
    if pin0.is_touched():
        break
    sleep(50)

running = True
start = running_time()
display.show(Image.ASLEEP)

# Step 2 & 3 - check for fuel Go, and the battery connected
while True:
    if button_a.was_pressed():
        break
    sleep(POLL_INTERVAL)

# Step 4 - check for navigation go


# Step 5 - check for launch sequence

# Final - check for button press

# Display the time on the OLED (or 7 seg?)
time = running_time() - start
display.scroll(int(time/1000))