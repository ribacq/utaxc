#!/bin/python3
# -*-coding:utf-8 -*
import curses;
from items import *;
from environment import *;

"""A simple game writen with the curses module"""

def utaxc(scr):
	"""The main function"""
	
	#curses settings
	curses.curs_set(0);
	curses.halfdelay(1);
	colors.load_colors();
	
	#Environment
	env = Environment(scr, 3);
	env.draw_frames();
	
	#Level
	lvl = Level(env, 'hq');
	lvl.load();
	
	#Text
	env.side.addstr(0,0, 'UTaxC', curses.color_pair(4));
	
	#Creation of the player
	player = Player(env, lvl.player_y, lvl.player_x);
	
	#Main loop
	while True:
		#Get user action
		entry = env.getch();
		if entry in controls.ctrlsPlayer.values():
			action = [action for (action, ctrl) in controls.ctrlsPlayer.items() if ctrl == entry];
			player.kbd_entry(action[0]);
		elif entry == controls.ctrlsEnv['pause']:
			env.pause();
		elif entry == controls.ctrlsEnv['quit']:
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
