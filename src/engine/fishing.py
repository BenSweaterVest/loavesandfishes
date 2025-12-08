"""
Fishing Mini-game - Catch fish through a simple rhythm/timing game
"""

import random
from typing import Optional, Dict, Any
from enum import Enum


class FishingDifficulty(Enum):
    """Fishing difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    LEGENDARY = "legendary"


class FishingResult(Enum):
    """Fishing attempt results"""
    CAUGHT = "caught"
    ESCAPED = "escaped"
    NOTHING = "nothing"
    ONGOING = "ongoing"


class FishingMinigame:
    """A fishing mini-game instance"""

    def __init__(self, fishing_spot_quality: int = 50):
        """
        Initialize fishing mini-game

        Args:
            fishing_spot_quality: Quality of fishing spot (0-100)
        """
        self.fishing_spot_quality = fishing_spot_quality
        self.is_active = False
        self.current_fish: Optional[Dict[str, Any]] = None

        # Mini-game state
        self.fish_position = 50  # 0-100
        self.hook_position = 50  # 0-100
        self.tension = 0  # 0-100 (breaks line at 100)
        self.progress = 0  # 0-100 (caught at 100)

        # Difficulty settings
        self.fish_speed = 5
        self.fish_change_direction_chance = 0.1
        self.tension_increase_rate = 2
        self.tension_decrease_rate = 1
        self.progress_increase_rate = 3

        # Player equipment bonuses
        self.net_quality = 1.0  # Multiplier from net upgrades
        self.bait_quality = 1.0  # Multiplier from bait

    def start_fishing(self):
        """Start a fishing attempt"""
        self.is_active = True

        # Determine if something bites
        bite_chance = self.fishing_spot_quality / 100

        if random.random() < bite_chance:
            # Something bit! Determine what
            self.current_fish = self._generate_fish()
            self._set_difficulty()
        else:
            # Nothing bites
            self.current_fish = None

        # Reset mini-game state
        self.fish_position = 50
        self.hook_position = 50
        self.tension = 0
        self.progress = 0

    def _generate_fish(self) -> Dict[str, Any]:
        """
        Generate a random fish encounter

        Returns:
            Dictionary with fish data
        """
        # Determine rarity
        roll = random.random()

        if roll < 0.05:  # 5% legendary
            tier = "special"
            difficulty = FishingDifficulty.LEGENDARY
        elif roll < 0.15:  # 10% tier 3
            tier = 3
            difficulty = FishingDifficulty.HARD
        elif roll < 0.40:  # 25% tier 2
            tier = 2
            difficulty = FishingDifficulty.MEDIUM
        else:  # 60% tier 1
            tier = 1
            difficulty = FishingDifficulty.EASY

        return {
            "tier": tier,
            "difficulty": difficulty,
            "size": random.randint(1, 10),  # 1-10 scale
            "caught": False
        }

    def _set_difficulty(self):
        """Set mini-game difficulty based on fish"""
        if not self.current_fish:
            return

        difficulty = self.current_fish["difficulty"]

        if difficulty == FishingDifficulty.EASY:
            self.fish_speed = 3
            self.fish_change_direction_chance = 0.05
            self.tension_increase_rate = 1
        elif difficulty == FishingDifficulty.MEDIUM:
            self.fish_speed = 5
            self.fish_change_direction_chance = 0.1
            self.tension_increase_rate = 2
        elif difficulty == FishingDifficulty.HARD:
            self.fish_speed = 8
            self.fish_change_direction_chance = 0.15
            self.tension_increase_rate = 3
        else:  # LEGENDARY
            self.fish_speed = 12
            self.fish_change_direction_chance = 0.2
            self.tension_increase_rate = 4

    def update(self, reel_in: bool = False) -> FishingResult:
        """
        Update fishing mini-game state

        Args:
            reel_in: True if player is reeling in

        Returns:
            Current fishing result
        """
        if not self.is_active:
            return FishingResult.NOTHING

        # No fish on the line
        if not self.current_fish:
            self.is_active = False
            return FishingResult.NOTHING

        # Move fish randomly
        if random.random() < self.fish_change_direction_chance:
            # Fish changes direction
            self.fish_position += random.randint(-self.fish_speed, self.fish_speed)
        else:
            # Fish continues current movement
            direction = 1 if random.random() < 0.5 else -1
            self.fish_position += self.fish_speed * direction

        # Keep fish in bounds
        self.fish_position = max(0, min(100, self.fish_position))

        # Calculate distance between hook and fish
        distance = abs(self.hook_position - self.fish_position)

        # Update tension
        if distance > 20:  # Fish is far from hook
            self.tension += self.tension_increase_rate
        else:
            self.tension = max(0, self.tension - self.tension_decrease_rate)

        # Line breaks if tension too high
        if self.tension >= 100:
            self.is_active = False
            return FishingResult.ESCAPED

        # Player reeling in
        if reel_in:
            # Move hook toward fish
            if self.hook_position < self.fish_position:
                self.hook_position += 3
            elif self.hook_position > self.fish_position:
                self.hook_position -= 3

            # Increase progress if close to fish
            if distance < 10:
                self.progress += self.progress_increase_rate * self.net_quality
            elif distance < 20:
                self.progress += (self.progress_increase_rate / 2) * self.net_quality

        # Fish caught!
        if self.progress >= 100:
            self.is_active = False
            self.current_fish["caught"] = True
            return FishingResult.CAUGHT

        return FishingResult.ONGOING

    def move_hook(self, direction: int):
        """
        Move the hook left or right

        Args:
            direction: -1 for left, 1 for right
        """
        self.hook_position += direction * 5
        self.hook_position = max(0, min(100, self.hook_position))

    def get_state(self) -> Dict[str, Any]:
        """
        Get current mini-game state for display

        Returns:
            Dictionary with current state
        """
        return {
            "active": self.is_active,
            "fish_position": self.fish_position,
            "hook_position": self.hook_position,
            "tension": self.tension,
            "progress": self.progress,
            "fish_tier": self.current_fish["tier"] if self.current_fish else None,
            "fish_size": self.current_fish["size"] if self.current_fish else None
        }

    def get_display_bar(self) -> str:
        """
        Get ASCII display of fishing bar

        Returns:
            ASCII art fishing bar
        """
        bar_length = 50
        fish_pos = int((self.fish_position / 100) * bar_length)
        hook_pos = int((self.hook_position / 100) * bar_length)

        # Create bar
        bar = ['-'] * bar_length

        # Place fish
        if 0 <= fish_pos < bar_length:
            bar[fish_pos] = 'F'

        # Place hook
        if 0 <= hook_pos < bar_length:
            if bar[hook_pos] == 'F':
                bar[hook_pos] = 'X'  # Hook on fish!
            else:
                bar[hook_pos] = 'H'

        bar_str = ''.join(bar)

        # Add bars
        tension_bar = '#' * int((self.tension / 100) * 20)
        progress_bar = '=' * int((self.progress / 100) * 20)

        display = []
        display.append(f"|{bar_str}|")
        display.append(f"Tension:  [{tension_bar:<20}] {self.tension}%")
        display.append(f"Progress: [{progress_bar:<20}] {self.progress}%")

        if self.current_fish:
            display.append(f"Fish Tier: {self.current_fish['tier']} | Size: {self.current_fish['size']}/10")

        return "\n".join(display)

    def upgrade_net(self, quality: float):
        """
        Upgrade fishing net

        Args:
            quality: Net quality multiplier (1.0 = basic, 1.5 = quality, 2.0 = miraculous)
        """
        self.net_quality = quality

    def use_bait(self, quality: float):
        """
        Use special bait

        Args:
            quality: Bait quality multiplier
        """
        self.bait_quality = quality


class FishingSpot:
    """A fishing spot location"""

    def __init__(self,
                 spot_id: str,
                 name: str,
                 quality: int,
                 available_fish: list):
        """
        Initialize fishing spot

        Args:
            spot_id: Unique identifier
            name: Spot name
            quality: Fishing quality (0-100)
            available_fish: List of fish IDs that can be caught here
        """
        self.spot_id = spot_id
        self.name = name
        self.quality = quality
        self.available_fish = available_fish

    def start_fishing(self) -> FishingMinigame:
        """
        Start fishing at this spot

        Returns:
            FishingMinigame instance
        """
        game = FishingMinigame(self.quality)
        game.start_fishing()
        return game


# Predefined fishing spots
FISHING_SPOTS = {
    "sea_of_galilee": FishingSpot(
        "sea_of_galilee",
        "Sea of Galilee",
        quality=80,
        available_fish=["carp_diem", "holy_mackerel", "sole_survivor", "bass_ackwards", "tilapia"]
    ),

    "jordan_river": FishingSpot(
        "jordan_river",
        "Jordan River",
        quality=60,
        available_fish=["carp_diem", "stone_loach", "eel_pray_for_you"]
    ),

    "bethesda_pool": FishingSpot(
        "bethesda_pool",
        "Pool of Bethesda",
        quality=70,
        available_fish=["holy_mackerel", "salmon_of_wisdom", "betta_together"]
    ),

    "miraculous_catch": FishingSpot(
        "miraculous_catch",
        "Miraculous Catch Site",
        quality=100,
        available_fish=["fishers_of_men_haden", "ichthys_divine", "leviathans_lament"]
    )
}
