from actions import Action, ActionType
from goals import GoalType


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

        # ----------------------------------------
        # Basic motivations
        # ----------------------------------------

        scores[ActionType.EAT] = 0.0

        if energy < 30:
            scores[ActionType.REST] = (
                (100 - energy) / 100
            )
        else:
            scores[ActionType.REST] = 0.0

        exploration_need = hunger / 100

        scores[ActionType.MOVE] = (
            0.05
            + exploration_need * 0.4
        )
        scores[ActionType.WAIT] = 0.01

        # ----------------------------------------
        # Food
        # ----------------------------------------

        visible_food = observation["visible_food"]

        closest_food = None

        if visible_food:

            closest_food = min(
                visible_food,
                key=lambda food: food["distance"]
            )

            distance = closest_food["distance"]

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

        # ----------------------------------------
        # Experience influence
        # ----------------------------------------

        # ----------------------------------------
        # Contextual experience
        # ----------------------------------------

        memory_system = observation["memory_system"]

        for action_type in ActionType:

            experiences = (
                memory_system.get_contextual_experience(
                    action_type,
                    observation
                )
            )

            if not experiences:
                continue

            weighted_score = 0.0
            total_weight = 0.0

            for similarity, memory in experiences:

                result_value = (
                    1.0
                    if memory.result["success"]
                    else -1.0
                )

                weight = similarity * memory.importance

                weighted_score += (
                    result_value * weight
                )

                total_weight += weight

            if total_weight > 0:

                experience = (
                    weighted_score / total_weight
                )

                scores[action_type] += (
                    experience * 0.3
                )

        # ----------------------------------------
        # Choose action
        # ----------------------------------------

        best_action_type = max(
            scores,
            key=scores.get
        )

        # ----------------------------------------
        # Create structured action
        # ----------------------------------------

        if (
            best_action_type == ActionType.MOVE_TO
            and closest_food is not None
        ):

            action = Action(
                type=ActionType.MOVE_TO,
                target={
                    "x": closest_food["x"],
                    "y": closest_food["y"]
                },
                goal=GoalType.FIND_FOOD
            )

        elif best_action_type == ActionType.EAT:

            action = Action(
                type=ActionType.EAT,
                goal=GoalType.EAT
            )

        elif best_action_type == ActionType.REST:

            action = Action(
                type=ActionType.REST,
                goal=GoalType.REST
            )

        else:

            action = Action(
                type=best_action_type,
                goal=GoalType.EXPLORE
            )

        return action, scores