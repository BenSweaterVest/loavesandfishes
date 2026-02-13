class_name Apostle
extends Resource

@export var apostle_id: String = ""
@export var apostle_name: String = ""
@export var alternate_name: String = ""
@export var title: String = ""
@export var town: String = ""
@export var town_number: int = 0

@export var battle_ability: Dictionary = {}
@export var key_power: Dictionary = {}
@export var personality: Dictionary = {}
@export var biblical_reference: String = ""
@export var recruitment_event: Dictionary = {}
@export var combo_fish: String = ""
@export var combo_attack: Dictionary = {}

func _init(apostle_id_param: String = "", apostle_data: Dictionary = {}) -> void:
	if apostle_id_param == "" or apostle_data.is_empty():
		return

	apostle_id = apostle_id_param
	apostle_name = str(apostle_data.get("name", ""))
	alternate_name = str(apostle_data.get("alternate_name", ""))
	title = str(apostle_data.get("title", ""))
	town = str(apostle_data.get("town", ""))
	town_number = int(apostle_data.get("town_number", 0))

	battle_ability = apostle_data.get("battle_ability", {})
	key_power = apostle_data.get("key_power", {})
	personality = apostle_data.get("personality", {})
	biblical_reference = str(apostle_data.get("biblical_reference", ""))
	recruitment_event = apostle_data.get("recruitment_event", {})
	combo_fish = str(apostle_data.get("combo_fish", ""))
	combo_attack = apostle_data.get("combo_attack", {})
