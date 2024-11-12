run code by being in AI-Final-Project\wordle-v2\wordle-v2  ***how ever you have the project
    Then run python -m wordle
    it runs as a module

    make sure to import what is needed to run

        pip install pygame_menu
                    pygame
                    win10toast

To run the genetice alg(version6.py)
Do the following 
cd geneticeAlg and then run
python version6.py

After implementing the WOC Approach
    - There is a set size for the number of experts that make up the crowd
    - Each expert will run the GA 10 times for variability and to calculate statistics later on
    - Each expert for a given run will save its best solution and add it to an agreement matrix
        --> It works by seeing what position a given letter is found and increments that value by 1
        --> For example, letter "T" was was found at posiion 1 among the experts 3 times across 5 experts
    - After all 10 run for each expert in the crowd, a consensus solution is determine based on the agreement matrix
                    
11/11: The final game has been implemented with the GA/WoC algorithm fully melded in. It is currently printing out a heatmap with statistics
       and running the user side game after that is closed out. It is run in the same way that is originally stated, python -m wordle in the
       AI-Final-Project\wordle-v2\wordle-v2 pathing.
