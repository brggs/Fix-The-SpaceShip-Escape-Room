from microbit import *
import radio

# This code runs on the Science Unit.
#
# It is inactive at first, until it receives a message from the Control Unit 
# telling it to wake up.
#
# It then shows the players the sensor information to allow them to work out
# where they are.  They then enter a course with the dials attached to 
# pins 0 (blue) and 1 (gold).
#
# Next it uses the microphone to listen for the message.
#
# Finally it is used in the launch sequence alongside the Control Unit, where
# both units display a number of different tasks, and checks for the correct
# inputs. 

#############################################################################
## This code is used to drive the OLED screen, skip down to see our code!   #
#############################################################################
OLED_ADDR = 0x3c
oled_screen = bytearray('b\x40') + bytearray(512)

def oled_initialize():
    for c in ([0xae], [0xa4], [0xd5, 0xf0], [0xa8, 0x3f], [0xd3, 0x00], [0 | 0x0], [0x8d, 0x14], [0x20, 0x00], [0x21, 0, 127], [0x22, 0, 63], [0xa0 | 0x1], [0xc8], [0xda, 0x12], [0x81, 0xcf], [0xd9, 0xf1], [0xdb, 0x40], [0xa6], [0xd6, 1], [0xaf]):
        i2c.write(OLED_ADDR, b'\x00' + bytearray(c))

def oled_set_pos(col=0, page=0):
    i2c.write(OLED_ADDR, b'\x00' + bytearray([0xb0 | page]))
    c1, c2 = col * 2 & 0x0F, col >> 3
    i2c.write(OLED_ADDR, b'\x00' + bytearray([0x00 | c1]))
    i2c.write(OLED_ADDR, b'\x00' + bytearray([0x10 | c2]))

def oled_clear_screen(c=0):
    global oled_screen
    oled_set_pos()
    for i in range(1, 513):
        oled_screen[i] = 0
    oled_draw_screen()

def oled_draw_screen():
    global oled_screen
    oled_set_pos()
    i2c.write(OLED_ADDR, oled_screen)

def oled_add_text(x, y, text):
    global oled_screen
    for i in range(0, min(len(text), 12 - x)):
        for c in range(0, 5):
            col = 0
            for r in range(1, 6):
                p = Image(text[i]).get_pixel(c, r - 1)
                col = col | (1 << r) if (p != 0) else col
            ind = x * 10 + y * 128 + i * 10 + c * 2 + 1
            oled_screen[ind], oled_screen[ind + 1] = col, col
    oled_set_pos(x * 5, y)
    ind0 = x * 10 + y * 128 + 1
    i2c.write(OLED_ADDR, b'\x40' + oled_screen[ind0 : (ind+1)])

oled_initialize()
oled_clear_screen()

############################
## Start of our code!      # 
############################

# This is used to convert the dial input number into a compass direction
DIR_DICT = { 0: 'S', 1: 'S', 2: 'SW', 3: 'W', 4: 'NW', 5: 'N', 6: 'NE', 7: 'E', 8: 'SE', 9: 'S', 10: 'S' }

# This is here to make testing easier - change this to False to get the code
# to skip to the start of step 3, and immediately show sensor data.
WAIT_FOR_START_MESSAGE = True

# How frequently to check for input (milliseconds)
POLL_INTERVAL = 200

# Variables to store input data
blue_val = 0
gold_val = 0
no_motion_count = 0

# This function checks the values of dials and the switch and updates the global 
# variables.
# It also sends a message to the Control Unit so it can also check the inputs.
def read_inputs():
    global blue_val, gold_val, no_motion_count
    blue_val = int(pin0.read_analog() / 100)
    gold_val = int(pin1.read_analog() / 100)

    if pin2.read_analog() < 100:
        no_motion_count += 1
    else:
        no_motion_count = 0
        
    radio.send('Blue %d' % blue_val)
    radio.send('Gold %d' % gold_val)
    if no_motion_count > 25:
        radio.send('No Motion')

# Turn on the radio
radio.config(group=42)
radio.on()

# Wait for the signal to start step 3
display.show(Image.ASLEEP)

