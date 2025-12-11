"""
Town System - Town exploration, NPCs, and locations
"""

from typing import List, Dict, Any, Optional
from enum import Enum


class LocationType(Enum):
    """Types of locations in a town"""
    INN = "inn"
    BAKER = "baker"
    FISHMONGER = "fishmonger"
    HOUSE = "house"
    CHURCH = "church"
    PLAZA = "plaza"
    GATE = "gate"
    FISHING_SPOT = "fishing_spot"
    SPECIAL = "special"


class NPCType(Enum):
    """Types of NPCs"""
    VILLAGER = "villager"
    MERCHANT = "merchant"
    APOSTLE = "apostle"
    QUEST_GIVER = "quest_giver"
    HEALER = "healer"
    FISHERMAN = "fisherman"
    PHARISEE = "pharisee"
    ROMAN = "roman"
    BEGGAR = "beggar"


class NPC:
    """Non-player character"""

    def __init__(self,
                 npc_id: str,
                 name: str,
                 npc_type: NPCType,
                 dialogue: List[str],
                 location: str = "plaza"):
        """
        Initialize NPC

        Args:
            npc_id: Unique NPC identifier
            name: NPC name
            npc_type: Type of NPC
            dialogue: List of dialogue lines
            location: Location in town
        """
        self.npc_id = npc_id
        self.name = name
        self.npc_type = npc_type
        self.dialogue = dialogue
        self.location = location
        self.dialogue_index = 0
        self.talked_to = False

        # Quest-related
        self.quest_id = None
        self.quest_complete_dialogue = None

        # Special interactions
        self.can_recruit = False
        self.can_battle = False
        self.can_heal = False

    def get_dialogue(self) -> str:
        """
        Get next dialogue line

        Returns:
            Dialogue string
        """
        if not self.dialogue:
            return "..."

        dialogue = self.dialogue[self.dialogue_index]
        self.dialogue_index = (self.dialogue_index + 1) % len(self.dialogue)
        self.talked_to = True

        return dialogue

    def reset_dialogue(self):
        """Reset dialogue to beginning"""
        self.dialogue_index = 0


class Location:
    """A location within a town"""

    def __init__(self,
                 location_id: str,
                 name: str,
                 location_type: LocationType,
                 description: str):
        """
        Initialize location

        Args:
            location_id: Unique location identifier
            name: Location name
            location_type: Type of location
            description: Description text
        """
        self.location_id = location_id
        self.name = name
        self.location_type = location_type
        self.description = description
        self.npcs: List[NPC] = []
        self.connected_locations: List[str] = []

        # Location properties
        self.can_rest = location_type == LocationType.INN
        self.can_shop = location_type in [LocationType.BAKER, LocationType.FISHMONGER]
        self.can_fish = location_type == LocationType.FISHING_SPOT
        self.is_exit = location_type == LocationType.GATE

    def add_npc(self, npc: NPC):
        """Add an NPC to this location"""
        self.npcs.append(npc)

    def get_npcs(self) -> List[NPC]:
        """Get all NPCs at this location"""
        return self.npcs


