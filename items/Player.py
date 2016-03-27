#!/bin/python3
# -*-coding:utf-8 -*
import curses;
from .Creature import Creature;

"""A module containing the Player class"""

class Player(Creature):
	"""The Player class"""
	
	def __init__(self, env, y, x):
		"""Constructor"""
		
		super(Player, self).__init__(env, y, x, 'ſ', 4, 1);
		self.score = 0;
		self.possible_running_actions.extend([]);
	
	def kbd_entry(self, entry):
		"""Treats a keyboard entry"""
		
		if entry in ('up', 'down', 'left', 'right'):
			#The Player wants to move
			self.move(entry);
		elif entry in ('action1', 'action2'):
			#The Player activates some stuff
			self.action(int(entry[-1]));
	
	def block_event(self, mode, direction):
		"""Acts according to the block the Player is coming into. This method is called by self.make_move (mode='make_move') or self.action (mode='action'). In the first case, returns True if further move is forbidden. In the second, returns True if an action is done, False otherwise."""
		(u, v) = self.dir_to_uv(direction);
		block = self.env.inch(u+self.y, v+self.x);
		
		if not super(Player, self).block_event(mode, direction):
			#There was no event defined by parent class. Player-specific events are defined now.
			if mode == 'make_move':
				#Automatic event, happens on touch
				if block == '$':
					#Money found
					self.env.disp_msg('Money found!', 'debug');
					self.score += 1;
					self.env.game.addstr(self.y+u, self.x+v, ' ');
					return False;
				else:
					#No event happening
					return False;
			else:
				#No event happening
				return False;
