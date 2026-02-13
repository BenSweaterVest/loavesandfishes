class_name FishingSystem
extends Node

signal fish_hooked(fish_id: String)
signal line_snapped
signal catch_successful(fish_data: Dictionary)

var current_rod: Dictionary = {}
var current_tension: float = 0.0
var max_tension: float = 100.0

var fishing_spot_quality: int = 50
var is_active: bool = false
var current_fish: Dictionary = {}

var fish_position: float = 50.0
var hook_position: float = 50.0
var progress: float = 0.0

var fish_speed: float = 5.0
var fish_change_direction_chance: float = 0.1
var tension_increase_rate: float = 2.0
var tension_decrease_rate: float = 1.0
var progress_increase_rate: float = 3.0

var net_quality: float = 1.0
var bait_quality: float = 1.0

func start_fishing(spot_quality: int = 50, rod: Dictionary = {}, bait: Dictionary = {}) -> void:
	fishing_spot_quality = spot_quality
	current_rod = rod
	net_quality = float(current_rod.get("net_quality", 1.0))
	bait_quality = float(bait.get("bait_quality", 1.0))

	is_active = true
	current_fish = {}
	fish_position = 50.0
	hook_position = 50.0
	current_tension = 0.0
	progress = 0.0

	var bite_chance = float(fishing_spot_quality) / 100.0
	bite_chance *= bait_quality
	if randf() < bite_chance:
		current_fish = _generate_fish()
		_set_difficulty(current_fish.get("difficulty", "easy"))
		fish_hooked.emit(str(current_fish.get("fish_id", "unknown")))
	else:
		is_active = false

func update(reel_in: bool = false) -> String:
	if not is_active:
		return "nothing"

	if current_fish.is_empty():
		is_active = false
		return "nothing"

	if randf() < fish_change_direction_chance:
		fish_position += randf_range(-fish_speed, fish_speed)
	else:
		var direction = 1.0 if randf() < 0.5 else -1.0
		fish_position += fish_speed * direction

	fish_position = clamp(fish_position, 0.0, 100.0)

	var distance = abs(hook_position - fish_position)
	if distance > 20.0:
		current_tension += tension_increase_rate
	else:
		current_tension = max(0.0, current_tension - tension_decrease_rate)

	if current_tension >= max_tension:
		is_active = false
		line_snapped.emit()
		return "escaped"

	if reel_in:
		if hook_position < fish_position:
			hook_position += 3.0
		elif hook_position > fish_position:
			hook_position -= 3.0

		if distance < 10.0:
			progress += progress_increase_rate * net_quality
		elif distance < 20.0:
			progress += (progress_increase_rate / 2.0) * net_quality

	if progress >= 100.0:
		is_active = false
		current_fish["caught"] = true
		catch_successful.emit(current_fish)
		return "caught"

	return "ongoing"

func move_hook(direction: int) -> void:
	hook_position += float(direction) * 5.0
	hook_position = clamp(hook_position, 0.0, 100.0)

func get_state() -> Dictionary:
	return {
		"active": is_active,
		"fish_position": fish_position,
		"hook_position": hook_position,
		"tension": current_tension,
		"progress": progress,
		"fish_tier": current_fish.get("tier", null),
		"fish_size": current_fish.get("size", null)
	}

func _generate_fish() -> Dictionary:
	var roll = randf()
	var tier = 1
	var difficulty = "easy"

	if roll < 0.05:
		tier = 4
		difficulty = "legendary"
	elif roll < 0.15:
		tier = 3
		difficulty = "hard"
	elif roll < 0.40:
		tier = 2
		difficulty = "medium"

	return {
		"fish_id": "tier_%s" % str(tier),
		"tier": tier,
		"difficulty": difficulty,
		"size": randi_range(1, 10),
		"caught": false
	}

func _set_difficulty(difficulty: String) -> void:
	match difficulty:
		"easy":
			fish_speed = 3.0
			fish_change_direction_chance = 0.05
			tension_increase_rate = 1.0
		"medium":
			fish_speed = 5.0
			fish_change_direction_chance = 0.1
			tension_increase_rate = 2.0
		"hard":
			fish_speed = 8.0
			fish_change_direction_chance = 0.15
			tension_increase_rate = 3.0
		_:
			fish_speed = 12.0
			fish_change_direction_chance = 0.2
			tension_increase_rate = 4.0
