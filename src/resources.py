from dataclasses import dataclass


@dataclass
class Food:
    x: int
    y: int
    nutrition: float = 40.0
    amount: int = 1