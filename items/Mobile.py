#!/bin/python3
# -*-coding:utf-8 -*
import curses;
from .Item import Item;

"""A module containing the Mobile class"""

class Mobile(Item):
	"""The Mobile class: every Item with an ability to move"""
	
	def __init__(self, env, y, x, char, color_pair, weight):
		"""Constructor"""
		
		super(Mobile, self).__init__(env, y, x, char, color_pair);
		self.weight = weight;
		self.possible_running_actions.extend(['fall', 'jump']);
		self.jump_phase = 0;
		self.jump_height = 3;
	
	def move(self, direction):
		"""
		Moves and displays the Mobile in the game pad, in the specified direction.
		-----
		This method has to be implemented by each subclass.
		"""
		
		raise NotImplementedError('Item object has no move method.');
	
	def make_move(self, *directions):
		"""Moves the Mobile one cell in each of the specified directions, which must be 'up', 'down', 'left' or 'right'"""
		
		for direction in directions:
			(u, v) = self.dir_to_uv(direction);
			
			#Erase Mobile
			self.erase();
			
			#The mobile moves only if no event has occured which prevent it from moving (i.e. the move is done in block_event or is not possible).
			if not self.block_event('make_move', direction) and not self.collision(direction):
				self.y += u;
				self.x += v;
			
			#Replace Mobile if out of game pad
			(h, w) = self.env.game.getmaxyx();
			if self.y < 0:
				self.y = 0;
			if self.y > h-1:
				self.y = h-1;
			if self.x < 0:
				self.x = 0;
			if self.x > w-2:
				self.x = w-2;
			
			self.env.save.addnstr(0, 0, '(y='+str(self.y)+', x='+str(self.x)+')       ', 17);
	
	def dir_to_uv(self, *directions):
		"""Returns a (u, v) tuple with u and v of values -1, 0 or +1. directions elements must be 'up', 'down', 'left' or 'right'. Sign of u is modified according to that of self.weight"""
		
		(u, v) = super(Mobile, self).dir_to_uv(*directions);
		
		#Gravity influence
		if self.weight < 0:
			u *= -1;
		
		return (u, v);
	
	def collision(self, direction):
		"""Collision testing method. direction must be 'up', 'down', 'left' or 'right'. The tested cell is the one directly next to the Mobile"""
		
		#Move vector
		(u, v) = self.dir_to_uv(direction);
		
		#Character at tested cell
		char = self.env.inch(self.y+u, self.x+v);
		
		#Condition of collision
		if char not in ' $':
			return True;
		else:
			return False;
	
	def block_event(self, direction):
		"""Acts upon the block the Player is colliding into. This method is called by self.make_move. Returns True if further move is forbidden. --- This method has to be implemented by each subclass."""
		
		raise NotImplementedError('Item object has no block_event method.');
	
	def ra_fall(self):
		"""'fall' running action"""
		for i in range(abs(self.weight)):
			self.move('down');
	
	def can_jump(self):
		"""Indicates whether the Player is able to jump"""
		ret = self.collision('down');
		return ret;
	
	def ra_jump(self):
		"""'jump' running action"""
		if self.jump_phase < self.jump_height and not self.collision('up'):
			#First half: ascencion
			self.make_move('up', 'up');
			self.jump_phase += 1;
		elif self.collision('down') or self.collision('up'):
			#Second half: fall
			self.jump_phase = 0;
			self.del_running_action('jump');
