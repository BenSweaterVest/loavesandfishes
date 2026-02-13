"""
Battle system - turn-based combat engine for Loaves and Fishes

This module handles all combat mechanics:
- Turn order (based on speed stats)
- Damage calculation (ATK vs DEF, type effectiveness, critical hits)
- Status effects and stat modifiers
- Victory/defeat conditions
- Miracle meter accumulation
- XP and reward distribution

COMBAT FLOW:
1. Battle initialized with player fish vs enemy/enemies
2. Each turn: Determine who acts first (based on speed)
3. Execute actions (attack, item, switch, flee, miracle, apostle)
4. Apply damage with formula
5. Check for faint/defeat
6. Repeat until victory, defeat, or flee

KEY FORMULAS:
- Damage = (base_power + ATK/2) × type_effectiveness × STAB × crit × random(0.85-1.0)
- Defense reduces damage: actual_damage = damage × (100 / (100 + DEF))
- Critical hit: 5% base chance, deals 1.5x damage
- Flee chance: 50% base + 20% per point of speed advantage

See constants.py for all balance values.
"""

from typing import Dict, List, Optional, Any, Tuple
import random
from enum import Enum

from .fish import Fish
from .player import Player
from .enemy import Enemy, Boss
from .apostle_abilities import APOSTLE_ABILITIES
from .miracles import MIRACLES

# Import constants - handle both direct and relative imports
try:
    from utils.constants import TYPE_CHART, BASE_CRIT_CHANCE, CRIT_MULTIPLIER
except ImportError:
    from ..utils.constants import TYPE_CHART, BASE_CRIT_CHANCE, CRIT_MULTIPLIER

try:
    from utils.data_loader import DataLoader
except ImportError:
    from ..utils.data_loader import DataLoader


class BattleAction(Enum):
    """
    Types of actions a player can take during battle.

    Each action type triggers different game logic:
    - ATTACK: Use one of the active fish's moves
    - SWITCH: Swap active fish with another from party
    - ITEM: Use a bread item (heal, revive, buff, etc.)
    - MIRACLE: Jesus uses his miracle meter (limit break)
    - APOSTLE: Call upon recruited apostle for special ability
    - RUN: Attempt to flee (not allowed in boss battles)
    """
    ATTACK = "attack"    # Use a fish move
    SWITCH = "switch"    # Change active fish
    ITEM = "item"        # Use bread item
    MIRACLE = "miracle"  # Jesus's limit break
    APOSTLE = "apostle"  # Apostle ability
    RUN = "run"          # Flee from battle


class BattleResult(Enum):
    """
    Possible outcomes of a battle.

    ONGOING: Battle still in progress
    VICTORY: Player defeated all enemies → rewards given
    DEFEAT: All player fish fainted → Game Over (or return to town)
    FLED: Successfully ran away → no rewards, no XP
    """
    VICTORY = "victory"  # All enemies defeated
    DEFEAT = "defeat"    # All fish fainted
    FLED = "fled"        # Escaped successfully
    ONGOING = "ongoing"  # Battle continues


class BattleLog:
    """
    Stores battle events for UI display.

    The battle log keeps a running list of all events that happen
    during combat (attacks, damage, faints, etc.).

    The UI typically shows the most recent 5-10 messages.

    Usage:
        log = BattleLog()
        log.add("Fish used Splash!")
        log.add("Enemy took 50 damage!")
        recent = log.get_recent(5)  # Get last 5 messages
    """

    def __init__(self):
        """Initialize an empty battle log"""
        self.events: List[str] = []  # List of event messages in order

    def add(self, message: str):
        """
        Add a message to the battle log.

        Messages are appended in chronological order.
        Each message represents one event (attack, damage, etc.)

        Args:
            message: Text description of what happened
        """
        self.events.append(message)

    def get_recent(self, count: int = 5) -> List[str]:
        """
        Get the most recent N messages from the log.

        Uses Python's negative slicing: events[-5:] gets last 5 items.

        Args:
            count: Number of recent messages to get (default 5)

        Returns:
            List of most recent messages (may be fewer than count if log is short)
        """
        return self.events[-count:]

    def clear(self):
        """
        Clear the entire battle log.

        Used when starting a new battle to reset the event history.
        """
        self.events.clear()


