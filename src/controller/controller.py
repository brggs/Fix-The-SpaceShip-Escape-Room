from microbit import *
import radio

# This code runs on the Control Unit.
#
# It keeps track of the players time, and tells them the current step they 
# are on, via the OLED screen.
#
# Players push the big red button to start (pin0).
#
# The code then waits for updates from the fuel tank and battery, before
# waking up the Science Unit for step 3.
#
# Once the Science Unit has signalled steps 3 and 4 are complete, the players
# must again press the big red button to start the launch sequence.  Both units
# display a number of different tasks, and checks for the correct inputs. 
#
# When this is complete on both units, the players press the big red button one
# last time to finish the challenge.  Their time is shown on the OLED screen.


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

############################
## Start of our code!      #
############################

# This skips the first two stages, to allow testing of the 
# just the science and command consoles in isolation.
SKIP_TO_STEP_3 = False

# How frequently to check for input (milliseconds)
POLL_INTERVAL = 50

# This variable keeps track of which button has been pressed.  It is set by 
# the read_inputs() function.
button_pressed = 0 

# This keeps track of the time when the players started the challenge
start = 0

# This function checks which buttons are active and updates the global 
# variable.
# It also sends a message to the Science Unit so it can also check the inputs.
def read_inputs():
    global button_pressed
    
    # This code translates the raw input from the button pad into the number
    # of the button which was pushed.
    button_raw = pin1.read_analog()
    if button_raw < 20:
        button_pressed = 1
    elif button_raw < 70:
        button_pressed = 2
    elif button_raw < 110:
        button_pressed = 3
    elif button_raw < 150:
        button_pressed = 4
    elif button_raw < 600:
        button_pressed = 5
    else:
        button_pressed = 0
        
    if button_pressed > 0:
        radio.send('Button %d' % button_pressed)
    
    if pin2.is_touched():
        radio.send('Flick Switch')
        
# This function updates the OLED to show the current time since the 
# players started the challenge.
def show_time(start):
    time = int((running_time() - start)/1000)
    mins = time / 60
    seconds = time % 60
    oled_add_text(6, 3, "%02d" % (mins,))
    oled_add_text(9, 3, "%02d" % (seconds,))

# Set up the screen and the radio
oled_initialize()
oled_clear_screen()
radio.config(group=42)

# Wait for the players to push the big red button
oled_add_text(0, 1, ' Push button')
oled_add_text(0, 2, '  to start!')
while True:
    if pin0.is_touched():
        break
    sleep(POLL_INTERVAL)

# Start the timer, and tell the players their first task
oled_add_text(0, 0, 'Next goal:    ')
oled_add_text(0, 1, ' Refill the  ')
oled_add_text(0, 2, '  fuel tank. ')
oled_add_text(0, 3, 'Time: 00:00')

start = running_time()
display.show(Image.ASLEEP)
radio.on()

# Step 1 - wait for a message from the fuel tank to say it has been refilled
while True:
    if SKIP_TO_STEP_3 or radio.receive() == "Fuel GO":
        # Send an acknowledgement to let the fuel micro:bit know it can shut down
        radio.send("Fuel_ACK")
        break

    show_time(start)
    sleep(POLL_INTERVAL)

# Step 2 - wait for a message from the battery to say it has been charged
oled_add_text(0, 1, ' Charge the ')
oled_add_text(0, 2, '  battery.  ')
while True:
    if SKIP_TO_STEP_3 or radio.receive() == "Battery GO":
        # Send an acknowledgement to let the battery micro:bit know it can shut down
        radio.send("Battery ACK")
        break
    show_time(start)
    sleep(POLL_INTERVAL)

# Step 3 - send a message to the Science Unit to wake it up
radio.send('Step3 START')
oled_add_text(0, 1, ' Set the   ')
oled_add_text(0, 2, '  course.  ')

# Wait for a message from the Science Unit to say that the course has been set
while True:
    if radio.receive() == "Nav GO":
        break
    show_time(start)
    sleep(POLL_INTERVAL)

# Step 4 - Wait for a message from the Science Unit to say that the message
# has been sent.
oled_add_text(0, 1, ' Send a     ')
oled_add_text(0, 2, '  message.  ')
while True:
    if radio.receive() == "Comms GO":
        break
    show_time(start)
    sleep(POLL_INTERVAL)

# Step 5 - wait for the players to press the big red button to start the launch
# sequence.
oled_add_text(0, 1, 'Start launch')
oled_add_text(0, 2, '  sequence. ')
while True:
    if pin0.is_touched():
        break
    show_time(start)
    sleep(POLL_INTERVAL)

# Send a message to the Science Unit to tell it to start Step 5
radio.send('Step5 START')

# For this step, we show a series of instructions, and check for the right inputs.
# Some of the inputs happen on the Science Unit, so we wait for radio messages to
# tell us about those.
# Throughout this, we use the read_inputs() function, which checks for player
# input and also sends input data to the Science Unit, as it is also running 
# through its own series of instructions & checks.

oled_add_text(0, 1, 'Turn blue   ')
oled_add_text(0, 2, ' dial right.')
while True:
    read_inputs()
    if radio.receive() == "Blue 10":
        break

    show_time(start)
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, 'Reverse     ')
oled_add_text(0, 2, ' polarity!  ')
while True:
    read_inputs()
    if button_pressed == 1:
        break

    show_time(start)
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, 'Turn gold   ')
oled_add_text(0, 2, ' to left!   ')
while True:
    read_inputs()
    if radio.receive() == "Gold 0":
        break
    
    show_time(start)
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, 'Everyone    ')
oled_add_text(0, 2, 'Stand still!')
while True:
    read_inputs()
    if radio.receive() == "No Motion":
        break
    
    show_time(start)
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, 'Engage      ')
oled_add_text(0, 2, 'giggle beam!')
while True:
    read_inputs()
    if button_pressed == 4:
        break

    show_time(start)
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, 'Turn gold   ')
oled_add_text(0, 2, ' dial right!')
while True:
    read_inputs()
    if radio.receive() == "Gold 10":
        break
    
    show_time(start)
    sleep(POLL_INTERVAL)

# The launch sequence steps are complete, for this unit.
# Wait until we get a message from the Science Unit telling us that
# all of its steps are complete as well.
oled_add_text(0, 1, ' Waiting... ')
oled_add_text(0, 2, '            ')
while True:
    read_inputs()
    if radio.receive() == 'Launch GO':
        # Send a reply to the Science Unit to let it know we've received the 
        # message.
        radio.send('Launch ACK')
        break
    
    show_time(start)
    sleep(POLL_INTERVAL)

# Everything is complete, wait for one final button press to end the challenge
oled_add_text(0, 1, ' Press the  ')
oled_add_text(0, 2, '  button!   ')
while True:
    if pin0.is_touched():
        break
    show_time(start)
    sleep(POLL_INTERVAL)

# Send the reply one extra time, to ensure the Science Unit shuts down
radio.send('Launch ACK')
    
oled_add_text(0, 0, '************')
oled_add_text(0, 1, 'Well Done!!!')
oled_add_text(0, 2, '************')

# Call show_time() one last time, to display the teams final time, then end
show_time(start)
