# Godot 4.3 - GDScript
extends Node

signal cutscene_started
signal cutscene_ended
signal dialogue_started
signal dialogue_ended
signal cutscene_action_requested(action: int, data: Dictionary)

class DialogueChoice:
	var text: String
	var next_node: String
	var action: Callable
	var condition: Callable

	func _init(
		choice_text: String,
		next_node_id: String = "",
		action_callback: Callable = Callable(),
		condition_callback: Callable = Callable()
	) -> void:
		text = choice_text
		next_node = next_node_id
		action = action_callback
		condition = condition_callback

	func is_available() -> bool:
		if condition.is_valid():
			return bool(condition.call())
		return true

class DialogueNode:
	var node_id: String
	var speaker: String
	var text: String
	var choices: Array[DialogueChoice] = []

	func _init(
		node_id_value: String,
		speaker_value: String,
		text_value: String,
		choices_value: Array[DialogueChoice] = []
	) -> void:
		node_id = node_id_value
		speaker = speaker_value
		text = text_value
		choices = choices_value

	func add_choice(choice: DialogueChoice) -> void:
		choices.append(choice)

	func get_available_choices() -> Array[DialogueChoice]:
		var available: Array[DialogueChoice] = []
		for choice in choices:
			if choice.is_available():
				available.append(choice)
		return available

class Dialogue:
	var dialogue_id: String
	var start_node: String
	var nodes: Dictionary = {}
	var current_node: String = ""

	func _init(dialogue_id_value: String, start_node_value: String) -> void:
		dialogue_id = dialogue_id_value
		start_node = start_node_value

	func add_node(node: DialogueNode) -> void:
		nodes[node.node_id] = node

	func start() -> void:
		current_node = start_node

	func get_current_node() -> DialogueNode:
		if current_node != "" and nodes.has(current_node):
			return nodes[current_node]
		return null

	func choose(choice_index: int) -> DialogueNode:
		var current = get_current_node()
		if current == null:
			return null

		var available_choices = current.get_available_choices()
		if choice_index >= 0 and choice_index < available_choices.size():
			var choice = available_choices[choice_index]
			if choice.action.is_valid():
				choice.action.call()
			if choice.next_node != "":
				current_node = choice.next_node
				return get_current_node()

		current_node = ""
		return null

	func is_finished() -> bool:
		var current = get_current_node()
		return current == null or current.get_available_choices().is_empty()

class CutsceneAction:
	enum ActionType {
		DIALOGUE,
		MOVE_PLAYER,
		MOVE_NPC,
		SHOW_IMAGE,
		PLAY_SOUND,
		WAIT,
		FADE_OUT,
		FADE_IN,
		BATTLE,
		RECRUIT_APOSTLE,
		RECEIVE_ITEM,
		SET_FLAG
	}

class CutsceneStep:
	var action: CutsceneAction.ActionType
	var data: Dictionary
	var wait_for_input: bool
	var completed: bool = false

	func _init(
		action_value: CutsceneAction.ActionType,
		data_value: Dictionary = {},
		wait_for_input_value: bool = false
	) -> void:
		action = action_value
		data = data_value
		wait_for_input = wait_for_input_value

	func execute(_game_state) -> bool:
		completed = true
		return true

class Cutscene:
	var cutscene_id: String
	var name: String
	var steps: Array[CutsceneStep] = []
	var current_step: int = 0
	var is_playing: bool = false
	var is_complete: bool = false

	func _init(cutscene_id_value: String, name_value: String) -> void:
		cutscene_id = cutscene_id_value
		name = name_value

	func add_step(step: CutsceneStep) -> void:
		steps.append(step)

	func start() -> void:
		is_playing = true
		is_complete = false
		current_step = 0

	func advance(game_state) -> bool:
		if current_step >= steps.size():
			is_playing = false
			is_complete = true
			return false

		var step = steps[current_step]
		if not step.completed:
			step.execute(game_state)

		if step.completed:
			current_step += 1

		return is_playing

	func get_current_step() -> CutsceneStep:
		if current_step >= 0 and current_step < steps.size():
			return steps[current_step]
		return null

	func skip() -> void:
		is_playing = false
		is_complete = true
		current_step = steps.size()

var dialogues: Dictionary = {}
var cutscenes: Dictionary = {}
var current_dialogue: Dialogue
var current_cutscene: Cutscene

