import random
import numpy as np
import time

# Color codes for feedback
GREEN = '\033[92m'   # Correct letter in the correct position
YELLOW = '\033[93m'  # Correct letter but in the wrong position
RESET = '\033[0m'    # Reset color

# Load guess and answer lists from text files
def load_word_list(filename):
        return [line.strip() for line in filename]

# Load the lists
GUESS_LIST = load_word_list('resources/guesses-list.txt')
ANSWER_LIST = load_word_list('resources/answers-list.txt')
TARGET_WORD = random.choice(ANSWER_LIST)  # Randomly choose a target from the answer list

print(TARGET_WORD)

# Fitness function for GA
def calculate_fitness(guess):
    fitness = 0
    for i in range(len(TARGET_WORD)):
        if guess[i] == TARGET_WORD[i]:  # Correct position (green)
            fitness += 2
        elif guess[i] in TARGET_WORD:   # Incorrect position (yellow)
            fitness += 1
    return fitness

# Initialize population with guesses from GUESS_LIST
def initialize_population(size):
    return [random.choice(GUESS_LIST) for _ in range(size)]

# GA Selection, Crossover, and Mutation
def select_parents(population, fitness_scores):
    # Selects 2 parents via probability
    # Higher probability (fitness) --> more likely to be selected
    return random.choices(population, weights=fitness_scores, k=2)

def crossover(parent1, parent2):
    child = ""
    for i in range(len(parent1)):
        # random.random() returns a value in the range [0, 1)
        child += parent1[i] if random.random() < 0.5 else parent2[i]
    return child

def mutate(word, mutation_rate=0.1):
    word_as_list = list(word)
    for i in range(len(word_as_list)):
        if random.random() < mutation_rate:
            word_as_list[i] = random.choice("abcdefghijklmnopqrstuvwxyz")
    return ''.join(word_as_list)

# Genetic Algorithm function
def genetic_algorithm(population_size=20, generations=100, mutation_rate=0.1):
    population = initialize_population(population_size)
    for generation in range(generations):
        fitness_scores = [calculate_fitness(word) for word in population]

        # Check if target word has been found
        if TARGET_WORD in population:
            print(f"GA found the target word in generation {generation}!")
            return TARGET_WORD

        # Selection and reproduction
        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population, fitness_scores)
            child1 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)

            child2 = crossover(parent2, parent1)
            child2 = mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        # Update population and output best guess
        population = new_population
        best_guess = max(population, key=calculate_fitness)
        best_fitness = calculate_fitness(best_guess)

    print(f"GA - Generation {generation}: Best Guess '{best_guess}' with Fitness {best_fitness}")
    # print(f"GA - Generation {generation}: Best Guess '{best_guess}' with Fitness {calculate_fitness(best_guess)}")

    print(f"Found in generation {generation}\nGA Finished - Best Guess:(hidden)")
    return best_guess

# Feedback for user's guess
def provide_feedback(guess):
    feedback = ""
    for i in range(len(TARGET_WORD)):
        if guess[i] == TARGET_WORD[i]:
            feedback += f"{GREEN}{guess[i]}{RESET}"  # Correct position (green)
        elif guess[i] in TARGET_WORD:
            feedback += f"{YELLOW}{guess[i]}{RESET}"  # Wrong position (yellow)
        else:
            feedback += guess[i]  # Not in word (no color)
    return feedback

# User guessing function
def user_guess():
    attempts = 6
    for attempt in range(1, attempts + 1):
        guess = input(f"Attempt {attempt}/{attempts}: Enter your guess: ").strip().lower()
        if guess not in GUESS_LIST:
            print("Invalid guess. Please enter a valid word.")
            continue
        
        feedback = provide_feedback(guess)
        print("Feedback:", feedback)
        
        if guess == TARGET_WORD:
            print(f"Congratulations! You've guessed the word '{TARGET_WORD}' in {attempt} attempts!")
            return True
    print(f"Sorry, you've used all attempts. The correct word was '{TARGET_WORD}'.")
    return False

