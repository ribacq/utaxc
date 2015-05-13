#!/bin/python3
# -*-coding:utf-8 -*
import curses;
import math;
from . import controls;

"""A module containing the Environment class"""

class Environment:
	"""The Environment class"""
	
	def __init__(self, scr, frames_color):
		"""Constructor"""
		
		#Window and pads
		self.scr = scr;
		self.scr.scrollok(1);
		self.game = curses.newpad(15, 81);
		self.game.scrollok(1);
		self.text = curses.newpad(2, 81);
		self.text.scrollok(1);
		self.side = curses.newpad(15, 17);
		self.side.scrollok(1);
		self.save = curses.newpad(2, 17);
		self.save.scrollok(1);
		
		#Frames color
		self.frames_color = frames_color;
		
		#List of all Items
		self.items = [];
		
		#Status variables
		self.msg_i = 1;
	
	def draw_frames(self):
		#Frames
		bord = '+' + '-'*80 + '+' + '-'*17 + '+';
		self.scr.addstr(0, 0, bord, curses.color_pair(self.frames_color));
		for i in range(1, 19):
			self.scr.addstr(i,0, '|', curses.color_pair(self.frames_color));
			self.scr.addstr(i,81, '|', curses.color_pair(self.frames_color));
			self.scr.addstr(i,99, '|', curses.color_pair(self.frames_color));
		self.scr.addstr(16,0, bord, curses.color_pair(self.frames_color));
		self.scr.addstr(19,0, bord, curses.color_pair(self.frames_color));
		self.refresh();
	
	def refresh(self):
		"""Refreshes the window and the four pads, displays the Items."""
		
		#Items
		for item in self.items:
			item.display();
		
		#Windows and pads
		self.scr.noutrefresh();
		self.game.noutrefresh(0,0, 1,1, 15,80);
		self.text.noutrefresh(0,0, 17,1, 18,80);
		self.side.noutrefresh(0,0, 1,82, 15,98);
		self.save.noutrefresh(0,0, 17,82, 18,98);
		curses.doupdate();
	
	def disp_msg(self, msg, style):
		"""Displays a message in the text pad. msg is the message to be displayed, style can be 'debug' or 'npc'. 'debug' numbers the messages and does not block the user, whereas 'npc' is an RPG-like message."""
		if style == 'npc':
			#npc: multiline (lines are automatically cut), pause before each scroll, text pad erased before and after display.
			self.text.erase();
			
			#0: top line of text pad is being used; 1: bottom line
			prints_on = 0;
			
			#If passed message is a string, it is converted into a list.
			if isinstance(msg, str):
				msg = [msg];
			
			#cut lines at 79 characters and removes trailing new lines.
			lines = [line[0:79].strip('\r\n') for line in msg];
			
			for line in lines:
				#Displays message and 'v' prompt
				self.text.addstr(prints_on, 0, line);
				self.text.addstr(1, 79, chr(controls.ctrlsPlayer['action2']), curses.color_pair(2));
				self.refresh();
				
				#Prompt
				entry = '';
				while entry != controls.ctrlsPlayer['action2'] and (prints_on == 1 or len(lines) == 1):
					entry = self.getch();
				
				#Scrolling and line choice
				if prints_on == 0:
					prints_on = 1;
				else:
					self.text.scroll();
					self.text.addstr(0, 79, ' ');
			
			self.text.erase();
		elif style == 'debug':
			#debug: one line, no pause, messages showed after scrolling.
			msg = msg.strip('\r\n');
			self.text.scroll();
			self.text.addstr(1, 0, '00');
			self.text.addnstr(1, 2-int(math.log(self.msg_i, 10)), str(self.msg_i)+'> '+msg, 80);
			if self.msg_i == 999:
				self.msg_i = 1;
			else:
				self.msg_i += 1;
	
	def add_item(self, item):
		"""A new Item is created."""
		self.items.append(item);
	
	def get_item_by_coordinates(self, y, x):
		"""Returns the Item at given coordinates, None if there is not one."""
		for item in self.items:
			if item.y == y and item.x == x:
				return item;
		
		return None;
	
	def exec_running_actions(self):
		"""Executes the running actions for every item."""
		for item in self.items:
			item.exec_running_actions();
	
	def pause(self):
		"""Pauses the game. This has to be improved."""
		self.disp_msg('Pause...', 'npc');
	
	def getch(self):
		"""A getch equivalent working with the halfdelay mode. The return value is of type int."""
		try:
			return self.scr.getch();
		except Exception:
			return '';
	
	def inch(self, y, x):
		"""A inch equivalent in the game pad"""
		return chr(self.game.inch(y, x) & 0xFF);
