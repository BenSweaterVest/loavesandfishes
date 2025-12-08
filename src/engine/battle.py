"""
Battle system - turn-based combat engine
"""

from typing import Dict, List, Optional, Any, Tuple
import random
from enum import Enum

from .fish import Fish
from .player import Player
from .enemy import Enemy, Boss

# Import constants - handle both direct and relative imports
try:
    from utils.constants import TYPE_CHART, BASE_CRIT_CHANCE, CRIT_MULTIPLIER
except ImportError:
    from ..utils.constants import TYPE_CHART, BASE_CRIT_CHANCE, CRIT_MULTIPLIER


class BattleAction(Enum):
    """Types of actions in battle"""
    ATTACK = "attack"
    SWITCH = "switch"
    ITEM = "item"
    MIRACLE = "miracle"
    APOSTLE = "apostle"
    RUN = "run"


class BattleResult(Enum):
    """Battle outcome"""
    VICTORY = "victory"
    DEFEAT = "defeat"
    FLED = "fled"
    ONGOING = "ongoing"


class BattleLog:
    """Stores battle events for display"""

    def __init__(self):
        self.events: List[str] = []

    def add(self, message: str):
        """Add a message to the battle log"""
        self.events.append(message)

    def get_recent(self, count: int = 5) -> List[str]:
        """Get most recent messages"""
        return self.events[-count:]

    def clear(self):
        """Clear the log"""
        self.events.clear()


