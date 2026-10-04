from actions import Action, ActionType


class Brain:

    def __init__(self):
        pass

    def decide(self, observation, memories=None):

        if memories is None:
            memories = []

        scores = {
            ActionType.WAIT: 0.0,
            ActionType.MOVE: 0.0,
            ActionType.EAT: 0.0,
            ActionType.REST: 0.0,
            ActionType.MOVE_TO: 0.0
        }

        hunger = observation["hunger"]
        energy = observation["energy"]

        # ----------------------------------------------------
        # Basic needs
        # ----------------------------------------------------

        scores[ActionType.EAT] = hunger / 100

        scores[ActionType.REST] = (
            (100 - energy) / 100
        )

        scores[ActionType.MOVE] = 0.05
        scores[ActionType.WAIT] = 0.01

        # ----------------------------------------------------
        # Food
        # ----------------------------------------------------

        visible_food = observation["visible_food"]

        if visible_food:

                closest_food = min(
            visible_food,
            key=lambda food: food["distance"]
        )

        distance = closest_food["distance"]

        # Если NPC уже находится рядом с едой,
        # желание съесть её становится главным.
        if distance == 0:

            scores[ActionType.EAT] = (
                1.0
                + hunger / 100
            )

        else:

            distance_factor = (
                1 / (1 + distance)
            )

            hunger_factor = hunger / 100

            scores[ActionType.MOVE_TO] = (
                0.5
                + hunger_factor
                + distance_factor
            )

        # ----------------------------------------------------
        # Memory
        # ----------------------------------------------------

        for memory in memories:

            try:
                action_type = ActionType(
                    memory.action
                )
            except ValueError:
                continue

            if memory.result["success"]:

                scores[action_type] += (
                    memory.importance * 0.1
                )

            else:

                scores[action_type] -= (
                    memory.importance * 0.1
                )

        # ----------------------------------------------------
        # Choose action
        # ----------------------------------------------------

        best_action_type = max(
            scores,
            key=scores.get
        )

        # ----------------------------------------------------
        # Create action
        # ----------------------------------------------------

        if (
            best_action_type == ActionType.MOVE_TO
            and visible_food
        ):

            closest_food = min(
                visible_food,
                key=lambda food: food["distance"]
            )

            action = Action(
                type=ActionType.MOVE_TO,
                target={
                    "x": closest_food["x"],
                    "y": closest_food["y"]
                }
            )

        else:

            action = Action(
                type=best_action_type
            )

        return action, scores