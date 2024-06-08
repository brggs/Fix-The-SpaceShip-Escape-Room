from microbit import *
import radio

# For testing/fixing the game when running live if necessary!

POLL_INTERVAL = 50

level = 0
descriptions = ['F', 'B', 'N']
messages = ['Fuel_GO', 'Battery_GO', 'Nav_GO']
radio.config(group=42)

while True:
    display.show(descriptions[level])

    if button_a.was_pressed():
        level += 1
        if level == 3: level = 0

    if button_b.was_pressed():
        radio.on()
        radio.send(messages[level])
        radio.off()
        display.show(Image.YES)
        sleep(1000)
    
    sleep(POLL_INTERVAL)