class Town:
    """Represents a town in the game"""

    def __init__(self, town_data: Dict[str, Any]):
        """
        Initialize town from data

        Args:
            town_data: Town data dictionary (from towns.json)
        """
        self.town_id = town_data["id"]
        self.name = town_data["name"]
        self.region = town_data["region"]
        self.description = town_data.get("description", "")
        self.biblical_reference = town_data.get("biblical_reference", "")

        # Locations in town
        self.locations: Dict[str, Location] = {}
        self.current_location = "plaza"  # Default starting location

        # Town features
        self.has_inn = True
        self.has_baker = True
        self.has_fishmonger = True
        self.has_fishing_spot = town_data.get("fishing_spot", False)

        # Story elements
        self.apostle_to_recruit = town_data.get("apostle")
        self.boss_battle = town_data.get("boss")
        self.main_quest = town_data.get("main_quest")

        # Build default town layout
        self._build_default_layout()

    def _build_default_layout(self):
        """Build default town layout with standard locations"""

        # Plaza (central area)
        plaza = Location(
            "plaza",
            f"{self.name} Plaza",
            LocationType.PLAZA,
            f"The central plaza of {self.name}. People gather here to trade and talk."
        )
        self.locations["plaza"] = plaza

        # Inn (healing and rest)
        inn = Location(
            "inn",
            f"{self.name} Inn",
            LocationType.INN,
            "A warm inn where weary travelers can rest and restore their strength."
        )
        plaza.connected_locations.append("inn")
        self.locations["inn"] = inn

        # Baker (shop)
        baker = Location(
            "baker",
            "Baker's Shop",
            LocationType.BAKER,
            "The aroma of fresh bread fills the air."
        )
        plaza.connected_locations.append("baker")
        self.locations["baker"] = baker

        # Fishmonger (shop)
        fishmonger = Location(
            "fishmonger",
            "Fishmonger",
            LocationType.FISHMONGER,
            "Fresh fish and fishing supplies."
        )
        plaza.connected_locations.append("fishmonger")
        self.locations["fishmonger"] = fishmonger

        # Town gate (exit)
        gate = Location(
            "gate",
            "Town Gate",
            LocationType.GATE,
            f"The gate leading out of {self.name}."
        )
        plaza.connected_locations.append("gate")
        self.locations["gate"] = gate

        # Fishing spot (if available)
        if self.has_fishing_spot:
            fishing_spot = Location(
                "fishing_spot",
                "Fishing Spot",
                LocationType.FISHING_SPOT,
                "A quiet spot by the water, perfect for fishing."
            )
            plaza.connected_locations.append("fishing_spot")
            self.locations["fishing_spot"] = fishing_spot

    def add_location(self, location: Location):
        """Add a custom location to the town"""
        self.locations[location.location_id] = location

    def get_location(self, location_id: str) -> Optional[Location]:
        """Get a location by ID"""
        return self.locations.get(location_id)

    def move_to_location(self, location_id: str) -> bool:
        """
        Move to a different location in town

        Args:
            location_id: Location to move to

        Returns:
            True if move was successful
        """
        if location_id in self.locations:
            self.current_location = location_id
            return True
        return False

    def get_current_location(self) -> Optional[Location]:
        """Get the current location"""
        return self.locations.get(self.current_location)

    def get_available_exits(self) -> List[str]:
        """
        Get locations you can move to from current location

        Returns:
            List of location IDs
        """
        current = self.get_current_location()
        if current:
            return current.connected_locations
        return []

    def add_npc(self, npc: NPC, location_id: str = "plaza"):
        """
        Add an NPC to a location

        Args:
            npc: NPC to add
            location_id: Location to add NPC to
        """
        location = self.get_location(location_id)
        if location:
            location.add_npc(npc)

    def create_default_npcs(self):
        """Create default NPCs for the town"""

        # Innkeeper
        innkeeper = NPC(
            f"{self.town_id}_innkeeper",
            "Innkeeper",
            NPCType.HEALER,
            [
                "Welcome to the inn! Rest here to restore your fish to full health.",
                "A good night's rest heals all wounds.",
                "Your fish look tired. Why not rest a while?"
            ],
            "inn"
        )
        innkeeper.can_heal = True
        self.add_npc(innkeeper, "inn")

        # Baker
        baker = NPC(
            f"{self.town_id}_baker",
            "Baker",
            NPCType.MERCHANT,
            [
                "Fresh bread, baked daily!",
                "My bread is the finest in all the land!",
                "The bread of life starts here!"
            ],
            "baker"
        )
        self.add_npc(baker, "baker")

        # Fishmonger
        fishmonger = NPC(
            f"{self.town_id}_fishmonger",
            "Fishmonger",
            NPCType.FISHERMAN,
            [
                "Looking for fish or fishing supplies?",
                "I've been fishing these waters all my life.",
                "The fish are biting today!"
            ],
            "fishmonger"
        )
        self.add_npc(fishmonger, "fishmonger")

        # Random villagers
        villagers_dialogue = [
            ["Have you heard the news?", "Strange things are happening lately.", "The Romans are always watching."],
            ["Welcome to our town!", "We don't get many visitors.", "Are you a traveling rabbi?"],
            ["The harvest was good this year.", "Thank the Lord for His blessings.", "Times are hard, but we endure."],
            ["I saw a miracle once...", "Some say a prophet walks among us.", "These are trying times."]
        ]

        for i, dialogue in enumerate(villagers_dialogue):
            villager = NPC(
                f"{self.town_id}_villager_{i}",
                f"Villager",
                NPCType.VILLAGER,
                dialogue,
                "plaza"
            )
            self.add_npc(villager, "plaza")


class TownManager:
    """Manages all towns and town navigation"""

    def __init__(self):
        """Initialize town manager"""
        self.towns: Dict[str, Town] = {}
        self.current_town: Optional[Town] = None

    def load_town(self, town_data: Dict[str, Any]) -> Town:
        """
        Load a town from data

        Args:
            town_data: Town data dictionary

        Returns:
            Town instance
        """
        town = Town(town_data)
        town.create_default_npcs()
        self.towns[town.town_id] = town
        return town

    def get_town(self, town_id: str) -> Optional[Town]:
        """Get a town by ID"""
        return self.towns.get(town_id)

    def enter_town(self, town_id: str) -> bool:
        """
        Enter a town

        Args:
            town_id: Town to enter

        Returns:
            True if successful
        """
        town = self.get_town(town_id)
        if town:
            self.current_town = town
            # Reset to plaza when entering town
            town.current_location = "plaza"
            return True
        return False

    def get_current_town(self) -> Optional[Town]:
        """Get the current town"""
        return self.current_town

    def get_current_location(self) -> Optional[Location]:
        """Get current location in current town"""
        if self.current_town:
            return self.current_town.get_current_location()
        return None
