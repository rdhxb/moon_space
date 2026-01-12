# game/systems/planet_manager.py

class PlanetManager:
    def __init__(self):
        self.current_id = "moon"
        self.unlocked = {"moon"}

        self.unlock_rules = {
            "mars": {"completed_missions": 1}
        }

    def is_unlocked(self, planet_id: str) -> bool:
        return planet_id in self.unlocked

    def can_unlock(self, planet_id: str, completed_missions: int) -> bool:
        rule = self.unlock_rules.get(planet_id)
        if not rule:
            return False
        return completed_missions >= rule["completed_missions"]

    def try_unlock(self, completed_missions: int) -> list[str]:
        newly = []
        for planet_id in self.unlock_rules.keys():
            if planet_id not in self.unlocked and self.can_unlock(planet_id, completed_missions):
                self.unlocked.add(planet_id)
                newly.append(planet_id)
        return newly

    def set_current(self, planet_id: str):
        if planet_id not in self.unlocked:
            return False
        self.current_id = planet_id
        return True
