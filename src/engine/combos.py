"""
Combo Attack System - Fish + Apostle combination attacks
"""

from typing import Dict, Any, Optional, List


class ComboAttack:
    """A combination attack between a fish and apostle"""

    def __init__(self,
                 combo_id: str,
                 name: str,
                 fish_id: str,
                 apostle_id: str,
                 description: str,
                 power: int,
                 attack_type: str = "Holy",
                 special_effect: Optional[str] = None):
        """
        Initialize combo attack

        Args:
            combo_id: Unique identifier
            name: Combo name
            fish_id: Required fish
            apostle_id: Required apostle
            description: Attack description
            power: Base power
            attack_type: Damage type
            special_effect: Special effect ID
        """
        self.combo_id = combo_id
        self.name = name
        self.fish_id = fish_id
        self.apostle_id = apostle_id
        self.description = description
        self.power = power
        self.attack_type = attack_type
        self.special_effect = special_effect

        # Meter cost
        self.miracle_meter_cost = 25  # % of miracle meter required

    def can_perform(self, fish, apostle_recruited: bool, miracle_meter: int) -> bool:
        """
        Check if combo can be performed

        Args:
            fish: Fish instance
            apostle_recruited: Whether apostle is recruited
            miracle_meter: Current miracle meter

        Returns:
            True if combo is possible
        """
        if not apostle_recruited:
            return False

        if fish.fish_id != self.fish_id:
            return False

        if miracle_meter < self.miracle_meter_cost:
            return False

        # Fish must not be fainted
        if fish.is_fainted():
            return False

        return True


# Define combo attacks (these match the fish.json data)
COMBO_ATTACKS = {
    "revelation_smack": ComboAttack(
        "revelation_smack",
        "Revelation Smack",
        "holy_mackerel",
        "john",
        "The beloved disciple and the holy fish unite! 200 Holy damage + blind all enemies.",
        power=200,
        attack_type="Holy",
        special_effect="blind_all"
    ),

    "rock_solid_defense": ComboAttack(
        "rock_solid_defense",
        "Rock Solid Defense",
        "stone_loach",
        "peter",
        "Unmovable as a rock! Grants party +100% DEF for 3 turns.",
        power=0,
        attack_type="Support",
        special_effect="def_boost_party"
    ),

    "thunder_pike": ComboAttack(
        "thunder_pike",
        "Thunder Pike",
        "thunder_pike",
        "james",
        "Sons of Thunder unite! 250 Holy damage to all enemies + paralyze chance.",
        power=250,
        attack_type="Holy",
        special_effect="paralyze_chance"
    ),

    "fishers_fortune": ComboAttack(
        "fishers_fortune",
        "Fisher's Fortune",
        "carp_diem",
        "andrew",
        "The first fish and first called! Doubles money earned from this battle.",
        power=100,
        attack_type="Normal",
        special_effect="double_money"
    ),

    "multiplication_feast": ComboAttack(
        "multiplication_feast",
        "Multiplication Feast",
        "salmon_of_wisdom",
        "philip",
        "Where shall we buy bread? Multiplies healing effects by 3 for 3 turns.",
        power=0,
        attack_type="Support",
        special_effect="triple_healing"
    ),

    "true_sight_strike": ComboAttack(
        "true_sight_strike",
        "True Sight Strike",
        "angler_of_light",
        "bartholomew",
        "Light reveals all! 180 damage + reveals all enemy weaknesses permanently.",
        power=180,
        attack_type="Holy",
        special_effect="reveal_weaknesses"
    ),

    "tax_evasion": ComboAttack(
        "tax_evasion",
        "Tax Evasion",
        "red_herring",
        "matthew",
        "Render unto Caesar! Steals 500 denarii + confuses all enemies.",
        power=150,
        attack_type="Dark",
        special_effect="steal_money_confuse"
    ),

    "doubting_combo": ComboAttack(
        "doubting_combo",
        "My Lord and My Cod",
        "cod_save_the_king",
        "thomas",
        "I believe! Critical hit (guaranteed) + 300 damage.",
        power=300,
        attack_type="Holy",
        special_effect="guaranteed_crit"
    ),

    "healing_waters": ComboAttack(
        "healing_waters",
        "Healing Waters",
        "betta_together",
        "james_alphaeus",
        "Better together! Heals party for 150 HP + cures all status effects.",
        power=150,
        attack_type="Water",
        special_effect="heal_cure_party"
    ),

    "righteous_fury": ComboAttack(
        "righteous_fury",
        "Righteous Fury",
        "swordfish",
        "thaddaeus",
        "Strike with righteous anger! 280 damage + party ATK boost.",
        power=280,
        attack_type="Physical",
        special_effect="party_atk_boost"
    ),

    "zealous_revolution": ComboAttack(
        "zealous_revolution",
        "Zealous Revolution",
        "fishers_of_men_haden",
        "simon_zealot",
        "Revolutionary power! 220 damage to all + boosts party SPD by 50%.",
        power=220,
        attack_type="Earth",
        special_effect="party_spd_boost"
    ),

    "betrayers_silver": ComboAttack(
        "betrayers_silver",
        "Thirty Pieces of Silver",
        "grouper_therapy",
        "judas",
        "The price of betrayal... Sacrifice fish for 1000 denarii + massive party boost.",
        power=0,
        attack_type="Dark",
        special_effect="sacrifice_for_power"
    ),

    "divine_ichthys": ComboAttack(
        "divine_ichthys",
        "Divine Ichthys",
        "ichthys_divine",
        "john",
        "The ultimate miracle! 500 Holy damage to all + fully heal party.",
        power=500,
        attack_type="Holy",
        special_effect="damage_and_heal"
    )
}


class ComboManager:
    """Manages combo attacks"""

    def __init__(self):
        """Initialize combo manager"""
        self.discovered_combos: List[str] = []

    def discover_combo(self, combo_id: str):
        """Mark a combo as discovered"""
        if combo_id not in self.discovered_combos and combo_id in COMBO_ATTACKS:
            self.discovered_combos.append(combo_id)

    def is_discovered(self, combo_id: str) -> bool:
        """Check if combo has been discovered"""
        return combo_id in self.discovered_combos

    def get_available_combos(self, fish, recruited_apostles: List[str], miracle_meter: int) -> List[ComboAttack]:
        """
        Get all combos available for a fish

        Args:
            fish: Fish instance
            recruited_apostles: List of recruited apostle IDs
            miracle_meter: Current miracle meter

        Returns:
            List of available combo attacks
        """
        available = []

        for combo in COMBO_ATTACKS.values():
            # Check if combo uses this fish
            if combo.fish_id != fish.fish_id:
                continue

            # Check if apostle is recruited
            if combo.apostle_id not in recruited_apostles:
                continue

            # Check if enough miracle meter
            if miracle_meter < combo.miracle_meter_cost:
                continue

            # Check if fish can perform it
            if combo.can_perform(fish, True, miracle_meter):
                available.append(combo)

                # Auto-discover combos when they become available
                if not self.is_discovered(combo.combo_id):
                    self.discover_combo(combo.combo_id)

        return available

    def get_combo(self, combo_id: str) -> Optional[ComboAttack]:
        """Get a specific combo"""
        return COMBO_ATTACKS.get(combo_id)

    def perform_combo(self, combo_id: str) -> Optional[ComboAttack]:
        """
        Perform a combo attack

        Args:
            combo_id: Combo to perform

        Returns:
            ComboAttack if performed, None otherwise
        """
        return self.get_combo(combo_id)
