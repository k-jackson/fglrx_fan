fglrx_fan
=========

A python daemon to control excessive fan speeds when using fglrx.

The script runs as a background python process, using the python-daemon library. It provides 5 parameters for GPU temperature ranges, and 5 parameters for fan speeds. The user can add or modify these ranges, which are stored in two lists at the top of the script. For simplicity's sake, a user only has to add a line to their .bashrc file (ie: 'python ~/folder/fanspeed.py'), and the program will run in the background. It is reccomended that a user customize the temperature and speed values to appropriate ranges for their GPU. The test card was an XFX HD 6800.

This is a very primative version, and feedback is welcome.

KJ
