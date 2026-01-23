# Space Explorer — dokumentacja projektu

**Autor:** Andrzej Raczkowski  
**Licencja:** MIT  
**Data dokumentu:** 2026-01-22

---

## 1. Czym jest Space Explorer

Space Explorer to izometryczna gra eksploracyjno‑survivalowa zbudowana w **Python + Pygame**. Gracz steruje statkiem na kafelkowej mapie (tilemap) i realizuje pętlę rozgrywki:

**eksploracja → wydobycie zasobów → zarządzanie ekwipunkiem → powrót do bazy → depozyt / sprzedaż → ulepszenia → progres (misje + odblokowanie planet)**

W aktualnej wersji projektu występują co najmniej dwie planety/biomy:
- **Moon** — planeta startowa,
- **Mars** — planeta odblokowywana po spełnieniu warunku (misje).

Gra jest zorganizowana modułowo: logika świata, encje, systemy ekonomii/progresu oraz UI są rozdzielone na osobne foldery.

---

## 2. Najważniejsze elementy rozgrywki

### 2.1. Sterowanie (wg `core/game.py`)
- **WASD** — ruch statku (z kolizjami i spalaniem paliwa)
- **E** — interakcja kontekstowa:
  - przy bazie: wejście do bazy (BaseUI),
  - na złożu: zebranie/„wydobycie” rudy (dodanie do inventory)
- **I** — otwórz/zamknij ekwipunek (INVUI)
- **T** — otwórz/zamknij tutorial overlay
- **ESC** — ekran zapisu/odczytu (Save/Load screen) w trakcie gry
- **1** — teleport na Mars (gdy Mars jest odblokowany)

> Uwaga: konkretne skróty w menu bazy są opisane w stopce BaseUI (np. strzałki/ENTER).

### 2.2. Baza (hub)
Baza jest stałym punktem na mapie (`world.base_pos`). W bazie gracz ma dostęp do:
- **Storage** — przenoszenie przedmiotów z ekwipunku do magazynu bazy,
- **Upgrades** — ulepszenia „materiałowe” (koszt w surowcach z magazynu bazy),
- **Missions** — podgląd misji dla aktualnej planety,
- **Cantor** — sprzedaż zasobów z magazynu bazy za złoto,
- **Gold Shop** — zakupy ulepszeń za złoto (np. speed / max fuel).

### 2.3. Ekwipunek (Inventory)
Ekwipunek jest **slotowy** oraz **stackowalny**:
- każdy slot przechowuje `ItemStack`,
- maksymalny rozmiar stacka zależy od definicji itemu (`stack_max` w `data/items.py`),
- liczba slotów zależy od `backpack_lvl` i może być zwiększana.

### 2.4. Paliwo (Fuel)
Statek posiada paliwo, które maleje w trakcie poruszania się:
- spalanie paliwa jest powiązane z ruchem (w `Ship.update()`),
- wejście do bazy w praktyce działa jak „serwis” (odświeżenie/ustawienie parametrów zależnie od implementacji w `Game/BaseUI`),
- przy braku paliwa prędkość jest ograniczana.

### 2.5. Misje i progres
System misji (`MissionTracker`) nalicza postęp m.in. za:
- zbieranie konkretnych itemów (`collect_item`),
- przebyty dystans (`travel`),
- otwarcie danego UI (`open_ui`),
- zdeponowanie itemów do bazy (`deposit_item`).

Misje mogą być filtrowane per planeta (`mission["planet"]`), a ich ukończenie zwiększa licznik ukończeń oraz poziom gracza.

### 2.6. Odblokowanie planet i komunikat HUD
`PlanetManager` posiada zestaw reguł odblokowania planet. Po spełnieniu warunku HUD wyświetla komunikat na górze ekranu:
- **Planet Mars Unlocked - press 1 to teleport**

---

## 3. Ekrany i stany gry (Game States)

W projekcie występuje przełączany stan gry (`self.game_state`) oraz odpowiadające mu UI:

