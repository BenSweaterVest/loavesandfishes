"""
Player class - represents Jesus and his party management
"""

from typing import List, Dict, Optional, Any
from .fish import Fish


class Player:
    """
    Represents Jesus (the player character).
    Manages party fish, inventory, apostles, money, and progression.
    """

    def __init__(self, name: str = "Jesus"):
        """Initialize the player"""
        self.name = name
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100

        # Base stats
        self.base_hp = 50
        self.max_hp = self._calculate_stat(self.base_hp, self.level)
        self.current_hp = self.max_hp

        # Fish party (4 active, unlimited storage)
        self.active_party: List[Fish] = []
        self.fish_storage: List[Fish] = []

        # Apostles
        self.recruited_apostles: List[str] = []  # List of apostle IDs

        # Inventory
        self.bread_items: Dict[str, int] = {}  # item_id -> quantity
        self.money = 0  # Denarii

        # Equipment
        self.equipped_robe: Optional[Dict[str, Any]] = None
        self.equipped_accessory: Optional[Dict[str, Any]] = None

        # Progression
        self.current_town = "nazareth"
        self.visited_towns: List[str] = ["nazareth"]
        self.completed_quests: List[str] = []
        self.found_parables: List[str] = []

        # Miracle meter (limit break)
        self.miracle_meter = 0.0  # 0-100%

        # Battle statistics
        self.battles_won = 0
        self.battles_lost = 0
        self.total_damage_dealt = 0

        # Game state
        self.difficulty = "normal"

    def _calculate_stat(self, base_stat: int, level: int) -> int:
        """Calculate stat based on level"""
        growth_rate = 0.05  # Jesus grows slower than fish
        return int(base_stat * (1 + growth_rate * (level - 1)))

    def add_fish_to_party(self, fish: Fish) -> bool:
        """
        Add a fish to the active party.
        Returns True if successful, False if party is full.
        """
        if len(self.active_party) >= 4:
            return False
        self.active_party.append(fish)
        return True

    def add_fish_to_storage(self, fish: Fish):
        """Add a fish to storage"""
        self.fish_storage.append(fish)

    def remove_fish_from_party(self, index: int) -> Optional[Fish]:
        """Remove a fish from party and return it"""
        if 0 <= index < len(self.active_party):
            return self.active_party.pop(index)
        return None

    def swap_fish(self, party_index: int, storage_index: int) -> bool:
        """
        Swap a fish between party and storage.
        Returns True if successful.
        """
        if party_index < 0 or party_index >= len(self.active_party):
            return False
        if storage_index < 0 or storage_index >= len(self.fish_storage):
            return False

        # Swap
        temp = self.active_party[party_index]
        self.active_party[party_index] = self.fish_storage[storage_index]
        self.fish_storage[storage_index] = temp
        return True

    def get_active_fish(self) -> List[Fish]:
        """Get list of non-fainted fish in party"""
        return [f for f in self.active_party if not f.is_fainted()]

    def has_usable_fish(self) -> bool:
        """Check if player has any non-fainted fish"""
        return len(self.get_active_fish()) > 0

    def add_bread_item(self, item_id: str, quantity: int = 1):
        """Add bread item to inventory"""
        if item_id in self.bread_items:
            self.bread_items[item_id] += quantity
        else:
            self.bread_items[item_id] = quantity

    def remove_bread_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Remove bread item from inventory.
        Returns True if successful, False if not enough items.
        """
        if item_id not in self.bread_items or self.bread_items[item_id] < quantity:
            return False

        self.bread_items[item_id] -= quantity
        if self.bread_items[item_id] <= 0:
            del self.bread_items[item_id]
        return True

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """Check if player has enough of an item"""
        return self.bread_items.get(item_id, 0) >= quantity

    def add_money(self, amount: int):
        """Add money (denarii)"""
        self.money += amount

    def spend_money(self, amount: int) -> bool:
        """
        Spend money. Returns True if successful, False if not enough money.
        """
        if self.money >= amount:
            self.money -= amount
            return True
        return False

    def recruit_apostle(self, apostle_id: str):
        """Recruit an apostle"""
        if apostle_id not in self.recruited_apostles:
            self.recruited_apostles.append(apostle_id)

    def has_apostle(self, apostle_id: str) -> bool:
        """Check if an apostle is recruited"""
        return apostle_id in self.recruited_apostles

    def equip_robe(self, robe: Dict[str, Any]):
        """Equip a robe"""
        self.equipped_robe = robe

    def equip_accessory(self, accessory: Dict[str, Any]):
        """Equip an accessory"""
        self.equipped_accessory = accessory

    def get_defense(self) -> int:
        """Get total defense including equipment"""
        base_def = 10  # Base defense

        if self.equipped_robe:
            base_def += self.equipped_robe.get("def_bonus", 0)

        return base_def

    def take_damage(self, damage: int) -> int:
        """
        Jesus takes damage. Returns actual damage dealt.
        Used when fish can't fight.
        """
        defense = self.get_defense()
        actual_damage = max(1, damage - defense // 2)

        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage

    def heal(self, amount: int) -> int:
        """Heal Jesus. Returns actual HP restored."""
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - old_hp

    def is_defeated(self) -> bool:
        """Check if Jesus is defeated (0 HP and no usable fish)"""
        return self.current_hp <= 0 or not self.has_usable_fish()

    def gain_xp(self, amount: int) -> bool:
        """
        Gain XP. Returns True if leveled up.
        """
        self.xp += amount

        if self.xp >= self.xp_to_next_level:
            return self.level_up()
        return False

    def level_up(self) -> bool:
        """Level up Jesus"""
        if self.level >= 50:
            return False

        self.level += 1
        self.xp -= self.xp_to_next_level

        # Recalculate stats
        old_max_hp = self.max_hp
        self.max_hp = self._calculate_stat(self.base_hp, self.level)
        self.current_hp += (self.max_hp - old_max_hp)

        return True

    def add_miracle_meter(self, amount: float):
        """Add to miracle meter (0-100)"""
        self.miracle_meter = min(100.0, self.miracle_meter + amount)

    def is_miracle_ready(self) -> bool:
        """Check if miracle meter is full"""
        return self.miracle_meter >= 100.0

    def use_miracle(self):
        """Use miracle (resets meter)"""
        self.miracle_meter = 0.0

    def visit_town(self, town_id: str):
        """Visit a town"""
        self.current_town = town_id
        if town_id not in self.visited_towns:
            self.visited_towns.append(town_id)

    def complete_quest(self, quest_id: str):
        """Mark a quest as completed"""
        if quest_id not in self.completed_quests:
            self.completed_quests.append(quest_id)

    def find_parable(self, parable_id: str):
        """Find a collectible parable"""
        if parable_id not in self.found_parables:
            self.found_parables.append(parable_id)

    def get_parable_count(self) -> int:
        """Get number of parables found"""
        return len(self.found_parables)

    def rest_at_inn(self):
        """Rest at inn (full heal)"""
        self.current_hp = self.max_hp
        for fish in self.active_party:
            fish.current_hp = fish.max_hp
            fish.clear_status_effects()

    def __str__(self) -> str:
        """String representation"""
        return f"{self.name} (Lv.{self.level}) - {self.current_hp}/{self.max_hp} HP"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for saving"""
        return {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "current_hp": self.current_hp,
            "active_party": [fish.to_dict() for fish in self.active_party],
            "fish_storage": [fish.to_dict() for fish in self.fish_storage],
            "recruited_apostles": self.recruited_apostles,
            "bread_items": self.bread_items,
            "money": self.money,
            "equipped_robe": self.equipped_robe,
            "equipped_accessory": self.equipped_accessory,
            "current_town": self.current_town,
            "visited_towns": self.visited_towns,
            "completed_quests": self.completed_quests,
            "found_parables": self.found_parables,
            "miracle_meter": self.miracle_meter,
            "battles_won": self.battles_won,
            "battles_lost": self.battles_lost,
            "difficulty": self.difficulty
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], fish_data_loader) -> 'Player':
        """Create player from saved dictionary"""
        player = cls(data["name"])
        player.level = data["level"]
        player.xp = data["xp"]
        player.current_hp = data["current_hp"]

        # Load fish (requires fish_data_loader to get fish stats)
        from .fish import Fish
        player.active_party = [
            Fish.from_dict(f_data, fish_data_loader.get_fish_by_id(f_data["fish_id"]))
            for f_data in data["active_party"]
        ]
        player.fish_storage = [
            Fish.from_dict(f_data, fish_data_loader.get_fish_by_id(f_data["fish_id"]))
            for f_data in data["fish_storage"]
        ]

        player.recruited_apostles = data["recruited_apostles"]
        player.bread_items = data["bread_items"]
        player.money = data["money"]
        player.equipped_robe = data.get("equipped_robe")
        player.equipped_accessory = data.get("equipped_accessory")
        player.current_town = data["current_town"]
        player.visited_towns = data["visited_towns"]
        player.completed_quests = data["completed_quests"]
        player.found_parables = data["found_parables"]
        player.miracle_meter = data.get("miracle_meter", 0.0)
        player.battles_won = data.get("battles_won", 0)
        player.battles_lost = data.get("battles_lost", 0)
        player.difficulty = data.get("difficulty", "normal")

        return player
