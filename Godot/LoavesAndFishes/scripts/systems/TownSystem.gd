extends Node2D

@onready var location_label: Label = $TownUI/LocationLabel

func _ready() -> void:
	GameState.town_changed.connect(_on_town_changed)
	_load_town_data(GameState.current_town)

func _on_town_changed(new_town_id: String) -> void:
	_load_town_data(new_town_id)

func _load_town_data(town_id: String) -> void:
	var all_towns = DataLoader.towns_data
	for town in all_towns:
		if town.get("id") == town_id:
			location_label.text = town.get("name", "Unknown Town")
			var story_dict = town.get("story", {})
			print(TextManager.get_text(story_dict))
			return
