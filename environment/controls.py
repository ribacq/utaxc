#!/bin/python3
# -*-coding:utf-8 -*
import curses;

"""Control keys configuration file"""

ctrlsEnv = {\
	'pause':ord('0'),\
	'quit':ord('q')\
}

ctrlsPlayer = {\
	'up':curses.KEY_UP,\
	'down':curses.KEY_DOWN,\
	'left':curses.KEY_LEFT,\
	'right':curses.KEY_RIGHT,\
	'action1':ord(' '),\
	'action2':ord('e')\
}
