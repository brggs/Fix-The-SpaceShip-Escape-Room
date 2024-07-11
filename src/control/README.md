# Control Unit

This is the brains of the escape room.  It shows the players their current task, as well as their time.

This micro:bit is housed in the control console, which includes an OLED panel, buttons and a switch.  This is also connected to the Big Red Button.

Photo

### Starting the game

Teams press the big red button to start the game.

### Steps 1-4

During these steps, the control unit displays a short description of the team's next task.  It keeps in sync with the other micro:bits via radio messages.

### Step 5 - Launch Sequence

Once the team reach step 5, they press the big red button again to start thh launch sequence.  This step requires the team to run through a series of actions - pushing buttons, etc.  Once all the tasks have been complete here, the unit waits for a message from the science unit indicating that all the actions have been completed there.

The team then pushes the big red button one final time to stop the clock.  Their final time is shown on the OLED screen.


## Equipment List

* A v2 micro:bit (this code will not run on the original v1 micro:bit as it does not have enough memory)

To build the console:
* ELECFREAKS Octopus:bit Breakout Board
* OLED Screen
* ABKeyboard
* Flick switch (I used [these](https://www.amazon.co.uk/dp/B0882PCXPM))


## Build

1. Build the console unit for the big red button
2. Install the big red button into the unit
3. Attach the cable to the big red button, and feed it through the hole in the console
4. Build the console unit for the control computer
5. Fix the breakout board to the back panel
6. Install the OLED Screen, ABKeyboard and flick switch into the console, connecting the wires to the breakout board.
   1. Pin 1 - ABKeyboard
   2. Pin 2 - Flick switch
7. Connect the wires from the big red button through the hole in the command console, to pin 0 on the breakout board.
8. Close the console unit
9.  Use the [micro:bit editor](https://python.microbit.org/v/3/) to download the [code](refuel.py) onto the micro:bit
10. Insert the micro:bit into the slot in the top of the console

Photos


## Setup/Reset

1. Check that the flick switch is switch off
2. Turn the micro:bit on

To reset, restart the micro:bit - but make sure you've made a note of the team's time first!  Also turn off the flick switch.