from ..data.missions import MISSIONS

class MissionTracker:
    def __init__(self, player):
        self.missions = MISSIONS
        self.progress = {mission_id: 0 for mission_id in self.missions}
        self.completed = set()
        self.player = player
        

    def _mark_done_if_needed(self, mission_id):
        target = self.missions[mission_id]["target"]
        if self.progress[mission_id] >= target:
            self.progress[mission_id] = target
            self.completed.add(mission_id)
            self.missions[mission_id]['is_compleated'] = True
            self.player.lvl += 0.5
            print(self.player.lvl)
            
            

    def on_item_collected(self, item_id, qty):
        if qty <= 0:
            return

        for mission_id, mission in self.missions.items():
            if mission["type"] != "collect_item":
                continue
            if mission["params"].get("item_id") != item_id:
                continue
            if mission_id in self.completed:
                continue

            self.progress[mission_id] += qty
            self._mark_done_if_needed(mission_id)

    def on_distance(self, delta_units):

        for mission_id, mission in self.missions.items():
            if mission["type"] != "travel":
                continue
            if mission_id in self.completed:
                continue
            
            self.progress[mission_id] += delta_units
            self._mark_done_if_needed(mission_id)


    def on_ui_open(self, ui_name):
        for mission_id, mission in self.missions.items():
            if mission['type'] != 'open_ui':
                continue
            if mission['params'].get('ui') != ui_name:
                continue
            if mission_id in self.completed:
                continue

            self.progress[mission_id] += 1
            self._mark_done_if_needed(mission_id)

    def on_item_depo(self, item_id, qty):
        for mission_id, mission in self.missions.items():
            if mission['type'] != 'deposit_item':
                continue
            if mission['params'].get('item_id') != item_id:
                continue
            if mission_id in self.completed:
                continue

            self.progress[mission_id] += qty
            self._mark_done_if_needed(mission_id)


    def get_row(self, mission_id):
        m = self.missions[mission_id]
        prog = self.progress.get(mission_id, 0)
        target = m["target"]
        done = mission_id in self.completed
        return (m["title"], prog, target, done)

    def iter_rows(self):
        for mission_id in self.missions:
            yield mission_id, self.get_row(mission_id)

    def debug_msg(self):
        print(self.progress)
        print(self.completed)
