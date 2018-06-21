# Serail 2 Text

Serial2Text is an utility to easily save a serial content. 
The idea came from the difficulties to save the content of the serial etheir from Putty or the Arduino IDE.
For sensor calibration, or debugging purpose it's important to get log, or data from the boards.
Serail2Text try to be a solution to archive these data.

<img src="/image/GUI.JPG" width="250"> <img src="/image/errormsg.JPG" width="250"> 

The project was born for a personal need, but was really instructive and help me to build skill on GUI interface, threading and python programming...
Hope it's can be helpful for you too :)

# Features
With Serial2Text you can:
* Configure your serial connection
* Monitor the serial
* Send to data to your board
* Save the content of the serial
* Add a file hearder on the saved serial (archive purpose / pandas columns...)
* Live graph (under development)

<img src="/image/sendcmd.JPG" width="250">        <img src="/image/hearder.JPG" width="250">

# Issues
The program was tested with several serial configuration, with different board (Arduino Uno, Arduino Nano, ESP32-devkitc).
The following issues were uncountere:
* Not saving the serial content
* Progam crash without warning when the serial ingoing message frequency is too high ()
If you encounter other issue or if you know how to solve this issue do not hesitate to contribute :)

# Github content:
In this Github, you will find:
* The python script
* Arduino Serial example (Serial 9600-19200, waiting to recivied data)
* Saved serial content example
* An Executable code (under development) 

<img src="/image/GUIwithtext.JPG" width="250">

Do not hesitate in you have any question or advice :)
