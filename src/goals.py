from enum import Enum


class GoalType(Enum):
    SURVIVE = "survive"
    FIND_FOOD = "find_food"
    EAT = "eat"
    REST = "rest"
    EXPLORE = "explore"