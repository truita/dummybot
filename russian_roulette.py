import random

magazine = [0] * 6
magazine_position = 0

def reload_function(): #Reloads the magazine / Changes the bullet position
    global magazine
    global magazine_position
    magazine = [0] * 6
    magazine_position = 0
    magazine[random.randint(0,5)] = 1

def pew_function():
    global magazine_position
    global magazine
    if 1 not in magazine: #If there are no bullets in the magazine returns 2
        return 2
    elif magazine[magazine_position] == 1: #If the bullet is on the current position returns 1
        magazine[magazine_position] = 0
        return 1
    else: #If the bullet isn't in the current position moves the magazine position by one
        magazine_position += 1
        return 0