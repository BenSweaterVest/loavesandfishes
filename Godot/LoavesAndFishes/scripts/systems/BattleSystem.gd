class_name BattleSystem
extends Node

signal battle_ended(result: String)
signal state_changed(new_state: BattleState)

enum BattleState { START, PLAYER_TURN, ENEMY_TURN, RESOLVING, ENDED }
var current_state: BattleState = BattleState.START

@export var player_side: Node2D
@export var enemy_side: Node2D
@export var battle_ui: CanvasLayer
@export var dialogue_box: Node

var player_fish: Fish
var enemy: Enemy

var action_menu: Control
var move_menu: Control

func _ready() -> void:
	if not battle_ui:
		battle_ui = get_parent().get_node_or_null("BattleUI") as CanvasLayer
	if not dialogue_box and battle_ui:
		dialogue_box = battle_ui.get_node_or_null("DialogueBox")
	if battle_ui:
		action_menu = battle_ui.get_node("ActionMenu") as Control
		move_menu = battle_ui.get_node("MoveMenu") as Control
		var attack_button = action_menu.get_node("AttackButton") as Button
		if attack_button:
			attack_button.pressed.connect(_on_attack_button_pressed)

func start_battle(fish: Fish, enemy_data: Dictionary) -> void:
	player_fish = fish
	enemy = Enemy.new(enemy_data)

	if action_menu:
		action_menu.hide()
	if move_menu:
		move_menu.hide()

	change_state(BattleState.START)
	await show_dialogue("A wild " + _get_entity_name(enemy) + " appeared!")
	_determine_first_attacker()

func change_state(new_state: BattleState) -> void:
	current_state = new_state
	state_changed.emit(new_state)

func _determine_first_attacker() -> void:
	if player_fish.spd >= enemy.spd:
		start_player_turn()
	else:
		start_enemy_turn()

func start_player_turn() -> void:
	change_state(BattleState.PLAYER_TURN)
	await show_dialogue("What will " + _get_entity_name(player_fish) + " do?")
	if action_menu:
		action_menu.show()

func _on_attack_button_pressed() -> void:
	if current_state != BattleState.PLAYER_TURN:
		return

	if action_menu:
		action_menu.hide()
	change_state(BattleState.RESOLVING)

	var moves = _get_entity_moves(player_fish)
	if moves.is_empty():
		await show_dialogue(_get_entity_name(player_fish) + " has no moves!")
		start_enemy_turn()
		return

	var move = moves[0]
	await execute_attack(player_fish, enemy, move, "Player")

func start_enemy_turn() -> void:
	change_state(BattleState.ENEMY_TURN)
	if action_menu:
		action_menu.hide()

	var moves = _get_entity_moves(enemy)
	if moves.is_empty():
		await show_dialogue(_get_entity_name(enemy) + " hesitates...")
		start_player_turn()
		return

	var move = moves.pick_random()
	await execute_attack(enemy, player_fish, move, "Enemy")

func execute_attack(attacker, defender, move: Dictionary, side: String) -> void:
	var move_name = str(move.get("name", "Attack"))
	await show_dialogue(_get_entity_name(attacker) + " used " + move_name + "!")

	var damage = calculate_damage(attacker, defender, move)
	defender.current_hp = max(0, defender.current_hp - damage)

	await show_dialogue("It dealt " + str(damage) + " damage!")

	if defender.current_hp <= 0:
		await handle_faint(defender, side)
		return

	if side == "Player":
		start_enemy_turn()
	else:
		start_player_turn()

func handle_faint(fainted_entity, side: String) -> void:
	change_state(BattleState.ENDED)
	await show_dialogue(_get_entity_name(fainted_entity) + " fainted!")

	if side == "Enemy":
		battle_ended.emit("defeat")
	else:
		battle_ended.emit("victory")

func show_dialogue(text: String) -> void:
	if dialogue_box and dialogue_box.has_method("display_text"):
		dialogue_box.display_text(text)
		await dialogue_box.text_finished

func calculate_damage(_attacker, _defender, _move: Dictionary) -> int:
	return 10

func _get_entity_name(entity) -> String:
	if entity is Fish:
		return entity.fish_name
	if entity is Enemy:
		return entity.enemy_name
	return "Unknown"

func _get_entity_moves(entity) -> Array:
	if entity is Fish:
		return entity.known_moves
	if entity is Enemy:
		return entity.attacks
	return []
