"""
Data loading utilities for Loaves and Fishes
Loads JSON data files for fish, apostles, towns, items, etc.
"""

import json
import os
from typing import Dict, List, Any, Optional

class DataLoader:
    """Loads and caches game data from JSON files"""

    def __init__(self, data_path: str = "src/data/"):
        self.data_path = data_path
        self._cache = {}

    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load a JSON file and cache it"""
        if filename in self._cache:
            return self._cache[filename]

        filepath = os.path.join(self.data_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._cache[filename] = data
                return data
        except FileNotFoundError:
            print(f"Error: Data file not found: {filepath}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {filepath}: {e}")
            return {}

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

def get_data_loader() -> DataLoader:
    """Get the singleton DataLoader instance"""
    global _data_loader
    if _data_loader is None:
        _data_loader = DataLoader()
    return _data_loader


# Convenience functions
def get_fish(fish_id: str) -> Optional[Dict[str, Any]]:
    """Convenience function to get a fish by ID"""
    return get_data_loader().get_fish_by_id(fish_id)

def get_apostle(apostle_id: str) -> Optional[Dict[str, Any]]:
    """Convenience function to get an apostle by ID"""
    return get_data_loader().get_apostle_by_id(apostle_id)

def get_town(town_id: str) -> Optional[Dict[str, Any]]:
    """Convenience function to get a town by ID"""
    return get_data_loader().get_town_by_id(town_id)

def get_item(item_id: str) -> Optional[Dict[str, Any]]:
    """Convenience function to get an item by ID"""
    return get_data_loader().get_item_by_id(item_id)
