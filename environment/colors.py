#!/bin/python3
# -*-coding:utf-8 -*
import curses;

"""Colors initialization module"""

def load_colors():
	"""Colors initialization function"""
	
	curses.init_pair(1, 3, 0); #1> Move block
	curses.init_pair(2, 7, 4); #2> Info
	curses.init_pair(3, 0, 7); #3> Frame
	curses.init_pair(4, 6, 0); #4> Player
	curses.init_pair(5, 3, 3); #5> Standard block
	curses.init_pair(6, 2, 0); #6> Treasure