class Battle:
    """
    Main battle system class.
    Manages turn-based combat between player's fish and enemies.
    """

    def __init__(self, player: Player, enemies: List[Enemy], is_boss: bool = False):
        """
        Initialize a new battle instance.

        Called when player encounters enemies (random battle, boss, etc.).
        Sets up initial battle state and selects starting combatants.

        Args:
            player: The player instance (contains party, items, stats)
            enemies: List of enemies to fight (1-3 enemies typically)
            is_boss: Whether this is a boss battle (default False)
                    Boss battles: Can't flee, may have dialogue/cutscenes

        Example:
            # Random encounter with 2 enemies
            enemies = [create_enemy("pharisee"), create_enemy("sadducee")]
            battle = Battle(player, enemies, is_boss=False)

            # Boss battle
            boss = create_boss("herod_antipas")
            battle = Battle(player, [boss], is_boss=True)

        Note:
            Automatically calls _initialize_battle() to set up
            starting fish/enemy and show battle start message.
        """
        # Store references
        self.player = player            # Player instance (party, inventory, etc.)
        self.enemies = enemies          # List of Enemy instances
        self.is_boss = is_boss          # Boss battle flag

        # ACTIVE COMBATANTS: Currently fighting fish/enemy
        # Set by _initialize_battle()
        self.active_fish: Optional[Fish] = None    # Player's current fish
        self.active_enemy: Optional[Enemy] = None  # Current enemy

        # BATTLE STATE
        self.turn_count = 0                      # Turn counter (starts at 0)
        self.result = BattleResult.ONGOING       # Battle not finished yet
        self.can_flee = not is_boss              # Can flee unless boss

        # BATTLE LOG: Stores all battle events for UI display
        self.log = BattleLog()  # Empty log, populated during battle

        # ABILITY TRACKING: One-time use abilities
        self.apostle_used = False  # Can only use apostle once per battle
        self.miracle_used = False  # Can only use miracle once per battle

        # ITEM/MIRACLE STATE
        self.bread_multiplier = 1.0
        self._queued_enemy_attack: Optional[Dict[str, Any]] = None

        # DATA LOADER
        self.data_loader = DataLoader()

        # INITIALIZE: Set up starting combatants and show intro
        self._initialize_battle()

    def _initialize_battle(self):
        """
        Set up the battle's initial state (internal helper).

        Called automatically by __init__().

        INITIALIZATION FLOW:
        1. Select player's first fish
        2. Select first enemy
        3. Show battle start message
        4. Show boss intro dialogue (if boss battle)

        EDGE CASES:
        - No fish available → Instant defeat
        - No enemies → Instant victory (should never happen)

        Note:
            This is a private helper method (starts with _).
            Called automatically, should not be called manually.
        """
        # STEP 1: SELECT FIRST FISH
        # Get list of non-fainted fish from player's party
        available = self.player.get_active_fish()

        if available:
            # Use first available fish
            self.active_fish = available[0]
        else:
            # NO FISH AVAILABLE: Instant defeat
            # This shouldn't happen in normal gameplay
            # (player should always have at least one fish)
            self.log.add("No fish available to battle!")
            self.result = BattleResult.DEFEAT
            return  # Exit early, battle over immediately

        # STEP 2: SELECT FIRST ENEMY
        # Use first enemy from the list
        if self.enemies:
            self.active_enemy = self.enemies[0]
        else:
            # NO ENEMIES: Instant victory
            # This is a bug if it happens (shouldn't create battle with no enemies)
            self.log.add("No enemies to fight!")
            self.result = BattleResult.VICTORY
            return  # Exit early, battle over immediately

        # STEP 3: BATTLE START MESSAGE
        # Build comma-separated list of enemy names
        # Example: "Pharisee, Sadducee, Tax Collector"
        enemy_names = ", ".join([e.name for e in self.enemies])
        self.log.add(f"Battle started against {enemy_names}!")

        # STEP 4: BOSS INTRO DIALOGUE (if boss battle)
        if self.is_boss:
            # Bosses have special intro_dialogue field
            # Shows flavor text before battle starts
            # Example: "Herod: You dare challenge me?"
            if hasattr(self.active_enemy, 'intro_dialogue'):
                self.log.add(f"{self.active_enemy.name}: {self.active_enemy.intro_dialogue}")

    def calculate_damage(self, attacker_stat: int, move: Dict[str, Any],
                        defender: Any, attacker_type: str = None) -> Tuple[int, bool, float]:
        """
        Calculate damage for an attack using the battle damage formula.

        DAMAGE FORMULA (step by step):
        1. Base Power: Random value from move's power range
           Example: Holy Splash has power [40, 60] → random between 40-60

        2. Add ATK Stat: damage = base_power + (ATK / 2)
           Example: ATK 50 adds 25 damage → 40 + 25 = 65

        3. Critical Hit: 5% chance to multiply by 1.5x
           Example: 65 damage → 97 on crit (65 × 1.5)

        4. Type Effectiveness: Multiply by matchup (0.5x, 1.0x, 1.5x, or 2.0x)
           Example: Holy vs Dark = 2.0x → 65 × 2.0 = 130

        5. STAB (Same Type Attack Bonus): +20% if move type matches attacker
           Example: Holy Mackerel using Holy move → 130 × 1.2 = 156

        6. Random Variance: Multiply by random 0.85-1.0
           Example: 156 × 0.92 = 143

        7. Minimum Damage: Always at least 1 damage

        TOTAL EXAMPLE:
        Holy Mackerel (ATK 50, Holy type) uses Holy Splash (40-60 power)
        vs Dark Enemy:
        - Base: 50 (random from 40-60)
        - +ATK: 50 + 25 = 75
        - Crit: 75 × 1.5 = 112 (if crit rolled)
        - Type: 112 × 2.0 = 224 (Holy → Dark super effective)
        - STAB: 224 × 1.2 = 268 (Holy fish, Holy move)
        - Random: 268 × 0.92 = 246
        - Final: 246 damage dealt

        This damage is BEFORE defense reduction (defender.take_damage() applies DEF).

        Args:
            attacker_stat: Attacker's effective ATK stat (after buffs/debuffs)
            move: Move dictionary with power, type, accuracy
            defender: Defender (Fish or Enemy instance)
            attacker_type: Type of attacker for STAB bonus (optional)

        Returns:
            Tuple of (final_damage, was_critical_hit, type_effectiveness_multiplier)

        Note:
            Defense is applied AFTER this calculation in the defender's take_damage() method.
            See fish.py:take_damage() for defense formula.
        """
        # STEP 1: Get base power (random from range or fixed value)
        power = move.get("power", [0, 0])
        if isinstance(power, list):
            # Power is a range [min, max] - pick random value
            base_damage = random.randint(power[0], power[1])
        else:
            # Power is a fixed value
            base_damage = power

        # STEP 2: Apply attacker's ATK stat
        # Formula: base_power + (ATK / 2)
        # This makes ATK meaningful but not overpowering
        damage = base_damage + (attacker_stat // 2)  # // is integer division (rounds down)

        # STEP 3: Check for critical hit (5% base chance)
        # Critical hits deal 1.5x damage (see constants.py)
        is_critical = random.random() < BASE_CRIT_CHANCE  # random.random() returns 0.0-1.0
        if is_critical:
            damage = int(damage * CRIT_MULTIPLIER)  # Default 1.5x

        # STEP 4: Type effectiveness
        # Get move type (Holy, Water, Earth, Spirit, Dark)
        move_type = move.get("type", "Normal")

        # Get defender type (fish use 'type', enemies use 'enemy_type')
        defender_type = getattr(defender, 'type', None)
        if not defender_type:
            defender_type = getattr(defender, 'enemy_type', 'Normal')

        # Look up effectiveness multiplier from TYPE_CHART
        effectiveness = self._get_type_effectiveness(move_type, defender_type)
        damage = int(damage * effectiveness)

        # STEP 5: STAB (Same Type Attack Bonus)
        # If attacker's type matches move type, +20% damage
        # Example: Holy Mackerel using Holy Splash gets STAB
        if attacker_type and move_type == attacker_type:
            damage = int(damage * 1.2)  # 20% bonus

        # STEP 6: Random variance (85-100%)
        # Prevents damage from being too predictable
        # Makes each attack feel slightly different
        damage = int(damage * random.uniform(0.85, 1.0))

        # STEP 7: Minimum 1 damage (prevents 0 damage stalling)
        damage = max(1, damage)

        # Return damage (before defense), crit flag, and type effectiveness
        return damage, is_critical, effectiveness

    def _get_type_effectiveness(self, attack_type: str, defend_type: str) -> float:
        """
        Get type effectiveness multiplier from TYPE_CHART.

        Looks up how effective one type is against another using the
        type chart defined in constants.py.

        Args:
            attack_type: Type of the attacking move (Holy, Water, Earth, Spirit, Dark)
            defend_type: Type of the defender (same types)

        Returns:
            Effectiveness multiplier:
            - 2.0 = Super effective (double damage)
            - 1.5 = Strong against
            - 1.0 = Neutral (normal damage)
            - 0.5 = Resisted (half damage)

        Example:
            effectiveness = _get_type_effectiveness("Holy", "Dark")
            # Returns 2.0 (Holy is super effective vs Dark)

        Note:
            If types aren't in chart, defaults to 1.0 (neutral).
            This handles "Normal" type or missing types gracefully.
        """
        # Look up in TYPE_CHART (imported from constants.py)
        # Chart format: TYPE_CHART[attacker][defender] = multiplier
        if attack_type in TYPE_CHART and defend_type in TYPE_CHART[attack_type]:
            return TYPE_CHART[attack_type][defend_type]

        # Default to neutral if type combo not found
        return 1.0

    def player_attack(self, move_index: int) -> bool:
        """
        Player's fish uses an attack against the active enemy.

        ATTACK FLOW:
        1. Validate fish/enemy exist and fish can use move
        2. Get move data from fish's known_moves list
        3. Roll accuracy check (move may miss)
        4. Calculate damage using battle formula
        5. Apply damage to enemy (enemy's defense reduces it)
        6. Build battle message with flavor text
        7. Award XP to fish based on damage dealt
        8. Increase miracle meter (limit break charge)
        9. Check if enemy defeated → handle rewards
        10. Check for boss phase transition

        Args:
            move_index: Which move to use (0-3, index in known_moves)

        Returns:
            True if action succeeded (even if missed)
            False if action failed validation (invalid move, can't use)

        Example:
            # Player selects move 0 (first move in list)
            success = battle.player_attack(0)
            # Fish uses move, calculates damage, applies it

        Note:
            Even if attack misses, returns True (action was valid).
            Only returns False if move can't be used at all.
        """
        # VALIDATION: Check battle state
        if not self.active_fish or not self.active_enemy:
            return False  # Invalid state - no combatants

        # VALIDATION: Check if fish can use this move
        # can_use_move() checks status effects (frozen, asleep, etc.)
        if not self.active_fish.can_use_move(move_index):
            self.log.add(f"{self.active_fish.name} cannot use that move!")
            return False

        # STEP 1: Get the move data
        # known_moves is a list of move dictionaries from fish data
        move = self.active_fish.known_moves[move_index]

        # STEP 2: Accuracy check
        # Most moves have 100% accuracy, but some may miss
        # Roll random 1-100, if higher than accuracy, attack misses
        accuracy = move.get("accuracy", 100)  # Default 100% if not specified
        if random.randint(1, 100) > accuracy:
            # Move missed - still uses turn, but no damage
            self.log.add(f"{self.active_fish.name} used {move['name']}, but it missed!")
            return True  # Action succeeded but missed

        # STEP 3: Calculate damage
        # Uses the comprehensive damage formula (see calculate_damage docstring)
        # Returns: damage (int), was_critical (bool), type_effectiveness (float)
        damage, is_crit, effectiveness = self.calculate_damage(
            self.active_fish.get_effective_stat("atk"),  # ATK after buffs/debuffs
            move,                                         # Move data (power, type, etc.)
            self.active_enemy,                            # Target for type lookup
            self.active_fish.type                         # For STAB bonus
        )

        # STEP 4: Apply damage to enemy
        # Enemy's take_damage() applies defense reduction formula
        # Returns actual damage dealt after defense
        actual_damage = self.active_enemy.take_damage(damage)

        # STEP 5: Build battle message with flavor text
        message = f"{self.active_fish.name} used {move['name']}!"

        # Add critical hit notification
        if is_crit:
            message += " Critical hit!"

        # Add type effectiveness flavor text
        if effectiveness > 1.0:
            message += " It's super effective!"  # 1.5x or 2.0x damage
        elif effectiveness < 1.0:
            message += " It's not very effective..."  # 0.5x damage

        # Show actual damage dealt
        message += f" ({actual_damage} damage)"
        self.log.add(message)

        # STEP 6: Award XP to fish
        # Fish gains XP equal to damage dealt (see constants.py)
        # This rewards using your strongest fish
        self.active_fish.gain_xp(actual_damage)

        # STEP 7: Increase miracle meter (limit break system)
        # Gains 0.1% per point of damage dealt
        # Deal 100 damage = +10% meter
        self.player.add_miracle_meter(actual_damage * 0.1)

        # STEP 8: Check if enemy was defeated
        if self.active_enemy.is_defeated():
            self.log.add(f"{self.active_enemy.name} was defeated!")
            self._handle_enemy_defeat()  # Awards XP/money, checks for victory

        # STEP 9: Check for boss phase transition
        # Some bosses change tactics at 50% HP, 25% HP, etc.
        if isinstance(self.active_enemy, Boss):
            if self.active_enemy.check_phase_transition():
                # Boss entered new phase - show special dialogue
                phase_dialogue = self.active_enemy.get_phase_dialogue()
                if phase_dialogue:
                    self.log.add(f"{self.active_enemy.name}: {phase_dialogue}")

        return True  # Attack succeeded

    def enemy_attack(self, attack: Optional[Dict[str, Any]] = None) -> bool:
        """
        Enemy performs an attack against the player's active fish.

        ATTACK FLOW:
        1. Validate enemy/fish exist
        2. Enemy AI chooses which attack to use
        3. Roll accuracy check (attack may miss)
        4. Calculate damage using battle formula
        5. Apply damage to player's fish (defense reduces it)
        6. Build battle message
        7. Increase miracle meter (taking damage charges it)
        8. Check if fish fainted → switch or defeat

        Returns:
            True if action succeeded (even if missed)
            False if action failed validation

        Note:
            Enemy attacks work identically to player attacks,
            just reversed. They use the same damage formula.

            Taking damage charges miracle meter FASTER than dealing
            damage (0.2% vs 0.1% per point), creating a "desperation"
            mechanic where losing battles builds meter for comebacks.
        """
        # VALIDATION: Check battle state
        if not self.active_enemy or not self.active_fish:
            return False  # Invalid state - no combatants

        # STEP 1: Enemy AI chooses attack (or use pre-queued attack)
        attack = self._queued_enemy_attack if self._queued_enemy_attack else self.active_enemy.choose_attack()
        self._queued_enemy_attack = None

        # STEP 2: Accuracy check
        # Same as player attacks - some moves may miss
        accuracy = attack.get("accuracy", 100)  # Default 100%
        if random.randint(1, 100) > accuracy:
            # Attack missed - still uses turn
            self.log.add(f"{self.active_enemy.name} used {attack['name']}, but it missed!")
            return True  # Action succeeded but missed

        # STEP 3: Calculate damage
        # Uses same formula as player attacks
        # enemy_type is used for STAB bonus (same as fish.type)
        damage, is_crit, effectiveness = self.calculate_damage(
            self.active_enemy.get_effective_stat("atk"),  # Enemy ATK
            attack,                                        # Attack data
            self.active_fish,                              # Target (player's fish)
            self.active_enemy.enemy_type                   # For STAB bonus
        )

        # STEP 4: Apply damage to player's fish
        # Fish's take_damage() applies defense reduction
        actual_damage = self.active_fish.take_damage(damage)

        # STEP 5: Build battle message
        message = f"{self.active_enemy.name} used {attack['name']}!"

        # Add critical hit notification
        if is_crit:
            message += " Critical hit!"

        # Show damage dealt (no type effectiveness message for enemies)
        message += f" ({actual_damage} damage)"
        self.log.add(message)

        # STEP 6: Increase miracle meter (DESPERATION MECHANIC)
        # Taking damage charges meter at 0.2% per point
        # This is DOUBLE the rate of dealing damage (0.1%)
        # Design: Encourages risky play, enables comebacks
        # Take 100 damage = +20% meter (vs +10% for dealing 100)
        self.player.add_miracle_meter(actual_damage * 0.2)

        # STEP 7: Check if fish fainted (reached 0 HP)
        if self.active_fish.is_fainted():
            self.log.add(f"{self.active_fish.name} fainted!")

            # BONUS: Fish fainting gives +10% miracle meter
            # This is a huge boost for comebacks in tough battles
            self.player.add_miracle_meter(10)

            # Handle fish faint (switch or defeat)
            self._handle_fish_faint()

        return True  # Attack succeeded

    def switch_fish(self, fish_index: int) -> bool:
        """
        Switch the active fish to a different one from the party.

        SWITCH MECHANICS:
        - Switching uses your turn (enemy attacks after)
        - Can't switch to fainted fish
        - Can't switch to fish already in battle
        - Resets stat modifiers on switched fish (buffs/debuffs cleared)

        This is a key strategy element:
        - Switch to counter enemy type
        - Switch to save low-HP fish
        - Switch to activate different apostle combos

        Args:
            fish_index: Index in active_party to switch to (0-3)

        Returns:
            True if switch succeeded
            False if invalid index or fish can't battle

        Example:
            # Player has 4 fish, wants to switch to 3rd one
            battle.switch_fish(2)  # 0-indexed, so 2 = third fish
            # "Go, [Fish Name]!" message appears
        """
        # Get player's party (list of up to 4 fish)
        party = self.player.active_party

        # VALIDATION: Check index is valid
        if fish_index < 0 or fish_index >= len(party):
            return False  # Invalid index

        # Get the target fish
        target_fish = party[fish_index]

        # VALIDATION: Can't switch to fainted fish
        if target_fish.is_fainted():
            self.log.add(f"{target_fish.name} has fainted and cannot battle!")
            return False

        # VALIDATION: Can't switch to fish already in battle
        if target_fish == self.active_fish:
            self.log.add(f"{target_fish.name} is already in battle!")
            return False

        # PERFORM SWITCH
        previous_fish = self.active_fish
        self.active_fish = target_fish
        self.log.add(f"Go, {self.active_fish.name}!")

        # Reset modifiers on the switched-out fish to avoid buff stacking
        if previous_fish:
            previous_fish.reset_stat_modifiers()

        return True  # Switch succeeded

    def use_item(self, item_id: str, target_index: int = 0) -> bool:
        """
        Use a bread item on a fish during battle.

        ITEM MECHANICS:
        - Using items uses your turn (enemy attacks after)
        - Items come from player's bread inventory
        - Each item has different effects (heal, revive, buff, cure status)
        - Items are consumed on use (removed from inventory)

        Common item types:
        - Manna Bread: Heals HP
        - Unleavened Bread: Cures status effects
        - Blessed Bread: Applies buffs
        - Fish Bread: Revives fainted fish

        Args:
            item_id: ID of bread item to use (e.g., "manna_bread")
            target_index: Which fish to use it on (0 = active fish)

        Returns:
            True if item was used successfully
            False if player doesn't have item

        Example:
            # Use manna bread to heal active fish
            battle.use_item("manna_bread")
            # Item is consumed, fish HP restored

        Note:
            This is a STUB implementation. Full item system needs:
            - Load item data from items.json
            - Apply effects based on item.effect field
            - Handle different target types (single, all, fainted only)
        """
        # VALIDATION: Check player has the item
        if not self.player.has_item(item_id):
            self.log.add("You don't have that item!")
            return False

        item_data = self.data_loader.get_item_by_id(item_id)
        if not item_data:
            self.log.add("That item has no effect.")
            return False

        # CONSUME ITEM: Remove from inventory
        self.player.remove_bread_item(item_id, 1)

        target_fish = self.active_fish
        if 0 <= target_index < len(self.player.active_party):
            target_fish = self.player.active_party[target_index]

        effect = item_data.get("effect", "")
        multiplier = self.bread_multiplier
        duration = int(item_data.get("duration", 0))

        if effect == "heal_hp":
            healed = target_fish.heal(int(item_data.get("power", 0) * multiplier))
            self.log.add(f"{target_fish.name} restored {healed} HP!")
        elif effect == "heal_and_cure_poison":
            healed = target_fish.heal(int(item_data.get("power", 0) * multiplier))
            target_fish.remove_status_effect("poisoned")
            self.log.add(f"{target_fish.name} restored {healed} HP and was cured!")
        elif effect == "heal_and_atk_boost":
            healed = target_fish.heal(int(item_data.get("heal_power", 0) * multiplier))
            boost = float(item_data.get("atk_boost", 0)) / 100.0
            if boost > 0:
                target_fish.apply_stat_modifier("atk", 1.0 + boost, duration)
            self.log.add(f"{target_fish.name} restored {healed} HP and felt stronger!")
        elif effect == "full_heal_all":
            for fish in self.player.active_party:
                fish.heal(fish.max_hp)
                fish.clear_status_effects()
            self.log.add("All fish were fully healed!")
        elif effect == "atk_boost":
            boost = float(item_data.get("boost_percent", 0)) / 100.0
            if boost > 0:
                target_fish.apply_stat_modifier("atk", 1.0 + boost, duration)
            self.log.add(f"{target_fish.name}'s attack rose!")
        elif effect == "spd_boost":
            boost = float(item_data.get("boost_percent", 0)) / 100.0
            if boost > 0:
                target_fish.apply_stat_modifier("spd", 1.0 + boost, duration)
            self.log.add(f"{target_fish.name}'s speed rose!")
        elif effect == "def_boost":
            boost = float(item_data.get("boost_percent", 0)) / 100.0
            if boost > 0:
                target_fish.apply_stat_modifier("def", 1.0 + boost, duration)
            self.log.add(f"{target_fish.name}'s defense rose!")
        elif effect == "enemy_atk_down" and self.active_enemy:
            debuff = float(item_data.get("debuff_percent", 0)) / 100.0
            if debuff > 0:
                self.active_enemy.apply_stat_modifier("atk", 1.0 - debuff, duration)
            self.log.add(f"{self.active_enemy.name}'s attack fell!")
        elif effect == "remove_all_debuffs":
            target_fish.clear_status_effects()
            target_fish.reset_stat_modifiers()
            self.log.add(f"{target_fish.name} was purified!")
        elif effect == "auto_revive":
            if target_fish.is_fainted():
                revive_hp = int(item_data.get("revive_hp", 1))
                target_fish.current_hp = max(1, revive_hp)
                self.log.add(f"{target_fish.name} was revived!")
            else:
                self.log.add("Nothing happened.")
        elif effect == "invincible":
            target_fish.apply_status_effect("invincible", duration)
            self.log.add(f"{target_fish.name} became invincible!")
        else:
            self.log.add("That item has no effect.")

        return True  # Item used successfully

    def try_flee(self) -> bool:
        """
        Attempt to flee from battle and escape to safety.

        FLEE MECHANICS:
        - Can't flee from boss battles (always False)
        - Base 50% chance to escape
        - Modified by speed ratio (faster fish = higher chance)
        - Failed flee uses your turn (enemy attacks)
        - Successful flee ends battle with no rewards

        FLEE CHANCE FORMULA:
        flee_chance = 50% + (speed_ratio - 1) × 20%

        Examples:
        - Fish SPD 30 vs Enemy SPD 30 (ratio 1.0) → 50% chance
        - Fish SPD 40 vs Enemy SPD 30 (ratio 1.33) → 56.6% chance
        - Fish SPD 30 vs Enemy SPD 40 (ratio 0.75) → 45% chance

        Faster fish are better at escaping!

        Returns:
            True if successfully fled (battle ends)
            False if failed to flee (enemy gets turn)

        Note:
            Fleeing gives NO rewards (no XP, no money).
            Use when low on HP and trying to preserve fish.
        """
        # VALIDATION: Check if fleeing is allowed
        # Boss battles don't allow fleeing (is_boss = True)
        if not self.can_flee:
            self.log.add("Can't escape from a boss battle!")
            return False

        # CALCULATE FLEE CHANCE
        # Base chance: 50% (coin flip)
        flee_chance = 0.5

        # SPEED MODIFIER: Compare fish speed to enemy speed
        if self.active_fish and self.active_enemy:
            # Calculate speed ratio (how much faster/slower fish is)
            # max(1, ...) prevents division by zero
            speed_ratio = self.active_fish.spd / max(1, self.active_enemy.spd)

            # Apply speed modifier
            # Each point of speed advantage/disadvantage = 20% change
            # speed_ratio 1.0 (equal) → +0% (no change)
            # speed_ratio 1.5 (50% faster) → +10% (60% total)
            # speed_ratio 0.5 (50% slower) → -10% (40% total)
            flee_chance += (speed_ratio - 1) * 0.2

        # ROLL FOR SUCCESS
        # random.random() returns 0.0-1.0
        if random.random() < flee_chance:
            # SUCCESS: Escaped safely
            self.log.add("Got away safely!")
            self.result = BattleResult.FLED  # Ends battle
            return True
        else:
            # FAILURE: Couldn't escape, enemy gets free turn
            self.log.add("Couldn't escape!")
            return False  # Battle continues, enemy attacks

    def execute_turn(self, player_action: BattleAction, player_data: Any = None) -> BattleResult:
        """
        Execute a full turn of battle (both player and enemy actions).

        TURN FLOW:
        1. Check if battle is already over
        2. Increment turn counter
        3. Determine turn order (based on speed)
        4. Execute faster action first
        5. If battle still ongoing, execute slower action
        6. Return current battle result

        TURN ORDER RULES:
        - Higher speed goes first
        - Tie goes to player (SPD >= enemy SPD)
        - Priority moves always go first
        - If one side's action ends battle, other doesn't act

        This creates strategic depth:
        - Fast fish attack first, potentially KO before taking damage
        - Slow fish might faint before attacking
        - Speed ties favor player (slight advantage)

        Args:
            player_action: What the player wants to do (ATTACK, SWITCH, ITEM, etc.)
            player_data: Additional data needed for action:
                - ATTACK: move_index (which move to use)
                - SWITCH: fish_index (which fish to switch to)
                - ITEM: item_id (which item to use)
                - RUN: None
                - MIRACLE: None
                - APOSTLE: apostle_id (which apostle to call)

        Returns:
            Current battle result (ONGOING, VICTORY, DEFEAT, or FLED)

        Example:
            # Player chooses ATTACK with move index 0
            result = battle.execute_turn(BattleAction.ATTACK, 0)
            # Both player and enemy attack (order based on speed)
            # Returns ONGOING, VICTORY, DEFEAT, or FLED
        """
        # CHECK: If battle already ended, don't execute turn
        if self.result != BattleResult.ONGOING:
            return self.result

        # INCREMENT TURN COUNTER
        # Used for effects that trigger after N turns, tracking battle length, etc.
        self.turn_count += 1

        # DETERMINE TURN ORDER
        # Compare speed stats to see who goes first
        player_goes_first = True  # Default to player (ties favor player)

        if self.active_fish and self.active_enemy:
            # Compare speeds: >= means player wins ties
            player_goes_first = self.active_fish.spd >= self.active_enemy.spd

        # PRIORITY MOVES
        player_priority = 0
        enemy_priority = 0
        if player_action == BattleAction.ATTACK and self.active_fish:
            move = self.active_fish.known_moves[player_data]
            player_priority = move.get("priority", 0)

        if self.active_enemy:
            self._queued_enemy_attack = self.active_enemy.choose_attack()
            enemy_priority = self._queued_enemy_attack.get("priority", 0)

        if player_priority != enemy_priority:
            player_goes_first = player_priority > enemy_priority

        # EXECUTE ACTIONS IN ORDER
        if player_goes_first:
            # PLAYER ACTS FIRST
            # Execute player's chosen action (attack, switch, item, etc.)
            self._execute_player_action(player_action, player_data)

            # Check if battle ended (enemy defeated, fled, etc.)
            if self.result == BattleResult.ONGOING:
                # Battle still ongoing - enemy acts
                self._execute_enemy_action()
        else:
            # ENEMY ACTS FIRST
            # Enemy attacks automatically
            self._execute_enemy_action()

            # Check if battle ended (all fish fainted)
            if self.result == BattleResult.ONGOING:
                # Battle still ongoing - player acts
                self._execute_player_action(player_action, player_data)

        # END-OF-TURN EFFECTS
        if self.result == BattleResult.ONGOING:
            self._apply_end_of_turn_effects()

        return self.result  # Return current battle status

    def _execute_player_action(self, action: BattleAction, data: Any):
        """
        Execute player's chosen action (internal helper).

        This method routes the player's action to the appropriate handler method.
        It's called by execute_turn() after determining turn order.

        Args:
            action: Type of action (ATTACK, SWITCH, ITEM, RUN, MIRACLE, APOSTLE)
            data: Action-specific data (move index, fish index, item id, etc.)

        Note:
            This is a private helper method (starts with _).
            External code should call execute_turn(), not this directly.
        """
        # Route to appropriate action handler based on action type
        if action == BattleAction.ATTACK:
            self.player_attack(data)  # data = move_index
        elif action == BattleAction.SWITCH:
            self.switch_fish(data)    # data = fish_index
        elif action == BattleAction.ITEM:
            self.use_item(data)       # data = item_id
        elif action == BattleAction.RUN:
            self.try_flee()           # data = None
        elif action == BattleAction.MIRACLE:
            self._use_miracle()       # data = None
        elif action == BattleAction.APOSTLE:
            self._use_apostle(data)   # data = apostle_id

    def _execute_enemy_action(self):
        """
        Execute enemy's action (internal helper).

        Enemy AI is simple: always attack with a random move.
        More complex enemies (bosses) may have smarter AI.

        Called by execute_turn() after determining turn order.

        Note:
            This is a private helper method (starts with _).
            Only checks if enemy can act, then calls enemy_attack().
        """
        # Only act if enemy exists and isn't defeated
        if self.active_enemy and not self.active_enemy.is_defeated():
            self.enemy_attack(self._queued_enemy_attack)

    def _handle_fish_faint(self):
        """
        Handle when the active fish faints (reaches 0 HP).

        FAINT MECHANICS:
        1. Check if any other fish can battle
        2. If yes: Auto-switch to next available fish
        3. If no: Player loses battle (DEFEAT)

        This is called automatically when fish HP drops to 0.
        Player doesn't get to choose which fish to switch to
        (it's automatic to keep battle flow smooth).

        Note:
            Fish fainting grants +10% miracle meter (see enemy_attack).
            Defeat increments player.battles_lost stat.
        """
        # Try to find another fish that can battle
        # get_active_fish() returns list of non-fainted fish
        available = self.player.get_active_fish()

        if not available:
            # NO FISH LEFT: Player loses battle
            self.log.add("All your fish have fainted!")
            self.result = BattleResult.DEFEAT  # Ends battle
            self.player.battles_lost += 1      # Track loss stat

            # Defeat consequences
            lost_money = self.player.money // 2
            self.player.money -= lost_money
            for fish in self.player.active_party:
                fish.revive(0.1)
                fish.clear_status_effects()
            self.log.add(f"You lost {lost_money} denarii and retreated to safety.")
        else:
            # FISH AVAILABLE: Auto-switch to next fish
            # Takes first available fish from list
            self.active_fish = available[0]
            self.log.add(f"Go, {self.active_fish.name}!")

            # Battle continues with new fish
            # Note: This doesn't use a turn, happens instantly

    def _handle_enemy_defeat(self):
        """
        Handle when an enemy is defeated (reaches 0 HP).

        DEFEAT MECHANICS:
        1. Award XP and money to player
        2. Remove defeated enemy from battle
        3. Check if all enemies defeated:
           - Yes: VICTORY! Battle ends
           - No: Next enemy appears

        Rewards are given per enemy, not per battle.
        Multi-enemy battles give rewards after each defeat.

        Note:
            XP is split among all fish in party (see player.gain_xp).
            Victory increments player.battles_won stat.
        """
        # AWARD REWARDS for defeating this enemy
        if self.active_enemy:
            # Get reward amounts from enemy data
            xp = self.active_enemy.xp_reward      # Experience points
            money = self.active_enemy.money_reward  # Denarii (game currency)

            # Grant rewards to player
            # player.gain_xp() distributes XP among party fish
            # player.add_money() adds to player's wallet
            self.player.gain_xp(xp)
            self.player.add_money(money)

            self.log.add(f"Gained {xp} XP and {money} denarii!")

        # REMOVE DEFEATED ENEMY from enemy list
        # List comprehension: keep only enemies that are NOT defeated
        self.enemies = [e for e in self.enemies if not e.is_defeated()]

        # CHECK FOR VICTORY: Are all enemies defeated?
        if not self.enemies:
            # ALL ENEMIES DEFEATED: Victory!
            self.log.add("Victory!")

            # BOSS DEFEAT DIALOGUE
            # Bosses have special defeat messages
            if self.is_boss and isinstance(self.active_enemy, Boss):
                # Show boss's defeat dialogue (story moment)
                self.log.add(f"{self.active_enemy.name}: {self.active_enemy.defeat_dialogue}")

            # End battle with victory
            self.result = BattleResult.VICTORY
            self.player.battles_won += 1  # Track victory stat

            # Additional victory rewards (optional data-driven hooks)
            if hasattr(self.active_enemy, "properties"):
                props = self.active_enemy.properties
                bonus_money = int(props.get("bonus_money", 0))
                bonus_xp = int(props.get("bonus_xp", 0))
                if bonus_money > 0:
                    self.player.add_money(bonus_money)
                    self.log.add(f"Bonus reward: {bonus_money} denarii!")
                if bonus_xp > 0:
                    self.player.gain_xp(bonus_xp)
                    self.log.add(f"Bonus reward: {bonus_xp} XP!")
        else:
            # ENEMIES REMAIN: Next enemy appears
            # Switch to next enemy in list
            self.active_enemy = self.enemies[0]
            self.log.add(f"{self.active_enemy.name} appears!")

            # Battle continues against new enemy
            # Player's fish stays in battle (doesn't auto-heal)

    def _use_miracle(self, miracle_id: Optional[str] = None):
        """
        Use Jesus's miracle ability (limit break system).

        MIRACLE MECHANICS:
        - Requires full miracle meter (100%)
        - Can only be used once per battle
        - Currently: Heals all fish + damages all enemies
        - Powerful comeback mechanic

        The miracle meter fills from:
        - Dealing damage (+0.1% per damage)
        - Taking damage (+0.2% per damage)
        - Fish fainting (+10%)
        - Using apostle abilities (+5%)

        Design: Should fill 1-2 times per average battle.
        Encourages aggressive and risky play.

        Note:
            This currently selects the first available miracle when
            none is specified.
        """
        if self.miracle_used:
            self.log.add("Miracle already used this battle!")
            return

        selected = MIRACLES.get(miracle_id) if miracle_id else None
        if selected is None:
            for miracle in MIRACLES.values():
                if self.player.miracle_meter >= miracle.meter_cost:
                    selected = miracle
                    break

        if selected is None:
            self.log.add("Miracle meter is not high enough!")
            return

        if self.player.miracle_meter < selected.meter_cost:
            self.log.add("Miracle meter is not high enough!")
            return

        self.player.miracle_meter = max(0.0, self.player.miracle_meter - selected.meter_cost)
        self.log.add(f"Jesus used {selected.name} miracle!")

        if selected.miracle_id == "healing_miracle":
            for fish in self.player.active_party:
                fish.heal(fish.max_hp)
                fish.clear_status_effects()
            self.log.add("All fish were healed!")
        elif selected.miracle_id == "loaves_and_fishes":
            self.bread_multiplier = 3.0
            self.log.add("Bread effects were multiplied!")
        elif selected.miracle_id == "divine_judgment":
            for enemy in self.enemies:
                enemy.take_damage(300)
                enemy.apply_stat_modifier("atk", 0.5, 3)
                enemy.apply_stat_modifier("def", 0.5, 3)
                enemy.apply_stat_modifier("spd", 0.5, 3)
            self.log.add("Divine judgment struck all enemies!")
        elif selected.miracle_id == "resurrection_power":
            for fish in self.player.active_party:
                if fish.is_fainted():
                    fish.revive(1.0)
                    fish.apply_status_effect("immunity", 2)
            self.log.add("The fallen rose again!")

        self.miracle_used = True

    def _use_apostle(self, apostle_id: str):
        """
        Use an apostle's special battle ability.

        APOSTLE MECHANICS:
        - Must have recruited the apostle first
        - Can only use once per battle
        - Each apostle has unique ability
        - Grants +5% miracle meter

        Example apostle abilities:
        - Peter: Revive one fainted fish at 50% HP
        - John: Heal all fish for 30 HP
        - James: Deal 50 damage to all enemies
        - Andrew: Buff all fish ATK by 50%
        - Thomas: Guarantee next attack is critical hit
        - Matthew: Give player extra money this battle

        Args:
            apostle_id: ID of apostle to call (e.g., "peter")

        Note:
            Abilities are loaded from APOSTLE_ABILITIES.
        """
        # VALIDATION: Can only use once per battle
        if self.apostle_used:
            self.log.add("Already used apostle ability this battle!")
            return

        # VALIDATION: Must have recruited apostle
        if not self.player.has_apostle(apostle_id):
            self.log.add("That apostle has not been recruited!")
            return

        ability = APOSTLE_ABILITIES.get(apostle_id)
        if not ability:
            self.log.add("That apostle has no ability yet!")
            return

        self.log.add(f"Called upon {ability.name}!")

        if ability.ability_id == "rock_foundation":
            for fish in self.player.active_party:
                fish.apply_stat_modifier("def", 1.5)
            self.log.add("Party defense rose!")
        elif ability.ability_id == "fishers_net":
            self.log.add("Enemy escape was prevented!")
        elif ability.ability_id == "sons_of_thunder":
            for enemy in self.enemies:
                enemy.take_damage(ability.power)
            self.log.add("Thunder struck all enemies!")
        elif ability.ability_id == "beloved_healing":
            for fish in self.player.active_party:
                fish.heal(ability.power)
            self.log.add("All fish were healed!")
        elif ability.ability_id == "multiplication":
            self.bread_multiplier = 3.0
            self.log.add("Bread effects were multiplied!")
        elif ability.ability_id == "true_sight":
            if self.active_enemy:
                self.log.add(f"Enemy HP: {self.active_enemy.current_hp}/{self.active_enemy.max_hp}")
        elif ability.ability_id == "tax_audit":
            self.player.add_money(100)
            for enemy in self.enemies:
                enemy.apply_stat_modifier("atk", 0.7)
            self.log.add("Enemy attack fell and money was gained!")
        elif ability.ability_id == "doubting_strike":
            if self.active_enemy and self.active_enemy.current_hp <= self.active_enemy.max_hp * 0.5:
                self.active_enemy.take_damage(ability.power)
                self.log.add("A devastating strike landed!")
            else:
                self.log.add("The enemy must be below 50% HP!")
                return
        elif ability.ability_id == "lesser_miracle":
            for fish in self.player.active_party:
                fish.heal(ability.power)
                fish.clear_status_effects()
            self.log.add("All fish were healed and cured!")
        elif ability.ability_id == "righteous_zeal" and self.active_fish:
            self.active_fish.apply_stat_modifier("atk", 1.4)
            self.active_fish.apply_stat_modifier("spd", 1.4)
            self.log.add("Your fish is filled with zeal!")
        elif ability.ability_id == "revolutionary_fervor" and self.active_fish:
            damage = int(self.active_fish.current_hp * 0.5)
            for enemy in self.enemies:
                enemy.take_damage(damage)
            self.log.add("Zealous damage struck all enemies!")
        elif ability.ability_id == "thirty_silver":
            sacrificed = next((f for f in self.player.active_party if not f.is_fainted()), None)
            if sacrificed:
                sacrificed.current_hp = 0
            self.player.add_money(300)
            for fish in self.player.active_party:
                fish.apply_stat_modifier("atk", 1.5)
            self.log.add("A sacrifice was made for power and silver!")

        # MARK AS USED
        self.apostle_used = True

        # GRANT MIRACLE METER: Using apostle gives +5%
        self.player.add_miracle_meter(5)

    def _apply_end_of_turn_effects(self):
        if self.active_fish:
            self._apply_status_damage(self.active_fish, "poisoned", 0.05, "poison")
            self._apply_status_damage(self.active_fish, "burned", 0.03, "burn")

        if self.active_enemy:
            self._apply_status_damage(self.active_enemy, "poisoned", 0.05, "poison")
            self._apply_status_damage(self.active_enemy, "burned", 0.03, "burn")

        self._tick_temporary_effects()

    def _tick_temporary_effects(self):
        for fish in self.player.active_party:
            fish.tick_temporary_effects()
        for enemy in self.enemies:
            enemy.tick_temporary_effects()

    def _apply_status_damage(self, target: Any, status: str,
                             max_hp_ratio: float, label: str):
        if "invincible" in target.status_effects:
            return
        if status not in target.status_effects:
            return
        damage = max(1, int(target.max_hp * max_hp_ratio))
        target.current_hp = max(0, target.current_hp - damage)
        self.log.add(f"{target.name} took {damage} {label} damage!")

    def get_battle_state(self) -> Dict[str, Any]:
        """
        Get current battle state for UI display.

        This method packages all battle info needed by the UI into
        one dictionary. The UI calls this every frame to render
        the battle screen.

        Returns:
            Dictionary containing all battle state:
            - turn: Current turn number
            - result: Battle result (ONGOING, VICTORY, DEFEAT, FLED)
            - active_fish: Player's current fish (Fish object)
            - active_enemy: Current enemy (Enemy object)
            - all_enemies: List of all enemies (for multi-enemy battles)
            - recent_log: Last 5 battle messages for text scroll
            - miracle_meter: Jesus's miracle meter (0-100)
            - can_flee: Whether fleeing is allowed (False for bosses)
            - apostle_used: Whether apostle was used this battle

        Example:
            state = battle.get_battle_state()
            ui.render_battle_screen(state)
            # UI can access state["active_fish"].current_hp, etc.

        Note:
            Returns object references, not copies.
            UI should NOT modify returned objects (read-only).
        """
        return {
            "turn": self.turn_count,              # Turn number (1, 2, 3, ...)
            "result": self.result,                # BattleResult enum
            "active_fish": self.active_fish,      # Current player fish
            "active_enemy": self.active_enemy,    # Current enemy
            "all_enemies": self.enemies,          # All remaining enemies
            "recent_log": self.log.get_recent(5), # Last 5 messages
            "miracle_meter": self.player.miracle_meter,  # 0-100
            "can_flee": self.can_flee,            # Can player flee?
            "apostle_used": self.apostle_used     # Apostle used yet?
        }