- **`start`** — StartScreen (Nowa gra / Load / Quit)
- **`play`** — właściwa rozgrywka (świat + statek + HUD + overlaye)
- **`save_load`** — ekran zapisu/odczytu (otwierany z `ESC`)
- **`base_menu`** — BaseUI (overlay bazy, otwierany z `E` w pobliżu bazy)

---

## 4. Architektura projektu (warstwy)

Projekt jest rozdzielony na warstwy odpowiedzialności:

- **core** — pętla gry, stany, integracja modułów,
- **world** — generowanie map i API świata (kafelki, kolizje, obiekty),
- **entities** — encje (Ship, Base),
- **render** — izometryczne renderowanie (kamera, tilesety, culling, cache),
- **systems** — logika „biznesowa”: inventory, misje, progres planet, upgrades, shop, zapis/odczyt, sprzedaż,
- **ui** — ekrany i overlaye,
- **data** — definicje itemów/misji/shopu oraz zasoby i zapisy.

### 4.1. Połączenia modułów (wysokopoziomowo)

```text
main.py
  └─ Game (game/core/game.py)
      ├─ World (game/world/planets.py -> world_map.py / mars_map.py)
      ├─ Ship (game/entities/ship.py)
      ├─ Base (game/entities/base.py)
      ├─ Camera (game/render/camera.py)
      ├─ IsoRender (game/render/iso_render.py) -> TileSet (game/render/TileSets.py)
      ├─ Systems:
      │    ├─ Inventory (game/systems/inventory.py)
      │    ├─ MissionTracker (game/systems/missions.py) -> data/missions.py
      │    ├─ PlanetManager (game/systems/planet_menageer.py)
      │    ├─ UpgradeSystem (game/systems/upgrade.py)
      │    ├─ Shop (game/systems/shop.py) -> data/shop.py
      │    ├─ SaveSystem (game/systems/save_system.py)
      │    └─ Cantor (game/systems/cantor.py)
      └─ UI:
           ├─ HUD (game/ui/hud.py)
           ├─ BaseUI (game/ui/base_ui.py)
           ├─ INVUI (game/ui/inventory_ui.py)
           ├─ PlayerUI (game/ui/player_ui.py)
           ├─ StartScreen (game/ui/start_screen.py)
           ├─ SaveLoadScreen (game/ui/save_load_screen.py)
           └─ Tutorial (game/ui/tutorial.py)
```

---

## 5. Struktura katalogów i odpowiedzialności

Poniższa sekcja opisuje zawartość folderów zgodnie z aktualną strukturą projektu.

### 5.1. `game/core/`
- `game.py` — klasa `Game`, integrator wszystkich komponentów:
  - inicjalizacja Pygame, okna (np. 1366×768), muzyki,
  - budowa świata (`build_world()`), stworzenie Ship/Base, systemów i UI,
  - obsługa pętli gry i przełączanie stanów.

### 5.2. `game/world/`
- `planets.py` — fabryka `build_world(planet_id)`:
  - zwraca obiekt świata dla danej planety (Moon/Mars).
- `world_map.py` — mapa Moon:
  - przechowuje `tile_data`, `objects_by_type`, `blocked_tiles`,
  - generuje przeszkody i złoża (np. drzewa, iron ore),
  - udostępnia `get_tile()` oraz metody do kolizji.
- `mars_map.py` — mapa Mars:
  - tworzy „ramkę” ścian na granicach mapy,
  - proceduralnie rozstawia przeszkody i złoża (np. `tree_mars`, `dust_dune`, `red_hematite_ore`),
  - zarządza `objects_by_type` i `blocked_tiles`.

### 5.3. `game/entities/`
- `ship.py` — `Ship` (gracz):
  - pozycja w tile space (`tx`, `ty`) + ruch i kolizje,
  - paliwo i prędkość,
  - `Inventory` gracza,
  - statystyki progresu (lvl, gold, backpack_lvl, mining_lvl),
  - serializacja stanu (get/set).
