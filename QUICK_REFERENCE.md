# Quick Reference - Loaves and Fishes

Fast lookup guide for developers. For detailed explanations, see `DEVELOPER_GUIDE.md`.

---

## Core Formulas

### Damage Calculation
```
damage = (base_power + ATK/2) × type_effectiveness × STAB × crit × random(0.85, 1.0)

type_effectiveness: 0.5x, 1.0x, 1.5x, or 2.0x
STAB (Same Type Attack Bonus): 1.2x if move type matches fish type
crit: 1.5x (5% chance)
```

### Defense Reduction
```
actual_damage = damage × (100 / (100 + defense))

Example:
- Defense 0: 100% damage
- Defense 50: 67% damage
- Defense 100: 50% damage
```

### Stat Growth
```
stat = base_stat × (1 + 0.07 × (level - 1))

Example (Base ATK 20):
- Level 1: 20
- Level 10: 32
- Level 50: 88
```

### Flee Chance
```
flee_chance = 50% + (speed_ratio - 1) × 20%

speed_ratio = player_fish_spd / enemy_spd

Example:
- Equal speed (1.0): 50%
- 50% faster (1.5): 60%
- 50% slower (0.5): 40%
```

### Miracle Meter
```
Fills from:
- Damage dealt: +0.1% per damage point
- Damage taken: +0.2% per damage point (desperation mechanic)
- Fish fainting: +10%
- Apostle use: +5%

Max: 100%
```

---

## Type Chart Quick Lookup

| Attacker → Defender | Holy | Water | Earth | Spirit | Dark |
|---------------------|------|-------|-------|--------|------|
| **Holy**            | 1.0  | 1.0   | 1.0   | 1.0    | **2.0** |
| **Water**           | 1.0  | 0.5   | **2.0**| 1.0   | 1.0  |
| **Earth**           | 1.0  | 0.5   | 1.0   | 1.0    | 1.0  |
| **Spirit**          | **1.5**| 1.0 | 1.0   | 1.0    | **1.5** |
| **Dark**            | 0.5  | 1.0   | 1.0   | 0.5    | 1.0  |

**Bold = Super effective (1.5x or 2.0x)**

**Key matchups:**
- Holy → Dark (2.0x): Light defeats darkness
- Water → Earth (2.0x): Water erodes earth
- Spirit → Holy/Dark (1.5x): Versatile spiritual power

---

## Common Code Patterns

### Load Data
```python
from utils.data_loader import get_data_loader, get_fish, get_apostle

# Get singleton loader
loader = get_data_loader()

# Get all fish
all_fish = loader.get_all_fish()

# Get specific fish
fish_data = loader.get_fish_by_id("holy_mackerel")

# Convenience functions
fish_data = get_fish("holy_mackerel")
apostle_data = get_apostle("peter")
```

### Create Fish Instance
```python
from engine.fish import Fish
from utils.data_loader import get_fish

# Get fish data from JSON
fish_data = get_fish("holy_mackerel")

# Create fish instance at level 5
fish = Fish("holy_mackerel", fish_data, level=5)

# Use fish
print(fish.name)  # "Holy Mackerel"
print(fish.max_hp)  # Calculated from base + level
```

### Battle Flow
```python
from engine.battle import Battle, BattleAction

# Create battle
battle = Battle(player, enemies, is_boss=False)

# Execute turn
result = battle.execute_turn(BattleAction.ATTACK, move_index=0)

# Check result
if result == BattleResult.VICTORY:
    print("Won!")
elif result == BattleResult.DEFEAT:
    print("Lost!")
```

### Access Dual-Text
```python
# All user-facing text has dual-text structure
fish_data = get_fish("holy_mackerel")

# Get text for current edition
edition = "default"  # or "christian_edition"
flavor = fish_data["flavor_text"][edition]

# Function to get text safely
def get_text(text_field, edition="default"):
    if isinstance(text_field, dict):
        return text_field.get(edition, text_field.get("default", ""))
    return text_field  # Fallback for non-dual-text
```

