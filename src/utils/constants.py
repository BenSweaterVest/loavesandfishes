"""
Game constants for Loaves and Fishes

This file contains all the balancing numbers, game rules, and configuration
values. If you want to mod the game or adjust difficulty, this is the place!

Organized by category:
- Game metadata (title, version)
- Balance constants (max level, party size, XP rates)
- Battle mechanics (damage, critical hits, type effectiveness)
- Status effects (durations, effects)
- Miracle meter (limit break system)
- Difficulty settings
- Visual settings (colors for UI)
- File paths
- Game messages
"""

# ============================================================================
# GAME METADATA
# ============================================================================

GAME_TITLE = "Loaves and Fishes"
GAME_VERSION = "0.1.0-alpha"
GAME_TAGLINE = "The Greatest Story Ever Played"

# ============================================================================
# SCREEN & PERFORMANCE
# ============================================================================

SCREEN_WIDTH = 1280   # Game window width in pixels
SCREEN_HEIGHT = 720   # Game window height in pixels (720p)
FPS = 60              # Target framerate (60 FPS for smooth animation)

# ============================================================================
# GAME BALANCE CONSTANTS
# ============================================================================

# Level caps and limits
MAX_LEVEL = 50        # Maximum level for fish and player
                      # Adjust this to make the game longer/shorter
                      # 50 levels = ~10-15 hours of gameplay

MAX_PARTY_SIZE = 4    # How many fish can fight at once
                      # Classic JRPG uses 4, but you could change to 3 or 6

MAX_FISH_STORAGE = 999  # Maximum fish in storage (basically unlimited)
MAX_ITEM_STACK = 99     # Maximum bread items per slot (Pokémon-style)

# ============================================================================
# XP & LEVELING SYSTEM
# ============================================================================

XP_PER_LEVEL = 100    # Flat XP requirement per level
                      # Fish need 100 XP to reach level 2, 100 more for level 3, etc.
                      # Simple and predictable for players
                      # Change to 200 to make leveling slower

FISH_XP_PER_DAMAGE = 1  # XP gained per point of damage dealt
                        # Deal 50 damage = gain 50 XP
                        # Encourages using your best fish

# ============================================================================
# BATTLE MECHANICS
# ============================================================================

BASE_CRIT_CHANCE = 0.05   # 5% base chance for critical hit
                          # 1 in 20 attacks will crit
                          # Can be increased by fish properties/abilities

CRIT_MULTIPLIER = 1.5     # Critical hits do 50% more damage
                          # Normal hit: 100 damage → Crit: 150 damage
                          # Increase to 2.0 for bigger crits

# ============================================================================
# TYPE EFFECTIVENESS CHART
# ============================================================================
#
# This chart determines how much damage types deal to each other.
# Format: TYPE_CHART[attacker_type][defender_type] = damage_multiplier
#
# Multipliers:
# - 2.0 = Super effective (double damage)
# - 1.5 = Strong against
# - 1.0 = Normal damage
# - 0.5 = Resisted (half damage)
# - 0.0 = Immune (no damage) - not currently used
#
# How to read this chart:
# "When a HOLY attack hits a DARK enemy, it deals 2.0x damage"
# "When a WATER attack hits an EARTH enemy, it deals 2.0x damage"
# "When a HOLY attack hits another HOLY, it deals 1.0x damage (neutral)"
#
# Design philosophy:
# - Holy counters Dark (light vs darkness)
# - Water counters Earth (floods wash away soil)
# - Spirit is versatile (strong vs Holy and Dark)
# - Each type has strengths and weaknesses
#
# ============================================================================

TYPE_CHART = {
    "Holy": {
        # Holy type: Righteous damage, anti-evil
        "Holy": 1.0,   # Neutral vs itself
        "Water": 1.0,  # Neutral vs Water
        "Earth": 1.0,  # Neutral vs Earth
        "Spirit": 1.0, # Neutral vs Spirit
        "Dark": 2.0    # SUPER EFFECTIVE vs Dark (holy light banishes darkness)
    },
    "Water": {
        # Water type: Flowing, adaptive, erodes earth
        "Holy": 1.0,   # Neutral vs Holy
        "Water": 0.5,  # RESISTED by Water (water on water = splash)
        "Earth": 2.0,  # SUPER EFFECTIVE vs Earth (water erodes soil)
        "Spirit": 1.0, # Neutral vs Spirit
        "Dark": 1.0    # Neutral vs Dark
    },
    "Earth": {
        # Earth type: Solid, sturdy, grounded
        "Holy": 1.0,   # Neutral vs Holy
        "Water": 0.5,  # RESISTED by Water (earth dissolves in water)
        "Earth": 1.0,  # Neutral vs itself
        "Spirit": 1.0, # Neutral vs Spirit
        "Dark": 1.0    # Neutral vs Dark
    },
    "Spirit": {
        # Spirit type: Ethereal, supernatural, versatile
        "Holy": 1.5,   # STRONG vs Holy (spiritual power transcends righteousness)
        "Water": 1.0,  # Neutral vs Water
        "Earth": 1.0,  # Neutral vs Earth
        "Spirit": 1.0, # Neutral vs itself
        "Dark": 1.5    # STRONG vs Dark (spirits can combat evil)
    },
    "Dark": {
        # Dark type: Shadow, corruption, evil
        "Holy": 0.5,   # RESISTED by Holy (darkness can't overcome light)
        "Water": 1.0,  # Neutral vs Water
        "Earth": 1.0,  # Neutral vs Earth
        "Spirit": 0.5, # RESISTED by Spirit (darkness weakened by spirit)
        "Dark": 1.0    # Neutral vs itself
    }
}

