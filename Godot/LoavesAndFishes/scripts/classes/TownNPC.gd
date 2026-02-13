class_name TownNPC
extends Area2D

@export var npc_name: String = "Villager"
@export var dialogue_lines: Array[String] = [
	"Have you heard the news?",
	"Strange things are happening lately.",
	"The Romans are always watching."
]

var player_in_range: bool = false
var current_line: int = 0

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)

func _on_body_entered(body: Node2D) -> void:
	if body.name == "PlayerCharacter":
		player_in_range = true

func _on_body_exited(body: Node2D) -> void:
	if body.name == "PlayerCharacter":
		player_in_range = false
		current_line = 0

func _unhandled_input(event: InputEvent) -> void:
	if player_in_range and event.is_action_pressed("ui_accept"):
		get_viewport().set_input_as_handled()
		var town_system = get_parent().get_parent()
		if town_system and town_system.has_method("show_dialogue"):
			town_system.show_dialogue(npc_name, dialogue_lines[current_line])
		current_line += 1
		if current_line >= dialogue_lines.size():
			current_line = 0
