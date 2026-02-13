class_name SaveSystem
extends Node

const SAVE_DIR = "user://saves/"
const MAX_SLOTS = 5
const SAVE_VERSION = "1.0"

func _ready() -> void:
	if not DirAccess.dir_exists_absolute(SAVE_DIR):
		DirAccess.make_dir_absolute(SAVE_DIR)

func _get_save_path(slot: int) -> String:
	return SAVE_DIR + "save_slot_" + str(slot) + ".json"

func save_game(slot: int, save_name: String = "") -> bool:
	if slot < 1 or slot > MAX_SLOTS:
		push_error("Invalid save slot: %s" % str(slot))
		return false

	var player_data: Dictionary = {}
	if GameState.player and GameState.player.has_method("to_dict"):
		player_data = GameState.player.to_dict()

	var save_data: Dictionary = {
		"version": SAVE_VERSION,
		"slot": slot,
		"save_name": save_name if save_name != "" else "Save " + str(slot),
		"timestamp": Time.get_datetime_string_from_system(),
		"playtime": float(GameState.playtime),
		"game_state": GameState.to_dict(),
		"player_data": player_data
	}

	var save_path = _get_save_path(slot)
	var file = FileAccess.open(save_path, FileAccess.WRITE)
	if file == null:
		push_error("Failed to open save file: " + save_path)
		return false

	file.store_string(JSON.stringify(save_data, "\t"))
	file.close()
	return true

func load_game(slot: int) -> bool:
	if slot < 1 or slot > MAX_SLOTS:
		push_error("Invalid save slot: %s" % str(slot))
		return false

	var save_path = _get_save_path(slot)
	if not FileAccess.file_exists(save_path):
		return false

	var content = FileAccess.get_file_as_string(save_path)
	if content == "":
		push_error("Save file is empty: " + save_path)
		return false

	var parsed = JSON.parse_string(content)
	if parsed == null or not (parsed is Dictionary):
		push_error("Failed to parse save file: " + save_path)
		return false

	var save_data: Dictionary = parsed
	var game_state_data = save_data.get("game_state", {})
	if game_state_data is Dictionary:
		GameState.from_dict(game_state_data)

	var player_data = save_data.get("player_data", {})
	if player_data is Dictionary and not player_data.is_empty():
		GameState.player = Player.from_dict(player_data)

	return true

func get_save_info(slot: int) -> Dictionary:
	var save_path = _get_save_path(slot)
	if not FileAccess.file_exists(save_path):
		return {}

	var content = FileAccess.get_file_as_string(save_path)
	if content == "":
		return {}

	var parsed = JSON.parse_string(content)
	if parsed == null or not (parsed is Dictionary):
		return {}

	var save_data: Dictionary = parsed
	var player_data: Dictionary = save_data.get("player_data", {})
	var party_size = 0
	if player_data.has("active_party") and player_data["active_party"] is Array:
		party_size = int(player_data["active_party"].size())

	return {
		"slot": slot,
		"save_name": save_data.get("save_name", "Save " + str(slot)),
		"timestamp": save_data.get("timestamp", ""),
		"playtime": save_data.get("playtime", 0.0),
		"player_name": player_data.get("name", "Unknown"),
		"player_level": player_data.get("level", 1),
		"location": player_data.get("current_town", "Unknown"),
		"party_size": party_size,
		"money": player_data.get("money", 0)
	}
