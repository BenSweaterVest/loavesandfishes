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
