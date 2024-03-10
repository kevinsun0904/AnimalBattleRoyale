"""This is the functions module. This module contains functions
for playing the board.
"""

import random
import string
from modules.classes import *

from time import sleep
from IPython.display import clear_output


def add_lists(list1, list2):
    """Add two lists by adding the elements with the
    same index
    
    Code written by me from previous assignment
    
    Parameters
    ----------
    list1 : list of int
        first list to add
    list2 : list of int
        second list to add
        
    Returns
    -------
    output : list of int
        sum of two lists
    """
    
    output = []
    
    # concurrently loop through elements in both lists
    for i, j in zip(list1, list2):
        output.append(i + j) # append the sum to output
    return output


def check_position(position, grid_size):
    """check whether position is valid given the grid size
    
    Parameters
    ----------
    position : array of length 2 containing int
        contains the row and column position of the animal to check
    grid_size : tuple of length 2 containing int
        contains the total rows and columns of the board
        
    Returns
    -------
    bool
        boolean of whether the position is valid
    """
    
    # check if the position is valid for both rows and columns
    for i in range(0, 2):
        if not (0 <= position[i] < grid_size[i]):
            return False
    return True


def battle(animal_one, animal_two, species_count):
    """starts a battle between two animals and mutates animals and 
    species_count depending o nthe result of the battle.
    
    order of attack: (similar to rock paper scissors)
    'none' << 'roar' < 'bump' < 'bite' < 'roar'
    
    Parameters
    ----------
    animal_one : Animal
        first animal in battle
    animal_two : Animal
        second animal in battle
    species_count : dict
        dictionary that maps the species name to the remaining count
        
    Returns
    -------
    Animal
        the animal that has won the battle
    """
    
    # get the attacks of both animals
    attack_one = animal_one.attack(animal_two)
    attack_two = animal_two.attack(animal_one)
    to_remove = None
    
    # Compare the two attacks to decide which animal to remove
    # If the attacks are the same, choose animal by random
    if attack_one == 'roar':
        if attack_two == 'bump':
            to_remove = animal_one
        elif attack_two == 'roar':
            to_remove = random.choice([animal_one, animal_two])
        else:
            to_remove = animal_two
    elif attack_one == 'bump':
        if attack_two == 'bite':
            to_remove = animal_one
        elif attack_two == 'bump':
            to_remove = random.choice([animal_one, animal_two])
        else:
            to_remove = animal_two
    elif attack_one == 'bite':
        if attack_two == 'roar':
            to_remove = animal_one
        elif attack_two == 'bite':
            to_remove = random.choice([animal_one, animal_two])
        else:
            to_remove = animal_two
    elif attack_one == 'none':
        if attack_two == 'none':
            to_remove = random.choice([animal_one, animal_two])
        else:
            to_remove = animal_one
    
    # set is_alive attribute to false so that it is skipped when
    # loading the board
    to_remove.is_alive = False
    
    # get the count of the species to remove and subtract it by 1
    curr_count = species_count.get(to_remove.species, 1) - 1
    if curr_count == 0: # if count is 0 remove species from dict
        if to_remove.species in species_count:
            species_count.pop(to_remove.species)
    else: # else update the species with the new count
        species_count.update({to_remove.species : curr_count})
    
    # return the winner animal
    if to_remove is animal_one:
        return animal_two
    else:
        return animal_one

    
def play_board(animals, n_iter = 25, grid_size = (5, 5), sleep_time = 0.3):
    """ plays the board using the animals provided
    
    This function was significantly modified from the provided function in previous
    assignment.
    
    Parameters
    ----------
    animals : set of Animal
        set containing all of the animals
    n_iter : int
        the number of iterations to run for this game. default = 25
    grid_size : tuple of length 2 containing int
        dimension of the grid, default = (5, 5)
    sleep_time : int
        the time between each iteration
    """
    
    # check if no animals are provided
    if len(animals) == 0:
        print("No animals provided!!!")
        return
    
    # If input is a single animal, put it in a list so that procedures work
    if not type(animals) == set:
        animals = {animals}
    
    # Update each animal to know about the grid_size they are on and set species_count
    # to check which species are left
    species_count = {} # map the species to its total count
    for animal in animals:
        # set grid size
        animal.set_grid_size(grid_size)
        
        # randomize the position of each animal
        animal.random_pos()
        
        # get previous count and increment by 1
        curr_count = 1 + species_count.get(animal.species, 0) 
        # update with the new count
        species_count.update({animal.species : curr_count})

    # loop through the iterations
    for it in range(n_iter):

        # initialize grid that only contains '.' for this iteration
        grid_list = [['.' for i in range(grid_size[1])] for j in range(grid_size[0])]
        # initialize grid that only contains None to store position of animal
        animal_grid = [[None for i in range(grid_size[1])] for j in range(grid_size[0])]

        animals_copy = animals.copy()
        # loop through all animals and update grids
        for animal in animals_copy:
            # skip animal and remove from set if not alive
            if not animal.is_alive:
                animals.remove(animal)
                continue
                
            # update with animal character for display
            grid_list[animal.position[0]][animal.position[1]] = animal.character
            # update with Animal object to store position
            animal_grid[animal.position[0]][animal.position[1]] = animal

        # Clear the previous iteration, print the new grid (as a string), and wait
        clear_output(True)
        print('\n'.join([' '.join(lst) for lst in grid_list]))
        sleep(sleep_time)
        
        # Check if a species has won
        if len(species_count) == 1:
            # print the only remaining species in species_count
            for winner in species_count.keys():
                print('\nWinner: ' + winner + '!!!!')
            # terminate the program
            return

        # Update animal position(s) for next turn
        for animal in animals:
            # clear animal from current location in animal_grid
            animal_grid[animal.position[0]][animal.position[1]] = None
            
            # move the animal to new location
            animal.move()
            row = animal.position[0]
            col = animal.position[1]

            # battle with animal in new location if there is an animal
            prev_animal = animal_grid[row][col]
            if not prev_animal == None:
                # store winner of battle in new location 
                animal_grid[row][col] = battle(animal, prev_animal, species_count)
            else:
                # store animal in new location since there was no other animal on this location
                animal_grid[row][col] = animal
                
    # print tie since winner was not found after iterations
    print("\nIts a tie!!!! The game didn't end in " + str(n_iter) + " iterations!!" )