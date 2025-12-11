"""
Apostle Abilities System - Special battle abilities for each apostle
"""

from typing import Dict, Any, Optional, List
from enum import Enum


class AbilityType(Enum):
    """Types of apostle abilities"""
    DAMAGE = "damage"
    HEAL = "heal"
    BUFF = "buff"
    DEBUFF = "debuff"
    SUPPORT = "support"
    SUMMON = "summon"


class ApostleAbility:
    """An apostle's special battle ability"""

    def __init__(self,
                 ability_id: str,
                 name: str,
                 apostle: str,
                 ability_type: AbilityType,
                 description: str,
                 power: int = 0,
                 targets: str = "single",  # single, all, party, self
                 cooldown: int = 3):
        """
        Initialize apostle ability

        Args:
            ability_id: Unique identifier
            name: Ability name
            apostle: Which apostle has this ability
            ability_type: Type of ability
            description: Description text
            power: Power value (damage, healing, etc.)
            targets: Targeting type
            cooldown: Turns between uses
        """
        self.ability_id = ability_id
        self.name = name
        self.apostle = apostle
        self.ability_type = ability_type
        self.description = description
        self.power = power
        self.targets = targets
        self.cooldown = cooldown
        self.current_cooldown = 0

        # Special effects
        self.effects: Dict[str, Any] = {}

    def use(self) -> bool:
        """
        Use the ability

        Returns:
            True if ability was used
        """
        if self.is_ready():
            self.current_cooldown = self.cooldown
            return True
        return False

    def is_ready(self) -> bool:
        """Check if ability is ready to use"""
        return self.current_cooldown == 0

    def tick_cooldown(self):
        """Reduce cooldown by 1"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def reset_cooldown(self):
        """Reset cooldown to 0"""
        self.current_cooldown = 0


# Define all 12 apostle abilities
APOSTLE_ABILITIES = {
    "peter": ApostleAbility(
        "rock_foundation",
        "Rock Foundation",
        "Peter",
        AbilityType.BUFF,
        "Upon this rock I will build my church! Grants +50% DEF to all party fish for 3 turns.",
        power=50,  # 50% DEF boost
        targets="party",
        cooldown=4
    ),

    "andrew": ApostleAbility(
        "fishers_net",
        "Fisher's Net",
        "Andrew",
        AbilityType.SUPPORT,
        "Catches all fleeing enemies in a miraculous net. Prevents enemy from fleeing for 3 turns.",
        targets="all_enemies",
        cooldown=3
    ),

    "james": ApostleAbility(
        "sons_of_thunder",
        "Sons of Thunder",
        "James",
        AbilityType.DAMAGE,
        "Thunder strikes from heaven! Deals 150 Holy damage to all enemies.",
        power=150,
        targets="all_enemies",
        cooldown=5
    ),

    "john": ApostleAbility(
        "beloved_healing",
        "Beloved's Healing",
        "John",
        AbilityType.HEAL,
        "The disciple Jesus loved brings divine healing. Restores 100 HP to all party fish.",
        power=100,
        targets="party",
        cooldown=4
    ),

    "philip": ApostleAbility(
        "multiplication",
        "Bread Multiplication",
        "Philip",
        AbilityType.SUPPORT,
        "Where shall we buy bread? Multiplies one bread item to affect all party fish.",
        targets="party",
        cooldown=5
    ),

    "bartholomew": ApostleAbility(
        "true_sight",
        "True Sight",
        "Bartholomew",
        AbilityType.SUPPORT,
        "An Israelite in whom there is no deceit! Reveals enemy HP and weaknesses.",
        targets="all_enemies",
        cooldown=3
    ),

    "matthew": ApostleAbility(
        "tax_audit",
        "Tax Audit",
        "Matthew",
        AbilityType.DEBUFF,
        "Former tax collector's skill. Steals 100 denarii from enemies and reduces their ATK by 30%.",
        power=30,  # 30% ATK reduction
        targets="all_enemies",
        cooldown=4
    ),

    "thomas": ApostleAbility(
        "doubting_strike",
        "Doubting Strike",
        "Thomas",
        AbilityType.DAMAGE,
        "My Lord and my God! Deals massive damage (200) but only if enemy is below 50% HP.",
        power=200,
        targets="single",
        cooldown=3
    ),

    "james_alphaeus": ApostleAbility(
        "lesser_miracle",
        "Lesser Miracle",
        "James (son of Alphaeus)",
        AbilityType.HEAL,
        "The lesser-known apostle performs a humble miracle. Restores 50 HP to all fish and cures status.",
        power=50,
        targets="party",
        cooldown=3
    ),

    "thaddaeus": ApostleAbility(
        "righteous_zeal",
        "Righteous Zeal",
        "Thaddaeus",
        AbilityType.BUFF,
        "Grants +40% ATK and +40% SPD to one fish for 3 turns.",
        power=40,
        targets="single",
        cooldown=4
    ),

    "simon_zealot": ApostleAbility(
        "revolutionary_fervor",
        "Revolutionary Fervor",
        "Simon the Zealot",
        AbilityType.DAMAGE,
        "Zealous strike! Deals damage equal to 50% of your current HP to all enemies.",
        power=50,  # % of current HP
        targets="all_enemies",
        cooldown=5
    ),

    "judas": ApostleAbility(
        "thirty_silver",
        "Thirty Silver",
        "Judas Iscariot",
        AbilityType.SUPPORT,
        "Betrayal for silver. Sacrifice one fish to gain 300 denarii and boost party ATK by 50% for 3 turns.",
        power=50,  # 50% ATK boost
        targets="party",
        cooldown=6
    )
}


class ApostleManager:
    """Manages apostle abilities in battle"""

    def __init__(self):
        """Initialize apostle manager"""
        self.recruited_apostles: List[str] = []
        self.abilities: Dict[str, ApostleAbility] = {}

    def recruit_apostle(self, apostle_id: str):
        """
        Recruit an apostle

        Args:
            apostle_id: Apostle to recruit
        """
        if apostle_id not in self.recruited_apostles:
            self.recruited_apostles.append(apostle_id)

            # Add their ability
            if apostle_id in APOSTLE_ABILITIES:
                self.abilities[apostle_id] = APOSTLE_ABILITIES[apostle_id]

    def has_apostle(self, apostle_id: str) -> bool:
        """Check if apostle is recruited"""
        return apostle_id in self.recruited_apostles

    def get_ability(self, apostle_id: str) -> Optional[ApostleAbility]:
        """Get an apostle's ability"""
        return self.abilities.get(apostle_id)

    def get_available_abilities(self) -> List[ApostleAbility]:
        """Get all abilities that are ready to use"""
        return [ability for ability in self.abilities.values() if ability.is_ready()]

    def tick_all_cooldowns(self):
        """Reduce all ability cooldowns"""
        for ability in self.abilities.values():
            ability.tick_cooldown()

    def reset_all_cooldowns(self):
        """Reset all ability cooldowns (for new battle)"""
        for ability in self.abilities.values():
            ability.reset_cooldown()

    def use_ability(self, apostle_id: str) -> Optional[ApostleAbility]:
        """
        Use an apostle's ability

        Args:
            apostle_id: Apostle whose ability to use

        Returns:
            The ability if used, None otherwise
        """
        ability = self.get_ability(apostle_id)
        if ability and ability.use():
            return ability
        return None
