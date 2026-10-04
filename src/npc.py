from actions import ActionType
from memory import MemorySystem


class NPC:
    def __init__(self, x, y):
        
        self.x = x
        self.y = y

        self.health = 100.0
        self.hunger = 0.0
        self.energy = 100.0

        self.alive = True

        self.memory = MemorySystem()

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

        if action == ActionType.WAIT:
            return self.wait()

        elif action == ActionType.MOVE:
            return self.move()

        elif action == ActionType.EAT:
            return self.eat()

        elif action == ActionType.REST:
            return self.rest()

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

    def eat(self):
        if self.hunger <= 0:
            return {
                "success": False,
                "message": "NPC is not hungry"
            }

        self.hunger -= 20

        if self.hunger < 0:
            self.hunger = 0

        return {
            "success": True,
            "message": "NPC ate"
        }

    def rest(self):
        self.energy += 10

        if self.energy > 100:
            self.energy = 100

        return {
            "success": True,
            "message": "NPC rested"
        }