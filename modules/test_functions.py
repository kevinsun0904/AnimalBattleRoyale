from modules.classes import *
from modules.functions import battle, check_position


def test_Eagle():
    assert callable(Eagle)
    eagle = Eagle()
    assert eagle.species == 'eagle'
    assert eagle.character == 'E'
    assert eagle.is_alive == True
    assert eagle.position == [0, 0]
    
    
def test_attack():
    dog = Dog()
    eagle = Eagle()
    turtle = Turtle()
    bear = Bear()
    snake = Snake()
    
    assert callable(dog.attack)
    assert dog.attack(turtle) in ['roar', 'bump', 'bite']
    assert turtle.attack(dog) == 'none'
    assert snake.attack(eagle) == 'none'
    assert snake.attack(dog) == 'bite'
    
    assert bear.attack(dog) == 'roar'
    assert bear.attack_index == 1
    bear.attack(dog)
    assert bear.attack(dog) == 'bite'
    assert bear.attack_index == 0
    
    
def test_battle():
    dog = Dog()
    eagle = Eagle()
    turtle = Turtle()
    bear = Bear()
    snake = Snake()
    
    species_count = {
        'dog' : 1,
        'eagle' : 1,
        'turtle' : 1,
        'bear' : 1,
        'snake' : 1
    }
    
    assert callable(battle)
    winner = battle(dog, turtle, species_count)
    assert type(winner) == Dog
    assert winner == dog
    assert not 'turtle' in species_count
    assert not turtle.is_alive
    
    winner = battle(eagle, snake, species_count)
    assert type(winner) == Eagle
    assert winner == eagle
    assert not 'snake' in species_count
    assert not snake.is_alive

    
def test_check_position():
    assert callable(check_position)
    
    assert check_position([0, 0], (5, 5))
    assert check_position([3, 2], (5, 10))
    
    assert not check_position([-1, 0], (5, 5))
    assert not check_position([10, 10], (4, 5))