from resources import Food


class World:
    def __init__(self, width=40, height=30):
        self.width = width
        self.height = height
        self.time = 0

        self.foods = [
        Food(15, 15),
        Food(5, 20),
        Food(30, 25),
    ]

    def update(self):
        self.time += 1

    def remove_empty_food(self):

        self.foods = [
            food
            for food in self.foods
            if food.amount > 0
        ]

    @property
    def hour(self):
        return (self.time // 60) % 24

    @property
    def is_night(self):
        return self.hour >= 20 or self.hour < 6