### Save/Load Fish
```python
# Save fish to dictionary
fish_dict = fish.to_dict()
# Returns: {"fish_id": "holy_mackerel", "level": 5, "xp": 120, ...}

# Load fish from dictionary
fish_data = get_fish(saved_dict["fish_id"])
fish = Fish.from_dict(saved_dict, fish_data)
```

---

## File Locations

### Code Structure
```
src/
├── engine/          # Core game systems
│   ├── battle.py    # Combat system
│   ├── fish.py      # Fish class
│   ├── player.py    # Player class
│   └── enemy.py     # Enemy classes
├── ui/              # User interface (future)
├── utils/           # Utilities
│   ├── data_loader.py  # JSON loading
│   └── constants.py    # Balance numbers
└── data/            # JSON game data
    ├── fish.json
    ├── enemies.json
    ├── apostles.json
    ├── items.json
    └── towns.json
```

### Important Files
- **Constants:** `src/utils/constants.py` (all balance numbers)
- **Type chart:** `src/utils/constants.py:TYPE_CHART`
- **Fish data:** `src/data/fish.json`
- **Damage formula:** `src/engine/battle.py:calculate_damage()`
- **Stat growth:** `src/engine/fish.py:_calculate_stat()`

---

## JSON Structure Quick Reference

### Fish Entry
```json
{
  "id": "holy_mackerel",
  "name": "Holy Mackerel",
  "tier": 1,
  "type": "Holy",
  "base_stats": {
    "hp": 50,
    "atk": 30,
    "def": 25,
    "spd": 35
  },
  "property": {
    "name": "Divine Protection",
    "effect": "damage_reduction_alone",
    "value": 0.5
  },
  "moves": [
    {
      "name": "Holy Splash",
      "type": "Holy",
      "category": "Physical",
      "power": [40, 60],
      "accuracy": 100,
      "level": 1,
      "description": {
        "default": "A blessed splash of water",
        "christian_edition": "Blessed waters from the Jordan"
      }
    }
  ],
  "flavor_text": {
    "default": "A righteous force of nature!",
    "christian_edition": "Blessed with divine power."
  }
}
```

### Enemy Entry
```json
{
  "id": "pharisee",
  "name": "Pharisee",
  "enemy_type": "Holy",
  "base_stats": {
    "hp": 60,
    "atk": 25,
    "def": 20,
    "spd": 30
  },
  "attacks": [
    {
      "name": "Judgment",
      "type": "Holy",
      "power": [35, 50],
      "accuracy": 95
    }
  ],
  "xp_reward": 50,
  "money_reward": 25,
  "flavor_text": {
    "default": "Judges harshly from their high horse",
    "christian_edition": "Religious leaders who test Jesus"
  }
}
```

### Dual-Text Template
```json
{
  "text_field": {
    "default": "Irreverent, funny, snarky version",
    "christian_edition": "Reverent, educational, respectful version"
  }
}
```

---

## Balance Numbers

### Core Constants
```python
# From constants.py

# Leveling
MAX_LEVEL = 50
XP_PER_LEVEL = 100  # Flat XP per level

# Party
MAX_PARTY_SIZE = 4
MAX_FISH_STORAGE = 999

# Combat
BASE_CRIT_CHANCE = 0.05  # 5%
CRIT_MULTIPLIER = 1.5    # 50% bonus

# Miracle Meter
MIRACLE_METER_MAX = 100
MIRACLE_GAIN_PER_DAMAGE_DEALT = 0.1  # 0.1% per damage
MIRACLE_GAIN_PER_DAMAGE_TAKEN = 0.2  # 0.2% per damage
MIRACLE_GAIN_FISH_FAINT = 10         # 10% when fish faints
```

### Recommended Stat Ranges

**Level 1 Fish:**
- HP: 40-60
- ATK: 20-35
- DEF: 15-30
- SPD: 25-40

**Level 1 Enemy:**
- HP: 50-80
- ATK: 15-30
- DEF: 10-25
- SPD: 20-35

