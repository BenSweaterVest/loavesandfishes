#!/usr/bin/env python3
"""
Battle System Test - Demonstrates the turn-based combat system
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.data_loader import get_data_loader
from engine.fish import Fish
from engine.player import Player
from engine.enemy import create_enemy, create_boss
from engine.battle import Battle, BattleAction, BattleResult


def print_separator():
    print("=" * 70)


def print_battle_state(battle: Battle):
    """Display current battle state"""
    state = battle.get_battle_state()

    print(f"\n{'='*70}")
    print(f"TURN {state['turn']}")
    print(f"{'='*70}")

    # Player side
    if state['active_fish']:
        fish = state['active_fish']
        hp_bar = create_hp_bar(fish.current_hp, fish.max_hp)
        print(f"\n🐟 YOUR FISH: {fish.name} (Lv.{fish.level})")
        print(f"   HP: {hp_bar} {fish.current_hp}/{fish.max_hp}")
        print(f"   Type: {fish.type}")

    # Enemy side
    if state['active_enemy']:
        enemy = state['active_enemy']
        hp_bar = create_hp_bar(enemy.current_hp, enemy.max_hp)
        print(f"\n⚔️  ENEMY: {enemy.name} (Lv.{enemy.level})")
        print(f"   HP: {hp_bar} {enemy.current_hp}/{enemy.max_hp}")

    # Battle log
    print(f"\n📜 BATTLE LOG:")
    for event in state['recent_log']:
        print(f"   • {event}")

    # Miracle meter
    miracle_percent = int(state['miracle_meter'])
    miracle_bar = create_meter_bar(miracle_percent)
    print(f"\n✨ MIRACLE METER: {miracle_bar} {miracle_percent}%")


def create_hp_bar(current: int, maximum: int, width: int = 20) -> str:
    """Create a visual HP bar"""
    if maximum == 0:
        return "[" + " " * width + "]"

    filled = int((current / maximum) * width)
    empty = width - filled

    # Color coding
    if current / maximum > 0.5:
        color = "█"  # Green
    elif current / maximum > 0.25:
        color = "▓"  # Yellow
    else:
        color = "▒"  # Red

    return "[" + (color * filled) + ("░" * empty) + "]"


def create_meter_bar(percent: int, width: int = 20) -> str:
    """Create a visual meter bar"""
    filled = int((percent / 100) * width)
    empty = width - filled
    return "[" + ("█" * filled) + ("░" * empty) + "]"


def display_move_menu(fish: Fish):
    """Display available moves"""
    print("\n⚔️  CHOOSE MOVE:")
    for i, move in enumerate(fish.known_moves):
        power = move.get('power', [0, 0])
        if isinstance(power, list):
            power_str = f"{power[0]}-{power[1]}"
        else:
            power_str = str(power)

        move_type = move.get('type', 'Normal')
        accuracy = move.get('accuracy', 100)

        print(f"   {i+1}. {move['name']} ({move_type}) - Power: {power_str}, Acc: {accuracy}%")


def run_demo_battle():
    """Run a demonstration battle"""
    print_separator()
    print("🐟 LOAVES AND FISHES - BATTLE SYSTEM DEMO")
    print_separator()

    # Load data
    loader = get_data_loader()

    # Create player
    player = Player("Jesus")

    # Create and add fish to party
    print("\n📋 Setting up battle...")
    print("   Creating Carp Diem (Level 5)...")
    carp_data = loader.get_fish_by_id("carp_diem")
    carp = Fish("carp_diem", carp_data, level=5)
    player.add_fish_to_party(carp)

    print("   Creating Holy Mackerel (Level 5)...")
    mackerel_data = loader.get_fish_by_id("holy_mackerel")
    mackerel = Fish("holy_mackerel", mackerel_data, level=5)
    player.add_fish_to_party(mackerel)

    # Give player some items
    player.add_bread_item("plain_pita", 3)
    player.add_money(100)

    # Create enemy
    print("   Creating Wild Bandit enemy...")
    enemy = create_enemy("wild_bandit", level=4)

    if not enemy:
        print("❌ Failed to create enemy!")
        return

    print(f"\n✅ Battle setup complete!")
    print(f"   Player has {len(player.active_party)} fish")
    print(f"   Enemy: {enemy.name} (Lv.{enemy.level})")

    # Start battle
    print("\n🎺 BATTLE START!")
    battle = Battle(player, [enemy], is_boss=False)

    # Battle loop
    turn = 0
    max_turns = 20  # Limit for demo

    while battle.result == BattleResult.ONGOING and turn < max_turns:
        turn += 1

        # Display battle state
        print_battle_state(battle)

        # Get player action (simulated)
        if battle.active_fish:
            print(f"\n{'='*70}")
            print("YOUR TURN")
            print(f"{'='*70}")

            display_move_menu(battle.active_fish)

            # Auto-select move 0 for demo (random for variety)
            import random
            move_index = random.randint(0, len(battle.active_fish.known_moves) - 1)

            print(f"\n   → Using move {move_index + 1}: {battle.active_fish.known_moves[move_index]['name']}")

            # Execute turn
            result = battle.execute_turn(BattleAction.ATTACK, move_index)

            # Small pause for readability
            input("\n   Press Enter to continue...")

    # Battle end
    print_separator()
    if battle.result == BattleResult.VICTORY:
        print("🎉 VICTORY!")
        print(f"   You defeated {enemy.name}!")
        print(f"   Your fish gained XP!")
        print(f"   You earned {enemy.money_reward} denarii!")
    elif battle.result == BattleResult.DEFEAT:
        print("💀 DEFEAT!")
        print("   All your fish fainted...")
    elif battle.result == BattleResult.FLED:
        print("🏃 FLED!")
        print("   You ran away safely!")

    print_separator()

    # Final stats
    print("\n📊 BATTLE STATISTICS:")
    print(f"   Turns: {turn}")
    print(f"   Player HP: {player.current_hp}/{player.max_hp}")
    print(f"   Fish Status:")
    for fish in player.active_party:
        status = "FAINTED" if fish.is_fainted() else "OK"
        print(f"      - {fish.name}: {fish.current_hp}/{fish.max_hp} HP [{status}]")

    print_separator()


def run_boss_demo():
    """Run a boss battle demonstration"""
    print_separator()
    print("👑 BOSS BATTLE DEMO - Steward of the Feast")
    print_separator()

    # Load data
    loader = get_data_loader()

    # Create player with stronger fish
    player = Player("Jesus")

    # Create higher level fish
    print("\n📋 Setting up boss battle...")
    print("   Creating Bass-ilica (Level 7)...")
    bass_data = loader.get_fish_by_id("basilica")
    bass = Fish("basilica", bass_data, level=7)
    player.add_fish_to_party(bass)

    print("   Creating Holy Mackerel (Level 7)...")
    mackerel_data = loader.get_fish_by_id("holy_mackerel")
    mackerel = Fish("holy_mackerel", mackerel_data, level=7)
    player.add_fish_to_party(mackerel)

    # Create boss
    print("   Creating Steward of the Feast (BOSS)...")
    boss = create_boss("steward_feast", level=5)

    if not boss:
        print("❌ Failed to create boss!")
        return

    print(f"\n✅ Boss battle setup complete!")
    print(f"   Boss: {boss.name}")
    print(f"   Biblical Reference: {boss.biblical_reference}")

    # Start battle
    print("\n🎺 BOSS BATTLE START!")
    print(f"   {boss.intro_dialogue}")

    battle = Battle(player, [boss], is_boss=True)

    # Auto-battle for demo (with some turns shown)
    import random
    turn = 0
    max_turns = 15

    while battle.result == BattleResult.ONGOING and turn < max_turns:
        turn += 1

        # Show every turn for boss
        print_battle_state(battle)

        if battle.active_fish:
            move_index = random.randint(0, len(battle.active_fish.known_moves) - 1)
            print(f"\n   → Using {battle.active_fish.known_moves[move_index]['name']}")

            result = battle.execute_turn(BattleAction.ATTACK, move_index)

            input("\n   Press Enter to continue...")

    # Battle end
    print_separator()
    if battle.result == BattleResult.VICTORY:
        print("🏆 BOSS DEFEATED!")
        print(f"   {boss.defeat_dialogue}")
    elif battle.result == BattleResult.DEFEAT:
        print("💀 DEFEAT!")
        print("   The boss was too strong...")

    print_separator()


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print(" BATTLE SYSTEM TEST ".center(70, "="))
    print("="*70)

    print("\nSelect demo:")
    print("  1. Regular Battle")
    print("  2. Boss Battle")
    print("  3. Both")

    choice = input("\nChoice (1-3): ").strip()

    if choice == "1":
        run_demo_battle()
    elif choice == "2":
        run_boss_demo()
    elif choice == "3":
        run_demo_battle()
        print("\n\n")
        run_boss_demo()
    else:
        print("Running regular battle demo...")
        run_demo_battle()


if __name__ == "__main__":
    main()
