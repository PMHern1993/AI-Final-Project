# import imp
import os
import random
from collections import Counter
import json
from datetime import datetime
from .game_state import GameState

class Game:

	def __init__(self):
		self.valid_guesses = None
		self.possible_answers = None
		self.word = "00000"
		self.turn = 0
		self.state = GameState.OK
		self.has_played_today = False
		self.fun_mode = False
		self.turn_history = list()
		self.replay = False
		self.today = datetime.strptime(datetime.today().strftime("%m/%d/%Y"), "%m/%d/%Y")

		self.setup()
	
	def open_dictionaries(self):
		with open("wordle\\resources\\answers-list.txt", "r") as f:
			self.possible_answers =  [word.strip() for word in f.readlines()]
		
		with open("wordle\\resources\\guesses-list.txt", "r") as f:
			self.valid_guesses = [word.strip() for word in f.readlines()]
	
	def open_scoreboard(self):
		if not os.path.exists("scoreboard.json"):
			with open("scoreboard.json", "w") as f:
				dummy_score = {"golf": [], "streak":0, "lastPlay": "01/01/1970"}
				json.dump(dummy_score, f)
		
		with open("scoreboard.json", "r") as f:
			obj = json.load(f)
			self.scoreboard = obj

	def select_word(self):
		self.word = random.choice(self.possible_answers)
	
	def setup(self):
		self.open_dictionaries()
		self.open_scoreboard()
		if not self.fun_mode:
			self.check_day()
			if not self.has_played_today:
				self.exit_fun_mode()
		self.select_word()
		random.seed()
		
	
	def enter_fun_mode(self):
		self.fun_mode = True
		random.seed()
	
	def exit_fun_mode(self):
		self.fun_mode = False
		self.check_day()
		seed = (self.today - datetime(1970, 1, 1)).total_seconds()
		random.seed(int(seed))
	
	def replay_word(self):
		self.fun_mode = True
		self.reset()
		self.replay = True
		self.check_day()
		seed = (self.today - datetime(1970, 1, 1)).total_seconds()
		random.seed(int(seed))
		self.select_word()

	
	def check_letters(self, guess):
		bits = list((0,0,0,0,0))
		for x, letter in enumerate(guess, start=0):
			if letter in self.word:
				bits[x] += 1
			if letter == self.word[x]:
				bits[x] += 1
		#remove extra letters from bits
		wc = Counter(self.word)
		gc = Counter(guess)
		for letter, count in gc.items():#goes over each unique letter
			if letter not in wc:
				continue
			if count <= wc[letter]:
				continue
			#if a letter appears more times
			#in the guess than in the chosen word
			extra = count - wc[letter]

			prev_index = 5
			while extra > 0:
				index = guess.rindex(letter, 0, prev_index)
				if bits[index] == 2:#dont remove a green letter
					prev_index -= 1
					continue
				bits[index] = 0
				prev_index = index
				extra -= 1

		return bits

	def check_guess(self, guess:str):
		if len(guess) != 5: #do nothing
			return GameState.TOO_FEW_LETTERS
			
		

		if guess not in self.valid_guesses:#print invalid msg and do nothing
			return GameState.INVALID_WORD
		
		#word is 5 letters long AND in dictionary
		bits = self.check_letters(guess)
		self.turn_history.append(bits)

		self.turn += 1

		

		if sum(bits) == 10:
			self.state = GameState.END_WIN
			self.save()
			return GameState.OK
		
		if self.turn == 6: #the game was lost
			self.state = GameState.END_LOSS
			self.save()
			return GameState.OK
		
		return self.state


	def save(self):
		if self.fun_mode:
			return


		scores = [-3, -2, -1, 0, 1, 2]

		if self.state == GameState.END_WIN:
			#print("Game won in", self.turn, "moves")
			self.scoreboard["golf"].append(scores[self.turn-1])
			self.scoreboard["streak"] += 1
		if self.state == GameState.END_LOSS:
			print("Game lost")
			self.scoreboard["golf"].append(4)
			self.scoreboard["streak"] = 0
		
		if len(self.scoreboard["golf"]) > 9:
			self.scoreboard["golf"] = self.scoreboard["golf"][-9:]
		
		if not self.fun_mode:
			self.scoreboard["lastPlay"] = self.today.strftime("%m/%d/%Y")
		
		with open("scoreboard.json", "w") as f:
			save_board = self.scoreboard
			if "score" in self.scoreboard:
				del save_board["score"]
			json.dump(save_board, f)
		
		
	def reset(self):
		self.check_day()
		self.turn_history = list()
		self.turn = 0
		self.state = GameState.OK
		if self.replay:
			self.enter_fun_mode()
		self.replay = False
		self.select_word()
	
	def check_day(self):
		last_play = self.scoreboard["lastPlay"]
		self.today = datetime.strptime(datetime.today().strftime("%m/%d/%Y"), "%m/%d/%Y")
		if self.today <= datetime.strptime(last_play, "%m/%d/%Y"):
				self.has_played_today = True

			
			