- `base.py` — `Base`:
  - pozycja bazy (`tx`, `ty`),
  - magazyn (Inventory),
  - logika depozytu i serializacja.

### 5.4. `game/render/`
- `camera.py` — `Camera`:
  - offset, zoom, centrowanie na obiekcie (`center_on`).
- `iso_render.py` — `IsoRender`:
  - izometryczna transformacja `tile_to_screen(tx, ty)`,
  - rysowanie tilemapy i obiektów (`objects_by_type`) z kolejnością izometryczną,
  - cache skalowania (wydajność),
  - rysowanie bazy i hintów (np. „Press E…”).
- `TileSets.py` — tilesety:
  - `MoonTileSet` i `MarsTileSet`: definicje tile’i i sprite’ów (np. `ore_iron`, `tree_mars`, `red_hematite_ore`).

### 5.5. `game/systems/`
- `inventory.py` — `Inventory` + `ItemStack`:
  - dodawanie/usuwanie itemów, stackowanie, resize,
  - liczenie zasobów, serializacja.
- `missions.py` — `MissionTracker`:
  - aktualizacja postępu misji i oznaczanie ukończenia,
  - filtrowanie misji per planeta,
  - naliczanie `compleated_count` i przyrostu levelu.
- `planet_menageer.py` — `PlanetManager`:
  - aktualna planeta (`current_id`) i zbiór odblokowanych (`unlocked`),
  - reguły odblokowania (np. Mars po ukończeniu określonej liczby misji),
  - serializacja.
- `upgrade.py` — `UpgradeSystem`:
  - koszty zależne od planety (`COSTS_BY_PLANET`),
  - sprawdza zasoby w magazynie bazy i poziom gracza,
  - podbija parametry gracza (np. backpack_lvl, mining_lvl).
- `shop.py` — `Shop`:
  - zakupy za złoto (np. speed / fuel),
  - po zakupie cena rośnie (`* 1.5`), ceny są zapisywane w save.
- `cantor.py` — `Cantor`:
  - sprzedaż itemów z magazynu bazy,
  - cena jednostkowa pochodzi z `data/items.py` (`value`),
  - transakcja „tnie” ilość do posiadanej i zwraca `(sold, earned)`.
- `save_system.py` — `SaveSystem`:
  - zapis/odczyt w JSON do `game/data/save/`,
  - atomowy zapis przez `.tmp` + `os.replace()`.

### 5.6. `game/ui/`
- `hud.py` — HUD:
  - hint wejścia do bazy,
  - komunikat o odblokowaniu Marsa na górze ekranu.
- `inventory_ui.py` — INVUI:
  - rysowanie slotów, stacków i ikon itemów (`icon_paths`),
  - overlay w stanie `play`.
- `player_ui.py` — PlayerUI:
  - panel parametrów gracza + paliwo.
- `base_ui.py` — BaseUI:
  - overlay bazy i podstany: storage / upgrade / missions / cantor / gold_shop,
  - obsługa nawigacji, wyboru oraz wywołań systemów (depo, upgrade, sprzedaż, zakupy).
- `start_screen.py` — StartScreen: menu startowe.
- `save_load_screen.py` — SaveLoadScreen: zapis/odczyt.
- `tutorial.py` — Tutorial: overlay instrukcji (różny per planeta).

