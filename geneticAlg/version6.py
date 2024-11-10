import random

# Color codes for feedback
GREEN = '\033[92m'   # Correct letter in the correct position
YELLOW = '\033[93m'  # Correct letter but in the wrong position
RESET = '\033[0m'    # Reset color

# Load guess and answer lists from text files
def load_word_list(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

# Load the lists
GUESS_LIST = load_word_list('guesses-list.txt')
ANSWER_LIST = load_word_list('answers-list.txt')
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
    return random.choices(population, weights=fitness_scores, k=2)

def crossover(parent1, parent2):
    child = ""
    for i in range(len(parent1)):
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
    print(f"GA - Generation {generation}: Best Guess '{best_guess}' with Fitness {calculate_fitness(best_guess)}")
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

    # Start user interaction for guessing
    print("\nNow it's your turn to guess!")
    user_result = user_guess()

    if ga_result == TARGET_WORD:
        print(f"The GA found the word '{TARGET_WORD}'!")
    if user_result:
        print(f"You guessed the word '{TARGET_WORD}'!")
    if ga_result != TARGET_WORD and not user_result:
        print(f"Neither found the word. The correct word was '{TARGET_WORD}'.")

# Run the game
play_wordle_with_ga()
