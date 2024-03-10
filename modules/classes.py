"""This is the classes module. This module contains classes
for defining different species of animals and methods for
both movement and attack.
"""

import random
from modules.functions import check_position, add_lists


class Animal():
    """This is the Animal abstract class used for polymorphism of
    specific species
    
    Class attributes
    ----------------
    attacks : list
        list containing all the attacks
        
    Attributes
    ----------
    character : chr
        Character representing the animal
    species : str
        name of the species of this animal
    is_alive : bool
        whether the animal is alive or not
    position : list
        list containing position of animal
    moves : list
        list containing the default list of possible moves
    grid_size : tuple
        tuple containing the dimensions of the grid
        
    Methods
    -------
    set_grid_size(grid_size)
        sets the grid_size of the animal with grid_size
    wander()
        finds the new possible position of animal
    move()
        sets the new position of animal
    random_pos()
        generates the position of animal by random
    attack(opponent)
        returns the attack of animals
    """
    
    attacks = ['roar', 'bump', 'bite']
    
    def __init__(self, species, character):
        """Constructor of Animal
        
        Parameters
        ----------
        species : str
            the species of this animal
        character : chr
        the character used to represent this animal
        """
        self.character = character
        self.species = species
        self.is_alive = True
        self.position = [0, 0]
        self.moves = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        self.grid_size = None
        
    def set_grid_size(self, grid_size):
        """sets the new grid_size of animal
        
        Parameters
        ----------
        grid_size : tuple
            dimensions of the board
        """
        
        self.grid_size = grid_size
        
    def wander(self):
        """finds and returns a new possible position by adding moves
        by random
        
        This function was implemented by me in a previous assignment
        
        Returns
        -------
        new_pos : list
            list containing the new valid position
        """
        
        has_new_pos = False
        # keep adding a random move until the position is valid
        while (not has_new_pos):
            move = random.choice(self.moves)
            new_pos = add_lists(self.position, move)
            #check if the position is valid using check_position function
            has_new_pos = check_position(new_pos, self.grid_size)
        return new_pos
    
    def move(self):
        """sets the position of the animal with a new valid position
        """
        
        self.position = self.wander()
    
    def random_pos(self):
        """sets the position of the animal to a random position
        """
        
        self.position[0] = random.randrange(self.grid_size[0])
        self.position[1] = random.randrange(self.grid_size[1])
    
    def attack(self, opponent):
        """ the default attack method, returns the attack taken by
        the animal
        
        Parameters
        ----------
        opponent : Animal
            the opponent to attack
        
        Returns
        -------
        str
            only returns 'none' for default attack
        """
        return 'none'

    
class Dog(Animal):
    """This class inherits from the abstract class Animal and is used to
    create Dog objects. The dog is spontaneous and can use any attack
    at random
    
    Methods
    -------
    attack(opponent)
        returns the attack of this dog
    """
    
    def __init__(self):
        """Constructor of Dog
        """
        
        # call Animal constructor to initialize variables in parent
        super().__init__('dog', 'D')
    
    def attack(self, opponent):
        """This method overrides the attack method of Animal
        and generates a random attack to take
        
        Parameters
        ----------
        opponent : Animal
            the animal to attack
        
        Returns
        -------
        str
            the attack taken by this dog
        """
        
        return random.choice(Animal.attacks)
    
    
class Turtle(Animal):
    """This class inherits from the abstract class Animal and is used to
    create Turtle objects. The turtle is peaceful and doesnt attack any
    other animal
    
    Attributes
    ----------
    can_move : bool
        whether this turtle can move or not
    
    Methods
    -------
    move()
        sets the new position of turtle after moving
    """
    
    def __init__(self):
        """Constructor of Turtle
        """
        
        super().__init__('turtle', 'T')
        self.can_move = True
    
    def move(self):
        """This method overrides the move method in Animal. The turtle moves
        every other round
        """
        
        if self.can_move:
            # call wander in Animal class when can move
            self.position = self.wander()
            self.can_move = False
        else:
            self.can_move = True
            
            
class Frog(Animal):
    """This class inherits from the abstract class Animal and is used to
    create Frog objects. The frog can jump double the distance of normal
    animals
    
    Methods
    -------
    move()
        sets the new position of turtle after moving
    """
    
    def __init__(self):
        """Constructor of Frog
        """
        
        super().__init__('frog', 'F')
        # replace moves with double the distance because the turtle jumps
        # double the distance
        self.moves = [[-2, 0], [2, 0], [0, 2], [0, -2]]
    
    def attack(self, opponent):
        """This method overrides the attack method in Animals. The frog only bumps
        its opponent
        
        Parameters
        ----------
        opponent : Animal
            opponent to attack
            
        Returns
        -------
        str
            the attack taken
        """
        
        return 'bump'

    
