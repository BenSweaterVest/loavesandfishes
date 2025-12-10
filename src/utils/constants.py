"""
Game constants for Loaves and Fishes
"""

# Game metadata
GAME_TITLE = "Loaves and Fishes"
GAME_VERSION = "0.1.0-alpha"
GAME_TAGLINE = "The Greatest Story Ever Played"

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Game balance constants
MAX_LEVEL = 50
MAX_PARTY_SIZE = 4
MAX_FISH_STORAGE = 999
MAX_ITEM_STACK = 99

# XP constants
XP_PER_LEVEL = 100  # Flat 100 XP per level for fish
FISH_XP_PER_DAMAGE = 1  # 1 XP per point of damage dealt

# Battle constants
BASE_CRIT_CHANCE = 0.05  # 5% base critical hit chance
CRIT_MULTIPLIER = 1.5  # Critical hits do 1.5x damage

# Type effectiveness
TYPE_CHART = {
    "Holy": {
        "Holy": 1.0,
        "Water": 1.0,
        "Earth": 1.0,
        "Spirit": 1.0,
        "Dark": 2.0  # Holy crushes Dark
    },
    "Water": {
        "Holy": 1.0,
        "Water": 0.5,  # Water resists Water
        "Earth": 2.0,  # Water beats Earth
        "Spirit": 1.0,
        "Dark": 1.0
    },
    "Earth": {
        "Holy": 1.0,
        "Water": 0.5,  # Earth resists Water
        "Earth": 1.0,
        "Spirit": 1.0,
        "Dark": 1.0
    },
    "Spirit": {
        "Holy": 1.5,  # Spirit strong vs Holy
        "Water": 1.0,
        "Earth": 1.0,
        "Spirit": 1.0,
        "Dark": 1.5  # Spirit strong vs Dark
    },
    "Dark": {
        "Holy": 0.5,  # Dark resists Holy
        "Water": 1.0,
        "Earth": 1.0,
        "Spirit": 0.5,  # Dark resists Spirit
        "Dark": 1.0
    }
}

# Status effects
STATUS_EFFECTS = {
    "blessed": {"duration": 3, "stat_bonus": 0.2},
    "cursed": {"duration": 3, "stat_penalty": 0.2},
    "poisoned": {"duration": 5, "damage_per_turn": 0.05},
    "burned": {"duration": 5, "damage_per_turn": 0.03},
    "frozen": {"duration": 2, "cannot_act": True},
    "paralyzed": {"duration": 3, "act_chance": 0.5},
    "confused": {"duration": 3, "self_attack_chance": 0.5},
    "asleep": {"duration": 3, "cannot_act": True},
    "blinded": {"duration": 3, "accuracy_penalty": 0.5},
    "stunned": {"duration": 1, "cannot_act": True}
}

# Miracle meter
MIRACLE_METER_MAX = 100
MIRACLE_GAIN_PER_DAMAGE_DEALT = 0.1  # +1% per 10 damage
MIRACLE_GAIN_PER_DAMAGE_TAKEN = 0.2  # +2% per 10 damage taken
MIRACLE_GAIN_FISH_FAINT = 10  # +10% when fish faints
MIRACLE_GAIN_APOSTLE_USE = 5  # +5% when apostle ability used

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
