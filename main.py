#!/usr/bin/env python3
"""
Loaves and Fishes - Main Entry Point
A 90s JRPG-style Biblical parody adventure

"The Greatest Story Ever Played"
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.constants import GAME_TITLE, GAME_VERSION, GAME_TAGLINE
from utils.data_loader import get_data_loader
from engine.fish import Fish


def print_banner():
    """Print the game banner"""
    print("=" * 60)
    print(f"  {GAME_TITLE}")
    print(f"  {GAME_TAGLINE}")
    print(f"  Version {GAME_VERSION}")
    print("=" * 60)
    print()


def test_data_loading():
    """Test that data files load correctly"""
    print("Testing data loading...")
    print()

    loader = get_data_loader()

    # Test fish data
    print("📟 Loading fish data...")
    all_fish = loader.get_all_fish()
    print(f"   Loaded {len(all_fish)} fish types")

    # Show a few fish
    for i, fish_data in enumerate(all_fish[:3]):
        print(f"   - {fish_data['name']} ({fish_data['type']}-type)")

    print()

    # Test apostles data
    print("✝️  Loading apostle data...")
    all_apostles = loader.get_all_apostles()
    print(f"   Loaded {len(all_apostles)} apostles")

    for i, apostle in enumerate(all_apostles[:3]):
        print(f"   - {apostle['name']} ({apostle['title']})")

    print()

    # Test towns data
    print("🏘️  Loading town data...")
    all_towns = loader.get_all_towns()
    print(f"   Loaded {len(all_towns)} towns")

    for i, town in enumerate(all_towns[:3]):
        print(f"   - {town['name']} (Town #{town['number']})")

    print()

    # Test items data
    print("🍞 Loading bread items...")
    bread_items = loader.get_bread_items()
    print(f"   Loaded {len(bread_items)} bread items")

    for i, item in enumerate(bread_items[:3]):
        print(f"   - {item['name']} ({item['cost']} denarii)")

    print()


def test_fish_system():
    """Test the fish battle system"""
    print("🐟 Testing Fish Battle System...")
    print()

    loader = get_data_loader()

    # Create a fish instance
    carp_data = loader.get_fish_by_id("carp_diem")
    if carp_data:
        carp = Fish("carp_diem", carp_data, level=1)
        print(f"Created fish: {carp}")
        print(f"  Type: {carp.type}")
        print(f"  Stats: ATK {carp.atk}, DEF {carp.defense}, SPD {carp.spd}")
        print(f"  Known moves: {len(carp.known_moves)}")
        for move in carp.known_moves:
            print(f"    - {move['name']} ({move['type']})")
        print()

        # Test leveling up
        print("Testing level up...")
        carp.gain_xp(100)
        print(f"After gaining 100 XP: {carp}")
        print(f"  Stats: ATK {carp.atk}, DEF {carp.defense}, SPD {carp.spd}")
        print()

        # Test taking damage
        print("Testing damage...")
        print(f"Before damage: {carp.current_hp}/{carp.max_hp} HP")
        damage_dealt = carp.take_damage(15)
        print(f"Took {damage_dealt} damage!")
        print(f"After damage: {carp.current_hp}/{carp.max_hp} HP")
        print()

        # Test healing
        print("Testing healing...")
        healed = carp.heal(10)
        print(f"Healed {healed} HP!")
        print(f"After healing: {carp.current_hp}/{carp.max_hp} HP")
        print()


def main():
    """Main entry point"""
    print_banner()

    print("Welcome to Loaves and Fishes!")
    print("A Pokémon-style JRPG about Jesus collecting fish and recruiting apostles.")
    print()

    print("Current Status: 🚧 IN DEVELOPMENT 🚧")
    print()

    # Run tests
    test_data_loading()
    test_fish_system()

    print("=" * 60)
    print("✅ All systems operational!")
    print()
    print("Next steps:")
    print("  - Implement battle system")
    print("  - Create town progression")
    print("  - Build UI/menu system")
    print("  - Add combat mechanics")
    print()
    print("Stay tuned for more updates!")
    print("=" * 60)


if __name__ == "__main__":
    main()
