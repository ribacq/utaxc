#!/bin/python
# -*-coding:utf-8 -*
import curses;
from items import *;
from environment import *;

"""
A simple game writen with the curses module
"""

def utaxc(scr):
	"""
	The main function
	"""
	
	#curses settings
	curses.curs_set(0);
	curses.halfdelay(1);
	load_colors();
	
	#Environment
	env = Environment(scr, 3, ctrlsEnv);
	env.draw_frames();
	
	#Level
	hq = Level(env, 'hq');
	hq.load();
	
	#Text
	env.side.addstr(0,0, 'UTaxC', curses.color_pair(4));
	
	#Creation of the player
	player = Player(env, 13, 0);
	player.move('down');
	
	#Main loop
	while True:
		#Get user action
		c = env.getch();
		if c in ctrlsPlayer.values():
			action = [action for action, ctrl in ctrlsPlayer.items() if ctrl == c];
			player.kbd_entry(action[0]);
		elif c == ctrlsEnv['pause']:
			env.pause();
		elif c == ctrlsEnv['quit']:
			break;
		
		#Execute running actions
		env.exec_running_actions();
		
		env.side.addnstr(1, 0, 'Score: '+str(player.score), 16);
		env.side.addnstr(2, 0, 'Weight: '+str(player.weight)+'   ', 16);
		
		#Refresh screen
		env.refresh();
	
	#End of function

#Main call
if __name__ == '__main__':
	curses.wrapper(utaxc);
