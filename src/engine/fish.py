"""
Fish class - represents a battle fish (weapon) in Loaves and Fishes
"""

from typing import Dict, List, Optional, Any
import random


class Fish:
    """
    Represents a fish that can be used in battle.
    Fish are like Pokémon - they have stats, moves, types, and can level up.
    """

    def __init__(self, fish_id: str, fish_data: Dict[str, Any], level: int = 1):
        """
        Initialize a fish instance

        Args:
            fish_id: Unique identifier for the fish type
            fish_data: Dictionary containing fish data from JSON
            level: Starting level (default 1)
        """
        self.fish_id = fish_id
        self.name = fish_data["name"]
        self.tier = fish_data["tier"]
        self.type = fish_data["type"]
        self.level = level
        self.xp = 0
        self.xp_to_next_level = 100  # Flat 100 XP per level

        # Base stats
        base_stats = fish_data["base_stats"]
        self.base_hp = base_stats["hp"]
        self.base_atk = base_stats["atk"]
        self.base_def = base_stats["def"]
        self.base_spd = base_stats["spd"]

        # Current stats (calculated from base + level)
        self.max_hp = self._calculate_stat(self.base_hp, level)
        self.current_hp = self.max_hp
        self.atk = self._calculate_stat(self.base_atk, level)
        self.defense = self._calculate_stat(self.base_def, level)
        self.spd = self._calculate_stat(self.base_spd, level)

        # Property (special ability)
        self.property = fish_data["property"]

        # Moves
        self.all_moves = fish_data["moves"]
        self.known_moves = self._get_available_moves()

        # Held item
        self.held_item: Optional[Dict[str, Any]] = None

        # Status effects
        self.status_effects: List[str] = []

        # Combo attack data
        self.combo_attack = fish_data.get("combo_attack", None)

        # Flavor text
        self.flavor_text = fish_data["flavor_text"]

        # Battle state
        self.stat_modifiers = {
            "atk": 1.0,
            "def": 1.0,
            "spd": 1.0,
            "accuracy": 1.0,
            "evasion": 1.0
        }

    def _calculate_stat(self, base_stat: int, level: int) -> int:
        """
        Calculate stat based on level using a linear growth formula.

        Stats grow 7% per level, meaning a Level 10 fish will have stats
        that are about 63% higher than at Level 1.

        Formula: stat = base_stat × (1 + 0.07 × (level - 1))
        Example: Base ATK of 20 at Level 10 = 20 × (1 + 0.07 × 9) = 32.6 → 32

        Args:
            base_stat: The stat value at level 1 (from JSON data)
            level: Current level of the fish (1-50)

        Returns:
            The calculated stat value as an integer

        Note:
            You can adjust growth_rate (0.07) to make fish stronger/weaker:
            - 0.05 = slower growth (5% per level)
            - 0.10 = faster growth (10% per level)
        """
        growth_rate = 0.07  # 7% growth per level - balanced for JRPG progression
        stat_value = base_stat * (1 + growth_rate * (level - 1))
        return int(stat_value)  # Convert to integer (rounds down)

    def _get_available_moves(self) -> List[Dict[str, Any]]:
        """Get moves available at current level"""
        available = []
        for move in self.all_moves:
            if move["level"] <= self.level:
                available.append(move)
        return available

    def gain_xp(self, amount: int) -> bool:
        """
        Add XP to the fish. Returns True if leveled up.

        Args:
            amount: Amount of XP to gain

        Returns:
            True if fish leveled up, False otherwise
        """
        # Apply property bonus if applicable
        if self.property.get("effect") == "xp_boost":
            amount = int(amount * self.property.get("value", 1.0))

        self.xp += amount

        # Check for level up
        if self.xp >= self.xp_to_next_level:
            return self.level_up()

        return False

    def level_up(self) -> bool:
        """
        Level up the fish. Returns True if successful.
        """
        if self.level >= 50:  # Max level
            return False

        self.level += 1
        self.xp -= self.xp_to_next_level

        # Recalculate stats
        old_max_hp = self.max_hp
        self.max_hp = self._calculate_stat(self.base_hp, self.level)
        self.current_hp += (self.max_hp - old_max_hp)  # Heal for the HP increase

        self.atk = self._calculate_stat(self.base_atk, self.level)
        self.defense = self._calculate_stat(self.base_def, self.level)
        self.spd = self._calculate_stat(self.base_spd, self.level)

        # Check for new moves
        new_moves = []
        for move in self.all_moves:
            if move["level"] == self.level:
                new_moves.append(move)
                if move not in self.known_moves:
                    self.known_moves.append(move)

        return True

    def take_damage(self, damage: int) -> int:
        """
        Apply damage to the fish and calculate actual damage after defense.

        Uses a damage reduction formula based on defense stat:
        actual_damage = raw_damage × (100 / (100 + defense))

        Examples:
        - Defense 0: Takes 100% damage
        - Defense 50: Takes 67% damage (100/(100+50))
        - Defense 100: Takes 50% damage (100/(100+100))
        - Defense 200: Takes 33% damage (100/(100+200))

        The formula ensures defense is valuable but never makes you invincible.

        Args:
            damage: Raw damage amount before defense reduction

        Returns:
            Actual damage dealt after defense calculation (minimum 1)

        Note:
            Defense is MULTIPLICATIVE with stat modifiers (buffs/debuffs).
            Always deals at least 1 damage to prevent stalling.
        """
        # Get current defense modifier (affected by buffs/debuffs)
        defense_mult = self.stat_modifiers["def"]

        # Calculate damage reduction based on defense
        # Formula: damage × (100 / (100 + effective_defense))
        # Higher defense = lower damage multiplier
        effective_defense = self.defense * defense_mult
        damage_multiplier = 100 / (100 + effective_defense)
        actual_damage = int(damage * damage_multiplier)

        # Ensure at least 1 damage is dealt (prevents immortality)
        actual_damage = max(1, actual_damage)

        # Apply special property effects (e.g., damage reduction abilities)
        if self.property.get("effect") == "damage_reduction_alone":
            # TODO: Check if this is the only fish remaining in party
            # If yes, apply 50% damage reduction bonus
            pass

        # Reduce HP, but never go below 0
        self.current_hp = max(0, self.current_hp - actual_damage)

        return actual_damage

    def heal(self, amount: int) -> int:
        """
        Heal the fish. Returns actual HP restored.

        Args:
            amount: Amount of HP to restore

        Returns:
            Actual HP restored
        """
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - old_hp

    def is_fainted(self) -> bool:
        """Check if fish has fainted (0 HP)"""
        return self.current_hp <= 0

    def revive(self, hp_percent: float = 0.5):
        """
        Revive a fainted fish

        Args:
            hp_percent: Percentage of max HP to restore (default 50%)
        """
        if self.is_fainted():
            self.current_hp = int(self.max_hp * hp_percent)

    def apply_status_effect(self, status: str):
        """Apply a status effect to the fish"""
        if status not in self.status_effects:
            self.status_effects.append(status)

    def remove_status_effect(self, status: str):
        """Remove a status effect from the fish"""
        if status in self.status_effects:
            self.status_effects.remove(status)

    def clear_status_effects(self):
        """Remove all status effects"""
        self.status_effects.clear()

    def apply_stat_modifier(self, stat: str, multiplier: float):
        """
        Apply a temporary stat modifier

        Args:
            stat: Stat to modify (atk, def, spd, accuracy, evasion)
            multiplier: Multiplier to apply (e.g., 1.2 for +20%)
        """
        if stat in self.stat_modifiers:
            self.stat_modifiers[stat] *= multiplier

    def reset_stat_modifiers(self):
        """Reset all stat modifiers to 1.0"""
        for stat in self.stat_modifiers:
            self.stat_modifiers[stat] = 1.0

    def can_use_move(self, move_index: int) -> bool:
        """Check if fish can use the specified move"""
        if move_index < 0 or move_index >= len(self.known_moves):
            return False

        # Check status effects
        if "frozen" in self.status_effects or "asleep" in self.status_effects:
            return False

        # Check if silenced (can only use physical moves)
        move = self.known_moves[move_index]
        if "silenced" in self.status_effects and move["category"] != "Physical":
            return False

        return True

    def equip_item(self, item: Dict[str, Any]):
        """Equip a held item to this fish"""
        self.held_item = item

    def unequip_item(self) -> Optional[Dict[str, Any]]:
        """Remove and return the held item"""
        item = self.held_item
        self.held_item = None
        return item

    def get_effective_stat(self, stat: str) -> int:
        """
        Get the effective value of a stat after modifiers

        Args:
            stat: Stat name (atk, def, spd)

        Returns:
            Effective stat value
        """
        base_value = getattr(self, stat, 0)
        modifier = self.stat_modifiers.get(stat, 1.0)

        # Apply held item bonuses
        if self.held_item:
            bonus_key = f"{stat}_bonus"
            if bonus_key in self.held_item:
                base_value += self.held_item[bonus_key]

        return int(base_value * modifier)

    def __str__(self) -> str:
        """String representation of the fish"""
        return f"{self.name} (Lv.{self.level}) - {self.current_hp}/{self.max_hp} HP"

    def __repr__(self) -> str:
        """Detailed representation for debugging"""
        return (f"Fish(id={self.fish_id}, name={self.name}, level={self.level}, "
                f"hp={self.current_hp}/{self.max_hp}, type={self.type})")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert fish to dictionary for saving to JSON.

        Only saves dynamic state that changes during gameplay.
        Static data (name, base stats, moves) comes from fish.json.

        Returns:
            Dictionary with all data needed to restore this fish's state

        Example saved data:
            {
                "fish_id": "holy_mackerel",
                "level": 15,
                "xp": 450,
                "current_hp": 48,
                "held_item": {"id": "focus_band", ...},
                "status_effects": ["blessed"]
            }
        """
        return {
            "fish_id": self.fish_id,          # Which fish type (links to JSON)
            "level": self.level,              # Current level (1-50)
            "xp": self.xp,                    # XP toward next level
            "current_hp": self.current_hp,    # Current HP (can be damaged)
            "held_item": self.held_item,      # Equipped item (or None)
            "status_effects": self.status_effects  # Active status effects
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], fish_data: Dict[str, Any]) -> 'Fish':
        """
        Create fish from saved dictionary (load game).

        This is a "class method" - called on the Fish class itself, not an instance.
        Usage: fish = Fish.from_dict(saved_data, fish_json_data)

        Args:
            data: Dictionary from save file (from to_dict())
            fish_data: Static fish data from fish.json

        Returns:
            Fully restored Fish instance with saved state

        Note:
            Stats are recalculated from base stats + level, ensuring
            balance changes in fish.json apply to saved fish.
        """
        # Create fish with saved level (recalculates all stats)
        fish = cls(data["fish_id"], fish_data, data["level"])

        # Restore saved state
        fish.xp = data["xp"]                              # Restore XP progress
        fish.current_hp = data["current_hp"]              # Restore HP (might be damaged)
        fish.held_item = data.get("held_item")            # Restore equipped item
        fish.status_effects = data.get("status_effects", [])  # Restore status effects

        return fish
