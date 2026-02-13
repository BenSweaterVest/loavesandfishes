"""
Game State Management - Central state and scene management
"""

from enum import Enum
from typing import Optional, Dict, Any
import random

from utils.data_loader import get_data_loader


class GameScene(Enum):
    """Game scenes/states"""
    TITLE = "title"
    TOWN = "town"
    WORLD_MAP = "world_map"
    BATTLE = "battle"
    MENU = "menu"
    SHOP = "shop"
    DIALOGUE = "dialogue"
    CUTSCENE = "cutscene"
    FISHING = "fishing"
    GAME_OVER = "game_over"
    CREDITS = "credits"


class EncounterType(Enum):
    """Random encounter types"""
    NONE = "none"
    WILD_BATTLE = "wild_battle"
    NPC_DIALOGUE = "npc_dialogue"
    TREASURE = "treasure"
    PARABLE = "parable"


class GameState:
    """Manages overall game state and scene transitions"""

    def __init__(self, player):
        """
        Initialize game state

        Args:
            player: Player instance
        """
        self.player = player
        self.current_scene = GameScene.TITLE
        self.previous_scene = None

        # Scene-specific state
        self.current_town = "Nazareth"
        self.current_shop = None
        self.current_battle = None
        self.current_dialogue = None
        self.current_cutscene = None

        # Quest tracking
        self.active_quests = []
        self.completed_quests = []
        self.available_quests = []

        # Parable collection
        self.collected_parables = []
        self.parables_seen = []

        # Progression flags
        self.story_flags = {
            "game_started": False,
            "first_fish_caught": False,
            "first_battle_won": False,
            "first_apostle_recruited": False,
            "cana_wedding_complete": False,
            "five_thousand_fed": False,
            "lazarus_raised": False,
            "temple_cleansed": False,
            "final_battle_unlocked": False,
            "game_completed": False
        }

        # Unlocked features
        self.unlocked_towns = ["Nazareth"]  # Start in hometown
        self.unlocked_fast_travel = []
        self.unlocked_miracles = []

        # Random encounters
        self.steps_since_encounter = 0
        self.encounter_rate = 0.1  # 10% per step

        # Game stats
        self.playtime = 0
        self.total_steps = 0
        self.fish_caught = 0
        self.battles_won = 0
        self.battles_fled = 0

    def change_scene(self, new_scene: GameScene, **kwargs):
        """
        Change to a new scene

        Args:
            new_scene: Scene to change to
            **kwargs: Scene-specific parameters
        """
        self.previous_scene = self.current_scene
        self.current_scene = new_scene

        # Handle scene-specific initialization
        if new_scene == GameScene.TOWN:
            self.current_town = kwargs.get("town", self.current_town)
        elif new_scene == GameScene.SHOP:
            self.current_shop = kwargs.get("shop")
        elif new_scene == GameScene.BATTLE:
            self.current_battle = kwargs.get("battle")
        elif new_scene == GameScene.DIALOGUE:
            self.current_dialogue = kwargs.get("dialogue")
        elif new_scene == GameScene.CUTSCENE:
            self.current_cutscene = kwargs.get("cutscene")

    def return_to_previous_scene(self):
        """Return to the previous scene"""
        if self.previous_scene:
            temp = self.current_scene
            self.current_scene = self.previous_scene
            self.previous_scene = temp

    def take_step(self) -> EncounterType:
        """
        Player takes a step (for random encounters)

        Returns:
            Type of encounter (if any)
        """
        self.total_steps += 1
        self.steps_since_encounter += 1

        # Check for random encounter
        if random.random() < self.encounter_rate:
            self.steps_since_encounter = 0

            # Determine encounter type
            roll = random.random()

            if roll < 0.7:  # 70% wild battle
                return EncounterType.WILD_BATTLE
            elif roll < 0.85:  # 15% NPC dialogue
                return EncounterType.NPC_DIALOGUE
            elif roll < 0.95:  # 10% treasure
                return EncounterType.TREASURE
            else:  # 5% parable
                return EncounterType.PARABLE

        return EncounterType.NONE

    def unlock_town(self, town: str):
        """Unlock a new town"""
        if town not in self.unlocked_towns:
            self.unlocked_towns.append(town)

    def unlock_fast_travel(self, town: str):
        """Unlock fast travel to a town"""
        if town not in self.unlocked_fast_travel and town in self.unlocked_towns:
            self.unlocked_fast_travel.append(town)

    def unlock_miracle(self, miracle: str):
        """Unlock a miracle ability"""
        if miracle not in self.unlocked_miracles:
            self.unlocked_miracles.append(miracle)

    def set_story_flag(self, flag: str, value: bool = True):
        """Set a story progression flag"""
        if flag in self.story_flags:
            self.story_flags[flag] = value

    def get_story_flag(self, flag: str) -> bool:
        """Get a story progression flag"""
        return self.story_flags.get(flag, False)

    def start_quest(self, quest_id: str):
        """Start a quest"""
        if quest_id not in self.active_quests and quest_id not in self.completed_quests:
            self.active_quests.append(quest_id)

    def complete_quest(self, quest_id: str):
        """Complete a quest"""
        if quest_id in self.active_quests:
            self.active_quests.remove(quest_id)
            self.completed_quests.append(quest_id)

    def collect_parable(self, parable_id: str):
        """Collect a parable"""
        if parable_id not in self.collected_parables:
            self.collected_parables.append(parable_id)

    def can_access_town(self, town: str) -> bool:
        """Check if player can access a town"""
        return town in self.unlocked_towns

    def get_current_region(self) -> str:
        """
        Get the current region based on town

        Returns:
            Region name
        """
        region_map = {
            "Nazareth": "Galilee",
            "Cana": "Galilee",
            "Capernaum": "Galilee",
            "Bethsaida": "Coastal",
            "Magdala": "Coastal",
            "Chorazin": "Coastal",
            "Tiberias": "Coastal",
            "Gadara": "Gentile",
            "Samaria": "Gentile",
            "Jericho": "Judean",
            "Bethany": "Judean",
            "Bethlehem": "Judean",
            "Jerusalem": "Jerusalem"
        }

        return region_map.get(self.current_town, "Unknown")

    def get_available_encounters(self) -> list:
        """
        Get available enemy encounters for current region

        Returns:
            List of enemy IDs
        """
        region = self.get_current_region()

        data_loader = get_data_loader()
        enemies_data = data_loader.load_json("enemies.json").get("enemies", [])
        return [e["id"] for e in enemies_data if e.get("region") == region]

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize game state to dictionary

        Returns:
            Dictionary of game state
        """
        return {
            "current_scene": self.current_scene.value,
            "current_town": self.current_town,
            "active_quests": self.active_quests,
            "completed_quests": self.completed_quests,
            "collected_parables": self.collected_parables,
            "story_flags": self.story_flags,
            "unlocked_towns": self.unlocked_towns,
            "unlocked_fast_travel": self.unlocked_fast_travel,
            "unlocked_miracles": self.unlocked_miracles,
            "playtime": self.playtime,
            "total_steps": self.total_steps,
            "fish_caught": self.fish_caught,
            "battles_won": self.battles_won,
            "battles_fled": self.battles_fled
        }

    def from_dict(self, data: Dict[str, Any]):
        """
        Deserialize game state from dictionary

        Args:
            data: Dictionary of game state
        """
        self.current_scene = GameScene(data.get("current_scene", "title"))
        self.current_town = data.get("current_town", "Nazareth")
        self.active_quests = data.get("active_quests", [])
        self.completed_quests = data.get("completed_quests", [])
        self.collected_parables = data.get("collected_parables", [])
        self.story_flags = data.get("story_flags", {})
        self.unlocked_towns = data.get("unlocked_towns", ["Nazareth"])
        self.unlocked_fast_travel = data.get("unlocked_fast_travel", [])
        self.unlocked_miracles = data.get("unlocked_miracles", [])
        self.playtime = data.get("playtime", 0)
        self.total_steps = data.get("total_steps", 0)
        self.fish_caught = data.get("fish_caught", 0)
        self.battles_won = data.get("battles_won", 0)
        self.battles_fled = data.get("battles_fled", 0)
