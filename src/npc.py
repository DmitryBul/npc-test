from memory import MemorySystem
from actions import Action, ActionType
import random
from world_memory import WorldMemory


class NPC:
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world
        

        self.explore_target = None

        self.health = 100.0
        self.hunger = 70.0
        self.energy = 100.0
        self.alive = True

        self.memory = MemorySystem()
        self.world_memory = WorldMemory()

    def update(self):
        if not self.alive:
            return

        self.hunger += 0.1
        self.energy -= 0.05

        if self.hunger >= 80:
            self.health -= 0.1

        if self.health <= 0:
            self.health = 0
            self.alive = False

    def perform_action(self, action):

        if not self.alive:
            return {
                "success": False,
                "message": "NPC is dead"
            }

        if action.type == ActionType.WAIT:
            return self.wait()

        elif action.type == ActionType.MOVE:

            if self.explore_target is None:
                self.choose_explore_target()

            return self.move_to(
                self.explore_target["x"],
                self.explore_target["y"]
            )

        elif action.type == ActionType.MOVE_TO:

            if action.target is None:
                return {
                    "success": False,
                    "message": "MOVE_TO has no target"
                }

            return self.move_to(
                action.target["x"],
                action.target["y"]
            )

        elif action.type == ActionType.EAT:

            food = self.get_food_at_position()

            return self.eat(food)

        elif action.type == ActionType.REST:
            return self.rest()

        return {
            "success": False,
            "message": "Unknown action"
        }

    def wait(self):
        return {
            "success": True,
            "message": "NPC waited"
        }

    def move(self):
        self.energy -= 1

        return {
            "success": True,
            "message": "NPC moved"
        }

    def eat(self, food):
        if food is None:
            return {
                "success": False,
                "message": "No food available"
            }

        if self.hunger <= 0:
            return {
                "success": False,
                "message": "NPC is not hungry"
            }

        old_hunger = self.hunger

        self.hunger -= food.nutrition

        if self.hunger < 0:
            self.hunger = 0

        food.amount -= 1

        return {
            "success": True,
            "message": (
                f"NPC ate food "
                f"and reduced hunger "
                f"from {old_hunger:.1f} "
                f"to {self.hunger:.1f}"
            ),
            "food_consumed": True
        }

    def rest(self):
        self.energy += 10

        if self.energy > 100:
            self.energy = 100

        return {
            "success": True,
            "message": "NPC rested"
        }

    def move_to(self, target_x, target_y):

        if not self.alive:
            return {
                "success": False,
                "message": "NPC is dead"
            }

        old_x = self.x
        old_y = self.y

        if self.x < target_x:
            self.x += 1

        elif self.x > target_x:
            self.x -= 1

        elif self.y < target_y:
            self.y += 1

        elif self.y > target_y:
            self.y -= 1

        else:

            self.explore_target = None

            return {
                "success": True,
                "message": "NPC reached target"
            }

        self.energy -= 1

        return {
            "success": True,
            "message": (
                f"NPC moved from "
                f"({old_x}, {old_y}) "
                f"to ({self.x}, {self.y})"
            )
        }

    def get_food_at_position(self):

        for food in self.world.foods:

            if (
                food.x == self.x
                and food.y == self.y
                and food.amount > 0
            ):
                return food

        return None

    def choose_explore_target(self):
        margin = 3

        target_x = random.randint(
            margin,
            self.world.width - margin - 1
        )

        target_y = random.randint(
            margin,
            self.world.height - margin - 1
        )

        self.explore_target = {
            "x": target_x,
            "y": target_y
        }

        return self.explore_target