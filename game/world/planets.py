from .world_map import WorldMap
from .mars_map import MarsMap

def build_world(planet_id: str):
    if planet_id == "moon":
        w = WorldMap()
        w.create_tree()
        w.create_iron_ores()
        return w

    if planet_id == "mars":
        return MarsMap(w=128, h=128, base_pos=(15, 15))

    raise ValueError(f"Unknown planet_id: {planet_id}")
