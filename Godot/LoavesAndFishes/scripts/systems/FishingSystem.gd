class_name FishingSystem
extends Node

signal fish_hooked(fish_id: String)
signal line_snapped
signal catch_successful(fish_data: Dictionary)

enum FishingDifficulty { EASY, MEDIUM, HARD, LEGENDARY }
enum FishingResult { CAUGHT, ESCAPED, NOTHING, ONGOING }

class FishingSpot:
	var spot_id: String
	var name: String
	var quality: int
	var available_fish: Array

	func _init(id: String, spot_name: String, spot_quality: int, fish_list: Array) -> void:
		spot_id = id
		name = spot_name
		quality = spot_quality
		available_fish = fish_list

	func start_fishing(system: FishingSystem) -> void:
		if system:
			system.start_fishing(quality, {}, {}, spot_id)

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

func start_fishing(
	spot_quality: int = 50,
	rod: Dictionary = {},
	bait: Dictionary = {},
	spot_id: String = ""
) -> void:
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
		current_fish = _generate_fish(spot_id)
		_set_difficulty(current_fish.get("difficulty", FishingDifficulty.EASY))
		fish_hooked.emit(str(current_fish.get("fish_id", "unknown")))
	else:
		current_fish = {}
		is_active = false

func update(reel_in: bool = false) -> FishingResult:
	if not is_active:
		return FishingResult.NOTHING

	if current_fish.is_empty():
		is_active = false
		return FishingResult.NOTHING

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
		return FishingResult.ESCAPED

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
		GameState.fish_caught += 1
		if QuestManager:
			for quest_id in GameState.active_quests:
				QuestManager.advance_quest(quest_id)
		return FishingResult.CAUGHT

	return FishingResult.ONGOING

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

func _generate_fish(spot_id: String) -> Dictionary:
	var roll = randf()
	var tier: Variant = 1
	var difficulty = FishingDifficulty.EASY

	if roll < 0.05:
		tier = "special"
		difficulty = FishingDifficulty.LEGENDARY
	elif roll < 0.15:
		tier = 3
		difficulty = FishingDifficulty.HARD
	elif roll < 0.40:
		tier = 2
		difficulty = FishingDifficulty.MEDIUM

	var available_ids: Array = _get_available_fish_ids(spot_id)
	var fish_entry = _pick_fish_by_tier(available_ids, tier)
	var fish_id = ""
	var fish_data: Dictionary = {}
	if not fish_entry.is_empty():
		fish_id = str(fish_entry.get("id", ""))
		fish_data = fish_entry

	return {
		"fish_id": fish_id,
		"fish_data": fish_data,
		"tier": tier,
		"difficulty": difficulty,
		"size": randi_range(1, 10),
		"caught": false
	}

func _get_available_fish_ids(spot_id: String) -> Array:
	if spot_id != "" and fishing_spots.has(spot_id):
		var spot: FishingSpot = fishing_spots[spot_id]
		return spot.available_fish
	return []

func _pick_fish_by_tier(available_ids: Array, tier: Variant) -> Dictionary:
	var all_fish = DataLoader.get_all_fish()
	if all_fish.is_empty():
		return {}

	var candidates: Array = []
	if available_ids.is_empty():
		candidates = all_fish
	else:
		for fish in all_fish:
			var fish_id = str(fish.get("id", ""))
			if available_ids.has(fish_id):
				candidates.append(fish)

	if candidates.is_empty():
		candidates = all_fish

	var tier_candidates: Array = []
	for fish in candidates:
		if _tier_matches(fish.get("tier", null), tier):
			tier_candidates.append(fish)

	var pool = tier_candidates if not tier_candidates.is_empty() else candidates
	return pool.pick_random()

func _tier_matches(fish_tier: Variant, desired_tier: Variant) -> bool:
	if fish_tier == null:
		return false
	if typeof(fish_tier) == TYPE_INT and typeof(desired_tier) == TYPE_INT:
		return int(fish_tier) == int(desired_tier)
	return str(fish_tier).to_lower() == str(desired_tier).to_lower()

func _set_difficulty(difficulty: int) -> void:
	match difficulty:
		FishingDifficulty.EASY:
			fish_speed = 3.0
			fish_change_direction_chance = 0.05
			tension_increase_rate = 1.0
		FishingDifficulty.MEDIUM:
			fish_speed = 5.0
			fish_change_direction_chance = 0.1
			tension_increase_rate = 2.0
		FishingDifficulty.HARD:
			fish_speed = 8.0
			fish_change_direction_chance = 0.15
			tension_increase_rate = 3.0
		_:
			fish_speed = 12.0
			fish_change_direction_chance = 0.2
			tension_increase_rate = 4.0

func get_display_bar() -> String:
	var bar_length = 50
	var fish_pos = int((fish_position / 100.0) * bar_length)
	var hook_pos = int((hook_position / 100.0) * bar_length)

	var bar: Array = []
	for index in range(bar_length):
		bar.append("-")

	if fish_pos >= 0 and fish_pos < bar_length:
		bar[fish_pos] = "F"

	if hook_pos >= 0 and hook_pos < bar_length:
		bar[hook_pos] = "X" if bar[hook_pos] == "F" else "H"

	var bar_str = "".join(bar)
	var tension_bar = "#".repeat(int((current_tension / 100.0) * 20))
	var progress_bar = "=".repeat(int((progress / 100.0) * 20))

	var display: Array = []
	display.append("|" + bar_str + "|")
	var tension_line = "Tension:  [" + tension_bar.ljust(20, " ") + "] "
	tension_line += str(int(current_tension)) + "%"
	var progress_line = "Progress: [" + progress_bar.ljust(20, " ") + "] "
	progress_line += str(int(progress)) + "%"
	display.append(tension_line)
	display.append(progress_line)

	if not current_fish.is_empty():
		var tier_text = str(current_fish.get("tier", "?"))
		var size_text = str(current_fish.get("size", "?"))
		display.append("Fish Tier: " + tier_text + " | Size: " + size_text + "/10")

	return "\n".join(display)

func upgrade_net(quality: float) -> void:
	net_quality = quality

func use_bait(quality: float) -> void:
	bait_quality = quality

var fishing_spots: Dictionary = {
	"sea_of_galilee": FishingSpot.new(
		"sea_of_galilee",
		"Sea of Galilee",
		80,
		["carp_diem", "holy_mackerel", "sole_survivor", "bass_ackwards", "tilapia"]
	),
	"jordan_river": FishingSpot.new(
		"jordan_river",
		"Jordan River",
		60,
		["carp_diem", "stone_loach", "eel_pray_for_you"]
	),
	"bethesda_pool": FishingSpot.new(
		"bethesda_pool",
		"Pool of Bethesda",
		70,
		["holy_mackerel", "salmon_of_wisdom", "betta_together"]
	),
	"miraculous_catch": FishingSpot.new(
		"miraculous_catch",
		"Miraculous Catch Site",
		100,
		["fishers_of_men_haden", "ichthys_divine", "leviathans_lament"]
	)
}
