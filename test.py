from enum import Enum

class FlagTypes():
    pole = 0
    subpole = 1
    fail = 2

other_flags = ((FlagTypes.subpole, FlagTypes.fail),
(FlagTypes.pole, FlagTypes.fail),
(FlagTypes.pole, FlagTypes.subpole))

flags = [True] * 3

print(other_flags[FlagTypes.pole])