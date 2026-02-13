class_name DialogueBox
extends Panel

signal text_finished
signal dialogue_closed
signal choice_selected(choice_index: int)

@onready var speaker_label: Label = $MarginContainer/VBoxContainer/SpeakerLabel
@onready var text_label: RichTextLabel = $MarginContainer/VBoxContainer/TextLabel
@onready var choices_container: VBoxContainer = $MarginContainer/VBoxContainer/ChoicesContainer
@onready var continue_icon: TextureRect = $ContinueIcon

var is_typing: bool = false
var text_speed: float = 0.03
var current_dialogue: DialogueManager.Dialogue

func _ready() -> void:
	hide()

func display_text(text_data: Variant, speaker: String = "") -> void:
	show()
	continue_icon.hide()
	_clear_choices()

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

func display_dialogue(dialogue: DialogueManager.Dialogue) -> void:
	current_dialogue = dialogue
	_show_current_node()

func _show_current_node() -> void:
	if current_dialogue == null:
		hide()
		dialogue_closed.emit()
		return

	var node = current_dialogue.get_current_node()
	if node == null:
		hide()
		dialogue_closed.emit()
		return

	display_text(node.text, node.speaker)
	await text_finished
	_show_choices(node.get_available_choices())

func _show_choices(choices: Array) -> void:
	_clear_choices()
	if choices.is_empty():
		continue_icon.show()
		return

	for i in range(choices.size()):
		var choice = choices[i]
		var button = Button.new()
		button.text = str(choice.text)
		button.pressed.connect(_on_choice_pressed.bind(i))
		choices_container.add_child(button)

func _on_choice_pressed(choice_index: int) -> void:
	choice_selected.emit(choice_index)
	if current_dialogue == null:
		return

	current_dialogue.choose(choice_index)
	_show_current_node()

func _clear_choices() -> void:
	if not choices_container:
		return
	for child in choices_container.get_children():
		child.queue_free()

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
	if choices_container and choices_container.get_child_count() > 0:
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
