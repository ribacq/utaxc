#!/bin/python3
# -*-coding:utf-8 -*
import curses;

"""A module containing the Item class"""

class Item(object):
	"""The Item class"""
	
	def __init__(self, env, y, x, char, color_pair):
		"""Constructor"""
		
		self.env = env;
		self.env.add_item(self);
		self.y = y;
		self.x = x;
		self.char = char;
		self.color_pair = color_pair;
		self.running_actions = [];
		self.possible_running_actions = [];
	
	def erase(self):
		"""Erases the Item form the gamepad."""
		
		self.env.game.addstr(self.y, self.x, ' ', curses.color_pair(self.color_pair));
	
	def display(self):
		"""Displays the Item --- This method has to be implemented by each subclass."""
		
		self.env.game.addstr(self.y, self.x, self.char, curses.color_pair(self.color_pair));
	
	def dir_to_uv(self, *directions):
		"""Returns a (u, v) tuple with u and v of values -1, 0 or +1. directions elements must be 'up', 'down', 'left' or 'right'."""
		
		(u, v) = (0, 0);
		
		for direction in directions:
			if direction == 'left':
				#(u, v) when going left
				v -= 1;
			elif direction == 'up':
				#(u, v) when going up
				u -= 1;
			elif direction == 'down':
				#(u, v) when going down
				u += 1;
			elif direction == 'right':
				#(u, v) when going right
				v += 1;
		
		return (u, v);
	
	def touch(self, origin):
		"""The Item has been touched by Item called origin."""
		
		raise NotImplementedError('Item object has no touch method.');
	
	def add_running_action(self, name):
		"""Adds a running action"""
		
		#If the given name is a valid running action of the Item
		if name in self.possible_running_actions and name not in self.running_actions:
			self.running_actions.append(name);
	
	def del_running_action(self, name):
		"""Deletes a running_action"""
		
		try:
			self.running_actions.remove(name);
		except ValueError:
			pass;
	
	def exec_running_actions(self):
		"""Executes the running actions"""
		
		for name in self.running_actions:
			self.env.save.addnstr(1, 0, name+' '*42, 16);
			if 'ra_'+name in self.__class__.__dict__:
				#Search it in self
				self.__class__.__dict__['ra_'+name](self);
			elif 'ra_'+name in self.__class__.__bases__[0].__dict__:
				#Search it in parent class
				self.__class__.__bases__[0].__dict__['ra_'+name](self);
