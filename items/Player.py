#!/bin/python3
# -*-coding:utf-8 -*
import curses;
from .Mobile import Mobile;

"""A module containing the Player class"""

class Player(Mobile):
	"""The Player class"""
	
	def __init__(self, env, y, x):
		"""Constructor"""
		
		super(Player, self).__init__(env, y, x, 'I', 4, 1);
		self.score = 0;
		self.possible_running_actions.extend([]);
		self.add_running_action('fall');
	
	def kbd_entry(self, entry):
		"""Treats a keyboard entry"""
		
		if entry in ('up', 'down', 'left', 'right'):
			#The Player wants to move
			self.move(entry);
		elif entry in ('action1', 'action2'):
			#The Player activates some stuff
			self.action(int(entry[-1]));
	
	def move(self, direction):
		"""Initiate move in the specified direction."""
		
		if direction in ('down', 'left', 'right'):
			#(u, v) when going left
			self.make_move(direction);
		elif direction == 'up':
			#(u, v) when going up
			climb_state = self.can_climb();
			if climb_state > 0:
				#Ladder
				self.make_move('up');
				if climb_state == 1:
					self.make_move('up');
			elif self.can_jump():
				#Jump
				self.add_running_action('jump');
	
	def action(self, num):
		"""The Player wants to do an action. num is 1 for main action and 2 for secondary action."""
		if num == 1:
			#Main action
			self.env.disp_msg('Action 1', 'debug');
		elif num == 2:
			#Secondary action
			if not self.block_event('action', 'right'):
				if not self.block_event('action', 'down'):
					if not self.block_event('action', 'left'):
						self.block_event('action', 'up');
	
	def can_climb(self):
		"""Indicates whether the Player is on a ladder"""
		(um, vm) = self.dir_to_uv('right');
		(ut, vt) = self.dir_to_uv('down', 'right');
		
		if self.env.inch(self.y+um, self.x+vm) == 'H':
			#In middle of ladder
			return 1;
		elif self.env.inch(self.y+ut, self.x+vt) == 'H':
			#On top of ladder
			return 2;
		else:
			#Not on ladder
			return 0;
	
	def block_event(self, mode, direction):
		"""Acts according to the block the Player is coming into. This method is called by self.make_move (mode='make_move') or self.action (mode='action'). In the first case, returns True if further move is forbidden. In the second, returns True if an action is done, False otherwise."""
		(u, v) = self.dir_to_uv(direction);
		block = self.env.inch(u+self.y, v+self.x);
		
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
		elif mode == 'action':
			#Manual event, happens on trigger
			if block == 'G':
				#Gravity inversion
				self.env.disp_msg('Gravity inversion!', 'debug');
				self.weight *= -1;
				self.del_running_action('jump');
				return True;
			elif block in 'T<^v>':
				#The block is an Item.
				item = self.env.get_item_by_coordinates(self.y+u, self.x+v);
				if item is not None:
					item.touch(self);
					return True;
				return False;
			else:
				#No event happening
				return False;
		else:
			#No event happening
			return False;