### 5.7. `game/data/`
- `items.py` — `ITEMS`: definicje itemów (nazwa, kategoria, stack_max, value, opis).
- `missions.py` — `MISSIONS`: definicje misji (importowane przez MissionTracker).
- `shop.py` — `SHOP`: definicje ulepszeń w Gold Shop (importowane przez Shop).
- `assets/` — grafiki i audio. (https://itch.io/game-assets/free/tag-top-down)
- `save/` — JSON-y zapisów.

---

## 6. Pętla gry (Game Loop) — jak to działa w praktyce

### 6.1. Klasyczny schemat w `Game.run()`
1. **Tick / dt**: `clock.tick(FPS)` wyznacza krok czasu.
2. **Input**: `handle_events()` zbiera eventy Pygame i:
   - przełącza stany (`start`, `play`, `save_load`, `base_menu`),
   - wywołuje interakcje (E, I, T, 1, ESC),
   - deleguje eventy do aktywnych ekranów UI (StartScreen/SaveLoadScreen/BaseUI).
3. **Update** (głównie w `play`):
   - `Ship.update(dt, world)` — ruch, kolizje, paliwo,
   - centrowanie kamery na graczu,
   - liczenie dystansu (misje `travel`),
   - wykrywanie „kontekstu” (near_base / near_ore).
4. **Render**: `draw()` rysuje:
   - świat (IsoRender + TileSet),
   - encje i obiekty,
   - HUD / PlayerUI / INVUI / Tutorial,
   - lub odpowiedni ekran stanu (StartScreen/SaveLoad/BaseUI).

### 6.2. Minimalna maszyna stanów (logika)
- `start` → `play` po wybraniu „New Game” albo po załadowaniu zapisu,
- `play` → `base_menu` po `E` (gdy `near_base`),
- `play` → `save_load` po `ESC`,
- `save_load` → `play` po wyjściu z ekranu zapisu/odczytu,
- `base_menu` → `play` po zamknięciu BaseUI.

---

## 7. Mechaniki: przepływ danych i integracja systemów

### 7.1. Kolizje
Kolizje bazują na:
- ścianach tilemapy (`tile_id == WALL`),
- `blocked_tiles` (przeszkody obiektowe, np. drzewa/wydmy).

Statek porusza się w tile space i testuje docelowy kafel poprzez `world.is_blocked(...)`.

### 7.2. Wydobycie / zbieranie rud
Schemat interakcji:
1. `Game.is_near_ore()` wykrywa, czy aktualny kafel gracza jest jednym z obiektów w `world.objects_by_type`.
2. Po wciśnięciu `E`:
   - następuje mapowanie `sprite_id → item_id` (np. `red_hematite_ore → hematite_ore`),
   - `Inventory.add(item_id, qty)` próbuje dodać item,
   - obiekt jest zdejmowany z mapy,
   - `MissionTracker.on_item_collected(item_id, qty)` aktualizuje misje.

### 7.3. Depozyt do bazy
W BaseUI (storage) gracz może przenieść itemy:
- źródło: `player.inventory`,
- cel: `base.storage`,
- po depozycie aktualizowane są misje `deposit_item`.

### 7.4. Ekonomia: Cantor i Gold Shop
- **Cantor**: sprzedaje itemy z **magazynu bazy** po cenie `ITEMS[item_id]["value"]` i dopisuje złoto do gracza.
- **Gold Shop**: kupuje ulepszenia za złoto:
  - `speed_upgrade` wpływa na `player.base_speed`,
  - `fuel_upg` wpływa na `player.max_fuel`,
  - ceny rosną po zakupie i są zapisywane w save.

### 7.5. Ulepszenia „materiałowe” (Upgrades)
`UpgradeSystem` konsumuje zasoby z magazynu bazy oraz podbija levele/parametry gracza (np. backpack/mining). Koszty mogą się różnić zależnie od planety.

### 7.6. Progres planet
`PlanetManager` trzyma:
- `current_id` (np. `moon`),
- `unlocked` (zbiór odblokowanych planet),
- `unlock_rules` (warunki odblokowania, np. na podstawie ukończonych misji).

Po odblokowaniu HUD pokazuje komunikat, a klawisz `1` teleportuje na Mars.

---

## 8. Zapis i odczyt (Save/Load)

### 8.1. Lokalizacja zapisów
Zapis odbywa się do katalogu:
- `game/data/save/`

### 8.2. Co jest zapisywane
System zapisu przechowuje m.in.:
- stan gracza (pozycja, inventory, paliwo, złoto, levele),
- stan bazy (storage),
- stan misji (progress, completed, current_planet),
- stan shopu (ceny),
- stan planet (aktualna planeta + odblokowane).

### 8.3. Atomowy zapis
Zapis przebiega przez plik tymczasowy `.tmp`, a następnie jest podmieniany przez `os.replace()`, co minimalizuje ryzyko uszkodzenia zapisu.

---

## 9. Schematy danych

Ta sekcja dokumentuje formaty, które powinny istnieć w `game/data/missions.py` oraz `game/data/shop.py` (ponieważ systemy importują te moduły).

### 9.1. `data/missions.py` — `MISSIONS`
`MISSIONS` to słownik:
- **klucz**: `mission_id` (string),
- **wartość**: dict z polami:

Wymagane:
- `title` (str) — nazwa misji do UI,
- `type` (str) — jeden z: `collect_item`, `travel`, `open_ui`, `deposit_item`,
- `params` (dict) — parametry zależne od `type`,
- `target` (int/float) — próg ukończenia.

Opcjonalne (w praktyce używane):
- `planet` (str) — np. `moon` / `mars` (MissionTracker filtruje po aktualnej planecie),
- `is_compleated` (bool) — flaga ustawiana po ukończeniu (zachowana pisownia jak w kodzie).

Przykłady rekordów:
- **collect_item**: `params: { "item_id": "iron_ore" }`
- **deposit_item**: `params: { "item_id": "iron_ore" }`
- **open_ui**: `params: { "ui": "inventory" }`
- **travel**: `params: {}` (lub inne według potrzeb)

### 9.2. `data/shop.py` — `SHOP`
`SHOP` to słownik:
- **klucz**: `upgrade_id` (string),
- **wartość**: dict z polami:

Wymagane (wg `Shop` i `BaseUI`):
- `title` (str) — nazwa do wyświetlenia,
- `price` (int) — koszt w złocie,
- `value` (int/float) — wartość efektu (np. +speed, +max_fuel).

Klucze oczekiwane przez logikę zakupów:
- `speed_upgrade`
- `fuel_upg`

---

## 10. Uruchomienie projektu

### 10.1. Wymagania
- Python 3.10+ (zalecane)
- Pygame

Instalacja:
- `pip install pygame`

### 10.2. Start gry
W katalogu głównym projektu znajduje się `main.py` (entrypoint). Typowy start:
- `python main.py`

---

## 11. Rozszerzanie projektu (najczęstsze scenariusze)

### 11.1. Dodanie nowego itemu / rudy
1. Dodaj wpis w `game/data/items.py` (`stack_max`, `value`, `description`).
2. Dodaj ikonę do `game/data/assets/` i dopisz ścieżkę w `INVUI.icon_paths` (`ui/inventory_ui.py`).
3. Dodaj sprite do tilesetu (`render/TileSets.py`) oraz mapowanie w świecie (np. `mars_map.py`).
4. Dodaj mapowanie `sprite_id → item_id` w logice interakcji w `Game`.

### 11.2. Dodanie misji
1. Dopisz rekord w `game/data/missions.py` zgodnie ze schematem z sekcji 9.1.
2. Upewnij się, że zdarzenie jest wywoływane:
   - `on_item_collected`, `on_distance`, `on_ui_open`, `on_item_depo`.
3. Przypisz `planet`, aby misja pojawiała się na właściwej planecie.

### 11.3. Dodanie nowej planety
1. Zaimplementuj mapę w `game/world/` z analogicznym API do `WorldMap`/`MarsMap`:
   - `get_tile()`, `is_blocked()`, `objects_by_type`, `blocked_tiles`, `base_pos`.
2. Dodaj obsługę w `build_world()` w `planets.py`.
3. Dodaj tileset w `render/TileSets.py`.
4. Dodaj reguły w `PlanetManager.unlock_rules`.
5. Rozszerz HUD/Tutorial o informację dla nowej planety.

---

## 12. Autorstwo i licencja

**Autor:** Andrzej Raczkowski  
**Licencja:** MIT

Rekomendacja repozytoryjna: w katalogu głównym dodaj plik `LICENSE` z treścią licencji MIT oraz krótką notę w README.

