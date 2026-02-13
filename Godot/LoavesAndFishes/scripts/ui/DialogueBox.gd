class_name DialogueBox
extends Panel

signal text_finished
signal dialogue_closed

@onready var speaker_label: Label = $MarginContainer/VBoxContainer/SpeakerLabel
@onready var text_label: RichTextLabel = $MarginContainer/VBoxContainer/TextLabel
@onready var continue_icon: TextureRect = $ContinueIcon

var is_typing: bool = false
var text_speed: float = 0.03

func _ready() -> void:
	hide()

func display_text(text_data: Variant, speaker: String = "") -> void:
	show()
	continue_icon.hide()

	var finalized_text = TextManager.get_text(text_data)

	if speaker.is_empty():
		speaker_label.hide()
	else:
		speaker_label.show()
		speaker_label.text = speaker

	text_label.text = finalized_text
	text_label.visible_characters = 0
	is_typing = true
	_typewriter_effect()

func _typewriter_effect() -> void:
	while text_label.visible_characters < text_label.get_total_character_count():
		if not is_typing:
			text_label.visible_characters = text_label.get_total_character_count()
			break
		text_label.visible_characters += 1
		await get_tree().create_timer(text_speed).timeout

	is_typing = false
	continue_icon.show()
	text_finished.emit()

func _input(event: InputEvent) -> void:
	if not visible:
		return

	var is_click = event is InputEventMouseButton and event.pressed
	var is_accept = event.is_action_pressed("ui_accept")
	if is_accept or (is_click and event.button_index == MOUSE_BUTTON_LEFT):
		get_viewport().set_input_as_handled()
		if is_typing:
			is_typing = false
		else:
			hide()
			dialogue_closed.emit()
