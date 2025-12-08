"""
Save and Load System - Persistent game state management
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path


class SaveSystem:
    """Manages game save and load operations"""

    def __init__(self, save_dir: str = None):
        """
        Initialize save system

        Args:
            save_dir: Directory for save files (default: ~/.loavesandfishes/saves)
        """
        if save_dir is None:
            # Use user's home directory
            home = Path.home()
            self.save_dir = home / ".loavesandfishes" / "saves"
        else:
            self.save_dir = Path(save_dir)

        # Create save directory if it doesn't exist
        self.save_dir.mkdir(parents=True, exist_ok=True)

        # Maximum number of save slots
        self.max_slots = 5

    def get_save_path(self, slot: int) -> Path:
        """
        Get path for a save slot

        Args:
            slot: Save slot number (1-5)

        Returns:
            Path to save file
        """
        return self.save_dir / f"save_slot_{slot}.json"

    def save_game(self, player, slot: int, save_name: str = None) -> bool:
        """
        Save the game state

        Args:
            player: Player instance to save
            slot: Save slot number (1-5)
            save_name: Optional custom save name

        Returns:
            True if save succeeded
        """
        if slot < 1 or slot > self.max_slots:
            print(f"Invalid save slot: {slot}. Must be 1-{self.max_slots}")
            return False

        try:
            # Build save data
            save_data = {
                "version": "1.0",
                "slot": slot,
                "save_name": save_name or f"Save {slot}",
                "timestamp": datetime.now().isoformat(),
                "playtime": 0,  # TODO: Track playtime
                "player_data": self._serialize_player(player)
            }

            # Write to file
            save_path = self.get_save_path(slot)
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            print(f"Game saved to slot {slot}: {save_path}")
            return True

        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, player, slot: int) -> bool:
        """
        Load game state

        Args:
            player: Player instance to load into
            slot: Save slot number (1-5)

        Returns:
            True if load succeeded
        """
        if slot < 1 or slot > self.max_slots:
            print(f"Invalid save slot: {slot}. Must be 1-{self.max_slots}")
            return False

        save_path = self.get_save_path(slot)

        if not save_path.exists():
            print(f"No save file found in slot {slot}")
            return False

        try:
            # Read save file
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            # Verify version (for future compatibility)
            version = save_data.get("version", "1.0")
            if version != "1.0":
                print(f"Warning: Save file version {version} may not be compatible")

            # Deserialize player data
            player_data = save_data.get("player_data", {})
            self._deserialize_player(player, player_data)

            print(f"Game loaded from slot {slot}")
            return True

        except Exception as e:
            print(f"Error loading game: {e}")
            return False

    def get_save_info(self, slot: int) -> Optional[Dict[str, Any]]:
        """
        Get information about a save file without loading it

        Args:
            slot: Save slot number

        Returns:
            Dictionary with save info, or None if no save exists
        """
        save_path = self.get_save_path(slot)

        if not save_path.exists():
            return None

        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            # Extract key info
            player_data = save_data.get("player_data", {})

            return {
                "slot": slot,
                "save_name": save_data.get("save_name", f"Save {slot}"),
                "timestamp": save_data.get("timestamp"),
                "playtime": save_data.get("playtime", 0),
                "player_name": player_data.get("name", "Unknown"),
                "player_level": player_data.get("level", 1),
                "location": player_data.get("current_town", "Unknown"),
                "party_size": len(player_data.get("active_party", [])),
                "money": player_data.get("money", 0)
            }

        except Exception as e:
            print(f"Error reading save info: {e}")
            return None

    def delete_save(self, slot: int) -> bool:
        """
        Delete a save file

        Args:
            slot: Save slot number

        Returns:
            True if deletion succeeded
        """
        save_path = self.get_save_path(slot)

        if not save_path.exists():
            print(f"No save file found in slot {slot}")
            return False

        try:
            save_path.unlink()
            print(f"Deleted save in slot {slot}")
            return True

        except Exception as e:
            print(f"Error deleting save: {e}")
            return False

    def list_saves(self) -> Dict[int, Dict[str, Any]]:
        """
        List all available saves

        Returns:
            Dictionary mapping slot numbers to save info
        """
        saves = {}

        for slot in range(1, self.max_slots + 1):
            info = self.get_save_info(slot)
            if info:
                saves[slot] = info

        return saves

    def _serialize_player(self, player) -> Dict[str, Any]:
        """
        Serialize player data to dictionary

        Args:
            player: Player instance

        Returns:
            Dictionary of player data
        """
        # Use the player's built-in to_dict method if available
        if hasattr(player, 'to_dict'):
            return player.to_dict()

        # Otherwise manually serialize
        return {
            "name": player.name,
            "level": player.level,
            "current_hp": player.current_hp,
            "max_hp": player.max_hp,
            "current_xp": player.current_xp,
            "money": player.money,
            "current_town": player.current_town,
            "active_party": [self._serialize_fish(f) for f in player.active_party],
            "fish_storage": [self._serialize_fish(f) for f in player.fish_storage],
            "bread_inventory": player.bread_inventory,
            "key_items": player.key_items,
            "equipped_robe": player.equipped_robe,
            "equipped_accessory": player.equipped_accessory,
            "recruited_apostles": player.recruited_apostles,
            "miracle_meter": player.miracle_meter,
            "battles_won": player.battles_won,
            "battles_lost": player.battles_lost,
            "completed_quests": getattr(player, 'completed_quests', []),
            "active_quests": getattr(player, 'active_quests', []),
            "collected_parables": getattr(player, 'collected_parables', []),
            "unlocked_towns": getattr(player, 'unlocked_towns', []),
            "unlocked_fast_travel": getattr(player, 'unlocked_fast_travel', [])
        }

    def _deserialize_player(self, player, data: Dict[str, Any]):
        """
        Deserialize player data from dictionary

        Args:
            player: Player instance to load into
            data: Dictionary of player data
        """
        # Use the player's built-in from_dict method if available
        if hasattr(player, 'from_dict'):
            player.from_dict(data)
            return

        # Otherwise manually deserialize
        player.name = data.get("name", "Jesus")
        player.level = data.get("level", 1)
        player.current_hp = data.get("current_hp", 100)
        player.max_hp = data.get("max_hp", 100)
        player.current_xp = data.get("current_xp", 0)
        player.money = data.get("money", 0)
        player.current_town = data.get("current_town", "Nazareth")

        # Load fish (requires Fish class to deserialize)
        # TODO: Implement fish deserialization
        player.active_party = []
        player.fish_storage = []

        player.bread_inventory = data.get("bread_inventory", {})
        player.key_items = data.get("key_items", [])
        player.equipped_robe = data.get("equipped_robe")
        player.equipped_accessory = data.get("equipped_accessory")
        player.recruited_apostles = data.get("recruited_apostles", [])
        player.miracle_meter = data.get("miracle_meter", 0)
        player.battles_won = data.get("battles_won", 0)
        player.battles_lost = data.get("battles_lost", 0)

        # Extended data
        if hasattr(player, 'completed_quests'):
            player.completed_quests = data.get("completed_quests", [])
        if hasattr(player, 'active_quests'):
            player.active_quests = data.get("active_quests", [])
        if hasattr(player, 'collected_parables'):
            player.collected_parables = data.get("collected_parables", [])
        if hasattr(player, 'unlocked_towns'):
            player.unlocked_towns = data.get("unlocked_towns", [])
        if hasattr(player, 'unlocked_fast_travel'):
            player.unlocked_fast_travel = data.get("unlocked_fast_travel", [])

    def _serialize_fish(self, fish) -> Dict[str, Any]:
        """
        Serialize a fish to dictionary

        Args:
            fish: Fish instance

        Returns:
            Dictionary of fish data
        """
        return {
            "fish_id": fish.fish_id,
            "nickname": fish.nickname,
            "level": fish.level,
            "current_hp": fish.current_hp,
            "max_hp": fish.max_hp,
            "current_xp": fish.current_xp,
            "atk": fish.atk,
            "defense": fish.defense,
            "spd": fish.spd,
            "type": fish.type,
            "known_moves": fish.known_moves,
            "status_effects": fish.status_effects,
            "held_item": getattr(fish, 'held_item', None)
        }

    def _deserialize_fish(self, data: Dict[str, Any]):
        """
        Deserialize a fish from dictionary

        Args:
            data: Dictionary of fish data

        Returns:
            Fish instance
        """
        # TODO: Import Fish class and create instance
        # This requires the Fish class to have a from_dict method or
        # a constructor that accepts serialized data
        pass

    def create_autosave(self, player) -> bool:
        """
        Create an autosave file

        Args:
            player: Player instance

        Returns:
            True if autosave succeeded
        """
        autosave_path = self.save_dir / "autosave.json"

        try:
            save_data = {
                "version": "1.0",
                "save_name": "Autosave",
                "timestamp": datetime.now().isoformat(),
                "playtime": 0,
                "player_data": self._serialize_player(player)
            }

            with open(autosave_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"Error creating autosave: {e}")
            return False

    def load_autosave(self, player) -> bool:
        """
        Load from autosave file

        Args:
            player: Player instance

        Returns:
            True if load succeeded
        """
        autosave_path = self.save_dir / "autosave.json"

        if not autosave_path.exists():
            return False

        try:
            with open(autosave_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            player_data = save_data.get("player_data", {})
            self._deserialize_player(player, player_data)

            print("Autosave loaded")
            return True

        except Exception as e:
            print(f"Error loading autosave: {e}")
            return False

    def export_save(self, slot: int, export_path: str) -> bool:
        """
        Export a save file to a specific location

        Args:
            slot: Save slot to export
            export_path: Path to export to

        Returns:
            True if export succeeded
        """
        save_path = self.get_save_path(slot)

        if not save_path.exists():
            print(f"No save file found in slot {slot}")
            return False

        try:
            import shutil
            shutil.copy(save_path, export_path)
            print(f"Save exported to {export_path}")
            return True

        except Exception as e:
            print(f"Error exporting save: {e}")
            return False

    def import_save(self, import_path: str, slot: int) -> bool:
        """
        Import a save file from a specific location

        Args:
            import_path: Path to import from
            slot: Slot to import into

        Returns:
            True if import succeeded
        """
        import_path = Path(import_path)

        if not import_path.exists():
            print(f"Import file not found: {import_path}")
            return False

        try:
            import shutil
            save_path = self.get_save_path(slot)
            shutil.copy(import_path, save_path)
            print(f"Save imported to slot {slot}")
            return True

        except Exception as e:
            print(f"Error importing save: {e}")
            return False


# Global save system instance
_save_system = None


def get_save_system(save_dir: str = None) -> SaveSystem:
    """
    Get or create the global save system instance

    Args:
        save_dir: Optional custom save directory

    Returns:
        SaveSystem instance
    """
    global _save_system

    if _save_system is None:
        _save_system = SaveSystem(save_dir)

    return _save_system
