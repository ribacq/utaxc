#!/bin/python
# -*-coding:utf-8 -*
import curses;
import items;

"""A module containing the Level class"""

class Level(object):
	"""The Level class"""
	
	def __init__(self, env, name):
		"""Constructor"""
		
		self.env = env;
		self.name = name;
		self.lines = [];
		with open('./data/levels/'+self.name+'.lvl', 'r') as f:
			self.lines = [line[0:80] for line in f];
	
	def load(self):
		"""Displays the level on screen"""
		
		#List of characters used to create an Item
		todo = [];
		
		#Line by line read of the level
		for i in range(15):
			for j in range(len(self.lines[i])):
				char = self.lines[i][j];
				if char in '#':
					#Standard block
					self.env.game.addstr(i, j, '#', curses.color_pair(5));
				elif char in '$':
					#Treasure block
					self.env.game.addstr(i, j, '$', curses.color_pair(6));
				elif char in 'HG':
					#Movement block
					self.env.game.addstr(i, j, char, curses.color_pair(1));
				elif char in 'T@':
					#Characters that will lead to the creation of an Item
					todo.append(char);
		
		#Extra info at the bottom
		for i in range(15, len(self.lines)):
			line = self.lines[i];
			line = line.strip('\r\n');
			if line[0] in todo:
				#The character has been read in the level
				if line[0] == 'T':
					#Sign Item to be created
					#Line format: '? y|x|Text'
					sign_info = line[2:].split('|');
					items.Sign(self.env, int(sign_info[0]), int(sign_info[1]), sign_info[2]);
				elif line[0] == '@':
					#Teleport Item to be created
					#Line format: '@ from_y|from_x|  |dest_y|dest_x|  |exit_direction'
					teleport_info = line[2:].split('|');
					items.Teleport(self.env, int(teleport_info[0]), int(teleport_info[1]), int(teleport_info[3]), int(teleport_info[4]), teleport_info[6]);
				todo.remove(line[0]);
			elif line[0] == '.':
				#A message is displayed
				self.env.disp_msg(line[2:]);