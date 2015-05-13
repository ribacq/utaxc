#!/bin/python3
# -*-coding:utf-8 -*
import curses;
import os;
import items;

"""A module containing the Level class"""

class Level(object):
	"""The Level class"""
	
	def __init__(self, env, name):
		"""Constructor"""
		
		#Environment instance
		self.env = env;
		
		#Level name
		self.name = name;
		
		#Initial Player coordinates
		self.player_y = 13;
		self.player_x = 0;
		
		#Absolute directory path in which the level (.lvl) files are
		levels_path = os.environ['HOME']+'/Documents/Python/utaxc/data/levels/';
		
		#Lines from the level file
		self.lines = [];
		with open(levels_path+self.name+'.lvl', 'r') as f:
			self.lines = [line.strip('\r\n') for line in f];
			self.lines = [line[0:80] for line in self.lines if len(line) > 0];
	
	def load(self):
		"""Displays the level on screen and creates Items present in it."""
		
		#List of characters used to create an Item
		todo = [];
		
		#Line by line read of the level
		for i in range(15):
			for j in range(len(self.lines[i])):
				char = self.lines[i][j];
				if char == 'I':
					#Player starting point
					self.player_y = i;
					self.player_x = j;
				elif char in '#':
					#Standard block
					self.env.game.addstr(i, j, '#', curses.color_pair(5));
				elif char in '$':
					#Treasure block
					self.env.game.addstr(i, j, '$', curses.color_pair(6));
				elif char in 'HG':
					#Movement block
					self.env.game.addstr(i, j, char, curses.color_pair(1));
				elif char in 'T<^v>':
					#Characters that will lead to the creation of an Item
					todo.append(char);
		
		#Extra info at the bottom
		#The declarations use several lines.
		#The current* variables are used to store temporary data in this case.
		current_class = None.__class__;
		current_info = [];
		welcome_msg = [];
		for i in range(15, len(self.lines)):
			line = self.lines[i];
			line = line.strip('\r\n');
			if line[0] in todo:
				#The character has been read in the level
				if line[0] == 'T':
					#Sign Item to be created
					#Format:
					#T y|x
					#T |Line 1
					#T |Line 2
					#T |...
					#T endsign
					
					linespt = line[2:].split('|');
					if current_class is None.__class__:
						#The Sign begins, getting the coordinates from the first line.
						current_info = [int(linespt[0]), int(linespt[1])];
						current_class = items.Sign.__class__;
					else:
						#The Sign has already begun, text will be added or the sign will end.
						if linespt[0] == '':
							#Text is added.
							current_info.append(linespt[1]);
						else:
							#End of sign declaration, creation of the Sign instance
							items.Sign(self.env, current_info[0], current_info[1], current_info[2:]);
							current_info = [];
							current_class = None.__class__;
							todo.remove(line[0]);
				elif line[0] in '<^v>':
					#Teleport Item to be created
					#Line format: 'd from_y|from_x|  |dest_y|dest_x', with d a character in '<^v>'
					if line[0] == '^':
						exit_direction = 'up';
					elif line[0] == 'v':
						exit_direction = 'down';
					elif line[0] == '<':
						exit_direction = 'left';
					elif line[0] == '>':
						exit_direction = 'right';
					
					current_info = line[2:].split('|');
					items.Teleport(self.env, int(current_info[0]), int(current_info[1]), int(current_info[3]), int(current_info[4]), exit_direction);
					todo.remove(line[0]);
			elif line[0] == '.':
				#Welcome message for the level.
				welcome_msg.append(line[2:]);
		
		self.env.disp_msg(welcome_msg, 'npc');