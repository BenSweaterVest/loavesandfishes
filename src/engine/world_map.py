"""
World Map System - Overworld travel and fast travel
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum


class TravelMethod(Enum):
    """Methods of travel"""
    WALK = "walk"
    FAST_TRAVEL = "fast_travel"
    BOAT = "boat"
    MIRACLE = "miracle"


class WorldLocation:
    """A location on the world map"""

    def __init__(self,
                 location_id: str,
                 name: str,
                 location_type: str,
                 position: Tuple[int, int]):
        """
        Initialize world location

        Args:
            location_id: Unique identifier
            name: Display name
            location_type: Type (town, dungeon, etc.)
            position: (x, y) coordinates on map
        """
        self.location_id = location_id
        self.name = name
        self.location_type = location_type
        self.position = position

        # Connections (roads between locations)
        self.connected_to: List[str] = []

        # Discovery and access
        self.discovered = False
        self.unlocked = False
        self.fast_travel_enabled = False

        # Regional info
        self.region = ""
        self.description = ""

    def add_connection(self, location_id: str):
        """Add a connection to another location"""
        if location_id not in self.connected_to:
            self.connected_to.append(location_id)

    def discover(self):
        """Mark location as discovered"""
        self.discovered = True

    def unlock(self):
        """Unlock location for travel"""
        self.unlocked = True
        self.discovered = True

    def enable_fast_travel(self):
        """Enable fast travel to this location"""
        if self.unlocked:
            self.fast_travel_enabled = True


class WorldMap:
    """Game world map"""

    def __init__(self):
        """Initialize world map"""
        self.locations: Dict[str, WorldLocation] = {}
        self.current_location: Optional[str] = None

        # Map dimensions
        self.width = 20
        self.height = 15

        # Travel costs
        self.steps_per_location = 100  # Steps between locations when walking

        # Build default map
        self._build_default_map()

    def _build_default_map(self):
        """Build the default world map with all 13 towns"""

        # Define all towns with their positions
        towns = [
            ("Nazareth", 5, 3, "Galilee"),
            ("Cana", 6, 4, "Galilee"),
            ("Capernaum", 8, 2, "Galilee"),
            ("Bethsaida", 10, 1, "Coastal"),
            ("Magdala", 9, 3, "Coastal"),
            ("Chorazin", 11, 2, "Coastal"),
            ("Tiberias", 9, 4, "Coastal"),
            ("Gadara", 12, 3, "Gentile"),
            ("Samaria", 7, 7, "Gentile"),
            ("Jericho", 9, 10, "Judean"),
            ("Bethany", 8, 11, "Judean"),
            ("Bethlehem", 7, 12, "Judean"),
            ("Jerusalem", 8, 12, "Jerusalem")
        ]

        for town_id, x, y, region in towns:
            location = WorldLocation(
                town_id.lower(),
                town_id,
                "town",
                (x, y)
            )
            location.region = region
            location.description = f"The town of {town_id}"

            # Nazareth starts unlocked
            if town_id == "Nazareth":
                location.unlock()
                location.enable_fast_travel()

            self.locations[town_id.lower()] = location

        # Define roads (connections between towns)
        connections = [
            ("nazareth", "cana"),
            ("cana", "capernaum"),
            ("capernaum", "bethsaida"),
            ("capernaum", "magdala"),
            ("bethsaida", "chorazin"),
            ("magdala", "tiberias"),
            ("tiberias", "gadara"),
            ("cana", "samaria"),
            ("samaria", "jericho"),
            ("jericho", "bethany"),
            ("bethany", "bethlehem"),
            ("bethlehem", "jerusalem"),
            ("bethany", "jerusalem")
        ]

        for loc1, loc2 in connections:
            if loc1 in self.locations and loc2 in self.locations:
                self.locations[loc1].add_connection(loc2)
                self.locations[loc2].add_connection(loc1)  # Bidirectional

    def get_location(self, location_id: str) -> Optional[WorldLocation]:
        """Get a location by ID"""
        return self.locations.get(location_id)

    def set_current_location(self, location_id: str):
        """Set the current location"""
        if location_id in self.locations:
            self.current_location = location_id
            self.locations[location_id].discover()

    def get_current_location(self) -> Optional[WorldLocation]:
        """Get current location"""
        if self.current_location:
            return self.locations.get(self.current_location)
        return None

    def can_travel_to(self, location_id: str) -> bool:
        """
        Check if player can travel to a location

        Args:
            location_id: Location to check

        Returns:
            True if travel is possible
        """
        target = self.get_location(location_id)
        if not target or not target.unlocked:
            return False

        current = self.get_current_location()
        if not current:
            return False

        # Can always fast travel to unlocked locations
        if target.fast_travel_enabled:
            return True

        # Can walk to connected locations
        return location_id in current.connected_to

    def get_accessible_locations(self, fast_travel: bool = False) -> List[WorldLocation]:
        """
        Get locations accessible from current position

        Args:
            fast_travel: If True, include all fast travel locations

        Returns:
            List of accessible locations
        """
        accessible = []
        current = self.get_current_location()

        if not current:
            return accessible

        for loc_id, location in self.locations.items():
            if not location.unlocked:
                continue

            # Fast travel to any unlocked fast travel point
            if fast_travel and location.fast_travel_enabled:
                accessible.append(location)
            # Walk to connected locations
            elif loc_id in current.connected_to:
                accessible.append(location)

        return accessible

    def travel_to(self, location_id: str, method: TravelMethod = TravelMethod.WALK) -> bool:
        """
        Travel to a location

        Args:
            location_id: Location to travel to
            method: Travel method

        Returns:
            True if successful
        """
        if not self.can_travel_to(location_id):
            return False

        target = self.get_location(location_id)
        if not target:
            return False

        # Fast travel is instant
        if method == TravelMethod.FAST_TRAVEL and target.fast_travel_enabled:
            self.set_current_location(location_id)
            return True

        # Walking requires connection
        current = self.get_current_location()
        if current and location_id in current.connected_to:
            self.set_current_location(location_id)
            return True

        return False

    def unlock_location(self, location_id: str):
        """Unlock a location"""
        location = self.get_location(location_id)
        if location:
            location.unlock()

    def enable_fast_travel(self, location_id: str):
        """Enable fast travel to a location"""
        location = self.get_location(location_id)
        if location:
            location.enable_fast_travel()

    def get_path(self, from_id: str, to_id: str) -> Optional[List[str]]:
        """
        Get path between two locations using BFS

        Args:
            from_id: Starting location
            to_id: Destination location

        Returns:
            List of location IDs representing path, or None if no path
        """
        if from_id not in self.locations or to_id not in self.locations:
            return None

        # BFS for shortest path
        from collections import deque

        queue = deque([(from_id, [from_id])])
        visited = {from_id}

        while queue:
            current, path = queue.popleft()

            if current == to_id:
                return path

            current_loc = self.locations[current]
            for neighbor in current_loc.connected_to:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def get_distance(self, from_id: str, to_id: str) -> int:
        """
        Get distance between two locations

        Args:
            from_id: Starting location
            to_id: Destination location

        Returns:
            Number of steps in path, or -1 if no path
        """
        path = self.get_path(from_id, to_id)
        if path:
            return len(path) - 1
        return -1

    def get_region_towns(self, region: str) -> List[WorldLocation]:
        """
        Get all towns in a region

        Args:
            region: Region name

        Returns:
            List of locations in region
        """
        return [loc for loc in self.locations.values() if loc.region == region]

    def get_discovered_locations(self) -> List[WorldLocation]:
        """Get all discovered locations"""
        return [loc for loc in self.locations.values() if loc.discovered]

    def get_unlocked_locations(self) -> List[WorldLocation]:
        """Get all unlocked locations"""
        return [loc for loc in self.locations.values() if loc.unlocked]

    def get_fast_travel_locations(self) -> List[WorldLocation]:
        """Get all locations with fast travel enabled"""
        return [loc for loc in self.locations.values() if loc.fast_travel_enabled]

    def get_map_ascii(self) -> str:
        """
        Get ASCII representation of the map

        Returns:
            ASCII map string
        """
        # Create empty grid
        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]

        # Mark locations
        for loc in self.locations.values():
            x, y = loc.position

            if y < self.height and x < self.width:
                if loc.location_id == self.current_location:
                    grid[y][x] = 'X'  # Current position
                elif loc.fast_travel_enabled:
                    grid[y][x] = '@'  # Fast travel point
                elif loc.unlocked:
                    grid[y][x] = 'O'  # Unlocked
                elif loc.discovered:
                    grid[y][x] = '?'  # Discovered but locked
                else:
                    grid[y][x] = ' '  # Unknown

        # Convert to string
        lines = []
        lines.append("=" * (self.width + 2))
        for row in grid:
            lines.append("|" + "".join(row) + "|")
        lines.append("=" * (self.width + 2))

        lines.append("\nLegend:")
        lines.append("X = Current Location")
        lines.append("@ = Fast Travel Point")
        lines.append("O = Unlocked Town")
        lines.append("? = Discovered")
        lines.append(". = Path/Road")

        return "\n".join(lines)
