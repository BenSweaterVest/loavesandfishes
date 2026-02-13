class_name ApostleManager
extends Node

enum AbilityType { DAMAGE, HEAL, BUFF, DEBUFF, SUPPORT, SUMMON }

class ApostleAbility:
	var ability_id: String
	var name: String
	var apostle: String
	var ability_type: int
	var description: String
	var power: int
	var targets: String
	var cooldown: int
	var current_cooldown: int = 0
	var effects: Dictionary = {}

	func _init(
		ability_id_value: String,
		name_value: String,
		apostle_value: String,
		ability_type_value: int,
		description_value: String,
		power_value: int = 0,
		targets_value: String = "single",
		cooldown_value: int = 3
	) -> void:
		ability_id = ability_id_value
		name = name_value
		apostle = apostle_value
		ability_type = ability_type_value
		description = description_value
		power = power_value
		targets = targets_value
		cooldown = cooldown_value

	func use() -> bool:
		if is_ready():
			current_cooldown = cooldown
			return true
		return false

	func is_ready() -> bool:
		return current_cooldown == 0

	func tick_cooldown() -> void:
		if current_cooldown > 0:
			current_cooldown -= 1

	func reset_cooldown() -> void:
		current_cooldown = 0

var apostle_abilities: Dictionary = {
	"peter": ApostleAbility.new(
		"rock_foundation",
		"Rock Foundation",
		"Peter",
		AbilityType.BUFF,
		"Upon this rock I will build my church! Grants +50% DEF to all party fish for 3 turns.",
		50,
		"party",
		4
	),
	"andrew": ApostleAbility.new(
		"fishers_net",
		"Fisher's Net",
		"Andrew",
		AbilityType.SUPPORT,
		"Catches all fleeing enemies in a miraculous net. Prevents enemy from fleeing for 3 turns.",
		0,
		"all_enemies",
		3
	),
	"james": ApostleAbility.new(
		"sons_of_thunder",
		"Sons of Thunder",
		"James",
		AbilityType.DAMAGE,
		"Thunder strikes from heaven! Deals 150 Holy damage to all enemies.",
		150,
		"all_enemies",
		5
	),
	"john": ApostleAbility.new(
		"beloved_healing",
		"Beloved's Healing",
		"John",
		AbilityType.HEAL,
		"The disciple Jesus loved brings divine healing. Restores 100 HP to all party fish.",
		100,
		"party",
		4
	),
	"philip": ApostleAbility.new(
		"multiplication",
		"Bread Multiplication",
		"Philip",
		AbilityType.SUPPORT,
		"Where shall we buy bread? Multiplies one bread item to affect all party fish.",
		0,
		"party",
		5
	),
	"bartholomew": ApostleAbility.new(
		"true_sight",
		"True Sight",
		"Bartholomew",
		AbilityType.SUPPORT,
		"An Israelite in whom there is no deceit! Reveals enemy HP and weaknesses.",
		0,
		"all_enemies",
		3
	),
	"matthew": ApostleAbility.new(
		"tax_audit",
		"Tax Audit",
		"Matthew",
		AbilityType.DEBUFF,
		"Former tax collector's skill. Steals 100 denarii from enemies and lowers ATK by 30%.",
		30,
		"all_enemies",
		4
	),
	"thomas": ApostleAbility.new(
		"doubting_strike",
		"Doubting Strike",
		"Thomas",
		AbilityType.DAMAGE,
		"My Lord and my God! Deals massive damage (200) but only if enemy is below 50% HP.",
		200,
		"single",
		3
	),
	"james_alphaeus": ApostleAbility.new(
		"lesser_miracle",
		"Lesser Miracle",
		"James (son of Alphaeus)",
		AbilityType.HEAL,
		"The lesser-known apostle performs a humble miracle. Restores 50 HP and cures status.",
		50,
		"party",
		3
	),
	"thaddaeus": ApostleAbility.new(
		"righteous_zeal",
		"Righteous Zeal",
		"Thaddaeus",
		AbilityType.BUFF,
		"Grants +40% ATK and +40% SPD to one fish for 3 turns.",
		40,
		"single",
		4
	),
	"simon_zealot": ApostleAbility.new(
		"revolutionary_fervor",
		"Revolutionary Fervor",
		"Simon the Zealot",
		AbilityType.DAMAGE,
		"Zealous strike! Deals damage equal to 50% of your current HP to all enemies.",
		50,
		"all_enemies",
		5
	),
	"judas": ApostleAbility.new(
		"thirty_silver",
		"Thirty Silver",
		"Judas Iscariot",
		AbilityType.SUPPORT,
		"Betrayal for silver. Sacrifice one fish for 300 denarii and boost party ATK for 3 turns.",
		50,
		"party",
		6
	)
}

var recruited_apostles: Array[String] = []
var abilities: Dictionary = {}

func recruit_apostle(apostle_id: String) -> void:
	if not recruited_apostles.has(apostle_id):
		recruited_apostles.append(apostle_id)
		if apostle_abilities.has(apostle_id):
			abilities[apostle_id] = apostle_abilities[apostle_id]

func has_apostle(apostle_id: String) -> bool:
	return recruited_apostles.has(apostle_id)

func get_ability(apostle_id: String) -> ApostleAbility:
	if abilities.has(apostle_id):
		return abilities[apostle_id]
	return null

func get_available_abilities() -> Array:
	var available: Array = []
	for ability in abilities.values():
		if ability.is_ready():
			available.append(ability)
	return available

func tick_all_cooldowns() -> void:
	for ability in abilities.values():
		ability.tick_cooldown()

func reset_all_cooldowns() -> void:
	for ability in abilities.values():
		ability.reset_cooldown()

func use_ability(apostle_id: String) -> ApostleAbility:
	var ability = get_ability(apostle_id)
	if ability and ability.use():
		return ability
	return null

func execute_overworld_ability(apostle_id: String) -> bool:
	return has_apostle(apostle_id)

func execute_battle_ability(apostle_id: String, _context: Dictionary = {}) -> bool:
	return use_ability(apostle_id) != null
