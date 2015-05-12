#!/bin/python
# -*-coding:utf-8 -*
import curses;
from Item import Item;

"""A module containing the Sign class."""

class Sign(Item):
	"""The Sign class."""
	
	def __init__(self, env, y, x, text):
		"""Constructor"""
		super(Sign, self).__init__(env, y, x, 'T', 2);
		self.text = text;
	
	def touch(self, origin):
		"""The Sign has been touched. Its text will be displayed."""
		self.env.disp_msg('Sign says: '+self.text);