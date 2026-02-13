extends Node
class_name DataLoader

# Singleton for loading all game data from JSON.

var fish_data: Array = []
var enemies_data: Array = []
var bosses_data: Array = []
var quests_data: Array = []
var apostles_data: Array = []
var items_data: Array = []
var equipment_data: Dictionary = {}
var parables_data: Array = []
var towns_data: Array = []
var messages_data: Dictionary = {}
var miracles_data: Array = []
var ui_strings_data: Dictionary = {}

func _ready() -> void:
	load_all_data()

func load_all_data() -> void:
	var fish_json = _load_json("res://data/fish.json")
	fish_data = fish_json.get("fish", [])

	var enemies_json = _load_json("res://data/enemies.json")
	enemies_data = enemies_json.get("enemies", [])

	var bosses_json = _load_json("res://data/bosses.json")
	bosses_data = bosses_json.get("bosses", [])

	var quests_json = _load_json("res://data/quests.json")
	quests_data = quests_json.get("quests", [])

	var apostles_json = _load_json("res://data/apostles.json")
	apostles_data = apostles_json.get("apostles", [])

	var items_json = _load_json("res://data/items.json")
	items_data = items_json.get("bread_items", [])
	equipment_data = items_json.get("equipment", {})

	var parables_json = _load_json("res://data/parables.json")
	parables_data = parables_json.get("parables", [])

	var towns_json = _load_json("res://data/towns.json")
	towns_data = towns_json.get("towns", [])

	messages_data = _load_json("res://data/messages.json")

	var miracles_json = _load_json("res://data/miracles.json")
	miracles_data = miracles_json.get("miracles", [])

	ui_strings_data = _load_json("res://data/ui_strings.json")

func _load_json(path: String) -> Variant:
	var content = FileAccess.get_file_as_string(path)
	if content == "":
		push_error("Failed to read JSON: " + path)
		return {}
	var parsed = JSON.parse_string(content)
	if parsed == null:
		push_error("Failed to parse JSON: " + path)
		return {}
	return parsed

func _find_by_id(items: Array, item_id: String) -> Dictionary:
	for item in items:
		if item.get("id", "") == item_id:
			return item
	return {}

func get_all_fish() -> Array:
	return fish_data

func get_fish_by_id(fish_id: String) -> Dictionary:
	return _find_by_id(fish_data, fish_id)

func get_all_enemies() -> Array:
	return enemies_data

func get_enemy_by_id(enemy_id: String) -> Dictionary:
	return _find_by_id(enemies_data, enemy_id)

func get_all_bosses() -> Array:
	return bosses_data

func get_boss_by_id(boss_id: String) -> Dictionary:
	return _find_by_id(bosses_data, boss_id)

func get_all_quests() -> Array:
	return quests_data

func get_quest_by_id(quest_id: String) -> Dictionary:
	return _find_by_id(quests_data, quest_id)

func get_all_apostles() -> Array:
	return apostles_data

func get_apostle_by_id(apostle_id: String) -> Dictionary:
	return _find_by_id(apostles_data, apostle_id)

func get_all_items() -> Array:
	return items_data

func get_item_by_id(item_id: String) -> Dictionary:
	return _find_by_id(items_data, item_id)

func get_equipment() -> Dictionary:
	return equipment_data

func get_all_parables() -> Array:
	return parables_data

func get_parable_by_id(parable_id: String) -> Dictionary:
	return _find_by_id(parables_data, parable_id)

func get_all_towns() -> Array:
	return towns_data

func get_town_by_id(town_id: String) -> Dictionary:
	return _find_by_id(towns_data, town_id)

func get_all_miracles() -> Array:
	return miracles_data

func get_miracle_by_id(miracle_id: String) -> Dictionary:
	return _find_by_id(miracles_data, miracle_id)

func get_message(key: String) -> String:
	if messages_data.has(key):
		return str(messages_data[key])
	return ""

func get_ui_string(key: String) -> String:
	if ui_strings_data.has(key):
		return str(ui_strings_data[key])
	return ""
