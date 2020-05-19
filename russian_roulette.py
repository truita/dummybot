import random

magazine = [0] * 6
magazine_position = 0

def reload_function():
    global magazine
    global magazine_position
    magazine = [0] * 6
    magazine_position = 0
    magazine[random.randint(0,5)] = 1

def pew_function():
    global magazine_position
    global magazine
    if magazine[magazine_position] == 1:
        return 1
    else:
        magazine_position += 1
        return 0