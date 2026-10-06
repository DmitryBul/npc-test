class WorldMemory:

    def __init__(self):
        self.locations = {}

    def remember_location(
        self,
        x,
        y,
        visible_food
    ):
        self.locations[(x, y)] = {
            "food": [
                {
                    "x": food["x"],
                    "y": food["y"],
                    "nutrition": food["nutrition"]
                }
                for food in visible_food
            ]
        }

    def get_location(self, x, y):
        return self.locations.get((x, y))

    def has_visited(self, x, y):
        return (x, y) in self.locations

    def get_all_locations(self):
        return self.locations

    def find_known_food(self):

        known_food = []

        for location in self.locations.values():

            for food in location["food"]:
                known_food.append(food)

        return known_food

    def get_known_food_targets(self, world):

        targets = []

        for food in self.find_known_food():

            for world_food in world.foods:

                if (
                    world_food.x == food["x"]
                    and world_food.y == food["y"]
                    and world_food.amount > 0
                ):
                    targets.append({
                        "x": world_food.x,
                        "y": world_food.y,
                        "nutrition": world_food.nutrition
                    })

        return targets