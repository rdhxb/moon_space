# Space Explorer

Izometryczna gra eksploracyjno‑survivalowa stworzona w **Python + Pygame**. Gracz steruje statkiem na kafelkowej mapie, zbiera zasoby, wraca do bazy, zarządza magazynem, realizuje misje i odblokowuje kolejne planety.

## Najważniejsze elementy

- **Izometryczny render (tilemap)** z kamerą i offsetami.
- **Dwie planety/biomy**:
  - **Moon** (start),
  - **Mars** (odblokowanie po spełnieniu warunku progresu).
- **Zasoby i rudy** (różne typy na Marsie), zbierane bezpośrednio na mapie.
- **Ekwipunek** (stackowanie), **magazyn bazy** oraz **sprzedaż** (Cantor).
- **System misji** (progres, warunek odblokowania planet).
- **Ulepszenia** (UpgradeSystem) powiązane z zasobami z magazynu bazy.
- **Save/Load** (zapis do plików JSON w `game/data/save/`).

## Pętla rozgrywki (game loop)

1. **Eksploracja** planety (ruch statku, kamera, kolizje).
2. **Pozyskiwanie zasobów** (interakcja z obiektami na mapie).
3. **Zarządzanie ekwipunkiem** i decyzja: zachować / przenieść do magazynu / sprzedać.
4. **Powrót do bazy**: magazyn, sklep/sprzedaż, ulepszenia.
5. **Misje i progres** → odblokowanie Marsa → kontynuacja pętli na nowych lokacjach.

W kodzie pętla jest realizowana w klasie `Game` (`game/core/game.py`) poprzez schemat:
**handle_events → update → draw** w stałym FPS.

## Sterowanie (skrót)

- **WASD** — ruch statku
- **E** — interakcja kontekstowa (baza / złoże)
- **I** — ekwipunek
- **T** — tutorial overlay
- **ESC** — ekran zapisu/odczytu w trakcie gry
- **1** — teleport na Mars (gdy odblokowany)

## Struktura projektu

Najważniejsze katalogi:

- `game/core/` — główny runtime gry (`Game`, game states, pętla gry)
- `game/world/` — generowanie i reprezentacja świata (Moon/Mars, tile data, obiekty)
- `game/render/` — render izometryczny, kamera, tilesety
- `game/entities/` — encje (Ship, Base)
- `game/systems/` — logika systemowa (inventory, missions, planet manager, save, shop, upgrades, cantor)
- `game/ui/` — warstwy UI (HUD, BaseUI, Inventory UI, ekrany start/save/load, tutorial)
- `game/data/` — dane gry (items/missions/shop) + `assets/` i `save/`

Minimalna mapa zależności (wysoki poziom):

- `core/game.py` orkiestruje całość i łączy: `world/*`, `render/*`, `entities/*`, `systems/*`, `ui/*`.
- `world/*` dostarcza tilemapę i obiekty; `render/*` rysuje świat na podstawie kamery.
- `entities/*` trzyma stan gracza/bazy; `systems/*` modyfikują stan (misje, sklep, ulepszenia, zapis).
- `ui/*` prezentuje stan (HUD, menu bazy, inventory) i obsługuje interakcje.

## Instalacja i uruchomienie

### Wymagania
- Python 3.10+ (zalecane)
- Pygame

### Instalacja zależności
```bash
pip install pygame
```

### Start gry
W katalogu głównym repozytorium:
```bash
python main.py
```

## Zapisy gry

Zapisy są tworzone jako pliki JSON w:
- `game/data/save/` (np. `player.json`, `base.json`, `mission.json`, `shop.json`, `planet.json`)

Mechanizm zapis/odczyt zapewnia `game/systems/save_system.py`.

## Progres i odblokowanie planet

Logika progresu planet jest w `game/systems/planet_menageer.py`:
- Start: `moon`
- Odblokowanie: `mars` po spełnieniu warunku (np. liczba ukończonych misji)

## Autor i licencja

**Autor:** Andrzej Raczkowski  
**Licencja:** MIT

> Repozytorium nie musi zawierać pełnego tekstu licencji w README — zalecane jest dodanie pliku `LICENSE` w root projektu (MIT).
