class_name Fish
extends Resource

@export var fish_id: String = ""
@export var fish_name: String = ""
@export var tier: int = 0
@export var fish_type: String = ""
@export var level: int = 1
@export var xp: int = 0
@export var xp_to_next_level: int = 100

@export var base_hp: int = 0
@export var base_atk: int = 0
@export var base_def: int = 0
@export var base_spd: int = 0

@export var max_hp: int = 0
@export var current_hp: int = 0
@export var atk: int = 0
@export var defense: int = 0
@export var spd: int = 0

@export var property: Dictionary = {}
@export var all_moves: Array = []
@export var known_moves: Array = []
@export var held_item: Dictionary = {}
@export var status_effects: Array = []
@export var combo_attack: Variant
@export var flavor_text: Dictionary = {}

var stat_modifiers: Dictionary = {
	"atk": 1.0,
	"def": 1.0,
	"spd": 1.0,
	"accuracy": 1.0,
	"evasion": 1.0
}

func _init(fish_id_param: String = "", fish_data: Dictionary = {}, level_param: int = 1) -> void:
	if fish_id_param == "" or fish_data.is_empty():
		return

	fish_id = fish_id_param
	fish_name = str(fish_data.get("name", ""))
	tier = int(fish_data.get("tier", 0))
	fish_type = str(fish_data.get("type", ""))
	level = int(level_param)

	var base_stats = fish_data.get("base_stats", {})
	base_hp = int(base_stats.get("hp", 0))
	base_atk = int(base_stats.get("atk", 0))
	base_def = int(base_stats.get("def", 0))
	base_spd = int(base_stats.get("spd", 0))

	max_hp = _calculate_stat(base_hp, level)
	current_hp = max_hp
	atk = _calculate_stat(base_atk, level)
	defense = _calculate_stat(base_def, level)
	spd = _calculate_stat(base_spd, level)

	property = fish_data.get("property", {})
	all_moves = fish_data.get("moves", [])
	known_moves = _get_available_moves()
	combo_attack = fish_data.get("combo_attack", null)
	flavor_text = fish_data.get("flavor_text", {})

func _calculate_stat(base_stat: int, level_value: int) -> int:
	var growth_rate := 0.07
	return int(base_stat * (1.0 + growth_rate * (level_value - 1)))

func _get_available_moves() -> Array:
	var available: Array = []
	for move in all_moves:
		if int(move.get("level", 0)) <= level:
			available.append(move)
	return available

func gain_xp(amount: int) -> bool:
	var final_amount = amount
	if property.get("effect", "") == "xp_boost":
		final_amount = int(amount * float(property.get("value", 1.0)))

	xp += final_amount
	if xp >= xp_to_next_level:
		return level_up()
	return false

func level_up() -> bool:
	if level >= 50:
		return false

	level += 1
	xp -= xp_to_next_level

	var old_max_hp = max_hp
	max_hp = _calculate_stat(base_hp, level)
	current_hp += (max_hp - old_max_hp)

	atk = _calculate_stat(base_atk, level)
	defense = _calculate_stat(base_def, level)
	spd = _calculate_stat(base_spd, level)

	for move in all_moves:
		if int(move.get("level", 0)) == level and not known_moves.has(move):
			known_moves.append(move)

	return true

func take_damage(damage: int) -> int:
	var defense_mult = float(stat_modifiers.get("def", 1.0))
	var effective_defense = defense * defense_mult
	var damage_multiplier = 100.0 / (100.0 + effective_defense)
	var actual_damage = int(damage * damage_multiplier)
	actual_damage = max(1, actual_damage)
	current_hp = max(0, current_hp - actual_damage)
	return actual_damage

func heal(amount: int) -> int:
	var old_hp = current_hp
	current_hp = min(max_hp, current_hp + amount)
	return current_hp - old_hp

func is_fainted() -> bool:
	return current_hp <= 0

func revive(hp_percent: float = 0.5) -> void:
	if is_fainted():
		current_hp = int(max_hp * hp_percent)

func apply_status_effect(status: String) -> void:
	if not status_effects.has(status):
		status_effects.append(status)

func remove_status_effect(status: String) -> void:
	if status_effects.has(status):
		status_effects.erase(status)

func clear_status_effects() -> void:
	status_effects.clear()

func apply_stat_modifier(stat: String, multiplier: float) -> void:
	if stat_modifiers.has(stat):
		stat_modifiers[stat] = float(stat_modifiers[stat]) * multiplier

func reset_stat_modifiers() -> void:
	for stat in stat_modifiers.keys():
		stat_modifiers[stat] = 1.0

func get_effective_stat(stat: String) -> int:
	var base_value = 0
	match stat:
		"atk":
			base_value = atk
		"def":
			base_value = defense
		"spd":
			base_value = spd
		_:
			base_value = 0

	if held_item is Dictionary:
		var bonus_key = stat + "_bonus"
		if held_item.has(bonus_key):
			base_value += int(held_item[bonus_key])

	var modifier = float(stat_modifiers.get(stat, 1.0))
	return int(base_value * modifier)

func to_dict() -> Dictionary:
	return {
		"fish_id": fish_id,
		"level": level,
		"xp": xp,
		"current_hp": current_hp,
		"held_item": held_item,
		"status_effects": status_effects
	}

static func from_dict(data: Dictionary) -> Fish:
	var fish_id_value = str(data.get("fish_id", ""))
	if fish_id_value == "":
		return null

	var fish_data = DataLoader.get_fish_by_id(fish_id_value)
	if fish_data.is_empty():
		return null

	var fish = Fish.new(fish_id_value, fish_data, int(data.get("level", 1)))
	fish.xp = int(data.get("xp", 0))
	fish.current_hp = int(data.get("current_hp", fish.max_hp))
	fish.held_item = data.get("held_item", null)
	fish.status_effects = data.get("status_effects", [])
	return fish
