# import imp
import os
import random
from collections import Counter
import json
from datetime import datetime
from .game_state import GameState

import numpy as np
import time
import matplotlib.pyplot as plt

import seaborn as sns  # For heatmaps

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
		
		# Instance of word is created her, we can run genetic algorithm here as well
		GREEN = '\033[92m'   # Correct letter in the correct position
		YELLOW = '\033[93m'  # Correct letter but in the wrong position
		RESET = '\033[0m'    # Reset color

		#ga_result, fitness = self.play_wordle_with_ga()
		#print(f"Resulting GA guess: {ga_result}")
		#print(f"Actual word: {self.word}")
		self.correctguesses = 0
		self.wordVault = []
		self.finalPercent = 0
		self.popSize = 0
		self.genSize = 0
		self.mutationRate = 0
		self.wisdomOfCrowds()
		print(f"The word was: {self.word}")
		print(f"The num of times the word was found during GA was: {self.correctguesses}")
		print(f"The best guesses from each generation: {self.wordVault}")
	
		
	
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

###############																											     #############
############### Everything below here is part of my attempt to translate Tyler's GA/WoC to Cristie's currently existing game ############# 
###############																												 #############
			
	def genetic_algorithm(self, population_size=90, generations=100, mutation_rate=0.2):
		population = self.initialize_population(population_size)
		self.popSize = population_size       # Establishing variables for data output
		self.genSize = generations			 # -
		self.mutationRate = mutation_rate	 # -
		for generation in range(generations):
			fitness_scores = [self.calculate_fitness(word) for word in population]
			if self.word in population:
				print(f"GA found the target word in generation {generation}!")
				self.correctguesses += 1
				return self.word
		
			new_population = []
			for _ in range(population_size // 2):
				parent1, parent2 = self.select_parents(population, fitness_scores)
				child1 = self.crossover(parent1, parent2)	
				child1 = self.mutate(child1, mutation_rate)

				child2 = self.crossover(parent2, parent1)
				child2 = self.mutate(child2, mutation_rate)
				new_population.extend([child1, child2])
		
			population = new_population
			best_guess = max(population, key=self.calculate_fitness)
			best_fitness = self.calculate_fitness(best_guess)
		print(f"GA - Generation {generation}: Best Guess '{best_guess}' with Fitness {best_fitness}")

		self.wordVault.append(best_guess)
		# if(best_guess == self.word):
		# 	self.correctguesses += 1
		print(f"Found in generation {generation}\nGA Finished - Best Guess:(hidden)")
		return best_guess
			
	#Added self as argument to access valid_guesses
	def initialize_population(self, size):
		return [random.choice(self.valid_guesses) for _ in range(size)]
			
	def calculate_fitness(self, guess):
		fitness = 0

		#print(type(self.word), self.word)
		#print(f"Type of guess: {type(guess)}")
		for i in range(len(self.word)):
			if guess[i] == self.word[i]:
				fitness += 2
			elif guess[i] in self.word:
				fitness += 1
		if guess == self.word:
			fitness += 3
		return fitness
	
	def select_parents(self, population, fitness_scores):
		# Selects 2 parents via probability
    	# Higher probability (fitness) --> more likely to be selected
		return random.choices(population, weights=fitness_scores, k=2)
	
	def crossover(self, parent1, parent2):
		child = ""
		# random.random() returns a value in the range [0, 1)
		for i in range(len(parent1)):
			child += parent1[i] if random.random() < 0.5 else parent2[i]
		return child
	
	def mutate(self, word, mutation_rate=0.1):
		word_as_list = list(word)
		for i in range(len(word_as_list)):
			if random.random() < mutation_rate:
				word_as_list[i] = random.choice("abcdefghijklmnopqrstuvwxyz")
		return ''.join(word_as_list)

	def play_wordle_with_ga(self):
		print("Ga is starting...")
		ga_result = self.genetic_algorithm()
		
		fitness = self.calculate_fitness(ga_result)

		return ga_result, fitness
	
	def wisdomOfCrowds(self):
		crowd_size = 5
		crowd_data = {}
		experts = [f'exper_{i}' for i in range(1, crowd_size + 1)] # each will run the GA separately
		ga_runs = [f'run_{i}' for i in range(1, 11)] # Used to obtain variability
		for expert in experts:
			crowd_data[expert] = {'runs': {}}

		agreement_matrices = {run: np.zeros((5, 26), dtype=int) for run in ga_runs}
		num = 1


		fitness_over_time = []
		for expert in experts:
			print(f"Starting GA runs for {expert}")

			for run in ga_runs:
				start_time = time.time()
				print(f"\tStarting {run} for {expert}")
				ga_result, fitness = self.play_wordle_with_ga()

				end_time = time.time()

				crowd_data[expert]['runs'][run] = {
            		'execution_time': end_time - start_time,
            		'best_solution': ga_result,
            		'solution_fitness': fitness,
            		'ga_instance': f'ga_instance_{num}'
        		}
				num += 1

				fitness_over_time.append(fitness)

				for i, letter in enumerate(ga_result):
					column_index = ord(letter) - ord('a')
					agreement_matrices[run][i][column_index] += 1
				
			print("Agreement matrix for run_1:")
			print(agreement_matrices['run_1'])

		consensus_solutions = {}
		run_num = 1
		for run in ga_runs:
			consensus_solution = self.consensusSolution(agreement_matrices, f"run_{run_num}")
			consensus_solutions[f"run_{run_num}"] = consensus_solution
			run_num += 1
		
		print(f"The consensus solution is...: {consensus_solutions}")
		
		for run_num, consensus_solution in consensus_solutions.items():
			if consensus_solution == self.word:
				self.finalPercent += 1

		self.finalPercent = (self.finalPercent / 10) * 100 #Finding % correct solutions in matrix
		self.heatPlot(agreement_matrices['run_1'])
		#self.fitnessPlot(fitness_over_time)

	def consensusSolution(self, agreement_matrices, run):
		agreement_matrix = agreement_matrices[run]
		num_positions = agreement_matrix.shape[0]
		consensus_solution = ""
		
		# For each position in the 5-letter word, find the letter with the highest frequency
		for position in range(num_positions):
			# Find the letter with the highest frequency in the current position
			letter_index = np.argmax(agreement_matrix[position]) # Column with the highest value for this row
			consensus_letter = chr(letter_index + ord('a'))      # Convert index to corresponding letter
			consensus_solution += consensus_letter				 # Add the consensus letter for this position

		return consensus_solution

	# def fitnessPlot(self, fitness_over_time):
	# 	plt.figure(figsize=(10, 6))
	# 	plt.plot(fitness_over_time, label='Fitness over Time', color='blue')
	# 	plt.xlabel('Run')
	# 	plt.ylabel('Fitness')
	# 	plt.title('Fitness Progression Over GA Runs')
	# 	plt.legend()
	# 	plt.show()	

	def heatPlot(self, agreement_matrix):
		print(agreement_matrix)
		generationAcc = (self.correctguesses / self.genSize) * 100
		mutation = self.mutationRate * 100
		plt.figure(figsize=(8, 6))
		sns.heatmap(agreement_matrix, annot=True, fmt="d", cmap="Blues", cbar=True,
                xticklabels=[chr(i + ord('a')) for i in range(26)],  # Label for 'a' to 'z'
                yticklabels=[f"Pos {i + 1}" for i in range(5)],      # Positions for 5 letters
                cbar_kws={'label': 'Frequency'})  
		plt.title(f"Consensus matrix: {self.word}", fontweight='bold')
		plt.text(0.85, 1.17, f"Generation num: {self.genSize}", ha='left', va='center', 
             fontsize=12, color='black', transform=plt.gca().transAxes)
		plt.text(0.85, 1.13, f"Generational GA Freq.: {self.correctguesses}", ha='left', va='center', 
             fontsize=12, color='black', transform=plt.gca().transAxes)
		plt.text(0.85, 1.09, f"GA Accuracy: {generationAcc}%", ha='left', va='center', 
             fontsize=12, color='black', transform=plt.gca().transAxes)
		plt.text(0.55, 1.17, f"Matrix guess accuracy (10): {self.finalPercent}%", ha='right', va='center', 
             fontsize=12, color='black', transform=plt.gca().transAxes)
		plt.text(0.27, 1.13, f"Population Size: {self.popSize}", ha='right', va='center', 
             fontsize=12, color='black', transform=plt.gca().transAxes)
		plt.text(0.31, 1.09, f"Mutation Rate: {mutation}%", ha='right', va='center', 
             fontsize=12, color='black', transform=plt.gca().transAxes)
		plt.subplots_adjust(top=0.85)
		plt.show()
		#plt.savefig("heatmap.png")

	 	
		
