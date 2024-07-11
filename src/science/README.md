# Science Unit

This unit handles step 3 (Setting the course), step 4 (sending a message) and part of step 5 (the launch sequence.)

As with the Control Unit, this micro:bit is housed in the control console, which includes an OLED panel, dials and a PIR sensor.  

Photo

This code does nothing when it first starts - it waits for a radio message from the control unit.  When it receives this, it activates the Step 3 code.

### Step 3

The unit wakes up, and shows a set of facts about the current location.  The team use these to work out where they are, then press the B button on the micro:bit to allow them to enter their course - direction and distance.

When this is correct, the code moves on to the next step.

### Step 4

This step is simple - the teams have to shout a message into the microphone.  Once enough noise has been detected, the micro:bit sends a message to the control unit, then waits for the signal to start the launch sequence.

### Step 5

This step requires the team to run through a series of actions - pushing buttons, etc.  Once all the tasks have been complete, the unit sends a message to the control unit and then shuts down.

Note: One of these actions is for the team to "Stand still".  This uses the PIR sensor in this unit, but I've found this can be a bit over sensitive!  A simple fix is to cover it up with your hand if this happens (or take out this bit of the code).


## Equipment List

* A v2 micro:bit, as the microphone is required (this code will also not run on the original v1 micro:bit as it does not have enough memory)
* ELECFREAKS Octopus:bit Breakout Board
* OLED Screen
* 2x Potentiometers
* 2x Dials (I used [these](https://coolcomponents.co.uk/products/anodized-aluminum-machined-knob-black-20mm-diameter))
* PIR Sensor


## Build

1. Build the console unit for the science computer
2. Fix the breakout board to the back panel
3. Install the OLED Screen, potentiometers and PIR sensor into the console, connecting the wires to the breakout board.
   1. Pin 0 - Blue dial
   2. Pin 1 - Gold dial
   3. Pin 2 - PIR
4. Close the console unit
5. Use the [micro:bit editor](https://python.microbit.org/v/3/) to download the [code](refuel.py) onto the micro:bit
6. Insert the micro:bit into the slot in the top of the console

Photos

## Setup/Reset

1. Turn the micro:bit on

To reset, restart the micro:bit.