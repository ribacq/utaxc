#!/bin/python3
# -*-coding:utf-8 -*
import curses;
from .Item import Item;
from .Player import Player;

"""A module containing the Sign class."""

class Sign(Item):
	"""The Sign class."""
	
	def __init__(self, env, y, x, text):
		"""Constructor"""
		super(Sign, self).__init__(env, y, x, 'T', 2);
		self.text = text;
	
	def touch(self, origin):
		"""The Sign has been touched. If it is by the Player, its text will be displayed."""
		if isinstance(origin, Player):
			self.env.disp_msg(self.text, 'npc');