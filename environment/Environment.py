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
		self.side = curses.newpad(15, 17);
		self.side.scrollok(1);
		self.text = curses.newpad(3, 81);
		self.text.scrollok(1);
		self.save = curses.newpad(3, 17);
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
		for i in range(1, 20):
			self.scr.addstr(i,0, '|', curses.color_pair(self.frames_color));
			self.scr.addstr(i,81, '|', curses.color_pair(self.frames_color));
			self.scr.addstr(i,99, '|', curses.color_pair(self.frames_color));
		self.scr.addstr(16,0, bord, curses.color_pair(self.frames_color));
		self.scr.addstr(20,0, bord, curses.color_pair(self.frames_color));
		self.refresh();
	
	def refresh(self):
		"""Refreshes the window and the four pads, displays the Items."""
		
		#Items
		for item in self.items:
			item.display();
		
		#Windows and pads
		self.scr.noutrefresh();
		self.game.noutrefresh(0,0, 1,1, 15,80);
		self.side.noutrefresh(0,0, 1,82, 15,98);
		self.text.noutrefresh(0,0, 17,1, 19,80);
		self.save.noutrefresh(0,0, 17,82, 19,98);
		curses.doupdate();
	
	def disp_msg(self, msg, style):
		"""Displays a message in the text pad. msg is the message to be displayed, style can be 'debug' or 'npc'. 'debug' numbers the messages and does not block the user, whereas 'npc' is an RPG-like message."""
		if style == 'npc':
			#npc: multiline (lines are automatically cut), pause before each scroll, text pad erased before and after display.
			self.text.erase();
			
			#Last line is being used.
			last = False;
			
			#If passed message is a string, it is converted into a list of (txt, attr) tuples.
			if isinstance(msg, str):
				msg = [(msg, '')];
			
			for i, (txt, attr) in enumerate(msg):
				#txt is the text to display, attr are the attributes
				#attr format: 'c,s', where c is a color_pair number (int) and s a character that can be ommited or be, 'b' for 'bold' and 'r' for 'reverse'.
				
				#Text is cut at 79 characters.
				txt = txt[0:79];
				
				#Attribute reading
				used_attr = curses.color_pair(0);
				attr = attr.split(',');
				if attr[0].isnumeric():
					#Color
					used_attr = curses.color_pair(int(attr[0]));
					del attr[0];
				
				if len(attr) > 0:
					#Bold or reverse
					if attr[0] == 'b':
						used_attr = used_attr | curses.A_BOLD;
					elif attr[0] == 'r':
						used_attr = used_attr | curses.A_REVERSE;
				
				#Displays message if the text is not a newline on the second line. If it's a newline on the first line, it is not displayed and its value is changed to '' (empty string);
				if txt != '\n' or not last:
					self.text.addstr(txt, used_attr);
					if txt == '\n' and not last:
						txt = '';
				
				last = bool(self.text.getyx()[0] == 2);
				
				#Prompt if the message is fully displayed, or the two lines have been used.
				if i == len(msg)-1 or (txt == '\n' and last):
					last = False;
					self.text.addstr(2, 79, chr(controls.ctrlsPlayer['action1']), curses.color_pair(2));
					self.refresh();
					entry = '';
					while entry != controls.ctrlsPlayer['action1']:
						entry = self.getch();
					self.text.erase();
			
			self.text.erase();
		elif style == 'debug':
			#debug: one line, no pause, messages showed after scrolling.
			msg = msg.strip('\r\n');
			self.text.scroll();
			self.text.addstr(2, 0, '00');
			self.text.addnstr(2, 2-int(math.log(self.msg_i, 10)), str(self.msg_i)+'> '+msg, 80);
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
