from actions import ActionType


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
            ActionType.REST: 0.0
        }

        hunger = observation["hunger"]
        energy = observation["energy"]

        # Базовые желания
        scores[ActionType.EAT] = hunger / 100
        scores[ActionType.REST] = (100 - energy) / 100
        scores[ActionType.MOVE] = 0.2
        scores[ActionType.WAIT] = 0.1

        # Опыт из памяти
        for memory in memories:
            action = ActionType(memory.action)

            if memory.result["success"]:
                scores[action] += memory.importance * 0.2
            else:
                scores[action] -= memory.importance * 0.2

        best_action = max(scores, key=scores.get)

        return best_action, scores