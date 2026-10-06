from dataclasses import dataclass
from enum import Enum

from goals import GoalType


class ActionType(Enum):
    WAIT = "wait"
    MOVE = "move"
    EAT = "eat"
    REST = "rest"
    MOVE_TO = "move_to"


@dataclass
class Action:
    type: ActionType
    target: dict | None = None
    goal: GoalType | None = None