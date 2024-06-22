from microbit import *
import radio

# For testing/fixing the game when running live if necessary!

POLL_INTERVAL = 50

level = 0
descriptions = ['Fuel', 'Battery', 'Step 3', 'Nav', 'Comms', 'Launch']
messages = ['Fuel GO', 'Battery GO', 'Step3 START', 'Nav GO', 'Comms GO', 'Launch GO']
radio.config(group=42)

while True:
    display.show(descriptions[level])

    if button_a.was_pressed():
        level += 1
        if level == len(descriptions): level = 0

    if button_b.was_pressed():
        radio.on()
        radio.send(messages[level])
        radio.off()
        display.show(Image.YES)
        sleep(1000)
    
    sleep(POLL_INTERVAL)