func register_dialogue(dialogue: Dialogue) -> void:
	dialogues[dialogue.dialogue_id] = dialogue

func register_cutscene(cutscene: Cutscene) -> void:
	cutscenes[cutscene.cutscene_id] = cutscene

func start_dialogue(dialogue_id: String) -> bool:
	var dialogue = dialogues.get(dialogue_id, null)
	if dialogue:
		dialogue.start()
		current_dialogue = dialogue
		dialogue_started.emit()
		return true
	return false

func start_cutscene(cutscene_id: String) -> bool:
	var cutscene = cutscenes.get(cutscene_id, null)
	if cutscene:
		cutscene.start()
		current_cutscene = cutscene
		cutscene_started.emit()
		return true
	return false

func advance_cutscene() -> bool:
	if current_cutscene == null:
		return false

	var step = current_cutscene.get_current_step()
	if step and not step.completed:
		await _execute_cutscene_step(step)

	current_cutscene.advance(GameState)
	if not current_cutscene.is_playing:
		cutscene_ended.emit()
	return current_cutscene.is_playing

func _execute_cutscene_step(step: CutsceneStep) -> void:
	match step.action:
		CutsceneAction.ActionType.WAIT:
			var duration = float(step.data.get("duration", 1.0))
			await get_tree().create_timer(duration).timeout
			step.completed = true
		CutsceneAction.ActionType.SET_FLAG:
			var flag = str(step.data.get("flag", ""))
			var value = bool(step.data.get("value", true))
			if flag != "":
				GameState.story_flags[flag] = value
			step.completed = true
		CutsceneAction.ActionType.RECRUIT_APOSTLE:
			var apostle_id = str(step.data.get("apostle_id", ""))
			if apostle_id != "" and GameState.player:
				GameState.player.recruit_apostle(apostle_id)
			step.completed = true
		CutsceneAction.ActionType.RECEIVE_ITEM:
			var item_id = str(step.data.get("item_id", ""))
			var count = int(step.data.get("count", 1))
			if item_id != "" and GameState.player:
				GameState.player.add_bread_item(item_id, count)
			step.completed = true
		CutsceneAction.ActionType.DIALOGUE:
			var dialogue_id = str(step.data.get("dialogue_id", ""))
			if dialogue_id != "":
				start_dialogue(dialogue_id)
			step.completed = true
		_:
			cutscene_action_requested.emit(step.action, step.data)
			step.completed = true

func is_in_dialogue() -> bool:
	return current_dialogue != null and not current_dialogue.is_finished()

func is_in_cutscene() -> bool:
	return current_cutscene != null and current_cutscene.is_playing

func create_simple_dialogue(
	dialogue_id: String,
	speaker: String,
	lines: Array[String]
) -> Dialogue:
	var dialogue = Dialogue.new(dialogue_id, "start")

	for i in range(lines.size()):
		var line = lines[i]
		var node_id = "node_" + str(i) if i > 0 else "start"
		var next_node = "node_" + str(i + 1) if i < lines.size() - 1 else ""
		var node = DialogueNode.new(node_id, speaker, line)

		if next_node != "":
			node.add_choice(DialogueChoice.new("Continue", next_node))
		else:
			node.add_choice(DialogueChoice.new("End", ""))

		dialogue.add_node(node)

	register_dialogue(dialogue)
	return dialogue

func create_quest_dialogue(
	dialogue_id: String,
	quest_giver: String,
	quest_text: String,
	accept_callback: Callable = Callable(),
	decline_callback: Callable = Callable()
) -> Dialogue:
	var dialogue = Dialogue.new(dialogue_id, "offer")

	var offer = DialogueNode.new("offer", quest_giver, quest_text)
	offer.add_choice(
		DialogueChoice.new("Accept Quest", "accepted", accept_callback)
	)
	offer.add_choice(
		DialogueChoice.new("Decline", "declined", decline_callback)
	)
	dialogue.add_node(offer)

	var accepted = DialogueNode.new(
		"accepted",
		quest_giver,
		"Thank you! May the Lord be with you on this journey."
	)
	accepted.add_choice(DialogueChoice.new("Farewell", ""))
	dialogue.add_node(accepted)

	var declined = DialogueNode.new(
		"declined",
		quest_giver,
		"I understand. Come back if you change your mind."
	)
	declined.add_choice(DialogueChoice.new("Farewell", ""))
	dialogue.add_node(declined)

	register_dialogue(dialogue)
	return dialogue
