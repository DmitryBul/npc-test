from dataclasses import dataclass


@dataclass
class Memory:
    observation: dict
    action: str
    result: dict
    importance: float = 0.0


class MemorySystem:
    def __init__(self, max_memories=100):
        self.memories = []
        self.max_memories = max_memories

    def remember(self, observation, action, result):
        memory = Memory(
        observation=observation,
        action=action.type.value,
        result=result,
        importance=self.calculate_importance(
            observation,
            result
        )
    )

        self.memories.append(memory)

        self._limit_memory()

    def retrieve(self, observation, limit=5):
        scored_memories = []

        for memory in self.memories:
            old_observation = memory.observation

            hunger_diff = (
                abs(observation["hunger"] - old_observation["hunger"]) / 100
            )

            energy_diff = (
                abs(observation["energy"] - old_observation["energy"]) / 100
            )

            health_diff = (
                abs(observation["health"] - old_observation["health"]) / 100
            )

            night_diff = (
                0
                if observation["is_night"] == old_observation["is_night"]
                else 1
            )

            distance = (
                hunger_diff
                + energy_diff
                + health_diff
                + night_diff
            )

            similarity = 1 / (1 + distance)

            scored_memories.append(
                (similarity, memory)
            )

        scored_memories.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            memory
            for _, memory in scored_memories[:limit]
        ]

    def calculate_importance(self, observation, result):
        importance = 0.1

        # Сильный голод делает событие более значимым
        if observation["hunger"] > 80:
            importance += 0.3

        # Низкая энергия тоже
        if observation["energy"] < 20:
            importance += 0.2

        # Неудачные действия важнее обычных
        if not result["success"]:
            importance += 0.4

        return min(importance, 1.0)

    def _limit_memory(self):
        if len(self.memories) <= self.max_memories:
            return

        self.memories.sort(
            key=lambda memory: memory.importance,
            reverse=True
        )

        self.memories = self.memories[:self.max_memories]

    def get_all(self):
        return self.memories

    def get_action_experience(self, action_type):
        successes = 0
        failures = 0

        for memory in self.memories:
            if memory.action != action_type.value:
                continue

            if memory.result["success"]:
                successes += 1
            else:
                failures += 1

        return successes, failures

    def get_contextual_experience(
        self,
        action_type,
        observation,
        limit=20
    ):
        relevant_memories = []

        for memory in self.memories:

            if memory.action != action_type.value:
                continue

            old = memory.observation

            hunger_diff = abs(
                observation["hunger"] - old["hunger"]
            ) / 100

            energy_diff = abs(
                observation["energy"] - old["energy"]
            ) / 100

            health_diff = abs(
                observation["health"] - old["health"]
            ) / 100

            night_diff = (
                0
                if observation["is_night"] == old["is_night"]
                else 1
            )

            # Есть ли еда в похожей ситуации?
            current_food = len(
                observation["visible_food"]
            )

            old_food = len(
                old["visible_food"]
            )

            food_diff = min(
                abs(current_food - old_food) / 3,
                1
            )

            distance = (
                hunger_diff
                + energy_diff
                + health_diff
                + night_diff
                + food_diff
            )

            similarity = 1 / (1 + distance)

            relevant_memories.append(
                (similarity, memory)
            )

        relevant_memories.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return relevant_memories[:limit]