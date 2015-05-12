#!/bin/python
# -*-coding:utf-8 -*
import curses;
from Item import Item;

"""A module containing the Teleport class."""

class Teleport(Item):
	"""The Teleport class."""
	
	def __init__(self, env, from_y, from_x, dest_y, dest_x, exit_direction):
		"""Constructor"""
		super(Teleport, self).__init__(env, from_y, from_x, '@', 1);
		self.dest_y = dest_y;
		self.dest_x = dest_x;
		self.exit_direction = exit_direction;
	
	def touch(self, origin):
		"""The Teleport has been touched. The one who touched it will be moved."""
		
		self.env.disp_msg('@ ('+str(self.y)+', '+str(self.x)+')');
		
		dest = self.env.get_item_by_coordinates(self.dest_y, self.dest_x);
		if isinstance(dest, Teleport):
			#The destination Teleport exists
			(u, v) = self.dir_to_uv(dest.exit_direction);
			origin.erase();
			origin.y = dest.y+u;
			origin.x = dest.x+v;