class Eagle(Animal):
    """This class inherits from the abstract class Animal and is used to
    create Eagle objects. The eagle can fly to any position on the board
    
    Methods
    -------
    move()
        sets the new position of turtle after moving
    attack(opponent)
        returns the attack of the eagle
    """
    
    def __init__(self):
        """Constructor for Eagle
        """
        
        super().__init__('eagle', 'E')
        
    def move(self):
        """This method overrides the move method in Animal. The eagle can fly
        to any tile on the board
        """
        
        self.random_pos()
        
    def attack(self, opponent):
        """This method overrides the attack method in animal and returns the
        attack of the eagle
        
        Parameters
        ----------
        opponent : Animal
            animal to attack
        
        Returns
        -------
        str
            the attack taken
        """
        
        if opponent.species == 'dog':
            return 'roar'
        elif opponent.species == 'frog':
            return 'bite'
        else:
            return random.choice(Animal.attacks)
        
        
class Bear(Animal):
    """This class inherits from the abstract class Animal and is used to
    create Bear objects. The bear rotates between the three attacks.
    
    Attributes
    ----------
    attack_index : int
        index of the attack the bear is currently on
    
    Methods
    -------
    attack(opponent)
        returns the attack of the bear
    """
    
    def __init__(self):
        """Constructor of Bear
        """
        
        super().__init__('bear', 'B')
        self.attack_index = 0
    
    def attack(self, opponent):
        """Overrides the attack method in animals and rotates between the 
        default attacks.
        
        Parameters
        ----------
        opoonenet : Animal
            the animal to attack
        
        Returns
        -------
        curr_attack : str
            attack according to current attack_index
        """
        curr_attack = Animal.attacks[self.attack_index]
        self.attack_index = (self.attack_index + 1) % 3
        return curr_attack

    
class Lion(Animal):
    """This class inherits from the abstract class Animal and is used to
    create Lion objects. Lions walk in the same direction for four rounds
    and then switch to a different direction by random
    
    Class Attributes:
    -----------------
    attacks : list
        a list containing only roar and bite
    
    Attributes
    ----------
    move_index : int
        index of move taken for current round
    move_count : int
        number of moves taken for current move
    
    Methods
    -------
    move()
        sets the new position of turtle after moving
    attack(opponent)
        returns the attack of the Lion
    """
    
    attacks = ['roar', 'bite']
    
    def __init__(self):
        """Constructor of Lion
        """
        
        super().__init__('lion', 'L')
        self.move_index = 0
        self.move_count = 0
        
    def wander(self):
        """Overrides the wander method in Animals. Keeps moving the 
        lion in the same direction for four times and switching to
        another direction until the position is valid
        """
        
        has_new_pos = False
        while not has_new_pos:
            # set current move
            move = self.moves[self.move_index]
            
            # increment move_count
            self.move_count += 1
            
            # reset move_count and switch to new move when the count is 4
            if (self.move_count == 4):
                self.move_count = 0
                self.move_index = random.randrange(4)
            
            # add move to position and check if valid
            new_pos = add_lists(self.position, move)
            has_new_pos = check_position(new_pos, self.grid_size)
            
        return new_pos
    
    def move(self):
        """Overrides the move method in animals
        """
        
        self.position = self.wander()
        
    def attack(self, opponent):
        """Overrides the attack method in Animals. 
        
        Parameters
        ----------
        opponent : Animal
            the animal to attack
        
        Returns
        -------
        str
            the attack taken
        """
        if opponent.species == 'snake':
            return 'roar'
        else:
            return random.choice(Lion.attacks)

        
class Snake(Animal):
    """This class inherits from the abstract class Animal and is used to
    create Snake objects. Snakes stay in the same position and bites any
    animal that intrudes.
    
    Methods
    -------
    move()
        sets the new position of turtle after moving
    attack(opponent)
        returns the attack of the Lion
    """
    
    def __init__(self):
        """Constructor of Snake
        """
        super().__init__('snake', 'S')
    
    def move(self):
        """Overrides the move method and makes sure the snake stays in place
        """
        return
        
    def attack(self, opponent):
        """Overrides the attack method in Animal
        
        Parameters
        ----------
        opponent : Animal
            the animal to attack
            
        Returns
        -------
        str
            the attack taken
        """
        
        if opponent.species == 'eagle':
            return 'none'
        return 'bite'