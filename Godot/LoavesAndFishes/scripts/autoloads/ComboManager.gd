# Godot 4.3 - GDScript
extends Node

class ComboAttack:
	var combo_id: String
	var name: String
	var fish_id: String
	var apostle_id: String
	var description: String
	var power: int
	var attack_type: String
	var special_effect: String
	var miracle_meter_cost: int = 25

	func _init(
		id: String,
		c_name: String,
		f_id: String,
		a_id: String,
		desc: String,
		pwr: int,
		type: String = "Holy",
		effect: String = ""
	) -> void:
		combo_id = id
		name = c_name
		fish_id = f_id
		apostle_id = a_id
		description = desc
		power = pwr
		attack_type = type
		special_effect = effect

	func can_perform(
		fish: Fish,
		apostle_recruited: bool,
		miracle_meter: float
	) -> bool:
		if not apostle_recruited:
			return false
		if fish.fish_id != fish_id:
			return false
		if miracle_meter < miracle_meter_cost:
			return false
		if fish.current_hp <= 0:
			return false
		return true

var combo_attacks: Dictionary = {}
var discovered_combos: Array[String] = []

func _ready() -> void:
	_init_combos()

func _init_combos() -> void:
	combo_attacks = {
		"revelation_smack": ComboAttack.new(
			"revelation_smack",
			"Revelation Smack",
			"holy_mackerel",
			"john",
			"The beloved disciple and the holy fish unite! 200 Holy damage + blind all enemies.",
			200,
			"Holy",
			"blind_all"
		),
		"rock_solid_defense": ComboAttack.new(
			"rock_solid_defense",
			"Rock Solid Defense",
			"stone_loach",
			"peter",
			"Unmovable as a rock! Grants party +100% DEF for 3 turns.",
			0,
			"Support",
			"def_boost_party"
		),
		"thunder_pike": ComboAttack.new(
			"thunder_pike",
			"Thunder Pike",
			"thunder_pike",
			"james",
			"Sons of Thunder unite! 250 Holy damage to all enemies + paralyze chance.",
			250,
			"Holy",
			"paralyze_chance"
		),
		"fishers_fortune": ComboAttack.new(
			"fishers_fortune",
			"Fisher's Fortune",
			"carp_diem",
			"andrew",
			"The first fish and first called! Doubles money earned from this battle.",
			100,
			"Normal",
			"double_money"
		),
		"multiplication_feast": ComboAttack.new(
			"multiplication_feast",
			"Multiplication Feast",
			"salmon_of_wisdom",
			"philip",
			"Where shall we buy bread? Multiplies healing effects by 3 for 3 turns.",
			0,
			"Support",
			"triple_healing"
		),
		"true_sight_strike": ComboAttack.new(
			"true_sight_strike",
			"True Sight Strike",
			"angler_of_light",
			"bartholomew",
			"Light reveals all! 180 damage + reveals all enemy weaknesses permanently.",
			180,
			"Holy",
			"reveal_weaknesses"
		),
		"tax_evasion": ComboAttack.new(
			"tax_evasion",
			"Tax Evasion",
			"red_herring",
			"matthew",
			"Render unto Caesar! Steals 500 denarii + confuses all enemies.",
			150,
			"Dark",
			"steal_money_confuse"
		),
		"doubting_combo": ComboAttack.new(
			"doubting_combo",
			"My Lord and My Cod",
			"cod_save_the_king",
			"thomas",
			"I believe! Critical hit (guaranteed) + 300 damage.",
			300,
			"Holy",
			"guaranteed_crit"
		),
		"healing_waters": ComboAttack.new(
			"healing_waters",
			"Healing Waters",
			"betta_together",
			"james_alphaeus",
			"Better together! Heals party for 150 HP + cures all status effects.",
			150,
			"Water",
			"heal_cure_party"
		),
		"righteous_fury": ComboAttack.new(
			"righteous_fury",
			"Righteous Fury",
			"swordfish",
			"thaddaeus",
			"Strike with righteous anger! 280 damage + party ATK boost.",
			280,
			"Physical",
			"party_atk_boost"
		),
		"zealous_revolution": ComboAttack.new(
			"zealous_revolution",
			"Zealous Revolution",
			"fishers_of_men_haden",
			"simon_zealot",
			"Revolutionary power! 220 damage to all + boosts party SPD by 50%.",
			220,
			"Earth",
			"party_spd_boost"
		),
		"betrayers_silver": ComboAttack.new(
			"betrayers_silver",
			"Thirty Pieces of Silver",
			"grouper_therapy",
			"judas",
			"The price of betrayal... Sacrifice fish for 1000 denarii + massive party boost.",
			0,
			"Dark",
			"sacrifice_for_power"
		),
		"divine_ichthys": ComboAttack.new(
			"divine_ichthys",
			"Divine Ichthys",
			"ichthys_divine",
			"john",
			"The ultimate miracle! 500 Holy damage to all + fully heal party.",
			500,
			"Holy",
			"damage_and_heal"
		)
	}

func discover_combo(combo_id: String) -> void:
	if not discovered_combos.has(combo_id) and combo_attacks.has(combo_id):
		discovered_combos.append(combo_id)

func is_discovered(combo_id: String) -> bool:
	return discovered_combos.has(combo_id)

func get_available_combos(
	fish: Fish,
	recruited_apostles: Array[String],
	miracle_meter: float
) -> Array[ComboAttack]:
	var available: Array[ComboAttack] = []
	if fish == null:
		return available

	for combo in combo_attacks.values():
		if combo.fish_id != fish.fish_id:
			continue
		if not recruited_apostles.has(combo.apostle_id):
			continue
		if miracle_meter < combo.miracle_meter_cost:
			continue
		if combo.can_perform(fish, true, miracle_meter):
			available.append(combo)
			if not is_discovered(combo.combo_id):
				discover_combo(combo.combo_id)

	return available

func perform_combo(combo_id: String) -> ComboAttack:
	if combo_attacks.has(combo_id):
		return combo_attacks[combo_id]
	return null
