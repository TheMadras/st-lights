# st-lights

## About
The goal of this project is to use a Raspberry Pi with addressable lights and Twilio to create a textable version of the *Stranger Things* light wall.

## Installation
Clone the git repository and install the required packages from the requirements.txt. Follow the tutorial by Adafruit at https://learn.adafruit.com/neopixels-on-raspberry-pi?view=all#python-installation-of-neopixel-library-3005996-1 to get the required packages for using the Adafruit library to control the LED string. Create an account on Twilio then fill out all necessary information in the Config file. You can also change the letters and their location within the letter mapping. Only capital letters and other characters are supported. Run main.py with Python 3 to start the program.

## Usage
The API supports a number of commands. To display a word on the light wall, simply text the Twilio number with a message. Any letters will be lit up on the wall and an exclamation point will cause all the letters to light up quickly and randomly for a few seconds. Commands can be sent with the syntax `<your-command-here>`. Currently supported commands are:
*  `<QUIT>` Quits the program and turns of the lights.
*  `<PAUSE>` Pauses the word currently being spelled.
*  `<STOP>` Stops the program and clears the message queue.
*  `<CLEAR>` Clears the message queue.
*  `<START>` Starts a paused or stopped program.