# ============================================================================
# STATUS EFFECTS
# ============================================================================
#
# Status effects are temporary conditions that affect fish in battle.
# Each effect has a duration (turns) and specific mechanics.
#
# How to add a new status effect:
# 1. Add it to this dictionary with duration and effects
# 2. Implement the effect in battle.py (damage, stat changes, etc.)
# 3. Add visual indication in UI
#
# ============================================================================

STATUS_EFFECTS = {
    "blessed": {
        "duration": 3,           # Lasts 3 turns
        "stat_bonus": 0.2        # +20% to all stats (ATK, DEF, SPD)
    },
    "cursed": {
        "duration": 3,
        "stat_penalty": 0.2      # -20% to all stats
    },
    "poisoned": {
        "duration": 5,           # Lasts 5 turns
        "damage_per_turn": 0.05  # Takes 5% max HP damage each turn
                                 # Fish with 100 HP loses 5 HP per turn
    },
    "burned": {
        "duration": 5,
        "damage_per_turn": 0.03  # Takes 3% max HP damage (weaker than poison)
    },
    "frozen": {
        "duration": 2,           # Shorter duration, but...
        "cannot_act": True       # Completely unable to act (brutal!)
    },
    "paralyzed": {
        "duration": 3,
        "act_chance": 0.5        # 50% chance to act each turn (coin flip)
    },
    "confused": {
        "duration": 3,
        "self_attack_chance": 0.5  # 50% chance to hit yourself instead!
    },
    "asleep": {
        "duration": 3,
        "cannot_act": True       # Can't act, but wakes up when hit
    },
    "blinded": {
        "duration": 3,
        "accuracy_penalty": 0.5  # -50% accuracy (half your attacks miss)
    },
    "stunned": {
        "duration": 1,           # Very short duration
        "cannot_act": True       # But guaranteed loss of turn
    }
}

# ============================================================================
# MIRACLE METER (Limit Break System)
# ============================================================================
#
# The miracle meter is a "limit break" system (like Final Fantasy).
# It fills during battle and allows Jesus to use powerful miracles.
#
# The meter fills from:
# - Dealing damage (rewards aggressive play)
# - Taking damage (rewards risky play - "desperation" mechanic)
# - Fish fainting (tragedy builds meter fast)
# - Using apostle abilities (combo power)
#
# Design: Meter should fill 1-2 times per average battle
#
# ============================================================================

MIRACLE_METER_MAX = 100  # Miracle meter goes from 0-100%

# Meter gain rates - adjust these to make miracles more/less frequent
MIRACLE_GAIN_PER_DAMAGE_DEALT = 0.1   # +0.1% per point of damage
                                       # Deal 100 damage = +10% meter
                                       # Rewards aggressive play

MIRACLE_GAIN_PER_DAMAGE_TAKEN = 0.2   # +0.2% per point of damage taken
                                       # Take 100 damage = +20% meter
                                       # "Desperation" mechanic (like FFX Overdrive)
                                       # Rewards risky/defensive play

MIRACLE_GAIN_FISH_FAINT = 10          # +10% when a fish faints
                                       # Losing a fish builds meter quickly
                                       # Allows comebacks in tough battles

MIRACLE_GAIN_APOSTLE_USE = 5          # +5% when apostle ability used
                                       # Encourages using apostle abilities
                                       # Creates synergy between systems

# Difficulty modifiers
DIFFICULTY_SETTINGS = {
    "easy": {
        "enemy_hp_mult": 0.7,
        "enemy_atk_mult": 0.8,
        "player_hp_mult": 1.2,
        "player_def_mult": 1.2,
        "xp_mult": 1.25,
        "money_mult": 1.25
    },
    "normal": {
        "enemy_hp_mult": 1.0,
        "enemy_atk_mult": 1.0,
        "player_hp_mult": 1.0,
        "player_def_mult": 1.0,
        "xp_mult": 1.0,
        "money_mult": 1.0
    },
    "hard": {
        "enemy_hp_mult": 1.5,
        "enemy_atk_mult": 1.3,
        "player_hp_mult": 1.0,
        "player_def_mult": 1.0,
        "xp_mult": 1.0,
        "money_mult": 0.8
    }
}

# Colors (for terminal/basic UI)
COLORS = {
    "Holy": "#FFD700",  # Gold
    "Water": "#1E90FF",  # Dodger Blue
    "Earth": "#8B4513",  # Saddle Brown
    "Spirit": "#9370DB",  # Medium Purple
    "Dark": "#4B0082",  # Indigo
    "Normal": "#FFFFFF",  # White
    "Critical": "#FF0000",  # Red
    "Heal": "#00FF00",  # Green
    "Super Effective": "#FFFF00",  # Yellow
    "Not Effective": "#808080"  # Gray
}

# File paths
DATA_PATH = "src/data/"
ASSETS_PATH = "assets/"
SAVES_PATH = "saves/"

# Save file
SAVE_FILE_EXTENSION = ".loaves"
AUTO_SAVE_ENABLED = True

# Debug mode
DEBUG_MODE = False
GOD_MODE = False  # Invincibility for testing

# Game messages
MESSAGES = {
    "super_effective": "It's super effective!",
    "not_effective": "It's not very effective...",
    "critical_hit": "A critical hit!",
    "miss": "The attack missed!",
    "fish_fainted": "{fish_name} has fainted!",
    "level_up": "{name} grew to level {level}!",
    "learned_move": "{fish_name} learned {move_name}!",
    "fish_transformed": "What? {fish_name} is transforming!",
    "ability_depleted": "{move_name} has no energy left!",
    "fled": "Got away safely!",
    "cant_flee": "Can't escape!"
}

# Special unlockables
SPECIAL_UNLOCKS = {
    "secret_code_unlocked": False,
    "ultimate_miracle": False,
    "hidden_fish": False,
    "secret_ending": False
}
