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

############################
## Start of our code
############################

POLL_INTERVAL = 50

time = 0
start = 0
running = False

def show_time(start):
    time = int((running_time() - start)/1000)
    mins = time / 60
    seconds = time % 60
    
    oled_add_text(6, 3, "%02d" % (mins,))
    oled_add_text(9, 3, "%02d" % (seconds,))

oled_initialize()
oled_clear_screen()

radio.config(group=42, power = 4)

oled_add_text(0, 1, ' Push button')
oled_add_text(0, 2, '  to start!')

# Push the big button to start
while True:
    if pin0.is_touched():
        break
    sleep(POLL_INTERVAL)

oled_add_text(0, 0, 'Next goal:    ')
oled_add_text(0, 1, ' Refill the  ')
oled_add_text(0, 2, '  fuel tank. ')
oled_add_text(0, 3, 'Time: 00:00')

running = True
start = running_time()
display.show(Image.ASLEEP)
radio.on()

# Step 2 - check for fuel Go
while True:
    if radio.receive() == "Fuel_GO":
        radio.send("Fuel_ACK")
        break

    show_time(start)
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, ' Charge the ')
oled_add_text(0, 2, '  battery.  ')

# Step 3 - check the battery connected
while True:
    if radio.receive() == "Battery_GO":
        radio.send('Battery_ACK')
        break
    show_time(start)
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, ' Send the   ')
oled_add_text(0, 2, '  message.  ')

# Step 4 - check for navigation go
while True:
    if radio.receive() == "Nav_GO":
        radio.send('Nav_ACK')
        break
    show_time(start)
    sleep(POLL_INTERVAL)

oled_add_text(0, 1, 'Enter launch')
oled_add_text(0, 2, '     code.  ')

# Step 5 - check for launch sequence
while True:
    if pin0.is_touched():
    #if pin1.read_digital() == 1:
        break
    show_time(start)
    sleep(POLL_INTERVAL)
    
oled_add_text(0, 1, ' Press the  ')
oled_add_text(0, 2, '  button!   ')

# Final - check for big button press
while True:
    if pin0.is_touched():
        break
    show_time(start)
    sleep(POLL_INTERVAL)


oled_add_text(0, 0, '************')
oled_add_text(0, 1, 'Well Done!!!')
oled_add_text(0, 2, '************')

show_time(start)