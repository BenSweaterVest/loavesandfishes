# Contributing to Loaves and Fishes

> **Welcome, fellow disciple of game development!** 🎮

Thank you for your interest in contributing to the Loaves and Fishes JRPG! This guide will help you add new content, fix bugs, and extend the game.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [How to Add New Content](#how-to-add-new-content)
3. [Code Style Guidelines](#code-style-guidelines)
4. [Testing Your Changes](#testing-your-changes)
5. [Submitting Changes](#submitting-changes)
6. [Common Recipes](#common-recipes)

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A text editor (VS Code, Sublime, vim, etc.)
- Basic understanding of Python and JSON
- Git for version control

### Setting Up Your Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/loavesandfishes.git
cd loavesandfishes

# Run the game to make sure everything works
python3 main.py

# Run tests (when available)
python3 -m pytest tests/
```

### Project Structure Overview

```
loavesandfishes/
├── main.py              # Game entry point
├── src/
│   ├── engine/          # Core game logic
│   ├── ui/              # User interface
│   └── utils/           # Helper functions
├── data/                # All game content (JSON)
│   ├── fish/
│   ├── enemies/
│   ├── quests/
│   └── ...
└── saves/               # Player save files
```

---

## How to Add New Content

### Adding a New Fish Species

**Difficulty**: ⭐ Easy
**Time**: ~10 minutes
**Files to Edit**: `src/data/fish.json`

#### Step 1: Define the Fish

Add an entry to the `fish` array in `src/data/fish.json`:

```json
{
  "fish_id": "divine_dolphin",
  "name": "Divine Dolphin",
  "type": "Holy",
  "description": "A sacred dolphin blessed by the seas. Known for its wisdom and grace.",
  "rarity": "rare",
  "base_stats": {
    "hp": 65,
    "attack": 70,
    "defense": 55,
    "sp_attack": 85,
    "sp_defense": 70,
    "speed": 90
  },
  "learnable_moves": [
    {"move_id": "holy_splash", "level": 5},
    {"move_id": "aqua_blessing", "level": 10},
    {"move_id": "divine_wave", "level": 15},
    {"move_id": "sacred_tsunami", "level": 25}
  ],
  "can_be_caught": true,
  "fishing_locations": ["Caesarea", "Tyre"],
  "fishing_difficulty": 60
}
```

#### Step 2: Balance the Stats

Use these guidelines for base stats (at level 5):

| Tier | Total Stats | HP Range | Example |
|------|-------------|----------|---------|
| Common | 200-250 | 40-50 | Sardine |
| Uncommon | 250-300 | 50-60 | Bass |
| Rare | 300-350 | 60-70 | Carp |
| Epic | 350-400 | 70-80 | Grouper |
| Legendary | 400-450 | 80-100 | Leviathan |

#### Step 3: Assign Moves

- **Level 5**: Basic move (20-30 power)
- **Level 10**: Secondary move (40-50 power)
- **Level 15**: Strong move (60-80 power)
- **Level 25+**: Ultimate move (90-120 power)

#### Step 4: Set Fishing Locations

- **Common fish**: 4-6 locations
- **Rare fish**: 2-3 locations
- **Legendary fish**: 1 location (usually late-game)

#### Step 5: Test It!

```python
# In main.py, add to your party for testing
test_fish = Fish("divine_dolphin", fish_data["divine_dolphin"], level=10)
self.player.party.append(test_fish)
```

---

### Adding a New Enemy

**Difficulty**: ⭐ Easy
**Time**: ~5 minutes
**Files to Edit**: `src/data/enemies.json`

#### Step 1: Define the Enemy

Add an entry to the `enemies` array in `src/data/enemies.json`:

```json
{
  "enemy_id": "shadow_serpent",
  "name": "Shadow Serpent",
  "type": "Dark",
  "description": "A serpent wreathed in darkness, tempting travelers astray.",
  "tier": 3,
  "base_level": 15,
  "base_stats": {
    "hp": 80,
    "attack": 65,
    "defense": 50,
    "sp_attack": 70,
    "sp_defense": 55,
    "speed": 75
  },
  "moves": [
    "shadow_bite",
    "dark_coil",
    "poison_fang",
    "temptation"
  ],
  "xp_reward": 120,
  "money_reward": 75,
  "item_drops": [
    {"item_id": "antidote", "chance": 0.3},
    {"item_id": "dark_scale", "chance": 0.1}
  ],
  "encounter_locations": ["Wilderness", "Dark_Cave"],
  "ai_strategy": "aggressive"
}
```

#### Step 2: Assign to Tier

| Tier | Level Range | Total Stats | Locations |
|------|-------------|-------------|-----------|
| 1 | 5-10 | 150-200 | Early towns |
| 2 | 10-15 | 200-250 | Mid-early towns |
| 3 | 15-25 | 250-300 | Mid towns |
| 4 | 25-35 | 300-400 | Late towns |
| 5 | 35-50 | 400-500 | Endgame areas |

#### Step 3: Balance Rewards

```python
xp_reward = base_level * 8
money_reward = base_level * 5
```

#### Step 4: Choose AI Strategy

- **`passive`**: Rarely attacks, prefers status moves
- **`defensive`**: Focuses on survival
- **`balanced`**: Mix of offense and defense
- **`aggressive`**: Always attacks with strongest move
- **`smart`**: Uses type effectiveness

---

### Adding a New Boss

**Difficulty**: ⭐⭐ Medium
**Time**: ~20 minutes
**Files to Edit**: `data/bosses/boss_data.json`

#### Step 1: Define the Boss

```json
{
  "boss_id": "pharisee_leader",
  "name": "Pharisee Leader",
  "type": "Dark",
  "description": "A proud leader who has strayed from the true path.",
  "location": "Jerusalem",
  "level": 40,
  "base_stats": {
    "hp": 300,
    "attack": 110,
    "defense": 95,
    "sp_attack": 120,
    "sp_defense": 100,
    "speed": 85
  },
  "moves": [
    "judgment",
    "false_witness",
    "stone_throw",
    "condemn"
  ],
  "phases": [
    {
      "hp_threshold": 0.5,
      "new_moves": ["righteous_fury"],
      "stat_boosts": {"attack": 1.2, "sp_attack": 1.2}
    }
  ],
  "xp_reward": 1000,
  "money_reward": 500,
  "guaranteed_drops": ["holy_relic", "boss_emblem"],
  "story_unlock": "jerusalem_complete",
  "dialogue_before": "You dare challenge the authority of the temple?",
  "dialogue_after": "Perhaps... there is another way..."
}
```

#### Step 2: Design Boss Mechanics

**Health Thresholds**: Bosses can have multiple phases

```json
"phases": [
  {
    "hp_threshold": 0.75,  // At 75% HP
    "new_moves": ["enrage"],
    "stat_boosts": {"attack": 1.1}
  },
  {
    "hp_threshold": 0.30,  // At 30% HP
    "new_moves": ["desperation"],
    "stat_boosts": {"attack": 1.5, "speed": 1.3},
    "heal_amount": 50
  }
]
```

#### Step 3: Balance Boss Difficulty

- **HP**: 5-10x normal enemy HP
- **Stats**: 1.5-2x normal enemy stats
- **Moves**: 5-8 moves (vs 2-4 for normal enemies)
- **Rewards**: 10x normal enemy rewards

---

### Adding a New Quest

**Difficulty**: ⭐⭐ Medium
**Time**: ~15 minutes
**Files to Edit**: `data/quests/quest_data.json`

#### Step 1: Define the Quest

```json
{
  "quest_id": "heal_the_sick",
  "name": "Heal the Sick",
  "description": "A sick villager in Capernaum needs healing. Bring them a Miracle Herb.",
  "type": "fetch",
  "giver": "village_elder",
  "location": "Capernaum",
  "requirements": {
    "min_level": 8,
    "required_apostles": [],
    "required_flags": ["capernaum_visited"]
  },
  "objectives": [
    {
      "type": "collect_item",
      "item_id": "miracle_herb",
      "quantity": 1,
      "description": "Find a Miracle Herb"
    }
  ],
  "rewards": {
    "xp": 200,
    "money": 150,
    "items": [{"item_id": "healing_potion", "quantity": 3}],
    "unlock_flag": "healer_reputation"
  },
  "dialogue": {
    "start": "Please, my child is very ill. I've heard of a Miracle Herb that could help...",
    "progress": "Have you found the Miracle Herb yet?",
    "complete": "Thank you! My child is already feeling better. Bless you!"
  }
}
```

#### Step 2: Quest Types

**Fetch Quest**:
```json
{
  "type": "fetch",
  "objectives": [
    {"type": "collect_item", "item_id": "holy_water", "quantity": 3}
  ]
}
```

**Battle Quest**:
```json
{
  "type": "battle",
  "objectives": [
    {"type": "defeat_enemy", "enemy_id": "demon", "quantity": 5}
  ]
}
```

**Story Quest**:
```json
{
  "type": "story",
  "objectives": [
    {"type": "talk_to_npc", "npc_id": "john"},
    {"type": "visit_location", "location_id": "Mount_of_Olives"},
    {"type": "trigger_cutscene", "cutscene_id": "sermon_on_mount"}
  ]
}
```

**Boss Quest**:
```json
{
  "type": "boss",
  "objectives": [
    {"type": "defeat_boss", "boss_id": "pharisee_leader"}
  ]
}
```

#### Step 3: Balance Quest Rewards

```python
# XP Reward Formula
xp_reward = min_level * 25

# Money Reward Formula
money_reward = min_level * 15

# Item Rewards
# Common quests: 1-2 common items
# Rare quests: 1 rare item + 2-3 common items
# Story quests: Unique items or unlocks
```

---

### Adding a New Parable

**Difficulty**: ⭐ Easy
**Time**: ~10 minutes
**Files to Edit**: `data/parables/parable_data.json`

#### Step 1: Define the Parable

```json
{
  "parable_id": "good_samaritan",
  "title": "The Good Samaritan",
  "scripture_reference": "Luke 10:25-37",
  "discovery_location": "Jericho",
  "discovery_method": "exploration",
  "text": [
    "A man was going down from Jerusalem to Jericho...",
    "He fell among robbers, who stripped him and beat him...",
    "A priest passed by on the other side...",
    "A Levite also passed by...",
    "But a Samaritan came to where he was and had compassion..."
  ],
  "moral": "Love your neighbor as yourself, regardless of who they are.",
  "interactive_choice": {
    "question": "Who was the true neighbor to the man in need?",
    "choices": [
      {"text": "The priest", "correct": false, "response": "The priest passed by without helping."},
      {"text": "The Levite", "correct": false, "response": "The Levite also ignored the man."},
      {"text": "The Samaritan", "correct": true, "response": "Correct! The Samaritan showed true compassion."}
    ]
  },
  "rewards": {
    "correct_answer": {
      "xp": 100,
      "items": [{"item_id": "compassion_charm", "quantity": 1}]
    },
    "completion": {
      "unlock_flag": "good_samaritan_learned"
    }
  }
}
```

#### Step 2: Discovery Methods

- **`exploration`**: Found by exploring a location
- **`npc_dialogue`**: Given by an NPC
- **`quest_reward`**: Rewarded for completing a quest
- **`boss_victory`**: Unlocked after defeating a boss
- **`story_event`**: Triggered by story progression

---

### Adding a New Town

**Difficulty**: ⭐⭐⭐ Advanced
**Time**: ~30 minutes
**Files to Edit**: `src/engine/world_map.py`, `data/towns/town_data.json`

#### Step 1: Add to World Map

In `src/engine/world_map.py`, add to `_build_default_map()`:

```python
towns = [
    # ... existing towns ...
    ("Emmaus", 5, 9, "Judean"),  # (name, x, y, region)
]

# Add connections
self.locations["Emmaus"].connections.extend(["Bethany", "Jerusalem"])
self.locations["Bethany"].connections.append("Emmaus")
```

#### Step 2: Define Town Data

In `data/towns/town_data.json`:

```json
{
  "town_id": "Emmaus",
  "name": "Emmaus",
  "region": "Judean",
  "description": "A peaceful village known for its warm hospitality.",
  "unlock_requirement": {
    "type": "story_flag",
    "flag": "mid_game_reached"
  },
  "npcs": [
    {
      "npc_id": "innkeeper",
      "name": "Cleopas",
      "type": "generic",
      "dialogue": ["Welcome, traveler! Rest your weary feet."],
      "location": "inn"
    }
  ],
  "shops": {
    "baker": {
      "items": ["bread", "healing_loaf", "fish_meal"]
    },
    "fishmonger": {
      "items": ["basic_rod", "quality_bait"]
    }
  },
  "fishing_spot": {
    "quality": 55,
    "available_fish": ["bass_of_galilee", "carp_of_capernaum"]
  },
  "boss": {
    "boss_id": "doubt_demon",
    "unlock_requirement": "emmaus_quest_complete"
  }
}
```

#### Step 3: Create Boss for Town

Add a boss (see "Adding a New Boss" section above).

#### Step 4: Add Quests

Add 2-3 quests specific to this town (see "Adding a New Quest" section).

---

### Adding a New Apostle Ability

**Difficulty**: ⭐⭐ Medium
**Time**: ~15 minutes
**Files to Edit**: `src/engine/apostle_abilities.py`

#### Step 1: Define the Ability

In `APOSTLE_ABILITIES` dict:

```python
"thomas": ApostleAbility(
    ability_id="doubting_strike",
    name="Doubting Strike",
    apostle="Thomas",
    ability_type=AbilityType.ATTACK,
    description="I will not believe unless I see! 150 damage, ignores defense.",
    power=150,
    targets="single",
    cooldown=4,
    special_effect="ignore_defense"
),
```

#### Step 2: Ability Types

```python
class AbilityType(Enum):
    ATTACK = "attack"      # Damage-dealing
    BUFF = "buff"          # Boost ally stats
    DEBUFF = "debuff"      # Lower enemy stats
    HEAL = "heal"          # Restore HP
    UTILITY = "utility"    # Special effects
```

#### Step 3: Special Effects

Available effects:
- `ignore_defense`: Damage ignores DEF
- `guaranteed_crit`: Always critical hit
- `apply_burn`: Inflicts Burn status
- `apply_poison`: Inflicts Poison status
- `apply_paralysis`: Inflicts Paralysis
- `flinch`: Target loses turn
- `heal_party`: Heals all allies
- `revive`: Brings back fainted fish

#### Step 4: Balance Guidelines

| Cooldown | Power Range | Effect Strength |
|----------|-------------|-----------------|
| 2 turns | 80-100 | Minor effect |
| 3 turns | 100-150 | Moderate effect |
| 4 turns | 150-200 | Major effect |
| 5 turns | 200-250 | Powerful effect |

---

### Adding a New Miracle

**Difficulty**: ⭐⭐ Medium
**Time**: ~10 minutes
**Files to Edit**: `src/engine/miracles.py`

#### Step 1: Define the Miracle

In `MIRACLES` dict:

```python
"transfiguration": Miracle(
    miracle_id="transfiguration",
    name="Transfiguration",
    miracle_type=MiracleType.BUFF,
    description="Radiant glory shines upon your party! All fish gain +100% ATK and SPD for 3 turns.",
    meter_cost=75,
    biblical_reference="Matthew 17:1-9",
    effect_power=100,  # 100% boost
    duration=3
),
```

#### Step 2: Miracle Types

```python
class MiracleType(Enum):
    HEALING = "healing"    # Restore HP
    REVIVAL = "revival"    # Revive fainted fish
    BUFF = "buff"          # Boost party
    ATTACK = "attack"      # Deal damage
```

#### Step 3: Balance Meter Costs

- **25% meter**: Minor effect (heal one fish)
- **50% meter**: Moderate effect (heal party, small buff)
- **75% meter**: Major effect (large buff, revive one)
- **100% meter**: Ultimate effect (full party revival, massive damage)

---

### Adding a New Combo Attack

**Difficulty**: ⭐⭐ Medium
**Time**: ~10 minutes
**Files to Edit**: `src/engine/combos.py`

#### Step 1: Define the Combo

In `COMBO_ATTACKS` dict:

```python
"divine_tempest": ComboAttack(
    combo_id="divine_tempest",
    name="Divine Tempest",
    fish_id="storm_sturgeon",
    apostle_id="james",
    description="Son of Thunder unleashes a holy storm! 220 Holy damage to all enemies.",
    power=220,
    attack_type="Holy",
    special_effect="hits_all"
),
```

#### Step 2: Choose Fish + Apostle Pairing

Look for thematic connections:
- **Peter** + Rock-type fish = Earth attacks
- **John** + Holy fish = Holy attacks
- **Matthew** + Common fish = Money/tax effects
- **James/John** (Sons of Thunder) + Water fish = Storm attacks

#### Step 3: Balance Combo Power

```python
# Normal move: 80-100 power
# Strong move: 100-150 power
# Combo attack: 150-250 power (costs 25% miracle meter)
```

#### Step 4: Special Effects

- `hits_all`: Damages all enemies
- `heal_party`: Also heals your party
- `steal_money`: Gain extra money
- `flinch_all`: All enemies lose turn
- `guaranteed_crit`: Always crits
- `ignore_type`: Ignores type effectiveness

---

## Code Style Guidelines

### Python Style

Follow [PEP 8](https://pep8.org/) with these specifics:

```python
# Good: Clear variable names
fish_species = "Holy Mackerel"
max_health_points = 100

# Bad: Unclear abbreviations
fs = "Holy Mackerel"
mhp = 100

# Good: Docstrings for all classes and functions
def calculate_damage(attacker, defender, move):
    """
    Calculate damage dealt by a move.

    Args:
        attacker: The attacking fish/enemy
        defender: The defending fish/enemy
        move: The move being used

    Returns:
        int: Damage amount
    """
    pass

# Good: Type hints
def add_fish(self, fish: Fish) -> bool:
    """Add a fish to the party."""
    pass

# Good: Meaningful class names
class BattleManager:
    """Manages all battle-related functionality."""
    pass

# Bad: Vague class names
class Manager:
    pass
```

### JSON Style

```json
{
  "good_formatting": {
    "indent": 2,
    "quotes": "double",
    "trailing_commas": false,
    "alphabetical_keys": true
  }
}
```

### Naming Conventions

- **Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case()`
- **Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **IDs in JSON**: `snake_case`

---

## Testing Your Changes

### Manual Testing Checklist

Before submitting changes, test:

- [ ] Game starts without errors
- [ ] New content appears in game
- [ ] No crashes during gameplay
- [ ] Save/load still works
- [ ] No broken quest chains
- [ ] Balanced stats (not too OP)

### Testing New Fish

```python
# Add to main.py temporarily for testing
test_fish = Fish("your_new_fish_id", fish_data["your_new_fish_id"], level=20)
self.player.party.append(test_fish)

# Test in battle
# - Does it learn moves correctly?
# - Are stats balanced?
# - Does it work with combos?
```

### Testing New Enemies

```python
# Spawn in a test battle
test_enemy = Enemy("your_new_enemy_id", enemy_data["your_new_enemy_id"])
battle = Battle(self.player, [test_enemy], BattleType.WILD)

# Check:
# - Is difficulty appropriate for tier?
# - Does AI work correctly?
# - Are rewards balanced?
```

### Testing New Quests

- Trigger the quest
- Complete all objectives
- Verify rewards are granted
- Check that completion flag is set
- Test with and without requirements

---

## Submitting Changes

### Git Workflow

```bash
# Create a feature branch
git checkout -b feature/add-dolphin-fish

# Make your changes
# Edit src/data/fish.json

# Test your changes
python3 main.py

# Commit with clear message
git add src/data/fish.json
git commit -m "Add Divine Dolphin fish species

- Added Divine Dolphin (Holy type, rare)
- Base stats: HP 65, ATK 70, SPD 90
- Available in Caesarea and Tyre
- Learns 4 water-based holy moves"

# Push to your fork
git push origin feature/add-dolphin-fish

# Create pull request on GitHub
```

### Commit Message Format

```
<type>: <short summary>

<detailed description>

<bullet points of changes>
```

**Types**:
- `feat`: New feature (new fish, quest, etc.)
- `fix`: Bug fix
- `balance`: Balance changes (stat adjustments)
- `docs`: Documentation changes
- `test`: Adding tests
- `refactor`: Code refactoring

**Example**:
```
feat: Add 5 new fish species for endgame

Added five legendary fish species for post-game content:
- Celestial Salmon (Holy/Spirit hybrid)
- Abyssal Eel (Dark type, highest SPD)
- Titan Tuna (Earth type, highest HP)
- Phoenix Perch (Fire type with revival)
- Seraphim Shark (Holy type, highest ATK)

All fish have:
- 400+ total base stats
- 5-6 learnable moves
- Fishing difficulty 80+
- Available only in post-game areas
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New content (fish, enemy, quest, etc.)
- [ ] Bug fix
- [ ] Balance change
- [ ] Documentation
- [ ] Code refactoring

## Testing
- [ ] Tested in-game
- [ ] No errors or crashes
- [ ] Save/load works
- [ ] Balanced appropriately

## Screenshots (if applicable)
Paste any relevant screenshots

## Checklist
- [ ] Code follows style guidelines
- [ ] JSON is properly formatted
- [ ] Tested thoroughly
- [ ] Updated documentation if needed
```

---

## Common Recipes

### Recipe: Creating a Quest Chain

**Goal**: Create 3 connected quests that tell a story

```json
// Quest 1: Introduction
{
  "quest_id": "peters_faith_1",
  "name": "Peter's Trial: The Storm",
  "requirements": {
    "required_apostles": ["peter"]
  },
  "rewards": {
    "unlock_flag": "peters_faith_2_available"
  }
}

// Quest 2: Middle Chapter
{
  "quest_id": "peters_faith_2",
  "name": "Peter's Trial: The Denial",
  "requirements": {
    "required_flags": ["peters_faith_1_complete"]
  },
  "rewards": {
    "unlock_flag": "peters_faith_3_available"
  }
}

// Quest 3: Conclusion
{
  "quest_id": "peters_faith_3",
  "name": "Peter's Trial: The Rock",
  "requirements": {
    "required_flags": ["peters_faith_2_complete"]
  },
  "rewards": {
    "items": [{"item_id": "peters_blessing", "quantity": 1}],
    "unlock_flag": "peter_ultimate_ability"
  }
}
```

---

### Recipe: Creating a Mini-Boss Rush

**Goal**: Add optional boss rush challenge

```json
{
  "quest_id": "boss_rush_challenge",
  "name": "Trial of Champions",
  "type": "boss",
  "requirements": {
    "min_level": 40,
    "required_flags": ["all_apostles_recruited"]
  },
  "objectives": [
    {"type": "defeat_boss", "boss_id": "champion_1"},
    {"type": "defeat_boss", "boss_id": "champion_2"},
    {"type": "defeat_boss", "boss_id": "champion_3"},
    {"type": "defeat_boss", "boss_id": "final_champion"}
  ],
  "special_rules": {
    "no_healing_between_battles": true,
    "no_items": false,
    "one_attempt_per_day": true
  },
  "rewards": {
    "xp": 5000,
    "money": 10000,
    "items": [
      {"item_id": "champion_trophy", "quantity": 1},
      {"item_id": "master_fishing_rod", "quantity": 1}
    ]
  }
}
```

---

### Recipe: Creating a Shiny/Rare Variant

**Goal**: Add a rare color variant of existing fish

```json
{
  "fish_id": "golden_mackerel",
  "name": "Golden Holy Mackerel",
  "type": "Holy",
  "description": "An extremely rare golden variant! Blessed by divine light.",
  "rarity": "legendary",
  "base_stats": {
    "hp": 60,      // +20% compared to normal
    "attack": 66,  // +20%
    "defense": 48, // +20%
    "sp_attack": 72, // +20%
    "sp_defense": 60, // +20%
    "speed": 78    // +20%
  },
  "appearance_rate": 0.01,  // 1% chance
  "fishing_locations": ["all"],  // Can appear anywhere
  "special_trait": "luck_boost",  // Increases item drop rates
  "unique_move": {
    "move_id": "golden_judgment",
    "name": "Golden Judgment",
    "power": 120,
    "type": "Holy",
    "description": "A devastating attack wreathed in golden light!"
  }
}
```

---

## Need Help?

### Resources

- **README.md**: Overview and quick start
- **STATUS.md**: Current implementation status
- **ROADMAP.md**: Future plans
- **ARCHITECTURE.md**: Technical design details

### Getting Support

- **Issues**: Report bugs or request features on GitHub Issues
- **Discussions**: Ask questions in GitHub Discussions
- **Discord**: Join our community server (if available)

### Common Questions

**Q: Can I add moves to existing fish?**
A: Yes! Just add to the `learnable_moves` array in the fish data.

**Q: How do I balance new content?**
A: Compare to existing content of similar level/tier. Test in-game thoroughly.

**Q: Can I add new types beyond the 5 existing?**
A: Advanced! Requires code changes to type effectiveness system. Open an issue first.

**Q: My JSON won't load. What's wrong?**
A: Use a JSON validator (jsonlint.com). Common issues: trailing commas, missing quotes.

**Q: How do I test without playing through the whole game?**
A: Modify `main.py` to start at specific location with specific party/level.

---

## Code of Conduct

- Be respectful and welcoming
- Give constructive feedback
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

---

## Thank You!

Your contributions help make Loaves and Fishes better for everyone. Whether you're adding a single fish or a whole new game system, your work is appreciated!

*"Freely you have received; freely give."* - Matthew 10:8

---

**Happy Contributing!** 🐟✨
