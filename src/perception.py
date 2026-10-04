class Perception:

    def __init__(self, npc, world, vision_range=8):
        self.npc = npc
        self.world = world
        self.vision_range = vision_range

    def observe(self):

        visible_food = []

        for food in self.world.foods:

            distance = abs(
                self.npc.x - food.x
            ) + abs(
                self.npc.y - food.y
            )

            if distance <= self.vision_range:

                visible_food.append({
                    "x": food.x,
                    "y": food.y,
                    "distance": distance,
                    "nutrition": food.nutrition
                })

        return {
            "position": {
                "x": self.npc.x,
                "y": self.npc.y
            },

            "health": self.npc.health,
            "hunger": self.npc.hunger,
            "energy": self.npc.energy,

            "time": self.world.time,
            "hour": self.world.hour,
            "is_night": self.world.is_night,

            "visible_food": visible_food
        }