# Run both the GA and user interaction
def play_wordle_with_ga():
    # print("Welcome to Wordle with GA Assistance!")
    # print("Try to guess the word. Meanwhile, the GA will also try to guess it.")
    # print("Let's see who finds it first!\n")

    # Start the GA in the background
    print("GA is starting...")
    ga_result = genetic_algorithm()
    fitness = calculate_fitness(ga_result)

    return ga_result, fitness

def play_wordle_as_user():
    # Start user interaction for guessing
    print("\nNow it's your turn to guess!")
    user_result = user_guess()

    return user_result

#-------------------------------------------------------------------------------------#
# Set up the crowds for WOC Approach
crowd_size = 5
crowd_data = {}
experts = [f'exper_{i}' for i in range(1, crowd_size + 1)] # each will run the GA separately
ga_runs = [f'run_{i}' for i in range(1, 11)] # Used to obtain variability

for expert in experts:
    crowd_data[expert] = {'runs': {}}

agreement_matrices = {run: np.zeros((5, 26), dtype=int) for run in ga_runs}
#-------------------------------------------------------------------------------------#
num = 1

# Run the game with WOC Approach
for expert in experts:
    print(f"Starting GA runs for {expert}")

    for run in ga_runs:
        start_time = time.time()
        print(f"\tStarting {run} for {expert}")
        
        ga_result, fitness = play_wordle_with_ga()

        end_time = time.time()

        # Add some of the results to data dictionary
        crowd_data[expert]['runs'][run] = {
            'execution_time': end_time - start_time,
            'best_solution': ga_result,
            'solution_fitness': fitness,
            'ga_instance': f'ga_instance_{num}'
        }
        num += 1

        # Update the agreement matrix for the current run based on `ga_result`
        for i, letter in enumerate(ga_result):
            column_index = ord(letter) - ord('a')  # Map 'a' to 0, 'b' to 1, ..., 'z' to 25
            agreement_matrices[run][i][column_index] += 1  # Increment the count for this letter at this position

# Example to see the agreement matrix for a specific run
print("Agreement matrix for run_1:")
print(agreement_matrices['run_1'])

#-------------------------------------------------------------------------------------#
# Combine the solutions from each expert for each run to form consensus solutions to see if they can guess the word
def build_consensus_solution(agreement_matrices, run):
    """
    Parameters:
    - agreement_matrices: Dictionary of agreement matrices across GA runs.
    - run: The specific run key to access the agreement matrix.
    
    Returns:
    - consensus_solution: A string representing the consensus word.
    """
    agreement_matrix = agreement_matrices[run]  # Access the agreement matrix for the specific run
    num_positions = agreement_matrix.shape[0]
    consensus_solution = ""

    # For each position in the 5-letter word, find the letter with the highest frequency
    for position in range(num_positions):
        # Find the letter with the highest frequency in the current position
        letter_index = np.argmax(agreement_matrix[position])  # Column with the highest value for this row
        consensus_letter = chr(letter_index + ord('a'))  # Convert index to corresponding letter
        consensus_solution += consensus_letter  # Add the consensus letter for this position
    
    return consensus_solution

# Generate the consensus solutions
consensus_solutions = {}

run_num = 1
for run in ga_runs:
    consensus_solution = build_consensus_solution(agreement_matrices, f"run_{run_num}")
    consensus_solutions[f"run_{run_num}"] = consensus_solution
    run_num += 1

print(consensus_solutions)
#-------------------------------------------------------------------------------------#

user_result = play_wordle_as_user()

# Results of GA and User playing Wordle
if ga_result == TARGET_WORD:
        print(f"The GA found the word '{TARGET_WORD}'!")
if user_result and ga_result != TARGET_WORD:
        print(f"You guessed the word '{TARGET_WORD}'! and the GA did not!")
if ga_result != TARGET_WORD and not user_result:
        print(f"Neither found the word. The correct word was '{TARGET_WORD}'.")