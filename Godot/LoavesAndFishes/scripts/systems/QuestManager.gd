extends Node
class_name QuestManager

signal quest_objective_updated(quest_id: String, objective_index: int)

var quest_progress: Dictionary = {}

func get_quest_details(quest_id: String) -> Dictionary:
	var quest = DataLoader.get_quest_by_id(quest_id)
	if quest.is_empty():
		return {}

	var details = quest.duplicate(true)
	var objectives = details.get("objectives", [])
	details["progress"] = _get_progress_array(quest_id, objectives)
	return details

func check_quest_requirements(quest_id: String) -> bool:
	var quest = DataLoader.get_quest_by_id(quest_id)
	if quest.is_empty():
		return false

	var objectives: Array = quest.get("objectives", [])
	if objectives.is_empty():
		return true

	var progress = _get_progress_array(quest_id, objectives)
	for i in range(objectives.size()):
		var objective: Dictionary = objectives[i]
		var required = _get_objective_required(objective)
		var derived = _get_objective_progress_from_state(objective)
		var current = max(int(progress[i]), derived)
		if current < required:
			return false
	return true

func advance_quest(quest_id: String) -> void:
	if not GameState.active_quests.has(quest_id):
		return

	var quest = DataLoader.get_quest_by_id(quest_id)
	if quest.is_empty():
		return

	var objectives: Array = quest.get("objectives", [])
	if objectives.is_empty():
		return

	var progress = _get_progress_array(quest_id, objectives)
	var incremented = false
	var updated = false

	for i in range(objectives.size()):
		var objective: Dictionary = objectives[i]
		var required = _get_objective_required(objective)
		var derived = _get_objective_progress_from_state(objective)
		var current = int(progress[i])
		var next = max(current, derived)

		if next < required and not incremented and derived <= current:
			next = min(required, current + 1)
			incremented = true

		if next != current:
			progress[i] = next
			updated = true
			quest_objective_updated.emit(quest_id, i)

	if updated:
		quest_progress[quest_id] = progress

func _get_progress_array(quest_id: String, objectives: Array) -> Array:
	var progress: Array = quest_progress.get(quest_id, [])
	if progress.size() != objectives.size():
		progress = []
		for i in range(objectives.size()):
			progress.append(0)
		quest_progress[quest_id] = progress
	return progress

func _get_objective_required(objective: Dictionary) -> int:
	if objective.has("count"):
		return int(objective.get("count", 1))
	if objective.has("amount"):
		return int(objective.get("amount", 1))
	return 1

func _get_objective_progress_from_state(objective: Dictionary) -> int:
	var objective_type = str(objective.get("type", ""))
	var target = str(objective.get("target", ""))
	var player = GameState.player

	match objective_type:
		"catch_fish":
			return _get_catch_fish_progress(player, target)
		"show_fish_types":
			return _get_unique_fish_types(player)
		"defeat_enemy":
			return _get_story_flag_int("defeated_enemy_" + target)
		"use_items":
			return _get_story_flag_int("used_items_" + target)
		"donate_money":
			return _get_story_flag_int("donated_money")
		"search_locations":
			return _get_story_flag_int("locations_searched")
		"complete_quests":
			return GameState.completed_quests.size()
		_:
			return 0

func _get_catch_fish_progress(player, target: String) -> int:
	if target == "any" or target == "":
		var total_fish = _get_total_fish_count(player)
		return max(int(GameState.fish_caught), total_fish)

	return _count_fish_by_id(player, target)

func _get_total_fish_count(player) -> int:
	if player == null:
		return 0
	return int(player.active_party.size() + player.fish_storage.size())

func _count_fish_by_id(player, fish_id: String) -> int:
	if player == null:
		return 0

	var count = 0
	for fish in player.active_party:
		if fish and fish.fish_id == fish_id:
			count += 1
	for fish in player.fish_storage:
		if fish and fish.fish_id == fish_id:
			count += 1
	return count

func _get_unique_fish_types(player) -> int:
	if player == null:
		return 0

	var types: Dictionary = {}
	for fish in player.active_party:
		if fish:
			types[fish.fish_type] = true
	for fish in player.fish_storage:
		if fish:
			types[fish.fish_type] = true
	return types.keys().size()

func _get_story_flag_int(flag: String) -> int:
	var value = GameState.story_flags.get(flag, 0)
	if value is int:
		return value
	if value is float:
		return int(value)
	return 0
