"""
Miracle System - Jesus's special abilities (limit breaks)
"""

from typing import Dict, Any, Optional
from enum import Enum


class MiracleType(Enum):
    """Types of miracles"""
    HEALING = "healing"
    OFFENSIVE = "offensive"
    SUPPORT = "support"
    RESURRECTION = "resurrection"


class Miracle:
    """A miracle ability"""

    def __init__(self,
                 miracle_id: str,
                 name: str,
                 miracle_type: MiracleType,
                 description: str,
                 meter_cost: int,
                 biblical_reference: str):
        """
        Initialize miracle

        Args:
            miracle_id: Unique identifier
            name: Miracle name
            miracle_type: Type of miracle
            description: Description and effects
            meter_cost: Miracle meter % required (0-100)
            biblical_reference: Biblical reference
        """
        self.miracle_id = miracle_id
        self.name = name
        self.miracle_type = miracle_type
        self.description = description
        self.meter_cost = meter_cost
        self.biblical_reference = biblical_reference

        # Effect values
        self.power = 0
        self.targets = "party"
        self.effects: Dict[str, Any] = {}

    def can_use(self, current_meter: int) -> bool:
        """
        Check if miracle can be used

        Args:
            current_meter: Current miracle meter value

        Returns:
            True if miracle can be used
        """
        return current_meter >= self.meter_cost


# Define the 4 main miracles
MIRACLES = {
    "healing_miracle": Miracle(
        "healing_miracle",
        "Healing Miracle",
        MiracleType.HEALING,
        "Your faith has made you whole! Fully heals all party fish and cures all status effects.",
        meter_cost=50,
        biblical_reference="Matthew 9:22 (Woman with bleeding)"
    ),

    "loaves_and_fishes": Miracle(
        "loaves_and_fishes",
        "Loaves and Fishes",
        MiracleType.SUPPORT,
        "Feed the multitude! Multiplies the effects of all bread items by 3x for this battle.",
        meter_cost=40,
        biblical_reference="Matthew 14:13-21 (Feeding of 5000)"
    ),

    "divine_judgment": Miracle(
        "divine_judgment",
        "Divine Judgment",
        MiracleType.OFFENSIVE,
        "The wrath of the righteous! Deals 300 Holy damage to all enemies and reduces their stats by 50% for 3 turns.",
        meter_cost=75,
        biblical_reference="Matthew 21:12-13 (Cleansing of Temple)"
    ),

    "resurrection_power": Miracle(
        "resurrection_power",
        "Resurrection Power",
        MiracleType.RESURRECTION,
        "Lazarus, come forth! Revives all fainted fish with full HP and grants immunity for 2 turns.",
        meter_cost=100,
        biblical_reference="John 11:43-44 (Raising of Lazarus)"
    )
}


class MiracleMeter:
    """Manages the miracle meter"""

    def __init__(self):
        """Initialize miracle meter"""
        self.current_meter = 0
        self.max_meter = 100
        self.meter_generation_rate = 5  # Per turn
        self.unlocked_miracles: list = ["healing_miracle"]  # Start with healing

    def add_meter(self, amount: int):
        """
        Add to miracle meter

        Args:
            amount: Amount to add
        """
        self.current_meter = min(self.max_meter, self.current_meter + amount)

    def reduce_meter(self, amount: int):
        """
        Reduce miracle meter

        Args:
            amount: Amount to reduce
        """
        self.current_meter = max(0, self.current_meter - amount)

    def fill_meter(self):
        """Fill meter to max"""
        self.current_meter = self.max_meter

    def reset_meter(self):
        """Reset meter to 0"""
        self.current_meter = 0

    def get_meter_percentage(self) -> int:
        """Get meter as percentage"""
        return int((self.current_meter / self.max_meter) * 100)

    def unlock_miracle(self, miracle_id: str):
        """Unlock a new miracle"""
        if miracle_id not in self.unlocked_miracles and miracle_id in MIRACLES:
            self.unlocked_miracles.append(miracle_id)

    def is_unlocked(self, miracle_id: str) -> bool:
        """Check if miracle is unlocked"""
        return miracle_id in self.unlocked_miracles

    def can_use_miracle(self, miracle_id: str) -> bool:
        """
        Check if a miracle can be used

        Args:
            miracle_id: Miracle to check

        Returns:
            True if miracle can be used
        """
        if not self.is_unlocked(miracle_id):
            return False

        miracle = MIRACLES.get(miracle_id)
        if miracle:
            return miracle.can_use(self.current_meter)

        return False

    def use_miracle(self, miracle_id: str) -> Optional[Miracle]:
        """
        Use a miracle

        Args:
            miracle_id: Miracle to use

        Returns:
            Miracle instance if used, None otherwise
        """
        if self.can_use_miracle(miracle_id):
            miracle = MIRACLES[miracle_id]
            self.reduce_meter(miracle.meter_cost)
            return miracle

        return None

    def get_available_miracles(self) -> list:
        """Get all miracles that can be used"""
        available = []
        for miracle_id in self.unlocked_miracles:
            if miracle_id in MIRACLES and self.can_use_miracle(miracle_id):
                available.append(MIRACLES[miracle_id])
        return available

    def tick(self):
        """Generate meter (called each turn)"""
        self.add_meter(self.meter_generation_rate)

    def on_damage_taken(self, damage: int):
        """
        Generate meter when damage is taken

        Args:
            damage: Damage amount
        """
        # Generate meter based on damage (1% per 10 damage)
        meter_gain = max(1, damage // 10)
        self.add_meter(meter_gain)

    def on_fish_fainted(self):
        """Generate meter when a fish faints"""
        self.add_meter(15)  # Significant meter gain

    def on_enemy_defeated(self):
        """Generate meter when enemy is defeated"""
        self.add_meter(10)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            "current_meter": self.current_meter,
            "unlocked_miracles": self.unlocked_miracles
        }

    def from_dict(self, data: Dict[str, Any]):
        """Deserialize from dictionary"""
        self.current_meter = data.get("current_meter", 0)
        self.unlocked_miracles = data.get("unlocked_miracles", ["healing_miracle"])


# Miracle unlock progression
MIRACLE_UNLOCK_CONDITIONS = {
    "healing_miracle": {
        "unlocked_at_start": True,
        "description": "Available from the beginning"
    },
    "loaves_and_fishes": {
        "quest": "multiplication_practice",
        "description": "Unlocked after feeding the 5000"
    },
    "divine_judgment": {
        "quest": "money_changers",
        "description": "Unlocked after cleansing the temple"
    },
    "resurrection_power": {
        "boss": "death_manifest",
        "description": "Unlocked after defeating Death and raising Lazarus"
    }
}
