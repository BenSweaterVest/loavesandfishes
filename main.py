#!/usr/bin/env python3
"""
Loaves and Fishes - Main Game Loop
A Pokémon-style JRPG about Jesus collecting fish and recruiting apostles

"The Greatest Story Ever Played"
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from engine.player import Player
from engine.game_state import GameState, GameScene, EncounterType
from engine.town import TownManager
from engine.world_map import WorldMap
from engine.dialogue import DialogueManager
from engine.apostle_abilities import ApostleManager
from engine.miracles import MiracleMeter
from engine.combos import ComboManager
from engine.fishing import FISHING_SPOTS
from ui.menu import MainMenu, MenuManager
from ui.shops import get_shop
from utils.save_system import get_save_system
from utils.data_loader import DataLoader


class LoavesAndFishesGame:
    """Main game class"""

    def __init__(self):
        """Initialize the game"""
        print("=" * 60)
        print("LOAVES AND FISHES".center(60))
        print("A Biblical JRPG Adventure".center(60))
        print("=" * 60)
        print()

        # Initialize core systems
        self.player = Player("Jesus")
        self.game_state = GameState(self.player)
        self.data_loader = DataLoader()

        # Initialize managers
        self.town_manager = TownManager()
        self.world_map = WorldMap()
        self.dialogue_manager = DialogueManager()
        self.menu_manager = MenuManager()
        self.apostle_manager = ApostleManager()
        self.combo_manager = ComboManager()

        # Initialize player systems
        self.miracle_meter = MiracleMeter()

        # Save system
        self.save_system = get_save_system()

        # Game running flag
        self.running = True

        # Load game data
        self._load_game_data()

    def _load_game_data(self):
        """Load all game data from JSON files"""
        print("Loading game data...")

        # Load towns
        towns_data = self.data_loader.get_all_towns()
        for town_data in towns_data:
            self.town_manager.load_town(town_data)

        print(f"Loaded {len(towns_data)} towns")
        print("Game data loaded successfully!")
        print()

    def show_title_screen(self):
        """Show title screen"""
        print("\n" + "=" * 60)
        print("""
        ┌─────────────────────────────────────────────┐
        │                                             │
        │        🐟 LOAVES AND FISHES 🍞               │
        │                                             │
        │   "I will make you fishers of men...        │
        │    and trainers of fish!"                   │
        │                                             │
        └─────────────────────────────────────────────┘
        """)
        print("=" * 60)
        print()
        print("1. New Game")
        print("2. Load Game")
        print("3. Quit")
        print()

        choice = input("Select option: ").strip()

        if choice == "1":
            self.new_game()
        elif choice == "2":
            self.load_game()
        elif choice == "3":
            self.running = False
        else:
            print("Invalid choice!")
            self.show_title_screen()

    def new_game(self):
        """Start a new game"""
        print("\n" + "=" * 60)
        print("NEW GAME".center(60))
        print("=" * 60)
        print()
        print("You are Jesus of Nazareth.")
        print("Your journey begins in your hometown...")
        print()
        input("Press Enter to begin...")

        # Set up initial state
        self.game_state.set_story_flag("game_started", True)
        self.game_state.current_town = "nazareth"
        self.world_map.set_current_location("nazareth")

        # Give starter fish
        print("\nYou approach the Sea of Galilee...")
        print("A small fish swims up to you - it's your first companion!")
        print()
        print("🐟 You received: Carp Diem (Lv. 1)")
        print()
        input("Press Enter to continue...")

        # Enter first town
        self.town_manager.enter_town("nazareth")
        self.game_state.change_scene(GameScene.TOWN)

        # Start main loop
        self.main_loop()

    def load_game(self):
        """Load a saved game"""
        print("\n" + "=" * 60)
        print("LOAD GAME".center(60))
        print("=" * 60)
        print()

        saves = self.save_system.list_saves()

        if not saves:
            print("No save files found!")
            input("Press Enter to return...")
            self.show_title_screen()
            return

        for slot, info in saves.items():
            print(f"\nSlot {slot}:")
            print(f"  Name: {info['save_name']}")
            print(f"  Location: {info['location']}")
            print(f"  Level: {info['player_level']}")
            print(f"  Party: {info['party_size']} fish")
            print(f"  Money: {info['money']} denarii")

        print()
        choice = input("Select slot (1-5) or 0 to cancel: ").strip()

        try:
            slot = int(choice)
            if slot == 0:
                self.show_title_screen()
                return
            if 1 <= slot <= 5:
                if self.save_system.load_game(self.player, slot):
                    # Load game state
                    print("\nGame loaded successfully!")
                    input("Press Enter to continue...")
                    self.main_loop()
                else:
                    print("Failed to load game!")
                    input("Press Enter...")
                    self.show_title_screen()
            else:
                print("Invalid slot!")
                self.load_game()
        except ValueError:
            print("Invalid input!")
            self.load_game()

    def main_loop(self):
        """Main game loop"""
        while self.running:
            # Handle current scene
            if self.game_state.current_scene == GameScene.TOWN:
                self.town_scene()
            elif self.game_state.current_scene == GameScene.WORLD_MAP:
                self.world_map_scene()
            elif self.game_state.current_scene == GameScene.MENU:
                self.menu_scene()
            elif self.game_state.current_scene == GameScene.FISHING:
                self.fishing_scene()
            elif self.game_state.current_scene == GameScene.TITLE:
                self.show_title_screen()
            else:
                # Unknown scene, return to town
                self.game_state.change_scene(GameScene.TOWN)

    def town_scene(self):
        """Handle town exploration"""
        town = self.town_manager.get_current_town()
        if not town:
            print("Error: No current town!")
            self.running = False
            return

        location = town.get_current_location()

        print("\n" + "=" * 60)
        print(f"{town.name} - {location.name}".center(60))
        print("=" * 60)
        print(f"\n{location.description}\n")

        # Show NPCs
        npcs = location.get_npcs()
        if npcs:
            print("People here:")
            for i, npc in enumerate(npcs, 1):
                print(f"  {i}. {npc.name}")
            print()

        # Show options
        print("What would you like to do?")
        print("1. Talk to someone")
        print("2. Move to another location")
        print("3. Open Menu")
        print("4. Leave town")

        if location.can_rest:
            print("5. Rest at inn (heal party)")
        if location.can_shop:
            print("6. Visit shop")
        if location.can_fish:
            print("7. Go fishing")

        print()
        choice = input("Choose action: ").strip()

        if choice == "1":
            self.talk_to_npc(npcs)
        elif choice == "2":
            self.move_in_town(town)
        elif choice == "3":
            self.game_state.change_scene(GameScene.MENU)
        elif choice == "4":
            self.game_state.change_scene(GameScene.WORLD_MAP)
        elif choice == "5" and location.can_rest:
            self.rest_at_inn()
        elif choice == "6" and location.can_shop:
            self.visit_shop(location)
        elif choice == "7" and location.can_fish:
            self.game_state.change_scene(GameScene.FISHING)

    def talk_to_npc(self, npcs):
        """Talk to an NPC"""
        if not npcs:
            return

        print()
        for i, npc in enumerate(npcs, 1):
            print(f"{i}. {npc.name}")

        choice = input("\nTalk to whom? (0 to cancel): ").strip()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(npcs):
                npc = npcs[idx]
                print(f"\n{npc.name}: {npc.get_dialogue()}")
                input("\nPress Enter...")
        except ValueError:
            pass

    def move_in_town(self, town):
        """Move to another location in town"""
        exits = town.get_available_exits()

        if not exits:
            print("\nNo other locations accessible from here.")
            input("Press Enter...")
            return

        print("\nWhere would you like to go?")
        for i, exit_id in enumerate(exits, 1):
            location = town.get_location(exit_id)
            if location:
                print(f"{i}. {location.name}")

        choice = input("\nGo to: (0 to cancel): ").strip()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(exits):
                town.move_to_location(exits[idx])
        except ValueError:
            pass

    def rest_at_inn(self):
        """Rest at the inn"""
        print("\n" + "=" * 60)
        print("The innkeeper welcomes you...")
        print("Your fish rest and are restored to full health!")
        print("=" * 60)
        # TODO: Actually heal party fish
        input("\nPress Enter...")

    def visit_shop(self, location):
        """Visit a shop"""
        shop_type = "baker" if location.location_type.value == "baker" else "fishmonger"
        town_id = self.game_state.current_town

        shop = get_shop(town_id.title(), shop_type)

        if shop:
            print(f"\n{shop.greeting}")
            # TODO: Implement shop interface
            input("\nPress Enter...")

    def world_map_scene(self):
        """Handle world map"""
        print("\n" + "=" * 60)
        print("WORLD MAP".center(60))
        print("=" * 60)
        print()
        print(self.world_map.get_map_ascii())
        print()

        print("1. Travel to location")
        print("2. Fast Travel")
        print("3. Return to town")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            self.travel_menu()
        elif choice == "2":
            self.fast_travel_menu()
        elif choice == "3":
            self.game_state.change_scene(GameScene.TOWN)

    def travel_menu(self):
        """Show travel menu"""
        current = self.world_map.get_current_location()
        accessible = self.world_map.get_accessible_locations(fast_travel=False)

        print("\nAccessible locations:")
        for i, loc in enumerate(accessible, 1):
            print(f"{i}. {loc.name}")

        choice = input("\nTravel to: (0 to cancel): ").strip()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(accessible):
                location = accessible[idx]
                if self.world_map.travel_to(location.location_id):
                    print(f"\nTraveling to {location.name}...")
                    self.game_state.current_town = location.location_id
                    self.town_manager.enter_town(location.location_id)
                    input("Press Enter...")
                    self.game_state.change_scene(GameScene.TOWN)
        except ValueError:
            pass

    def fast_travel_menu(self):
        """Show fast travel menu"""
        locations = self.world_map.get_fast_travel_locations()

        if not locations:
            print("\nNo fast travel locations unlocked yet!")
            input("Press Enter...")
            return

        print("\nFast travel to:")
        for i, loc in enumerate(locations, 1):
            print(f"{i}. {loc.name}")

        choice = input("\nFast travel to: (0 to cancel): ").strip()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(locations):
                location = locations[idx]
                self.world_map.travel_to(location.location_id, method="fast_travel")
                print(f"\n✨ Fast traveling to {location.name}...")
                self.game_state.current_town = location.location_id
                self.town_manager.enter_town(location.location_id)
                input("Press Enter...")
                self.game_state.change_scene(GameScene.TOWN)
        except ValueError:
            pass

    def menu_scene(self):
        """Handle menu"""
        self.menu_manager.push_menu(MainMenu(self.player))

        while self.menu_manager.current_menu():
            menu = self.menu_manager.current_menu()
            print("\n" + "\n".join(menu.get_display_text()))

            choice = input("\nSelect: ").strip().lower()

            if choice in ['w', 'up']:
                menu.move_up()
            elif choice in ['s', 'down']:
                menu.move_down()
            elif choice in ['e', 'enter', 'select']:
                menu.select()
            elif choice in ['q', 'back', 'exit']:
                self.menu_manager.pop_menu()
                if not self.menu_manager.menu_stack:
                    self.game_state.return_to_previous_scene()
                    return

    def fishing_scene(self):
        """Handle fishing mini-game"""
        print("\n" + "=" * 60)
        print("FISHING".center(60))
        print("=" * 60)
        print()
        print("Fishing mini-game coming soon!")
        print("For now, you automatically catch a random fish.")
        print()
        input("Press Enter...")
        self.game_state.return_to_previous_scene()

    def save_game(self, slot: int = 1):
        """
        Save the game

        Args:
            slot: Save slot (1-5)
        """
        if self.save_system.save_game(self.player, slot):
            print(f"\nGame saved to slot {slot}!")
        else:
            print("\nFailed to save game!")
        input("Press Enter...")

    def quit_game(self):
        """Quit the game"""
        print("\n" + "=" * 60)
        print("Would you like to save before quitting?")
        print("1. Save and Quit")
        print("2. Quit without Saving")
        print("3. Cancel")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            self.save_game(1)
            self.running = False
        elif choice == "2":
            self.running = False
        # else continue running


def main():
    """Main entry point"""
    game = LoavesAndFishesGame()
    game.show_title_screen()

    print("\n" + "=" * 60)
    print("Thank you for playing Loaves and Fishes!".center(60))
    print("May God bless you!".center(60))
    print("=" * 60)


if __name__ == "__main__":
    main()
