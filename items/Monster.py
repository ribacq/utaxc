#!/bin/python3
# -*-coding:utf-8 -*
import curses;
from .Creature import Creature;
from random import choice;

"""A module containing the Monster class"""

class Monster(Creature):
	"""The Monster class"""
	
	def __init__(self, env, y, x, char):
		"""Constructor"""
		
		super(Monster, self).__init__(env, y, x, char, 7, 1);
		
		self.possible_running_actions.extend(['move']);
		self.add_running_action('move');
	
	def ra_move(self):
		"""Move running action for the monster"""
		self.move(choice(('left', 'right')));
