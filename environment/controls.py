#!/bin/python
# -*-coding:utf-8 -*
import curses;

"""Control keys configuration file"""

ctrlsEnv = {\
	'pause':ord('0'),\
	'quit':curses.KEY_END\
}

ctrlsPlayer = {\
	'up':curses.KEY_UP,\
	'down':curses.KEY_DOWN,\
	'left':curses.KEY_LEFT,\
	'right':curses.KEY_RIGHT,\
	'action1':ord(' '),\
	'action2':ord('c'),\
}