**Boss (Level 10):**
- HP: 200-300
- ATK: 50-70
- DEF: 40-60
- SPD: 40-60

---

## Git Workflow

```bash
# Start new feature
git checkout -b feature/my-feature

# Make changes
git add .
git commit -m "Add feature description"

# Push changes
git push -u origin feature/my-feature

# After PR approved, merge to main
git checkout main
git pull origin main
```

**Commit Message Format:**
```
Add/Update/Fix: Brief description

- Specific change 1
- Specific change 2

Closes #123 (if fixing issue)
```

---

## Testing Checklist

### When Adding New Fish
- [ ] Entry in `fish.json` with all required fields
- [ ] Dual-text for `flavor_text` and move `description`
- [ ] `id` matches filename convention (lowercase, underscores)
- [ ] Sprite file exists: `assets/images/fish/{id}.png`
- [ ] Stats balanced for tier
- [ ] At least one move at level 1
- [ ] Type in TYPE_CHART

### When Modifying Battle System
- [ ] Test all damage scenarios (normal, crit, super effective, resisted)
- [ ] Test victory condition
- [ ] Test defeat condition
- [ ] Test flee mechanic
- [ ] Test miracle meter filling
- [ ] Test fish leveling up
- [ ] Check battle log messages

### When Changing Balance
- [ ] Update `constants.py` (not hardcoded values)
- [ ] Test with existing saves (should work)
- [ ] Document change in commit message
- [ ] Consider impact on all fish/enemies

---

## Common Errors & Quick Fixes

| Error | Quick Fix |
|-------|-----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `KeyError: 'default'` | Add dual-text structure to field |
| `json.JSONDecodeError` | Check JSON syntax (trailing commas, quotes) |
| Image not loading | Verify file exists, check capitalization |
| Audio not playing | Check format (OGG for music, WAV for SFX) |
| Fish stats wrong | Recalculated from base + level (expected) |
| Damage always 1 | Defense too high or ATK too low |
| XP not gained | Check `gain_xp()` called after damage |

---

## Keyboard Shortcuts (Future UI)

```
# Battle
1-4       - Select move
I         - Open items
S         - Switch fish
M         - Use miracle
A         - Call apostle
R         - Run (flee)

# Menu
ESC       - Back/Cancel
ENTER     - Confirm
Arrow Keys - Navigate

# Debug (dev mode)
F1        - Toggle god mode
F2        - Level up active fish
F3        - Fill miracle meter
F12       - Toggle debug info
```

---

## Asset Specifications

### Images
| Type | Size | Format | Notes |
|------|------|--------|-------|
| Fish sprite | 128x128 | PNG | Transparency required |
| Enemy sprite | 128-256 | PNG | Transparency required |
| Background | 1280x720 | PNG/JPEG | 16:9 ratio |
| Item icon | 64x64 | PNG | Small, simple |
| UI button | 200x50 | PNG | Multiple states |

### Audio
| Type | Format | Bitrate | Loop |
|------|--------|---------|------|
| Music | OGG | 128-192kbps | Yes |
| SFX | WAV/OGG | N/A | No |

---

## Useful Commands

### Python
```bash
# Run game
python main.py

# Run tests
pytest tests/

# Check code style
pylint src/

# Format code
black src/
```

### JSON Validation
```bash
# Validate JSON file
python -m json.tool src/data/fish.json

# Or use online: https://jsonlint.com/
```

### Asset Conversion
```bash
# Resize image
convert input.png -resize 128x128 output.png

# Convert audio to OGG
ffmpeg -i input.mp3 -c:a libvorbis output.ogg
```

---

## Links to Full Documentation

- **[README.md](README.md)** - Project overview and setup
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Complete development guide
- **[ASSETS_GUIDE.md](ASSETS_GUIDE.md)** - Working with images and audio
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and fixes
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[TONE_GUIDE.md](TONE_GUIDE.md)** - Writing dual-text content
- **[GODOT_MIGRATION.md](GODOT_MIGRATION.md)** - Godot 4.x migration plan

---

**Need more detail? Check the full docs above!** 📚
