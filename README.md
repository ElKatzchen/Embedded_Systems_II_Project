# Embedded_Systems_II_Project
In the current Git is available the codes for both, TIVA in .c format and
Raspberry in .py format.

## Raspberry
For the Raspberry, it is necesary to download miniconda and activate a new
enviroment with the following libraries:

Open CV
Numpy
Mediapipe
PySerial

This libraries are used to make the AI work and to transmit the data via UART.

## TIVA
For the TIVA, the Git contains a series of files wich make the codes work. The
only necesaru=y step to make it compile and upload is to write ./Compile in the
terminal. This way the code will be compiled and uploaded by itself

## Aditional Information
To make both, the TIVA nad the Raspberry work, there are some considerations.

1. The Raspberry must be the Pi4 or Pi5.
2. If a normal webcam is needed, it is necesary to change the IP on the .py file
   to a 0. If a cellphone is needed, it is necesary to link both, the Raspberry
   and the cellphone to the same wifi network and download "droidcam" on the
   cellhpone. Aditionally, the IP must be changed for the one provided by droidcam
3. The code works with bluetooth, if a USB wire is needed, it is necesary to change
   the .py file. The part that must change is the serial comunicarion, which must be
   "/dev/ttyACM0". If a bluetooth module is needed, it is necesary to go to
   /dev/serial/by-id adn copy all that path with the name of the bluetooth module.

## Thanks for reading the README, enjoy the code and please do not copy, just use
## as a guide for your future projects.