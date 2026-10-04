from enum import Enum


class ActionType(Enum):
    WAIT = "wait"
    MOVE = "move"
    EAT = "eat"
    REST = "rest"