# PTZControl
Python control of a PTZ
Authors: 
M.Sc. Guilherme Marra
M.Sc. Mario Baldini
Adalto Myiai: undergraduate student

This project is in development in the Technology Faculty - SENAI DOURADOS MS - BRAZIL

The main subject is the control of an Axis Communications YP3040 Rotor, used to hold any kind of antenna, for cubesat monitoring and reading.

Specifically, it is being used with a 435Mhz 10-element antenna.

The main python code uses PyEphem lib for predictions, and a TTL RS485 USB stick for serial comm. with the rotor.

Satellite telemetry data form celestrak.com are acquired automatically, by specifying the cubesat catalog number