while WAIT_FOR_START_MESSAGE and radio.receive() != "Step3 START":
    sleep(1000)

# Step 3a - Find out where we are
# Show the sensor readings, and allow the players to enter the course
# by pushing B then turning the dials.
display.show(Image.CONFUSED)

showSensors = True
while True:
    if button_a.was_pressed():
        showSensors = True
    if button_b.was_pressed():
        showSensors = False
    
    if showSensors:
        oled_add_text(0, 0, '--Sensors---')
        oled_add_text(0, 1, ' C: Forest  ')
        oled_add_text(0, 2, ' A: Oxygen  ')
        oled_add_text(0, 3, ' T: 28 deg  ')
    else:
        read_inputs()
                
        oled_add_text(0, 0, '-Set Course-')
        oled_add_text(0, 1, ' Dir:   %s   ' % (DIR_DICT[blue_val]))
        oled_add_text(0, 2, ' Dist:  %2d   ' % (gold_val))
        oled_add_text(0, 3, '            ')

        if blue_val == 7 and gold_val == 4:
            # The players entered the correct answer
            break

# Send a message to the Control Unit so it knows we're on to the next step
radio.send('Nav GO')

# Step 4 - Wait for the message to be shouted in the mic

display.clear()
oled_add_text(0, 0, '---Comms----')
oled_add_text(0, 1, '   Waiting  ')
oled_add_text(0, 2, '    for     ')
oled_add_text(0, 3, '   message  ')
        
# Keeps track of how long the players have been shouting for
message_amount = 0
while True:    
    if microphone.sound_level() > 100:
        message_amount += 0.5
        if message_amount >= 5:
            if True:
                break

    # Update the display to show how much of the message has sent
    for y in range(5):
        if message_amount > (4 - y):
            for x in range(5):
                display.set_pixel(x, y, 9)
        
    sleep(500)

# The message has now been sent, so send a radio message to the Control Unit
# to let it know
radio.send('Comms GO')
oled_clear_screen()
display.show(Image.HAPPY)

# Wait for the message from the Control Unit to start Step 5 - the
# launch sequence.
while True:
    if radio.receive() == "Step5 START":
        break    
    sleep(POLL_INTERVAL)

display.show(Image.CONFUSED)

# For this step, we show a series of instructions, and check for the right inputs.
# Some of the inputs happen on the Control Unit, so we wait for radio messages to
# tell us about those.
# Throughout this, we use the read_inputs() function, which checks for player
# input and also sends input data to the Control Unit, as it is also running 
# through its own series of instructions & checks.

oled_add_text(0, 1, 'Engage     ')
oled_add_text(0, 2, 'Gigglebeam!')

while True:
    read_inputs()
    if radio.receive() == "Button 4":
        break
    
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, 'Eject       ')
oled_add_text(0, 2, ' Glorps!    ')

while True:
    read_inputs()
    if radio.receive() == "Button 5":
        break
    
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, 'Turn blue    ')
oled_add_text(0, 2, ' dial left ! ')

while True:
    read_inputs()
    if blue_val == 0:
        break
    
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, 'Engage      ')
oled_add_text(0, 2, ' Teleport!  ')

while True:
    read_inputs()
    if radio.receive() == "Button 2":
        break
    
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, 'Prime Flux  ')
oled_add_text(0, 2, ' Capacitor! ')

while True:
    read_inputs()
    if radio.receive() == "Flick Switch":
        break
    
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, 'Activate    ')
oled_add_text(0, 2, ' warp core! ')

while True:
    read_inputs()
    if radio.receive() == "Button 3":
        break
    sleep(POLL_INTERVAL)

display.show(Image.HAPPY)
oled_add_text(0, 1, '            ')
oled_add_text(0, 2, ' Waiting... ')

# The launch sequence steps are complete, for this unit.

# Send a message to the Control Unit to let it know, until it sends a response
# back confirming the step is complete
while radio.receive() != 'Launch ACK':
    read_inputs()
    radio.send('Launch GO')
    sleep(200)

# We are done, shut down
oled_clear_screen()
radio.off()
