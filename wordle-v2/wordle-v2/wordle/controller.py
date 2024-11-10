from pygame.locals import QUIT, K_BACKSPACE, K_RETURN
from pygame.time import Clock
import pygame

import os
import pygame_menu
import pyperclip
import win10toast

from .button import SideViewButton, OptionsButton
from .util import get_theme
from .card import Card
from .key import Key
from .sideview import SideView
from .colors import *
from .game import Game
from .game_state import GameState
from .lockout_view import Lockout




class Controller:

	font:pygame.font.Font = pygame.font.SysFont("System1", 40)

	def __init__(self, fun_mode=False):
		#instance setup
		self.size = (400, 600)

		self.game = Game()
		self.buffer = ""
		self.show_word = False

		
		self.sideview_button = SideViewButton((self.size[0] - 25, 0), (25, 25))
		self.sideview_button.set_action(self.button_click, pygame.MOUSEBUTTONDOWN)

		self.options_button = OptionsButton((0,0), (25,25))
		self.options_button.set_action(self.clicked_option_button, pygame.MOUSEBUTTONDOWN)

		self.lockout_view = Lockout(size=self.size)

		self.toaster = win10toast.ToastNotifier()

		#pygame setup
		self.window = pygame.display.set_mode(self.size)
		pygame.display.set_caption("Le-Word")
		if os.path.exists("wordle\\resources\\icon.ico"):
			icon = pygame.Surface.convert(pygame.image.load("wordle\\resources\\icon.ico"))
			pygame.display.set_icon(icon)
		self.grid:list[list[Card]] = self.make_cards()
		self.keys:list[list[Key]] = self.make_keys()
		self.key_color_map = {letter:-1 for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
		self.should_prompt_invalid = False
		self.invalid_word_prompt = self.font.render("Invalid word", True, WHITE)
		self.word_prompt = self.font.render("Correct word: " + self.game.word, True, WHITE)
		self.sideview = SideView((700 - 400, self.size[1]))
		self.sideview.share_button.set_action(self.share, pygame.MOUSEBUTTONDOWN)
		self.sideview.is_in_fun_mode = self.game.fun_mode

		self.menu = None
		self.get_menu()
	

	def make_cards(self):
		rows = list()
		for y in range(6):
			row = list()
			for x in range(5):
				card = Card()
				coord = (x*(card.size[0] + 10) + 30, y*(card.size[1] + 10) + 30)
				card.set_pos(coord)
				row.append(card)
			rows.append(row)
		return rows
	
	def draw_cards(self):
		for row in self.grid:
			for card in row:
				card.draw(self.window)
				  
	def make_input_keys(self):
		w, _ = Key.font.size("Back")
		back_key = Key("Back", (w + 10, 40))
		w, _ = Key.font.size("Enter")
		enter_key = Key("Enter", (w + 10, 40))
		return (back_key, enter_key)			 
	
	def make_keys(self):
		back_key, enter_key = self.make_input_keys()
		letters = ["QWERTYUIOP", "ASDFGHJKL", "^ZXCVBNM$"]
		keys:list[list[Key]] = list()
		offset = 0
		for y, row in enumerate(letters, start=0):
			row_keys = list()
			offset += 10
			if y == 2:#if last row, reset offset
				offset = 10
			for x, letter in enumerate(row, start=0):
				key = Key(letter)
				if y == 2 and x != 0:#for all keys in the last row, except the first one
					x -= 1
				coord = ((x*(key.size[0] + 5)) + 15 + offset,
						(y*(key.size[1] + 5)) + 450)
				if letter == "^":#if enter_key
					offset += enter_key.size[0] + 5#add size of button to offset
					enter_key.set_pos(coord)#update key with pos
					continue#dont append this filler to the key list
				if letter == "$":#if back_key
					offset += back_key.size[0] + 5#add size of button to offset
					back_key.set_pos(coord)#update key with pos
					continue#dont append this filler to the key list
				key.set_pos(coord)#add (non-filler) key to list for row
				row_keys.append(key)#add keys in row to list of rows
			keys.append(row_keys)
		
		#this order doesnt matter bc draw position is set by the postion set above
		keys[1].append(back_key)
		keys[2].append(enter_key)

		return keys

	def draw_keyboard(self):
		for row in self.keys:
			for key in row:
				key.draw(self.window)
	
	def get_menu(self):
		self.menu = pygame_menu.Menu("Options", 300, 500, enabled=False, theme=get_theme())
		if not self.game.fun_mode:
			self.menu.add.button("Enter Fun Mode", action=self.enter_fun_mode)
		else:
			if self.game.has_played_today:
				self.menu.add.button("Replay", action=self.replay_word)
			self.menu.add.button("Skip word", action=self.reset)
			self.menu.add.button("Exit Fun Mode", action=self.exit_fun_mode)
		
		self.menu.add.button("Close", action=self.menu.disable)
	
	def retract(self):
		self.size = (400,600)
		self.window = pygame.display.set_mode(self.size)
		if self.sideview_button.state:
			self.sideview_button.state = 0
		
	
	def extend(self):
		self.size = (700,600)
		self.window = pygame.display.set_mode(self.size)
		if not self.sideview_button.state:
			self.sideview_button.state = 1
		
	
	def clicked_option_button(self):
		self.retract()
		self.get_menu()
		self.menu.enable()

	def enter_fun_mode(self):
		self.sideview.is_in_fun_mode = True
		self.game.enter_fun_mode()
		self.reset()
	
	def exit_fun_mode(self):
		self.sideview.is_in_fun_mode = False
		self.game.exit_fun_mode()
		self.reset()
	
	def replay_word(self):
		self.reset()
		self.game.replay_word()
		self.word_prompt = self.font.render("Correct word: " + self.game.word, True, WHITE)

	def clear(self):
		self.window.fill(BLACK)
	

	def push_buffer(self, char:str):#
		if len(self.buffer) < 5: #if fewer than 5 chars in buffer
			self.buffer += char #add char to buffer
			buff_len = len(self.buffer) - 1 #the card index to edit
			#self.grid[self.turn][buff_len].clear() #clear prev text on card
			self.grid[self.game.turn][buff_len].set_text(self.buffer[-1]) #set new text on card
	

	def pop_buffer(self):#
		if len(self.buffer) > 0: #if more than 0 chars in buffer
			buff_len = len(self.buffer) - 1 #the card index to edit
			#self.grid[self.turn][buff_len].clear() #clear prev text on card
			self.grid[self.game.turn][buff_len].set_text("") #set text to nothing
			self.buffer = self.buffer[:-1] #remove last char from buffer


	def color_cards(self, bits:list):
		for i, bit in enumerate(bits, start=0):
			letter = self.buffer[i]
			self.grid[self.game.turn-1][i].used = True
			self.grid[self.game.turn-1][i].set_state(bit)
			if bit == 0:
				#self.grid[self.turn][i].fill(GRAY)
				self.key_color_map[letter.upper()] = max(self.key_color_map[letter], 0)

			if bit == 1:
				#self.grid[self.turn][i].set_state(bit)
				self.key_color_map[letter.upper()] = max(self.key_color_map[letter], 1)
			
			if bit == 2:
				#self.grid[self.turn][i].set_state(bit)
				self.key_color_map[letter.upper()] = max(self.key_color_map[letter], 2)
	
		
	def color_keys(self):
		for row in self.keys:
			for key in row:
				if len(key.letter) > 1:
					continue

				if self.key_color_map[key.letter] == -1:
					key.bg_color = GRAY
					key.text_color = WHITE
				
				if self.key_color_map[key.letter] == 0:
					key.bg_color = BLACK
					key.text_color = GRAY
				
				if self.key_color_map[key.letter] == 1:
					key.bg_color = YELLOW
				
				if self.key_color_map[key.letter] == 2:
					key.bg_color = GREEN
	

	def update_sideview(self):
		sideview_scoreboard = self.game.scoreboard
		sideview_scoreboard["score"] = [-3, -2, -1, 0, 1, 2, 4][self.game.turn]
		if self.game.state == GameState.END_WIN:
			sideview_scoreboard["score"] = [-3, -2, -1, 0, 1, 2, 4][self.game.turn-1]
		self.sideview.scoreboard = sideview_scoreboard

	def get_share_text(self):
		share_text = ""
		for turn in self.game.turn_history:
			for bit in turn:
				
				if bit == 0:
					share_text += "."
				if bit == 1:
					share_text += "o"
				if bit == 2:
					share_text += "x"
			share_text += "\n"
		return share_text

	def share(self):
		share_text = self.get_share_text()
		pyperclip.copy(share_text)
		if os.path.exists("wordle\\resources\\icon.ico"):
			self.toaster.show_toast("Le-Word", "Results copied to clipboard!", "wordle\\resources\\icon.ico", threaded=True)
		else:
			self.toaster.show_toast("Le-Word", "Results copied to clipboard!", threaded=True)
		
		
	
	def button_click(self):
		self.sideview_button.set_state(1 if self.sideview_button.state == 0 else 0)
		#self.show_sideview = not self.show_sideview
		if self.sideview_button.state == 1:			
			self.extend()
		if self.sideview_button.state == 0:
			self.retract()
		#print(self.sideview_button.state)

	
	def draw(self):
		self.clear()
		self.draw_cards()
		self.draw_keyboard()
		self.sideview_button.draw(self.window)
		self.options_button.draw(self.window)

		if self.sideview_button.state == 1:#should show sideview on state 1
			self.update_sideview()
			self.sideview.draw(self.window)

		if self.sideview.game_ended:#display correct word on win/loss
			self.window.blit(self.word_prompt, (30,0))

		if self.should_prompt_invalid:
			self.window.blit(self.invalid_word_prompt, (30,0))
		
		if self.menu.is_enabled():
			self.menu.draw(self.window)
			self.menu.update(pygame.event.get())
		

		pygame.display.update()
	
	def reset(self):
		for row in self.grid:
			for card in row:
				card.reset()
		self.buffer = ""
		self.game.reset()
		self.key_color_map = {letter:-1 for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
		self.color_keys()
		self.sideview.game_ended = False
		self.show_word = False
		self.word_prompt = self.font.render("Correct word: " + self.game.word, True, WHITE)
		self.menu.disable()
		if os.path.exists("wordle\\resources\\icon.ico"):
			icon = pygame.Surface.convert(pygame.image.load("wordle\\resources\\icon.ico"))
			pygame.display.set_icon(icon)

	def handle_click(self, event:pygame.event.Event):

		pos = event.pos
		x, y = pos

		#was click in the sideview
		if x > 400:
			self.sideview.handle_click(event, (400,0))

		#check for sideview button click
		rect = pygame.Rect(*self.sideview_button.pos, *self.sideview_button.size)
		#print((*self.sideview_button.pos, *self.sideview_button.size), (*rect.topleft, *rect.size))
		if rect.collidepoint(x,y):
			#print("Should click")
			self.sideview_button.handle_event(event)
		
		rect = pygame.Rect(*self.options_button.pos, *self.options_button.size)
		if rect.collidepoint(x,y):
			self.options_button.handle_event(event)


		#if nothing triggers in the above code, then this click
		#is extraneous unless it is low enough to be for the keyboard
		if y < 440:
			return
		
		#did a key get clicked
		for row in self.keys:
			for key in row:
				rect = pygame.Rect(*key.pos, *key.size)
				if rect.collidepoint(*pos):
					if key.letter == "Back":
						self.backspace()
						return
					
					if key.letter == "Enter":
						self.enter()
						return
					
					self.push_buffer(key.letter)
		
	def display_lockout(self):
		if self.size[0] > 400:
			self.retract()
			self.sideview_button.state = 0

		self.lockout_view.draw(self.window)
	
	def backspace(self):
		self.pop_buffer()
		if self.should_prompt_invalid:
			self.should_prompt_invalid = False
		
	def enter(self):
		if (self.game.state & GameState.ENDED):
			self.reset()
			return

		if self.game.state == GameState.OK:
			guess = self.buffer.lower()
			state = self.game.check_guess(guess)

			if state == GameState.TOO_FEW_LETTERS:
				pass#do nothing
			
			if state == GameState.INVALID_WORD:
				self.should_prompt_invalid = True	
							
			if state == GameState.OK:
				self.color_cards(self.game.turn_history[-1])
				self.color_keys()
				self.buffer = ""
			
			if self.game.state & GameState.ENDED:#if the game ended bc of the previous guess
				self.sideview.game_ended = True
				self.show_word = True

			
			return

		
	
	def handle_event(self, event:pygame.event.Event):
		if event.type == pygame.KEYDOWN:			
			if event.key == K_BACKSPACE:
				self.backspace()
				return
				

			if event.key == K_RETURN:
				self.enter()
					
			if "a" <= event.unicode <= "z":
				self.push_buffer(event.unicode.upper())
					
		if event.type == pygame.MOUSEBUTTONDOWN:
			#print(event.pos)
			self.handle_click(event)
			return

	
	def run(self):
		clock = Clock()
		


		play = True
		while play:
			
			clock.tick(60)
			if pygame.event.peek(pygame.QUIT):
				play = False
				break

			if self.game.has_played_today and not self.game.fun_mode:
				self.display_lockout()
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_TAB:
							self.sideview.is_in_fun_mode = True
							self.game.enter_fun_mode()
							self.reset()
					if event.type == QUIT:
						play = False
				continue


			
			self.draw()
			

			for event in pygame.event.get():
				self.handle_event(event)

#--------------------------------------------------------------------------------------------#				
	def run_auto(self, guesses):
        # Run the game with a list of automated guesses.
        # Args:
        #    guesses (list): A list of words guessed by the GA.
        # Returns:
        #    score (int): A score based on performance, e.g., the number of attempts needed.
        
		self.reset()  # Reset the game state for each new solution
		score = 0
		for guess in guesses:
			result = self.make_guess(guess)
			score += 1
			if result == "correct":  # Assuming this is the result when guessed correctly
				break
			
		return score
#--------------------------------------------------------------------------------------------#
				

