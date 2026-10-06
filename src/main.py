import pygame

from world import World
from npc import NPC
from perception import Perception
from brain import Brain


# ============================================================
# Configuration
# ============================================================

CELL_SIZE = 20
FPS = 10

WINDOW_WIDTH = 40 * CELL_SIZE
WINDOW_HEIGHT = 30 * CELL_SIZE


# ============================================================
# Initialization
# ============================================================

pygame.init()

screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)

pygame.display.set_caption("NPC Life")

clock = pygame.time.Clock()

world = World()
npc = NPC(10, 15, world)

perception = Perception(
    npc,
    world
)

brain = Brain()


# ============================================================
# Console output
# ============================================================

def print_separator():
    print("=" * 60)


def print_npc_state(npc):
    status = "ALIVE" if npc.alive else "DEAD"

    print("  NPC state:")
    print(f"    Status:   {status}")
    print(f"    Position: ({npc.x}, {npc.y})")
    print(f"    Health:   {npc.health:.1f}")
    print(f"    Hunger:   {npc.hunger:.1f}")
    print(f"    Energy:   {npc.energy:.1f}")

    if npc.explore_target:
        print(
            f"    Explore target: "
            f"({npc.explore_target['x']}, "
            f"{npc.explore_target['y']})"
        )


def print_visible_food(observation):
    foods = observation["visible_food"]

    print()
    print("  Perception:")

    if not foods:
        print("    No food visible")
        return

    for food in foods:
        print(
            f"    Food at "
            f"({food['x']}, {food['y']}) "
            f"| distance: {food['distance']} "
            f"| nutrition: {food['nutrition']:.1f}"
        )


def print_decision(scores, action):
    print()
    print("  Decision:")

    sorted_scores = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for action_type, score in sorted_scores:
        marker = (
            "→"
            if action_type == action.type
            else " "
        )

        print(
            f"    {marker} "
            f"{action_type.value.upper():5} "
            f"{score:.3f}"
        )

    print()
    print(
        f"  Chosen action: "
        f"{action.type.value.upper()}"
    )

    if action.target:
        print(
            f"  Target: "
            f"({action.target['x']}, "
            f"{action.target['y']})"
        )


def print_action_result(result):
    print()

    status = (
        "SUCCESS"
        if result["success"]
        else "FAILED"
    )

    print(f"  Action result: {status}")
    print(f"  Message: {result['message']}")


def print_memory(memories, npc):
    print()
    print("  Memory:")

    print(
        f"    Total stored: "
        f"{len(npc.memory.get_all())}"
    )

    print(
        f"    Similar experiences: "
        f"{len(memories)}"
    )

    if not memories:
        print("    Most relevant: None")
        return

    memory = memories[0]

    print(
        f"    Most relevant: "
        f"{memory.action.upper()} "
        f"| importance: {memory.importance:.2f}"
    )


def print_tick(
    world,
    npc,
    observation,
    action,
    scores,
    result,
    memories
):
    print()
    print_separator()

    print(
        f"TIME | Tick: {world.time:04d} "
        f"| Hour: {world.hour:02d} "
        f"| Night: {world.is_night}"
    )

    print_separator()

    print()
    print("  World memory:")
    print(
        f"    Known locations: "
        f"{len(npc.world_memory.get_all_locations())}"
    )

    print_separator()

    print_npc_state(npc)


    print_visible_food(
        observation
    )

    print()
    print("  Known food:")

    known_food = observation.get(
        "known_food",
        []
    )

    print_separator()

    if not known_food:
        print("    None")
    else:
        for food in known_food:
            print(
                f"    Food remembered at "
                f"({food['x']}, {food['y']})"
            )

    print_decision(
        scores,
        action
    )

    if action.target:
        print()
        print(
            f"  Target: "
            f"({action.target['x']}, "
            f"{action.target['y']})"
        )

    print_action_result(
        result
    )

    print_memory(
        memories,
        npc
    )

    print_separator()


# ============================================================
# Rendering
# ============================================================

def draw_world():
    screen.fill(
        (30, 30, 30)
    )

    for x in range(world.width):
        for y in range(world.height):

            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(
                screen,
                (50, 50, 50),
                rect,
                1
            )


def draw_food():
    for food in world.foods:

        rect = pygame.Rect(
            food.x * CELL_SIZE,
            food.y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        pygame.draw.rect(
            screen,
            (200, 150, 50),
            rect
        )


def draw_npc():
    rect = pygame.Rect(
        npc.x * CELL_SIZE,
        npc.y * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    pygame.draw.rect(
        screen,
        (0, 200, 100),
        rect
    )


def draw():
    draw_world()
    draw_food()
    draw_npc()

    pygame.display.flip()


# ============================================================
# Main simulation loop
# ============================================================

running = True

while running:

    # --------------------------------------------------------
    # Events
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # --------------------------------------------------------
    # World update
    # --------------------------------------------------------

    world.update()

    # --------------------------------------------------------
    # NPC internal state update
    # --------------------------------------------------------

    npc.update()

    # --------------------------------------------------------
    # Perception
    # --------------------------------------------------------

    observation = perception.observe()

    npc.world_memory.remember_location(
        npc.x,
        npc.y,
        observation["visible_food"]
    )

    known_food = npc.world_memory.get_known_food_targets(
        world
    )

    observation["known_food"] = known_food

    observation["memory_system"] = npc.memory

    memories = npc.memory.retrieve(
        observation
    )

    action, scores = brain.decide(
        observation,
        memories
    )

    result = npc.perform_action(
        action
    )

    world.remove_empty_food()

    npc.memory.remember(
        observation,
        action,
        result
    )

    # --------------------------------------------------------
    # Console
    # --------------------------------------------------------

    print_tick(
        world,
        npc,
        observation,
        action,
        scores,
        result,
        memories
    )

    # --------------------------------------------------------
    # Rendering
    # --------------------------------------------------------

    draw()

    # --------------------------------------------------------
    # Simulation speed
    # --------------------------------------------------------

    clock.tick(FPS)


# ============================================================
# Shutdown
# ============================================================

pygame.quit()