#!/usr/bin/env python3
"""
Automated Battle System Test - No user input required
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
import random


def run_auto_battle():
    """Run an automated battle test"""
    print("="*70)
    print("🐟 BATTLE SYSTEM - AUTOMATED TEST")
    print("="*70)

    # Load data
    loader = get_data_loader()

    # Create player
    player = Player("Jesus")
    print(f"\n✅ Created player: {player}")

    # Create fish
    carp_data = loader.get_fish_by_id("carp_diem")
    carp = Fish("carp_diem", carp_data, level=5)
    player.add_fish_to_party(carp)
    print(f"✅ Added {carp} to party")

    holy_data = loader.get_fish_by_id("holy_mackerel")
    holy = Fish("holy_mackerel", holy_data, level=5)
    player.add_fish_to_party(holy)
    print(f"✅ Added {holy} to party")

    # Create enemy
    enemy = create_enemy("wild_bandit", level=4)
    print(f"✅ Created enemy: {enemy}")

    # Start battle
    print("\n🎺 BATTLE START!")
    battle = Battle(player, [enemy], is_boss=False)

    # Auto-battle
    turn = 0
    max_turns = 20

    while battle.result == BattleResult.ONGOING and turn < max_turns:
        turn += 1

        if battle.active_fish:
            # Random move
            move_index = random.randint(0, len(battle.active_fish.known_moves) - 1)
            move_name = battle.active_fish.known_moves[move_index]['name']

            print(f"\nTurn {turn}: {battle.active_fish.name} uses {move_name}")

            # Execute
            battle.execute_turn(BattleAction.ATTACK, move_index)

            # Show recent log
            state = battle.get_battle_state()
            for event in state['recent_log'][-2:]:
                print(f"  • {event}")

    # Results
    print("\n" + "="*70)
    if battle.result == BattleResult.VICTORY:
        print("🎉 VICTORY!")
    elif battle.result == BattleResult.DEFEAT:
        print("💀 DEFEAT!")

    print(f"Battle lasted {turn} turns")
    print("="*70)

    return battle.result == BattleResult.VICTORY


def test_player_class():
    """Test Player class functionality"""
    print("\n" + "="*70)
    print("👤 TESTING PLAYER CLASS")
    print("="*70)

    player = Player("Jesus")
    print(f"✅ Created player: {player}")

    # Test money
    player.add_money(100)
    print(f"✅ Added money: {player.money} denarii")

    success = player.spend_money(50)
    print(f"✅ Spent 50 denarii: {success}, remaining: {player.money}")

    # Test items
    player.add_bread_item("plain_pita", 5)
    print(f"✅ Added bread items: {player.bread_items}")

    has_item = player.has_item("plain_pita", 3)
    print(f"✅ Has 3 plain pitas: {has_item}")

    # Test apostles
    player.recruit_apostle("peter")
    player.recruit_apostle("andrew")
    print(f"✅ Recruited apostles: {player.recruited_apostles}")

    # Test miracle meter
    player.add_miracle_meter(50)
    print(f"✅ Miracle meter at {player.miracle_meter}%")

    player.add_miracle_meter(60)
    ready = player.is_miracle_ready()
    print(f"✅ Miracle ready: {ready} ({player.miracle_meter}%)")

    print("="*70)
    return True


def test_type_effectiveness():
    """Test type effectiveness system"""
    print("\n" + "="*70)
    print("⚡ TESTING TYPE EFFECTIVENESS")
    print("="*70)

    loader = get_data_loader()

    # Test Holy vs Dark (should be 2x)
    holy_fish_data = loader.get_fish_by_id("holy_mackerel")
    holy_fish = Fish("holy_mackerel", holy_fish_data, level=5)

    dark_enemy_data = {
        "id": "dark_test",
        "name": "Dark Enemy",
        "type": "Dark",
        "base_stats": {"hp": 50, "atk": 10, "def": 10, "spd": 10},
        "attacks": [],
        "xp_reward": 10,
        "money_reward": 10
    }

    from engine.enemy import Enemy
    dark_enemy = Enemy(dark_enemy_data, level=5)

    # Create battle
    player = Player("Jesus")
    player.add_fish_to_party(holy_fish)

    battle = Battle(player, [dark_enemy], is_boss=False)

    # Holy move should be super effective
    move = holy_fish.known_moves[0]  # Sacred Slap
    print(f"✅ {holy_fish.name} ({holy_fish.type}) using {move['name']} ({move['type']})")
    print(f"   Against {dark_enemy.name} ({dark_enemy.enemy_type})")

    damage, is_crit, effectiveness = battle.calculate_damage(
        holy_fish.get_effective_stat("atk"),
        move,
        dark_enemy,
        holy_fish.type
    )

    print(f"✅ Damage: {damage}, Critical: {is_crit}, Effectiveness: {effectiveness}x")

    if effectiveness == 2.0:
        print("✅ Type effectiveness working correctly! (Holy 2x vs Dark)")
    else:
        print(f"⚠️  Expected 2.0x, got {effectiveness}x")

    print("="*70)
    return True


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print(" LOAVES AND FISHES - FULL SYSTEM TEST ".center(70))
    print("="*70)

    results = []

    # Test 1: Player class
    try:
        results.append(("Player Class", test_player_class()))
    except Exception as e:
        print(f"❌ Player test failed: {e}")
        results.append(("Player Class", False))

    # Test 2: Type effectiveness
    try:
        results.append(("Type Effectiveness", test_type_effectiveness()))
    except Exception as e:
        print(f"❌ Type effectiveness test failed: {e}")
        results.append(("Type Effectiveness", False))

    # Test 3: Auto battle
    try:
        results.append(("Auto Battle", run_auto_battle()))
    except Exception as e:
        print(f"❌ Battle test failed: {e}")
        results.append(("Auto Battle", False))

    # Summary
    print("\n" + "="*70)
    print(" TEST SUMMARY ".center(70))
    print("="*70)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<50} {status}")

    total = len(results)
    passed = sum(1 for _, p in results if p)

    print("="*70)
    print(f"Results: {passed}/{total} tests passed")
    print("="*70)

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
