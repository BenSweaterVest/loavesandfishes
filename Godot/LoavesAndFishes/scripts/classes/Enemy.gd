class_name Enemy
extends Resource

@export var enemy_id: String = ""
@export var enemy_name: String = ""
@export var enemy_type: String = ""
@export var level: int = 1

@export var max_hp: int = 0
@export var current_hp: int = 0
@export var atk: int = 0
@export var defense: int = 0
@export var spd: int = 0

@export var attacks: Array = []
@export var xp_reward: int = 0
@export var money_reward: int = 0
@export var item_drops: Array = []
@export var ai_pattern: String = "random"
@export var properties: Dictionary = {}

@export var status_effects: Array = []

var stat_modifiers: Dictionary = {
	"atk": 1.0,
	"def": 1.0,
	"spd": 1.0
}
var timed_stat_modifiers: Dictionary = {
	"atk": [],
	"def": [],
	"spd": []
}
var status_durations: Dictionary = {}

func _init(enemy_data: Dictionary = {}, level_param: int = 1) -> void:
	if enemy_data.is_empty():
		return

	enemy_id = str(enemy_data.get("id", ""))
	enemy_name = str(enemy_data.get("name", ""))
	enemy_type = str(enemy_data.get("type", ""))
	level = int(level_param)

	var base_stats = enemy_data.get("base_stats", {})
	max_hp = _scale_stat(int(base_stats.get("hp", 0)), level)
	current_hp = max_hp
	atk = _scale_stat(int(base_stats.get("atk", 0)), level)
	defense = _scale_stat(int(base_stats.get("def", 0)), level)
	spd = _scale_stat(int(base_stats.get("spd", 10)), level)

	attacks = enemy_data.get("attacks", [])
	xp_reward = int(enemy_data.get("xp_reward", level * 10 + 20))
	money_reward = int(enemy_data.get("money_reward", level * 5 + 10))
	item_drops = enemy_data.get("item_drops", [])
	ai_pattern = str(enemy_data.get("ai_pattern", "random"))
	properties = enemy_data.get("properties", {})

func _scale_stat(base_stat: int, level_value: int) -> int:
	var growth_rate := 0.05
	return int(base_stat * (1.0 + growth_rate * (level_value - 1)))

func choose_attack() -> Dictionary:
	if attacks.is_empty():
		return {
			"name": "Strike",
			"type": "Physical",
			"power": [atk / 2, atk],
			"accuracy": 100
		}

	if ai_pattern == "random":
		return attacks.pick_random()
	if ai_pattern == "strongest_first":
		var strongest = attacks[0]
		var strongest_power = 0
		for attack in attacks:
			var power = attack.get("power", [0, 0])
			var max_power = int(power[1]) if power is Array and power.size() > 1 else int(power)
			if max_power > strongest_power:
				strongest = attack
				strongest_power = max_power
		return strongest
	if ai_pattern == "cycle":
		return attacks.pick_random()
	return attacks.pick_random()

func take_damage(damage: int) -> int:
	var defense_mult = float(stat_modifiers.get("def", 1.0))
	var actual_damage = max(1, int(damage * (100.0 / (100.0 + defense * defense_mult))))
	current_hp = max(0, current_hp - actual_damage)
	return actual_damage

func heal(amount: int) -> int:
	var old_hp = current_hp
	current_hp = min(max_hp, current_hp + amount)
	return current_hp - old_hp

func is_defeated() -> bool:
	return current_hp <= 0

func apply_status_effect(status: String, turns: int = 0) -> void:
	if status != "immunity" and status_effects.has("immunity"):
		return
	if not status_effects.has(status):
		status_effects.append(status)
	if turns > 0:
		var remaining = int(status_durations.get(status, 0))
		status_durations[status] = max(remaining, turns)

func remove_status_effect(status: String) -> void:
	if status_effects.has(status):
		status_effects.erase(status)
	if status_durations.has(status):
		status_durations.erase(status)

func apply_stat_modifier(stat: String, multiplier: float, turns: int = 0) -> void:
	if stat_modifiers.has(stat):
		stat_modifiers[stat] = float(stat_modifiers[stat]) * multiplier
		if turns > 0 and timed_stat_modifiers.has(stat):
			timed_stat_modifiers[stat].append({
				"multiplier": multiplier,
				"turns": turns
			})

func reset_stat_modifiers() -> void:
	for stat in stat_modifiers.keys():
		stat_modifiers[stat] = 1.0
	for stat in timed_stat_modifiers.keys():
		timed_stat_modifiers[stat].clear()

func tick_temporary_effects() -> void:
	for stat in timed_stat_modifiers.keys():
		var entries: Array = timed_stat_modifiers[stat]
		if entries.is_empty():
			continue
		var remaining: Array = []
		for entry in entries:
			var turns_left = int(entry.get("turns", 0)) - 1
			if turns_left <= 0:
				var multiplier = float(entry.get("multiplier", 1.0))
				if multiplier != 0.0:
					stat_modifiers[stat] = float(stat_modifiers[stat]) / multiplier
			else:
				entry["turns"] = turns_left
				remaining.append(entry)
		timed_stat_modifiers[stat] = remaining

	if status_durations.is_empty():
		return
	var expired: Array[String] = []
	for status in status_durations.keys():
		var turns_left = int(status_durations.get(status, 0)) - 1
		if turns_left <= 0:
			expired.append(status)
		else:
			status_durations[status] = turns_left
	for status in expired:
		remove_status_effect(status)

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
	var modifier = float(stat_modifiers.get(stat, 1.0))
	return int(base_value * modifier)