class Battle:
    """
    Main battle system class.
    Manages turn-based combat between player's fish and enemies.
    """

    def __init__(self, player: Player, enemies: List[Enemy], is_boss: bool = False):
        """
        Initialize a battle

        Args:
            player: The player instance
            enemies: List of enemies to fight
            is_boss: Whether this is a boss battle (can't flee)
        """
        self.player = player
        self.enemies = enemies
        self.is_boss = is_boss

        # Current active combatants
        self.active_fish: Optional[Fish] = None
        self.active_enemy: Optional[Enemy] = None

        # Battle state
        self.turn_count = 0
        self.result = BattleResult.ONGOING
        self.can_flee = not is_boss

        # Battle log
        self.log = BattleLog()

        # Used abilities tracking
        self.apostle_used = False
        self.miracle_used = False

        # Initialize battle
        self._initialize_battle()

    def _initialize_battle(self):
        """Set up the battle"""
        # Set first fish
        available = self.player.get_active_fish()
        if available:
            self.active_fish = available[0]
        else:
            self.log.add("No fish available to battle!")
            self.result = BattleResult.DEFEAT
            return

        # Set first enemy
        if self.enemies:
            self.active_enemy = self.enemies[0]
        else:
            self.log.add("No enemies to fight!")
            self.result = BattleResult.VICTORY
            return

        # Battle start message
        enemy_names = ", ".join([e.name for e in self.enemies])
        self.log.add(f"Battle started against {enemy_names}!")

        if self.is_boss:
            # Boss intro dialogue
            if hasattr(self.active_enemy, 'intro_dialogue'):
                self.log.add(f"{self.active_enemy.name}: {self.active_enemy.intro_dialogue}")

    def calculate_damage(self, attacker_stat: int, move: Dict[str, Any],
                        defender: Any, attacker_type: str = None) -> Tuple[int, bool, float]:
        """
        Calculate damage for an attack.

        Args:
            attacker_stat: Attacker's ATK stat
            move: Move dictionary
            defender: Defender (Fish or Enemy)
            attacker_type: Type of attacker (for STAB bonus)

        Returns:
            Tuple of (damage, is_critical, effectiveness_multiplier)
        """
        # Get base power
        power = move.get("power", [0, 0])
        if isinstance(power, list):
            base_damage = random.randint(power[0], power[1])
        else:
            base_damage = power

        # Apply attacker's ATK stat
        damage = base_damage + (attacker_stat // 2)

        # Check for critical hit
        is_critical = random.random() < BASE_CRIT_CHANCE
        if is_critical:
            damage = int(damage * CRIT_MULTIPLIER)

        # Type effectiveness
        move_type = move.get("type", "Normal")
        # Get defender type (fish use 'type', enemies use 'enemy_type')
        defender_type = getattr(defender, 'type', None)
        if not defender_type:
            defender_type = getattr(defender, 'enemy_type', 'Normal')

        effectiveness = self._get_type_effectiveness(move_type, defender_type)
        damage = int(damage * effectiveness)

        # STAB (Same Type Attack Bonus) - 20% bonus if move matches user's type
        if attacker_type and move_type == attacker_type:
            damage = int(damage * 1.2)

        # Randomness (85-100%)
        damage = int(damage * random.uniform(0.85, 1.0))

        # Minimum 1 damage
        damage = max(1, damage)

        return damage, is_critical, effectiveness

    def _get_type_effectiveness(self, attack_type: str, defend_type: str) -> float:
        """Get type effectiveness multiplier"""
        if attack_type in TYPE_CHART and defend_type in TYPE_CHART[attack_type]:
            return TYPE_CHART[attack_type][defend_type]
        return 1.0

    def player_attack(self, move_index: int) -> bool:
        """
        Player's fish uses an attack.

        Args:
            move_index: Index of move to use

        Returns:
            True if action succeeded
        """
        if not self.active_fish or not self.active_enemy:
            return False

        # Check if fish can use move
        if not self.active_fish.can_use_move(move_index):
            self.log.add(f"{self.active_fish.name} cannot use that move!")
            return False

        # Get the move
        move = self.active_fish.known_moves[move_index]

        # Check accuracy
        accuracy = move.get("accuracy", 100)
        if random.randint(1, 100) > accuracy:
            self.log.add(f"{self.active_fish.name} used {move['name']}, but it missed!")
            return True

        # Calculate damage
        damage, is_crit, effectiveness = self.calculate_damage(
            self.active_fish.get_effective_stat("atk"),
            move,
            self.active_enemy,
            self.active_fish.type
        )

        # Apply damage
        actual_damage = self.active_enemy.take_damage(damage)

        # Build message
        message = f"{self.active_fish.name} used {move['name']}!"
        if is_crit:
            message += " Critical hit!"
        if effectiveness > 1.0:
            message += " It's super effective!"
        elif effectiveness < 1.0:
            message += " It's not very effective..."

        message += f" ({actual_damage} damage)"
        self.log.add(message)

        # Give fish XP for damage dealt
        self.active_fish.gain_xp(actual_damage)

        # Add to miracle meter
        self.player.add_miracle_meter(actual_damage * 0.1)

        # Check if enemy defeated
        if self.active_enemy.is_defeated():
            self.log.add(f"{self.active_enemy.name} was defeated!")
            self._handle_enemy_defeat()

        # Check for boss phase transition
        if isinstance(self.active_enemy, Boss):
            if self.active_enemy.check_phase_transition():
                phase_dialogue = self.active_enemy.get_phase_dialogue()
                if phase_dialogue:
                    self.log.add(f"{self.active_enemy.name}: {phase_dialogue}")

        return True

    def enemy_attack(self) -> bool:
        """
        Enemy performs an attack.

        Returns:
            True if action succeeded
        """
        if not self.active_enemy or not self.active_fish:
            return False

        # Choose attack
        attack = self.active_enemy.choose_attack()

        # Check accuracy
        accuracy = attack.get("accuracy", 100)
        if random.randint(1, 100) > accuracy:
            self.log.add(f"{self.active_enemy.name} used {attack['name']}, but it missed!")
            return True

        # Calculate damage
        damage, is_crit, effectiveness = self.calculate_damage(
            self.active_enemy.get_effective_stat("atk"),
            attack,
            self.active_fish,
            self.active_enemy.enemy_type
        )

        # Apply damage
        actual_damage = self.active_fish.take_damage(damage)

        # Build message
        message = f"{self.active_enemy.name} used {attack['name']}!"
        if is_crit:
            message += " Critical hit!"

        message += f" ({actual_damage} damage)"
        self.log.add(message)

        # Add to miracle meter when taking damage
        self.player.add_miracle_meter(actual_damage * 0.2)

        # Check if fish fainted
        if self.active_fish.is_fainted():
            self.log.add(f"{self.active_fish.name} fainted!")
            self.player.add_miracle_meter(10)  # Bonus for fish fainting
            self._handle_fish_faint()

        return True

    def switch_fish(self, fish_index: int) -> bool:
        """
        Switch to a different fish.

        Args:
            fish_index: Index in party to switch to

        Returns:
            True if switch succeeded
        """
        party = self.player.active_party
        if fish_index < 0 or fish_index >= len(party):
            return False

        target_fish = party[fish_index]
        if target_fish.is_fainted():
            self.log.add(f"{target_fish.name} has fainted and cannot battle!")
            return False

        if target_fish == self.active_fish:
            self.log.add(f"{target_fish.name} is already in battle!")
            return False

        # Switch
        self.active_fish = target_fish
        self.log.add(f"Go, {self.active_fish.name}!")
        return True

    def use_item(self, item_id: str, target_index: int = 0) -> bool:
        """
        Use a bread item.

        Args:
            item_id: ID of bread item to use
            target_index: Index of fish to target (default 0 = active fish)

        Returns:
            True if item was used
        """
        # TODO: Implement item effects based on item data
        # For now, basic healing
        if not self.player.has_item(item_id):
            self.log.add("You don't have that item!")
            return False

        # Use item
        self.player.remove_bread_item(item_id, 1)

        # Simple heal for now (will be expanded with item data)
        if self.active_fish:
            healed = self.active_fish.heal(30)
            self.log.add(f"Used item! {self.active_fish.name} restored {healed} HP!")

        return True

    def try_flee(self) -> bool:
        """
        Attempt to flee from battle.

        Returns:
            True if successfully fled
        """
        if not self.can_flee:
            self.log.add("Can't escape from a boss battle!")
            return False

        # 50% base chance, modified by speed
        flee_chance = 0.5
        if self.active_fish and self.active_enemy:
            speed_ratio = self.active_fish.spd / max(1, self.active_enemy.spd)
            flee_chance += (speed_ratio - 1) * 0.2

        if random.random() < flee_chance:
            self.log.add("Got away safely!")
            self.result = BattleResult.FLED
            return True
        else:
            self.log.add("Couldn't escape!")
            return False

    def execute_turn(self, player_action: BattleAction, player_data: Any = None) -> BattleResult:
        """
        Execute a full turn of battle.

        Args:
            player_action: Action player wants to take
            player_data: Additional data for action (move index, item id, etc.)

        Returns:
            Current battle result
        """
        if self.result != BattleResult.ONGOING:
            return self.result

        self.turn_count += 1

        # Determine turn order based on speed
        player_goes_first = True
        if self.active_fish and self.active_enemy:
            player_goes_first = self.active_fish.spd >= self.active_enemy.spd

        # Priority moves always go first
        # TODO: Check for priority moves

        # Execute actions
        if player_goes_first:
            self._execute_player_action(player_action, player_data)
            if self.result == BattleResult.ONGOING:
                self._execute_enemy_action()
        else:
            self._execute_enemy_action()
            if self.result == BattleResult.ONGOING:
                self._execute_player_action(player_action, player_data)

        return self.result

    def _execute_player_action(self, action: BattleAction, data: Any):
        """Execute player's chosen action"""
        if action == BattleAction.ATTACK:
            self.player_attack(data)
        elif action == BattleAction.SWITCH:
            self.switch_fish(data)
        elif action == BattleAction.ITEM:
            self.use_item(data)
        elif action == BattleAction.RUN:
            self.try_flee()
        elif action == BattleAction.MIRACLE:
            self._use_miracle()
        elif action == BattleAction.APOSTLE:
            self._use_apostle(data)

    def _execute_enemy_action(self):
        """Execute enemy's action"""
        if self.active_enemy and not self.active_enemy.is_defeated():
            self.enemy_attack()

    def _handle_fish_faint(self):
        """Handle when player's fish faints"""
        # Try to find another fish
        available = self.player.get_active_fish()

        if not available:
            # No more fish - player loses
            self.log.add("All your fish have fainted!")
            self.result = BattleResult.DEFEAT
            self.player.battles_lost += 1
        else:
            # Auto-switch to next available fish
            self.active_fish = available[0]
            self.log.add(f"Go, {self.active_fish.name}!")

    def _handle_enemy_defeat(self):
        """Handle when an enemy is defeated"""
        # Give rewards
        if self.active_enemy:
            xp = self.active_enemy.xp_reward
            money = self.active_enemy.money_reward

            self.player.gain_xp(xp)
            self.player.add_money(money)

            self.log.add(f"Gained {xp} XP and {money} denarii!")

        # Remove defeated enemy
        self.enemies = [e for e in self.enemies if not e.is_defeated()]

        # Check if all enemies defeated
        if not self.enemies:
            self.log.add("Victory!")
            if self.is_boss and isinstance(self.active_enemy, Boss):
                self.log.add(f"{self.active_enemy.name}: {self.active_enemy.defeat_dialogue}")
            self.result = BattleResult.VICTORY
            self.player.battles_won += 1
        else:
            # Switch to next enemy
            self.active_enemy = self.enemies[0]
            self.log.add(f"{self.active_enemy.name} appears!")

    def _use_miracle(self):
        """Use Jesus's miracle ability"""
        if not self.player.is_miracle_ready():
            self.log.add("Miracle meter is not full!")
            return

        # TODO: Implement different miracle types
        # For now: Heal all fish
        self.log.add("Jesus used Loaves and Fishes miracle!")
        self.log.add("All fish were healed!")

        for fish in self.player.active_party:
            fish.heal(50)

        # Damage all enemies
        for enemy in self.enemies:
            enemy.take_damage(30)
            self.log.add(f"{enemy.name} took 30 damage!")

        self.player.use_miracle()
        self.miracle_used = True

    def _use_apostle(self, apostle_id: str):
        """Use an apostle's battle ability"""
        if self.apostle_used:
            self.log.add("Already used apostle ability this battle!")
            return

        if not self.player.has_apostle(apostle_id):
            self.log.add("That apostle has not been recruited!")
            return

        # TODO: Implement specific apostle abilities
        self.log.add(f"Called upon {apostle_id}!")
        self.apostle_used = True
        self.player.add_miracle_meter(5)

    def get_battle_state(self) -> Dict[str, Any]:
        """Get current battle state for UI display"""
        return {
            "turn": self.turn_count,
            "result": self.result,
            "active_fish": self.active_fish,
            "active_enemy": self.active_enemy,
            "all_enemies": self.enemies,
            "recent_log": self.log.get_recent(5),
            "miracle_meter": self.player.miracle_meter,
            "can_flee": self.can_flee,
            "apostle_used": self.apostle_used
        }
