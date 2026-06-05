# Ratventure

A text-based roguelike adventure game built in Python. You play as a hero who must fight through hordes of rats, defeat a fearsome Guardian, and finally confront the Rat King to break the curse on the kingdom.

---

## Features

- **Procedural map** — configurable grid size (5×5 minimum), randomised Rat King placement each run
- **6 enemy types** — Rat Minion, Plague Rat, Stealth Rat, Rat Guardian, Rat King, and a passive Friendly Rat
- **Levelling system** — gain EXP from battles, level up to Lv.10 with increasing HP and stats
- **Inventory** — health packs and a weapon can drop from enemies
- **Healing springs** — rest at marked tiles to recover HP between fights
- **Dynamic combat** — armor mitigation, poison damage, boss healing, dodge mechanics, and flee attempts
- **Rich enemy dialogue** — each enemy has context-aware taunts and flavour text
- **Morality mechanic** — killing the Friendly Rat punishes the hero

---

## Requirements

- Python 3.9 or higher
- No third-party dependencies — standard library only

---

## Installation

```bash
git clone https://github.com/keanedt/Ratventure.git
cd Ratventure
python main.py
```

---

## How to Play

### Objective

Defeat **10 rats** to trigger the Guardian's arrival, kill the **Rat Guardian** to earn the chance for the key to drop, collect the **Key**, then reach and defeat the **Rat King**.

### Controls

| Key | Action |
|-----|--------|
| `W` | Move North |
| `S` | Move South |
| `A` | Move West |
| `D` | Move East |

### Movement Menu

```
1. Move
2. Help
3. Backpack
0. Quit
```

### Combat Menu

```
1. Attack
2. Flee (50% success)
3. Use Health Pack
```

### Map Symbols

| Symbol | Meaning |
|--------|---------|
| `H` | Your hero |
| `X` | Rat King (visible only with the Key) |
| `?` | Guardian imminent (10th rat approaching) |
| `~` | Healing spring |

---

## Enemy Guide

| Enemy | HP | Damage | Spawn Rate | Notes |
|-------|----|--------|------------|-------|
| Rat Minion | 6–22 | 1–4 | 60% | Standard enemy |
| Plague Rat | 4–16 | 2–5 + poison | 20% | 1–3 poison damage per round |
| Stealth Rat | 4–16 | 1–5 | 20% | 33% dodge chance |
| Rat Guardian | 30 | 4–8 | Required boss | Heals 3–6 HP/round, can't be fled |
| Rat King | 48 | 5–11 + poison | Final boss | Heals 5–9 HP/round, can't be fled |
| Friendly Rat | 10 | 0 | 10% | Passive — killing it drops your HP to 5 |

---

## Game Progression

```
Start
  │
  ├─ Explore map, fight rats (Minion / Plague / Stealth / Friendly)
  │    └─ Gain EXP → level up → find health packs & weapon
  │
  ├─ Kill 10 rats → Rat Guardian appears, blocking progress
  │
  ├─ Defeat Guardian → rats can now drop the Key
  │
  ├─ Collect the Key → Rat King's location (X) revealed on map
  │
  └─ Reach Rat King → fight the final boss → Victory
```

---

## Hero Stats

| Stat | Starting Value | Growth |
|------|---------------|--------|
| HP | 20 | +3 max HP per level |
| Armor | 0 | Found as loot |
| Weapon | Bare hands | Found as loot |
| Health Packs | 0 | Found as loot |

Levelling up also heals 50% of your new max HP.

---

## Project Structure

```
Ratventure/
├── main.py        # Entry point and replay loop
├── game.py        # Core game loop, map logic, menus
├── combat.py      # Combat system and damage calculations
├── entities.py    # Hero and all enemy classes
├── display.py     # ASCII art rendering and map display
└── README.md
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.
