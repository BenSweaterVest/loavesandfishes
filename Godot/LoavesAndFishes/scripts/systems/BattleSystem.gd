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

@export var auto_start_test_battle: bool = true

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
		var item_button = action_menu.get_node_or_null("ItemButton") as Button
		if item_button:
			item_button.pressed.connect(_on_item_button_pressed)
		var apostle_button = action_menu.get_node_or_null("ApostleButton") as Button
		if apostle_button:
			apostle_button.pressed.connect(_on_apostle_button_pressed)
		var run_button = action_menu.get_node_or_null("RunButton") as Button
		if run_button:
			run_button.pressed.connect(_on_run_button_pressed)
		var switch_button = action_menu.get_node_or_null("SwitchButton") as Button
		if switch_button:
			switch_button.pressed.connect(_on_switch_button_pressed)

	if auto_start_test_battle:
		_start_test_battle()

func _start_test_battle() -> void:
	if not DataLoader:
		return

	var test_player = Player.new()
	var holy_mackerel_data = DataLoader.get_fish_by_id("holy_mackerel")
	if holy_mackerel_data.is_empty():
		return
	var starter_fish = Fish.new("holy_mackerel", holy_mackerel_data, 5)
	test_player.add_fish_to_party(starter_fish)

	var enemy_data = DataLoader.get_enemy_by_id("skeptical_scholar")
	if enemy_data.is_empty():
		return

	start_battle(starter_fish, enemy_data)

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

func _on_run_button_pressed() -> void:
	if current_state != BattleState.PLAYER_TURN:
		return

	if action_menu:
		action_menu.hide()
	change_state(BattleState.RESOLVING)

	var flee_chance = 0.5
	if player_fish and enemy:
		var speed_ratio = float(player_fish.spd) / max(1.0, float(enemy.spd))
		flee_chance += (speed_ratio - 1.0) * 0.2

	if randf() < flee_chance:
		await show_dialogue("Got away safely!")
		change_state(BattleState.ENDED)
		battle_ended.emit("fled")
		return

	await show_dialogue("Couldn't escape!")
	start_enemy_turn()

func _on_item_button_pressed() -> void:
	if current_state != BattleState.PLAYER_TURN:
		return

	if action_menu:
		action_menu.hide()
	change_state(BattleState.RESOLVING)
	await show_dialogue("Feature coming soon!")
	start_enemy_turn()

func _on_switch_button_pressed() -> void:
	if current_state != BattleState.PLAYER_TURN:
		return

	if action_menu:
		action_menu.hide()
	change_state(BattleState.RESOLVING)
	await show_dialogue("Feature coming soon!")
	start_enemy_turn()

func _on_apostle_button_pressed() -> void:
	if current_state != BattleState.PLAYER_TURN:
		return

	if action_menu:
		action_menu.hide()
	change_state(BattleState.RESOLVING)
	await show_dialogue("Feature coming soon!")
	start_enemy_turn()

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

func calculate_damage(attacker, defender, move: Dictionary) -> int:
	var power = move.get("power", [0, 0])
	var base_damage = 0
	if power is Array and power.size() >= 2:
		base_damage = randi_range(int(power[0]), int(power[1]))
	else:
		base_damage = int(power)

	var attacker_stat = _get_attacker_stat(attacker)
	var damage = base_damage + int(attacker_stat / 2)

	var is_critical = randf() < 0.05
	if is_critical:
		damage = int(damage * 1.5)

	var move_type = str(move.get("type", "Normal"))
	var defender_type = _get_defender_type(defender)
	var effectiveness = Constants.get_type_effectiveness(move_type, defender_type)
	damage = int(damage * effectiveness)

	var attacker_type = _get_attacker_type(attacker)
	if attacker_type != "" and move_type == attacker_type:
		damage = int(damage * 1.2)

	damage = int(damage * randf_range(0.85, 1.0))
	return max(1, damage)

func _get_attacker_stat(attacker) -> int:
	if attacker and attacker.has_method("get_effective_stat"):
		return int(attacker.get_effective_stat("atk"))
	if attacker is Fish:
		return attacker.atk
	if attacker is Enemy:
		return attacker.atk
	return 0

func _get_attacker_type(attacker) -> String:
	if attacker is Fish:
		return attacker.fish_type
	if attacker is Enemy:
		return attacker.enemy_type
	return ""

func _get_defender_type(defender) -> String:
	if defender is Fish:
		return defender.fish_type
	if defender is Enemy:
		return defender.enemy_type
	return "Normal"

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
