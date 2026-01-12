from .world_map import WorldMap

def build_world(planet_id: str):
    if planet_id == "moon":
        return WorldMap()
    if planet_id == "mars":
        return WorldMap()
    raise ValueError(f"Unknown planet_id: {planet_id}")