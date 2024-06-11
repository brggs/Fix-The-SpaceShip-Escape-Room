from microbit import *
import radio

############################
## OLED Code, skip down to see our code!
############################
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
## Start of our code
############################

POLL_INTERVAL = 200

time = 0
start = 0
running = False

radio.config(group=42)
radio.on()

# Wait for the signal to start step 4
display.show(Image.ASLEEP)

while radio.receive() != "Step4_START":
    sleep(1000)

radio.send("Step4_START_ACK")

# Step 4 - Set the course
display.show(Image.CONFUSED)

showSensors = True
while True:
    if button_a.was_pressed():
        showSensors = True
    if button_b.was_pressed():
        showSensors = False
    
    if showSensors:
        oled_add_text(0, 0, '--Sensors---')
        oled_add_text(0, 1, ' C: Jungle  ')
        oled_add_text(0, 2, ' A: Oxygen  ')
        oled_add_text(0, 3, ' T: 28 deg  ')
    else:
        dir_input = pin0.read_analog()
        dir = ''

        if dir_input > 880:
            dir = 'S'
        elif dir_input > 770:
            dir = 'SE'
        elif dir_input > 660:
            dir = 'E'
        elif dir_input > 550:
            dir = 'NE'
        elif dir_input > 440:
            dir = 'N'
        elif dir_input > 330:
            dir = 'NW'
        elif dir_input > 220:
            dir = 'W'
        elif dir_input > 110:
            dir = 'SW'
        else:
            dir = 'S'
        
        dist_input = pin0.read_analog() #TODO Pin1
        dist = int(dist_input / 100)
        
        oled_add_text(0, 0, '-Set Course-')
        oled_add_text(0, 1, ' Dir:   %s   ' % (dir))
        oled_add_text(0, 2, ' Dist:  %2d   ' % (dist))
        oled_add_text(0, 3, '            ')

        if dir == 'NE' and dist == 5:
            break


# Step 5 - Send a message

display.clear()
oled_add_text(0, 0, '---Comms----')
oled_add_text(0, 1, '   Waiting  ')
oled_add_text(0, 2, '    for     ')
oled_add_text(0, 3, '   message  ')
        
message_amount = 0
while True:    
    if microphone.sound_level() > 100:
        message_amount += 0.5
        if message_amount >= 5:
            if True:
                break

    for y in range(5):
        if message_amount > (4 - y):
            for x in range(5):
                display.set_pixel(x, y, 9)
        
    sleep(500)

display.show(Image.HAPPY)
oled_clear_screen()

while True:
    radio.send("Step5_GO")
    sleep(500)

