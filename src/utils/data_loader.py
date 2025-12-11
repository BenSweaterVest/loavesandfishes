"""
Data loading utilities for Loaves and Fishes

This module handles all JSON data loading for the game.
It uses a caching system to load files only once, improving performance.

ARCHITECTURE:
The game is DATA-DRIVEN - all content (fish, enemies, quests, etc.) comes from JSON files.
This means you can add/modify content WITHOUT changing code!

How it works:
1. JSON files in src/data/ contain all game content
2. DataLoader reads these files once and caches them
3. Game code requests data by ID (e.g., "holy_mackerel")
4. DataLoader returns the data from cache

Benefits:
- Easy content creation (just edit JSON files)
- No code changes needed for new content
- Modding-friendly (swap JSON files)
- Dual-text system works seamlessly

Usage:
    loader = DataLoader()
    fish_data = loader.get_fish_by_id("holy_mackerel")
    print(fish_data["name"])  # "Holy Mackerel"
    print(fish_data["flavor_text"]["default"])  # Irreverent version
"""

import json
import os
from typing import Dict, List, Any, Optional

class DataLoader:
    """
    Loads and caches game data from JSON files.

    This class is responsible for:
    1. Loading JSON files from the data directory
    2. Caching loaded data (so we don't re-read files constantly)
    3. Providing convenience methods to get specific data

    The caching system means files are read once when first accessed,
    then served from memory for all subsequent requests.
    """

    def __init__(self, data_path: str = "src/data/"):
        """
        Initialize the DataLoader.

        Args:
            data_path: Path to the directory containing JSON data files.
                      Defaults to "src/data/" which works from project root.
                      Use different path for tests or modded content.
        """
        self.data_path = data_path
        self._cache = {}  # Dictionary to store loaded JSON data
                         # Format: {filename: json_data}

    def load_json(self, filename: str) -> Dict[str, Any]:
        """
        Load a JSON file from the data directory with caching.

        This method:
        1. Checks if the file was already loaded (in cache)
        2. If cached, returns cached data immediately (fast!)
        3. If not cached, loads from disk and caches it
        4. Handles errors gracefully (returns empty dict if file missing/broken)

        Args:
            filename: Name of the JSON file (e.g., "fish.json")

        Returns:
            Dictionary containing the parsed JSON data.
            Returns empty dict {} if file is missing or invalid.

        Example:
            data = loader.load_json("fish.json")
            # First call: reads from disk
            # Subsequent calls: returns cached version (instant)

        Error handling:
            - FileNotFoundError: File doesn't exist → prints error, returns {}
            - JSONDecodeError: File has invalid JSON → prints error, returns {}
        """
        # Check cache first (fast path - no disk I/O)
        if filename in self._cache:
            return self._cache[filename]

        # File not in cache - need to load from disk
        filepath = os.path.join(self.data_path, filename)

        try:
            # Open file with UTF-8 encoding (supports dual-text with special characters)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Parse JSON into Python dictionary
                self._cache[filename] = data  # Store in cache for future requests
                return data

        except FileNotFoundError:
            # File doesn't exist - probably misnamed or missing
            print(f"Error: Data file not found: {filepath}")
            print(f"Make sure {filename} exists in {self.data_path}")
            return {}  # Return empty dict so game doesn't crash

        except json.JSONDecodeError as e:
            # File exists but has invalid JSON syntax
            print(f"Error: Invalid JSON in {filepath}: {e}")
            print(f"Check for missing commas, brackets, or quotes")
            return {}  # Return empty dict so game doesn't crash

    def get_fish_data(self) -> Dict[str, Any]:
        """Load all fish data"""
        return self.load_json("fish.json")

    def get_fish_by_id(self, fish_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific fish by ID"""
        fish_data = self.get_fish_data()
        for fish in fish_data.get("fish", []):
            if fish["id"] == fish_id:
                return fish
        return None

    def get_all_fish(self) -> List[Dict[str, Any]]:
        """Get list of all fish"""
        fish_data = self.get_fish_data()
        return fish_data.get("fish", [])

    def get_apostles_data(self) -> Dict[str, Any]:
        """Load all apostle data"""
        return self.load_json("apostles.json")

    def get_apostle_by_id(self, apostle_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific apostle by ID"""
        apostles_data = self.get_apostles_data()
        for apostle in apostles_data.get("apostles", []):
            if apostle["id"] == apostle_id:
                return apostle
        return None

    def get_all_apostles(self) -> List[Dict[str, Any]]:
        """Get list of all apostles"""
        apostles_data = self.get_apostles_data()
        return apostles_data.get("apostles", [])

    def get_items_data(self) -> Dict[str, Any]:
        """Load all items data"""
        return self.load_json("items.json")

    def get_bread_items(self) -> List[Dict[str, Any]]:
        """Get all bread items"""
        items_data = self.get_items_data()
        return items_data.get("bread_items", [])

    def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific bread item by ID"""
        items = self.get_bread_items()
        for item in items:
            if item["id"] == item_id:
                return item
        return None

    def get_equipment(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all equipment (robes, accessories, fish items)"""
        items_data = self.get_items_data()
        return items_data.get("equipment", {})

    def get_towns_data(self) -> Dict[str, Any]:
        """Load all town data"""
        return self.load_json("towns.json")

    def get_town_by_id(self, town_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific town by ID"""
        towns_data = self.get_towns_data()
        for town in towns_data.get("towns", []):
            if town["id"] == town_id:
                return town
        return None

    def get_town_by_number(self, town_number: int) -> Optional[Dict[str, Any]]:
        """Get a town by its number (1-13)"""
        towns_data = self.get_towns_data()
        for town in towns_data.get("towns", []):
            if town["number"] == town_number:
                return town
        return None

    def get_all_towns(self) -> List[Dict[str, Any]]:
        """Get list of all towns"""
        towns_data = self.get_towns_data()
        return towns_data.get("towns", [])

    def get_type_effectiveness(self, attacker_type: str, defender_type: str) -> float:
        """Get type effectiveness multiplier"""
        fish_data = self.get_fish_data()
        type_chart = fish_data.get("type_chart", {})

        if attacker_type in type_chart and defender_type in type_chart[attacker_type]:
            return type_chart[attacker_type][defender_type]
        return 1.0  # Default to neutral

    def clear_cache(self):
        """Clear the data cache (useful for reloading during development)"""
        self._cache.clear()

    def reload_data(self):
        """Reload all data from files"""
        self.clear_cache()
        # Preload common data
        self.get_fish_data()
        self.get_apostles_data()
        self.get_items_data()
        self.get_towns_data()


# Singleton instance
_data_loader = None

# ============================================================================
# SINGLETON PATTERN
# ============================================================================
#
# We use a "singleton" pattern for DataLoader, meaning there's only ONE
# instance shared across the entire game.
#
# Why? Because we want ONE cache that everyone shares.
# If every part of the game created its own DataLoader, they'd each
# re-read all the JSON files (slow and wasteful).
#
# Instead: ONE DataLoader, ONE cache, shared by all.
#
# Usage:
#   loader = get_data_loader()  # Always returns the same instance
#   fish = loader.get_fish_by_id("holy_mackerel")
#
# ============================================================================

_data_loader = None  # Global variable to store the singleton instance

def get_data_loader() -> DataLoader:
    """
    Get the singleton DataLoader instance.

    This function ensures only ONE DataLoader exists for the entire game.

    Returns:
        The shared DataLoader instance

    Example:
        loader1 = get_data_loader()
        loader2 = get_data_loader()
        # loader1 and loader2 are THE SAME OBJECT
        # They share the same cache
    """
    global _data_loader  # Access the global singleton variable

    # If this is the first time calling, create the DataLoader
    if _data_loader is None:
        _data_loader = DataLoader()

    # Return the singleton instance (same one every time)
    return _data_loader


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================
#
# These are shortcuts that let you get data in one line.
# Instead of:
#   loader = get_data_loader()
#   fish = loader.get_fish_by_id("holy_mackerel")
#
# You can just write:
#   fish = get_fish("holy_mackerel")
#
# Much cleaner!
#
# ============================================================================

def get_fish(fish_id: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to get a fish by ID.

    Args:
        fish_id: Fish identifier (e.g., "holy_mackerel")

    Returns:
        Fish data dictionary or None if not found

    Example:
        fish = get_fish("holy_mackerel")
        print(fish["name"])  # "Holy Mackerel"
    """
    return get_data_loader().get_fish_by_id(fish_id)

def get_apostle(apostle_id: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to get an apostle by ID.

    Args:
        apostle_id: Apostle identifier (e.g., "peter")

    Returns:
        Apostle data dictionary or None if not found
    """
    return get_data_loader().get_apostle_by_id(apostle_id)

def get_town(town_id: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to get a town by ID.

    Args:
        town_id: Town identifier (e.g., "nazareth")

    Returns:
        Town data dictionary or None if not found
    """
    return get_data_loader().get_town_by_id(town_id)

def get_item(item_id: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to get an item by ID.

    Args:
        item_id: Item identifier (e.g., "manna_bread")

    Returns:
        Item data dictionary or None if not found
    """
    return get_data_loader().get_item_by_id(item_id)
