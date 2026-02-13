"""
Enemy classes - represents enemies and bosses
"""

from typing import Dict, List, Optional, Any
import random


class Enemy:
    """
    Represents an enemy in battle.
    Similar to Fish but simpler - no leveling system, fixed stats.
    """

    def __init__(self, enemy_data: Dict[str, Any], level: int = 1):
        """
        Initialize an enemy

        Args:
            enemy_data: Dictionary containing enemy data
            level: Enemy level (for scaling)
        """
        self.enemy_id = enemy_data["id"]
        self.name = enemy_data["name"]
        self.enemy_type = enemy_data["type"]
        self.level = level

        # Base stats
        base_stats = enemy_data["base_stats"]
        self.max_hp = self._scale_stat(base_stats["hp"], level)
        self.current_hp = self.max_hp
        self.atk = self._scale_stat(base_stats["atk"], level)
        self.defense = self._scale_stat(base_stats["def"], level)
        self.spd = self._scale_stat(base_stats.get("spd", 10), level)

        # Attacks
        self.attacks = enemy_data.get("attacks", [])

        # Rewards
        self.xp_reward = enemy_data.get("xp_reward", level * 10 + 20)
        self.money_reward = enemy_data.get("money_reward", level * 5 + 10)
        self.item_drops = enemy_data.get("item_drops", [])

        # AI behavior
        self.ai_pattern = enemy_data.get("ai_pattern", "random")

        # Special properties
        self.properties = enemy_data.get("properties", {})

        # Status effects
        self.status_effects: List[str] = []

        # Stat modifiers
        self.stat_modifiers = {
            "atk": 1.0,
            "def": 1.0,
            "spd": 1.0
        }
        self.timed_stat_modifiers = {stat: [] for stat in self.stat_modifiers}
        self.status_durations: Dict[str, int] = {}

        # Track last used attack for cycle pattern
        self._last_attack_index = -1

    def _scale_stat(self, base_stat: int, level: int) -> int:
        """Scale stat based on level"""
        # Enemies grow about 5% per level
        growth_rate = 0.05
        return int(base_stat * (1 + growth_rate * (level - 1)))

    def choose_attack(self) -> Dict[str, Any]:
        """
        Choose which attack to use based on AI pattern.
        Returns the chosen attack dictionary.
        """
        if not self.attacks:
            # Default attack if none defined
            return {
                "name": "Strike",
                "type": "Physical",
                "power": [self.atk // 2, self.atk],
                "accuracy": 100
            }

        if self.ai_pattern == "random":
            return random.choice(self.attacks)
        elif self.ai_pattern == "strongest_first":
            # Use strongest attack if available, otherwise random
            strongest = max(self.attacks, key=lambda a: max(a.get("power", [0])))
            return strongest
        elif self.ai_pattern == "cycle":
            # Cycle through attacks in order
            if not self.attacks:
                return random.choice(self.attacks)
            self._last_attack_index = (self._last_attack_index + 1) % len(self.attacks)
            return self.attacks[self._last_attack_index]
        else:
            return random.choice(self.attacks)

    def take_damage(self, damage: int) -> int:
        """
        Apply damage to the enemy. Returns actual damage dealt.
        """
        defense_mult = self.stat_modifiers["def"]
        actual_damage = max(1, int(damage * (100 / (100 + self.defense * defense_mult))))

        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage

    def heal(self, amount: int) -> int:
        """Heal the enemy. Returns actual HP restored."""
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - old_hp

    def is_defeated(self) -> bool:
        """Check if enemy is defeated"""
        return self.current_hp <= 0

    def apply_status_effect(self, status: str, turns: Optional[int] = None):
        """Apply a status effect"""
        if status != "immunity" and "immunity" in self.status_effects:
            return
        if status not in self.status_effects:
            self.status_effects.append(status)
        if turns and turns > 0:
            current = self.status_durations.get(status, 0)
            self.status_durations[status] = max(current, turns)

    def remove_status_effect(self, status: str):
        """Remove a status effect"""
        if status in self.status_effects:
            self.status_effects.remove(status)
        if status in self.status_durations:
            del self.status_durations[status]

    def apply_stat_modifier(self, stat: str, multiplier: float,
                            turns: Optional[int] = None):
        """Apply a temporary stat modifier"""
        if stat in self.stat_modifiers:
            self.stat_modifiers[stat] *= multiplier
            if turns and turns > 0:
                self.timed_stat_modifiers[stat].append({
                    "multiplier": multiplier,
                    "turns": turns
                })

    def reset_stat_modifiers(self):
        """Reset all stat modifiers"""
        for stat in self.stat_modifiers:
            self.stat_modifiers[stat] = 1.0
        for stat in self.timed_stat_modifiers:
            self.timed_stat_modifiers[stat] = []

    def tick_temporary_effects(self):
        """Tick down temporary stat modifiers and timed status effects"""
        for stat, entries in self.timed_stat_modifiers.items():
            if not entries:
                continue
            remaining_entries = []
            for entry in entries:
                entry["turns"] -= 1
                if entry["turns"] <= 0:
                    multiplier = entry["multiplier"]
                    if multiplier:
                        self.stat_modifiers[stat] /= multiplier
                else:
                    remaining_entries.append(entry)
            self.timed_stat_modifiers[stat] = remaining_entries

        if not self.status_durations:
            return
        expired = []
        for status, turns in self.status_durations.items():
            turns -= 1
            if turns <= 0:
                expired.append(status)
            else:
                self.status_durations[status] = turns
        for status in expired:
            self.remove_status_effect(status)

    def get_effective_stat(self, stat: str) -> int:
        """Get effective stat value after modifiers"""
        base_value = getattr(self, stat, 0)
        modifier = self.stat_modifiers.get(stat, 1.0)
        return int(base_value * modifier)

    def __str__(self) -> str:
        """String representation"""
        return f"{self.name} (Lv.{self.level}) - {self.current_hp}/{self.max_hp} HP"

    def __repr__(self) -> str:
        """Debug representation"""
        return f"Enemy(id={self.enemy_id}, name={self.name}, level={self.level}, hp={self.current_hp}/{self.max_hp})"


class Boss(Enemy):
    """
    Represents a boss enemy with special mechanics.
    Bosses can have multiple phases, special gimmicks, and unique behaviors.
    """

    def __init__(self, boss_data: Dict[str, Any], level: int = 1):
        """Initialize a boss"""
        super().__init__(boss_data, level)

        # Boss-specific data
        self.boss_id = boss_data["id"]
        self.title = boss_data.get("title", "")
        self.phases = boss_data.get("phases", 1)
        self.current_phase = 1

        # Gimmicks and special mechanics
        self.gimmick = boss_data.get("gimmick", None)
        self.special_conditions = boss_data.get("special_conditions", [])

        # Dialogue
        self.intro_dialogue = boss_data.get("intro_dialogue", "...")
        self.defeat_dialogue = boss_data.get("defeat_dialogue", "...")
        self.phase_transitions = boss_data.get("phase_transitions", {})

        # Biblical reference
        self.biblical_reference = boss_data.get("biblical_reference", "")

    def check_phase_transition(self) -> bool:
        """
        Check if boss should transition to next phase.
        Returns True if phase transition occurred.
        """
        if self.current_phase >= self.phases:
            return False

        # Check HP threshold for phase transition
        hp_percent = (self.current_hp / self.max_hp) * 100

        # Transition at 66%, 33% for 3-phase bosses
        # Transition at 50% for 2-phase bosses
        if self.phases == 2 and hp_percent <= 50 and self.current_phase == 1:
            self.transition_phase()
            return True
        elif self.phases == 3:
            if hp_percent <= 66 and self.current_phase == 1:
                self.transition_phase()
                return True
            elif hp_percent <= 33 and self.current_phase == 2:
                self.transition_phase()
                return True

        return False

    def transition_phase(self):
        """Transition to next phase"""
        self.current_phase += 1

        # Heal a bit on phase transition
        heal_amount = int(self.max_hp * 0.1)
        self.heal(heal_amount)

        # Reset stat modifiers
        self.reset_stat_modifiers()

        # Boost stats for new phase
        self.stat_modifiers["atk"] *= 1.2
        self.stat_modifiers["def"] *= 1.1

    def get_phase_dialogue(self) -> Optional[str]:
        """Get dialogue for current phase"""
        return self.phase_transitions.get(str(self.current_phase), None)

    def __str__(self) -> str:
        """String representation"""
        phase_str = f" [Phase {self.current_phase}/{self.phases}]" if self.phases > 1 else ""
        return f"{self.name}{phase_str} (Lv.{self.level}) - {self.current_hp}/{self.max_hp} HP"


# Enemy data templates (will be loaded from JSON in the future)
ENEMY_TEMPLATES = {
    "skeptical_scholar": {
        "id": "skeptical_scholar",
        "name": "Skeptical Scholar",
        "type": "Normal",
        "base_stats": {
            "hp": 25,
            "atk": 8,
            "def": 6,
            "spd": 10
        },
        "attacks": [
            {
                "name": "Doubt",
                "type": "Spirit",
                "power": [6, 10],
                "accuracy": 90,
                "effect": "confusion"
            },
            {
                "name": "Question",
                "type": "Normal",
                "power": [8, 12],
                "accuracy": 100
            }
        ],
        "xp_reward": 15,
        "money_reward": 10,
        "ai_pattern": "random"
    },
    "wild_bandit": {
        "id": "wild_bandit",
        "name": "Wild Bandit",
        "type": "Dark",
        "base_stats": {
            "hp": 35,
            "atk": 12,
            "def": 8,
            "spd": 12
        },
        "attacks": [
            {
                "name": "Steal",
                "type": "Dark",
                "power": [8, 14],
                "accuracy": 90,
                "effect": "steal_money"
            },
            {
                "name": "Slash",
                "type": "Physical",
                "power": [10, 16],
                "accuracy": 95
            }
        ],
        "xp_reward": 20,
        "money_reward": 25,
        "ai_pattern": "random"
    }
}

BOSS_TEMPLATES = {
    "steward_feast": {
        "id": "steward_feast",
        "name": "Steward of the Feast",
        "type": "Normal",
        "base_stats": {
            "hp": 60,
            "atk": 12,
            "def": 10,
            "spd": 8
        },
        "attacks": [
            {
                "name": "Wine Toss",
                "type": "Water",
                "power": [12, 18],
                "accuracy": 85,
                "effect": "confusion"
            },
            {
                "name": "Harsh Critique",
                "type": "Spirit",
                "power": [8, 12],
                "accuracy": 100,
                "effect": "atk_down"
            },
            {
                "name": "Sommelier Sniff",
                "type": "Status",
                "power": [0, 0],
                "accuracy": 100,
                "effect": "evasion_up"
            }
        ],
        "xp_reward": 100,
        "money_reward": 200,
        "phases": 1,
        "gimmick": "Gets progressively drunker and sloppier",
        "intro_dialogue": "This wine is... *hic*... absolutely unacceptable!",
        "defeat_dialogue": "Wait... this new wine is... magnificent! My apologies!",
        "biblical_reference": "John 2:1-11 (Wedding at Cana)",
        "ai_pattern": "random"
    }
}


def create_enemy(enemy_id: str, level: int = 1) -> Optional[Enemy]:
    """
    Factory function to create an enemy by ID.

    Args:
        enemy_id: Enemy template ID
        level: Enemy level

    Returns:
        Enemy instance or None if not found
    """
    if enemy_id in ENEMY_TEMPLATES:
        return Enemy(ENEMY_TEMPLATES[enemy_id], level)
    return None


def create_boss(boss_id: str, level: int = 1) -> Optional[Boss]:
    """
    Factory function to create a boss by ID.

    Args:
        boss_id: Boss template ID
        level: Boss level

    Returns:
        Boss instance or None if not found
    """
    if boss_id in BOSS_TEMPLATES:
        return Boss(BOSS_TEMPLATES[boss_id], level)
    return None
