# DEVELOPER GUIDE
## Understanding the Loaves and Fishes Codebase

**Target Audience**: Beginner to intermediate programmers
**Goal**: Help you understand, modify, and extend the game

---

## 📚 TABLE OF CONTENTS

1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [Key Concepts](#key-concepts)
4. [File Structure](#file-structure)
5. [Important Files Explained](#important-files-explained)
6. [How the Dual-Text System Works](#how-the-dual-text-system-works)
7. [How to Add New Content](#how-to-add-new-content)
8. [Common Patterns](#common-patterns)
9. [Debugging Tips](#debugging-tips)
10. [Next Steps](#next-steps)

---

## 🚀 QUICK START

### Running the Game

```bash
# From project root
python main.py
```

### Project Structure (Simplified)

```
loavesandfishes/
├── main.py              # Game entry point - start here!
├── src/
│   ├── data/           # ALL game content (fish, quests, etc.)
│   ├── engine/         # Game logic (battles, fish, player)
│   ├── ui/             # User interface code
│   └── utils/          # Helpers (data loading, constants)
└── saves/              # Player save files
```

---

## 🏗️ ARCHITECTURE OVERVIEW

### The Big Picture

Loaves and Fishes uses a **data-driven architecture**:

```
JSON Data Files ──→ DataLoader ──→ Game Classes ──→ Game Logic
(src/data/)         (utils/)       (engine/)        (main.py)
```

**What this means:**
- **Content** (fish, quests, items) lives in JSON files
- **Code** (battle system, leveling) lives in Python files
- You can add content WITHOUT changing code!

### Why This Matters

**Adding a new fish:**
- ❌ Old way: Write code, compile, test
- ✅ Our way: Edit fish.json, run game

**Benefits:**
- Easy modding (just swap JSON files)
- No programming knowledge needed to add content
- Less chance of bugs (no code changes)
- Dual-text system works automatically

---

## 💡 KEY CONCEPTS

### 1. Data-Driven Design

All game content is in JSON files. The code just knows how to USE that content.

**Example: Fish**

```json
// File: src/data/fish.json
{
  "id": "holy_mackerel",
  "name": "Holy Mackerel",
  "type": "Holy",
  "base_stats": {
    "hp": 50,
    "atk": 30,
    "def": 25,
    "spd": 35
  },
  "flavor_text": {
    "default": "A righteous force of nature!",
    "christian_edition": "Blessed with divine power."
  }
}
```

```python
# File: src/engine/fish.py
class Fish:
    def __init__(self, fish_id, fish_data, level):
        self.name = fish_data["name"]        # Load from JSON
        self.type = fish_data["type"]        # Load from JSON
        self.flavor_text = fish_data["flavor_text"]  # Dual-text!
```

The Fish class doesn't hardcode ANY fish data - it all comes from JSON!

### 2. Dual-Text System

Every user-facing string has TWO versions:

```python
{
  "flavor_text": {
    "default": "Snarky, irreverent version",
    "christian_edition": "Reverent, educational version"
  }
}
```

**How it works:**
1. Player chooses edition at game start
2. Game stores choice (default vs christian_edition)
3. When displaying text, game picks correct version
4. Everything else stays the same!

**Implementation:**
```python
# Get the right version based on player choice
edition = player.edition  # "default" or "christian_edition"
text = fish_data["flavor_text"][edition]
```

See **[TONE_GUIDE.md](TONE_GUIDE.md)** for content guidelines.

### 3. Singleton Pattern (DataLoader)

The DataLoader uses a "singleton" pattern - only ONE instance exists.

**Why?**
- Loads JSON files ONCE (fast)
- Caches data in memory (no re-reading)
- Everyone shares the same cache

**How to use:**
```python
from src.utils.data_loader import get_data_loader

loader = get_data_loader()  # Get the singleton
fish_data = loader.get_fish_by_id("holy_mackerel")
```

No matter where you call `get_data_loader()`, you get the SAME DataLoader.

### 4. Type Effectiveness (Like Pokémon)

Fish have types (Holy, Water, Earth, Spirit, Dark).
Types have strengths and weaknesses:

```python
# Holy vs Dark = 2.0x damage (super effective)
# Water vs Earth = 2.0x damage
# Water vs Water = 0.5x damage (resisted)
```

All defined in **constants.py** `TYPE_CHART`.

---

## 📂 FILE STRUCTURE

### Data Files (src/data/)

All JSON files containing game content:

```
src/data/
├── fish.json          # 21 fish species (complete with dual-text)
├── enemies.json       # 40 enemy types
├── bosses.json        # 13 boss battles
├── quests.json        # 45 quests
├── apostles.json      # 12 apostles (disciples)
├── items.json         # 13 bread items
├── parables.json      # 40 collectible teachings
├── towns.json         # 13 towns to visit
├── messages.json      # Battle/system messages
├── miracles.json      # 4 miracle abilities (limit breaks)
└── ui_strings.json    # UI/menu text
```

**ALL of these have dual-text!** (788 dual-text instances total)

### Engine Files (src/engine/)

Core game logic:

```
src/engine/
├── fish.py            # Fish class (stats, leveling, moves)
├── player.py          # Player class (Jesus, party management)
├── enemy.py           # Enemy & Boss classes
├── battle.py          # Turn-based combat system
├── game_state.py      # Overall game state tracker
├── world_map.py       # Town connections, travel
├── fishing.py         # Fishing mini-game
├── dialogue.py        # Dialogue system
├── town.py            # Town interaction logic
├── combos.py          # Fish + Apostle combo attacks
├── miracles.py        # Miracle system (limit breaks)
└── apostle_abilities.py  # Apostle special abilities
```

### Utility Files (src/utils/)

Helper systems:

```
src/utils/
├── constants.py       # ALL game balance numbers
├── data_loader.py     # JSON loading & caching
└── save_system.py     # Save/load functionality
```

---

## 🔍 IMPORTANT FILES EXPLAINED

### constants.py - Game Balance Central

**What it does:** All the numbers that make the game tick.

**When to edit:**
- Game is too easy/hard
- Leveling is too slow/fast
- Want to change type effectiveness
- Adjusting status effect durations

**Example changes:**
```python
# Make leveling faster
XP_PER_LEVEL = 50  # Was 100

# Make crits hit harder
CRIT_MULTIPLIER = 2.0  # Was 1.5

# Change type matchup
TYPE_CHART["Holy"]["Dark"] = 3.0  # Was 2.0 (now even stronger!)
```

**Documentation:** Every constant has inline comments explaining what it does!

### data_loader.py - JSON Loading System

**What it does:** Reads all JSON files and caches them.

**You rarely need to edit this**, but it's important to understand:

```python
# How it works
loader = get_data_loader()  # Singleton - same instance always
fish_data = loader.get_fish_by_id("holy_mackerel")  # Get specific fish
all_fish = loader.get_all_fish()  # Get all fish
```

**Key features:**
- Caching (files loaded once)
- Error handling (won't crash if JSON is broken)
- Convenience methods (easy to get what you need)

### fish.py - Fish Class

**What it does:** Represents a fish that can battle.

**Key methods:**
- `__init__()` - Create a fish from JSON data
- `_calculate_stat()` - Calculate stat based on level
- `gain_xp()` - Add XP, check for level up
- `level_up()` - Increase level, recalculate stats
- `take_damage()` - Apply damage with defense formula
- `to_dict()` / `from_dict()` - Save/load fish

**How stats work:**
```python
# Formula: stat = base_stat × (1 + 0.07 × (level - 1))
# Example: ATK 20 at level 10
# = 20 × (1 + 0.07 × 9)
# = 20 × 1.63
# = 32.6 → 32
```

Change `growth_rate` in `_calculate_stat()` to adjust power curve.

### battle.py - Combat System

**What it does:** Turn-based battle engine.

**Flow:**
1. Initialize battle (player fish vs enemies)
2. Determine turn order (based on SPD stat)
3. Execute actions (attack, item, switch, etc.)
4. Calculate damage (ATK vs DEF, type effectiveness, crits)
5. Check for victory/defeat
6. Reward XP and money

**Damage formula:**
```python
# 1. Base damage
base_damage = move_power × (attacker_atk / defender_def)

# 2. Type effectiveness
type_mult = TYPE_CHART[move_type][defender_type]

# 3. Critical hit?
if random() < CRIT_CHANCE:
    damage *= CRIT_MULTIPLIER

# 4. Random variation (85-100%)
damage *= random(0.85, 1.0)

# 5. Final damage
final_damage = int(base_damage × type_mult × other_mults)
```

---

## 🎨 HOW THE DUAL-TEXT SYSTEM WORKS

### In JSON Files

```json
{
  "flavor_text": {
    "default": "A righteous force of nature! SLAPS HARD!",
    "christian_edition": "Blessed with divine power and strength."
  }
}
```

### In Python Code

```python
# Option 1: Manual selection
edition = "default"  # or "christian_edition"
text = fish_data["flavor_text"][edition]

# Option 2: Helper function (to be implemented)
def get_text(data, edition):
    if isinstance(data, dict) and "default" in data:
        return data.get(edition, data["default"])
    return data  # Not dual-text, return as-is
```

### Displaying Dual-Text

```python
# When showing fish description
fish = Fish("holy_mackerel", fish_data, level=5)
edition = player.edition  # Player's chosen edition

# Get the right text
flavor = fish.flavor_text[edition]
print(flavor)

# Default: "A righteous force of nature! SLAPS HARD!"
# Christian: "Blessed with divine power and strength."
```

### Adding New Dual-Text

When creating new content with user-facing text:

```json
{
  "new_field": {
    "default": "Irreverent version (snarky, funny)",
    "christian_edition": "Reverent version (respectful, educational)"
  }
}
```

**See [TONE_GUIDE.md](TONE_GUIDE.md) for writing guidelines!**

---

## ➕ HOW TO ADD NEW CONTENT

### Adding a New Fish

**File:** `src/data/fish.json`

1. Copy an existing fish entry
2. Change the ID (must be unique)
3. Adjust stats, type, moves
4. Write dual-text flavor text
5. Save and test!

```json
{
  "id": "divine_dolphin",  // MUST be unique!
  "name": "Divine Dolphin",
  "tier": 3,
  "type": "Holy",
  "base_stats": {
    "hp": 65,
    "atk": 70,
    "def": 55,
    "spd": 90
  },
  "flavor_text": {
    "default": "A sacred dolphin who's WAY too confident!",
    "christian_edition": "A dolphin blessed by divine light."
  },
  "property": {
    "effect": "healing_aura",
    "value": 0.05
  },
  "moves": [
    {"name": "Holy Splash", "level": 1, "power": 40},
    {"name": "Divine Wave", "level": 10, "power": 80}
  ]
}
```

**No code changes needed!** The Fish class will load it automatically.

### Adding a New Enemy

**File:** `src/data/enemies.json`

Same process as fish - copy, modify, save!

### Adding a New Quest

**File:** `src/data/quests.json`

```json
{
  "id": "heal_the_sick",
  "number": 46,
  "title": "Heal the Sick",
  "location": "Capernaum",
  "dialogue": {
    "start": {
      "default": "Hey, can you help? My kid's sick!",
      "christian_edition": "Please help my child. They are very ill."
    },
    "complete": {
      "default": "You did it! Thanks!",
      "christian_edition": "Thank you! My child is healed!"
    }
  },
  "requirements": {
    "level": 5,
    "apostles": []
  },
  "objectives": [
    {
      "type": "defeat_boss",
      "target": "fever_demon",
      "count": 1
    }
  ],
  "rewards": {
    "xp": 200,
    "money": 100,
    "items": ["healing_bread"]
  }
}
```

**Again, no code changes!** The quest system reads it automatically.

---

## 🔧 COMMON PATTERNS

### Pattern 1: Loading Data

```python
from src.utils.data_loader import get_data_loader

# Get the singleton
loader = get_data_loader()

# Load specific fish
fish_data = loader.get_fish_by_id("holy_mackerel")

# Load all fish
all_fish = loader.get_all_fish()

# Check if exists
if fish_data:
    print(fish_data["name"])
else:
    print("Fish not found!")
```

### Pattern 2: Creating Game Objects

```python
from src.engine.fish import Fish
from src.utils.data_loader import get_data_loader

# Load the fish data from JSON
loader = get_data_loader()
fish_data = loader.get_fish_by_id("holy_mackerel")

# Create a Fish instance
fish = Fish("holy_mackerel", fish_data, level=10)

# Now you can use it
print(fish.name)  # "Holy Mackerel"
print(fish.current_hp)  # Calculated from base HP + level
```

### Pattern 3: Save/Load

```python
# Saving
fish_save_data = fish.to_dict()
save_file["fish"] = fish_save_data

# Loading
from src.engine.fish import Fish
fish = Fish.from_dict(saved_data, fish_data)
```

### Pattern 4: Type Effectiveness

```python
from src.utils.constants import TYPE_CHART

# Get multiplier
attacker_type = "Holy"
defender_type = "Dark"
multiplier = TYPE_CHART[attacker_type][defender_type]

# Apply to damage
damage = base_damage * multiplier

# Check if super effective
if multiplier > 1.0:
    print("It's super effective!")
```

---

## 🐛 DEBUGGING TIPS

### JSON Errors

**Problem:** Game crashes on startup
**Likely cause:** Broken JSON syntax

**How to find:**
1. Look at the error message - it tells you which file
2. Common issues:
   - Missing comma
   - Extra comma at end of array/object
   - Mismatched brackets `{}` or `[]`
   - Missing quotes around strings
3. Use a JSON validator: [jsonlint.com](https://jsonlint.com)

**Example broken JSON:**
```json
{
  "name": "Holy Mackerel"  // ❌ Missing comma!
  "type": "Holy"
}
```

**Fixed:**
```json
{
  "name": "Holy Mackerel",  // ✅ Added comma
  "type": "Holy"
}
```

### Fish Not Loading

**Problem:** New fish doesn't appear in game

**Checklist:**
- [ ] Did you add it to fish.json?
- [ ] Is the JSON syntax valid? (no red squiggles)
- [ ] Is the `"id"` field unique?
- [ ] Did you save the file?
- [ ] Did you restart the game?

### Stat Calculation Issues

**Problem:** Fish stats seem wrong

**Check:**
1. `fish.py` line 96: `growth_rate = 0.07`
2. Base stats in JSON
3. Formula: `base_stat × (1 + 0.07 × (level - 1))`

**Example calculation:**
```python
# Fish level 10, base HP 50
hp = 50 * (1 + 0.07 * 9)
hp = 50 * 1.63
hp = 81.5 → 81
```

### Type Effectiveness Not Working

**Problem:** Holy attack doesn't do 2x damage to Dark

**Check:**
1. `constants.py` line 109: `"Dark": 2.0`
2. Battle damage calculation in `battle.py`
3. Make sure using correct type names (case-sensitive!)

---

## 🎓 NEXT STEPS

### For Beginners

1. **Read the code comments** - Every important file has detailed comments
2. **Add a new fish** - Practice with the JSON system
3. **Modify constants** - Make the game easier/harder
4. **Read TONE_GUIDE.md** - Learn to write dual-text content

### For Intermediate Developers

1. **Study battle.py** - Understand combat math
2. **Read ARCHITECTURE.md** - System design details
3. **Implement missing features** - Check ROADMAP.md
4. **Add new status effects** - Extend the battle system

### For Advanced Developers

1. **Migrate to Godot** - See GODOT_MIGRATION_PLAN.md
2. **Implement UI** - Create visual interface
3. **Add animations** - Sprite-based combat
4. **Steam integration** - Achievements, cloud saves

---

## 📚 ADDITIONAL RESOURCES

### Documentation Files

- **[README.md](README.md)** - Project overview
- **[TONE_GUIDE.md](TONE_GUIDE.md)** - Writing dual-text content
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[GAME_ELEMENTS.md](GAME_ELEMENTS.md)** - Complete content reference
- **[GODOT_MIGRATION_PLAN.md](GODOT_MIGRATION_PLAN.md)** - Migrating to Godot engine

### Code Documentation

- **constants.py** - Heavily commented game balance values
- **fish.py** - Detailed method documentation
- **data_loader.py** - Explains data-driven architecture
- **battle.py** - Combat formulas explained

### Learning Python

If you're new to Python:
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)
- Type hints: `def function(arg: str) -> int:`
- Dictionaries: `{"key": "value"}`
- Classes: `class ClassName:`

---

## ❓ FAQ

**Q: Can I add content without knowing Python?**
A: YES! Just edit the JSON files. No coding required.

**Q: How do I make the game harder?**
A: Edit `constants.py`:
- Reduce `XP_PER_LEVEL` (slower leveling)
- Increase enemy HP/ATK in `enemies.json`
- Change `DIFFICULTY_SETTINGS["normal"]`

**Q: Can I create a mod?**
A: YES! Replace the JSON files in `src/data/`. The game is mod-friendly.

**Q: Where do I add new types?**
A: Edit `TYPE_CHART` in `constants.py`, but you'll need to update battle.py too.

**Q: How do I test my changes?**
A: Just run `python main.py` - changes to JSON are instant!

---

## 🤝 GETTING HELP

**Found a bug?**
- Check if JSON is valid
- Read the error message carefully
- Search for similar issues

**Need help?**
- Read this guide again
- Check inline code comments
- Look at similar examples in the code

**Want to contribute?**
- See [CONTRIBUTING.md](CONTRIBUTING.md)
- All contributions welcome!

---

**Welcome to the team! Happy coding! 🐟✨**

*"Give a developer a fish, and they code for a day. Teach a developer to fish, and they refactor for a lifetime."*
