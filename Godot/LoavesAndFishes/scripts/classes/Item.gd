class_name Item
extends Resource

@export var item_id: String = ""
@export var item_name: String = ""
@export var item_type: String = ""
@export var effect: String = ""
@export var power: int = 0
@export var cost: int = 0
@export var town: String = ""
@export var flavor_text: Dictionary = {}
@export var quick_item: bool = false

@export var raw_data: Dictionary = {}

func _init(item_id_param: String = "", item_data: Dictionary = {}) -> void:
	if item_id_param == "" or item_data.is_empty():
		return

	item_id = item_id_param
	item_name = str(item_data.get("name", ""))
	item_type = str(item_data.get("type", ""))
	effect = str(item_data.get("effect", ""))
	power = int(item_data.get("power", 0))
	cost = int(item_data.get("cost", 0))
	town = str(item_data.get("town", ""))
	flavor_text = item_data.get("flavor_text", {})
	quick_item = bool(item_data.get("quick_item", false))

	raw_data = item_data
