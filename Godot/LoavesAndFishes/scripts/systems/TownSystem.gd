extends Node2D

@onready var location_label: Label = $TownUI/LocationLabel
@onready var dialogue_box: DialogueBox = $TownUI/DialogueBox

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

func show_dialogue(speaker: String, text: String) -> void:
	$PlayerCharacter.set_physics_process(false)
	dialogue_box.display_text(text, speaker)
	await dialogue_box.dialogue_closed
	$PlayerCharacter.set_physics_process(true)

func register_location_search(count: int = 1) -> void:
	var current = int(GameState.story_flags.get("locations_searched", 0))
	GameState.story_flags["locations_searched"] = current + max(1, count)
	if QuestManager:
		for quest_id in GameState.active_quests:
			QuestManager.advance_quest(quest_id)
