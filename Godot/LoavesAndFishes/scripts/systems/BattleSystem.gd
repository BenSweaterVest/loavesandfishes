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
var item_menu: Control
var battle_ui_layer: CanvasLayer

@export var auto_start_test_battle: bool = true

func _ready() -> void:
	if not battle_ui:
		battle_ui = get_parent().get_node_or_null("BattleUI") as CanvasLayer
	battle_ui_layer = battle_ui
	if not dialogue_box and battle_ui:
		dialogue_box = battle_ui.get_node_or_null("DialogueBox")
	if battle_ui:
		action_menu = battle_ui.get_node("ActionMenu") as Control
		move_menu = battle_ui.get_node("MoveMenu") as Control
		item_menu = battle_ui.get_node_or_null("ItemMenu") as Control
		var attack_button = action_menu.get_node("AttackButton") as Button
		if attack_button:
			attack_button.pressed.connect(_on_attack_button_pressed)
		var item_button = action_menu.get_node_or_null("ItemButton") as Button
		if item_button:
			item_button.pressed.connect(_on_item_button_pressed)
		var apostle_button = action_menu.get_node_or_null("ApostleButton") as Button
		if apostle_button:
			apostle_button.pressed.connect(_on_apostle_button_pressed)
		var miracle_button = action_menu.get_node_or_null("MiracleButton") as Button
		if miracle_button:
			miracle_button.pressed.connect(_on_miracle_button_pressed)
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
	GameState.current_battle = self

	if action_menu:
		action_menu.hide()
	if move_menu:
		move_menu.hide()
	if item_menu:
		item_menu.hide()

	change_state(BattleState.START)
	_update_effect_display()
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
	_tick_timed_effects()
	_update_effect_display()
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
	await _show_item_menu()

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
	var player = GameState.player
	if not player:
		await show_dialogue("No Apostle combos available right now.")
		start_enemy_turn()
		return

	var combos = ComboManager.get_available_combos(
		player_fish,
		player.recruited_apostles,
		player.miracle_meter
	)
	if combos.is_empty():
		var ability_info = _get_first_available_apostle_ability(player)
		if not ability_info.is_empty():
			var ability = ability_info["ability"]
			var apostle_id = ability_info["apostle_id"]
			var context = {
				"battle": self,
				"player": player,
				"active_fish": player_fish,
				"enemy": enemy,
				"party": player.active_party
			}
			ApostleManager.execute_battle_ability(apostle_id, context)
			await show_dialogue(ability.name + " was used!")
			start_enemy_turn()
			return

		await show_dialogue("No Apostle combos available right now.")
		start_enemy_turn()
		return

	var combo = combos[0]
	var performed = ComboManager.perform_combo(combo.combo_id)
	if performed == null:
		await show_dialogue("No Apostle combos available right now.")
		start_enemy_turn()
		return

	player.miracle_meter = max(0.0, player.miracle_meter - float(combo.miracle_meter_cost))
	var combo_text = player_fish.fish_name + " and " + combo.apostle_id
	combo_text += " used " + combo.name + "!"
	await show_dialogue(combo_text)

	var combo_move = {
		"name": combo.name,
		"power": combo.power,
		"type": combo.attack_type
	}
	var damage = calculate_damage(player_fish, enemy, combo_move)
	enemy.current_hp = max(0, enemy.current_hp - damage)
	await show_dialogue("It dealt " + str(damage) + " damage!")
	if enemy.current_hp <= 0:
		await handle_faint(enemy, "Enemy")
		return

	start_enemy_turn()

func _on_miracle_button_pressed() -> void:
	if current_state != BattleState.PLAYER_TURN:
		return

	if action_menu:
		action_menu.hide()
	change_state(BattleState.RESOLVING)

	var miracle_id = _get_first_available_miracle()
	if miracle_id == "":
		await show_dialogue("No miracles available right now.")
		start_enemy_turn()
		return

	var result = MiracleSystem.perform_miracle(miracle_id)
	if not result:
		await show_dialogue("No miracles available right now.")
		start_enemy_turn()
		return

	await show_dialogue(_get_miracle_battle_text(miracle_id))
	start_enemy_turn()

func start_enemy_turn() -> void:
	change_state(BattleState.ENEMY_TURN)
	if action_menu:
		action_menu.hide()
	_update_effect_display()

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
		_register_enemy_defeated(enemy)
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

func apply_divine_judgment(damage_amount: int, debuff_multiplier: float, turns: int) -> void:
	if enemy == null:
		return

	enemy.current_hp = max(0, enemy.current_hp - damage_amount)
	enemy.apply_stat_modifier("atk", debuff_multiplier, turns)
	enemy.apply_stat_modifier("def", debuff_multiplier, turns)
	enemy.apply_stat_modifier("spd", debuff_multiplier, turns)
	GameState.story_flags["divine_judgment_turns"] = turns

func _register_enemy_defeated(defeated_enemy: Enemy) -> void:
	if defeated_enemy == null:
		return

	var enemy_id = str(defeated_enemy.enemy_id)
	if enemy_id != "":
		var flag = "defeated_enemy_" + enemy_id
		var current = int(GameState.story_flags.get(flag, 0))
		GameState.story_flags[flag] = current + 1

	_advance_active_quests()

func _register_item_used(item_tag: String) -> void:
	if item_tag == "":
		return

	var flag = "used_items_" + item_tag
	var current = int(GameState.story_flags.get(flag, 0))
	GameState.story_flags[flag] = current + 1
	_advance_active_quests()

func _show_item_menu() -> void:
	if not item_menu:
		start_enemy_turn()
		return

	var player = GameState.player
	if not player or player.bread_items.is_empty():
		await show_dialogue("No items available.")
		start_player_turn()
		return

	_clear_menu_children(item_menu)
	for item_id in player.bread_items.keys():
		var count = int(player.bread_items.get(item_id, 0))
		if count <= 0:
			continue
		var item_data = DataLoader.get_item_by_id(item_id)
		var item_name = item_data.get("name", item_id) if not item_data.is_empty() else item_id
		var button = Button.new()
		button.text = item_name + " x" + str(count)
		button.pressed.connect(_on_item_selected.bind(item_id))
		item_menu.add_child(button)

	var back_button = Button.new()
	back_button.text = "Back"
	back_button.pressed.connect(_close_item_menu)
	item_menu.add_child(back_button)
	item_menu.show()

func _on_item_selected(item_id: String) -> void:
	if item_menu:
		item_menu.hide()
		_clear_menu_children(item_menu)

	if _use_bread_item(item_id):
		_register_item_use_tags(item_id)
		start_enemy_turn()
		return

	await show_dialogue("That item had no effect.")
	start_player_turn()

func _close_item_menu() -> void:
	if item_menu:
		item_menu.hide()
		_clear_menu_children(item_menu)
	start_player_turn()

func _update_effect_display() -> void:
	if battle_ui_layer and battle_ui_layer.has_method("update_effects"):
		battle_ui_layer.update_effects(player_fish, enemy)

func _use_bread_item(item_id: String) -> bool:
	var player = GameState.player
	if not player or not player.has_item(item_id):
		return false

	var item_data = DataLoader.get_item_by_id(item_id)
	if item_data.is_empty():
		return false

	player.remove_bread_item(item_id, 1)
	var effect = str(item_data.get("effect", ""))
	var multiplier = _get_bread_multiplier()
	var duration = int(item_data.get("duration", 0))

	match effect:
		"heal_hp":
			player_fish.heal(int(item_data.get("power", 0) * multiplier))
		"heal_and_cure_poison":
			player_fish.heal(int(item_data.get("power", 0) * multiplier))
			player_fish.remove_status_effect("poisoned")
		"heal_and_atk_boost":
			player_fish.heal(int(item_data.get("heal_power", 0) * multiplier))
			var boost = float(item_data.get("atk_boost", 0)) / 100.0
			if boost > 0:
				player_fish.apply_stat_modifier("atk", 1.0 + boost, duration)
		"full_heal_all":
			for fish in player.active_party:
				fish.heal(fish.max_hp)
				fish.clear_status_effects()
		"atk_boost":
			var boost = float(item_data.get("boost_percent", 0)) / 100.0
			if boost > 0:
				player_fish.apply_stat_modifier("atk", 1.0 + boost, duration)
		"spd_boost":
			var boost = float(item_data.get("boost_percent", 0)) / 100.0
			if boost > 0:
				player_fish.apply_stat_modifier("spd", 1.0 + boost, duration)
		"def_boost":
			var boost = float(item_data.get("boost_percent", 0)) / 100.0
			if boost > 0:
				player_fish.apply_stat_modifier("def", 1.0 + boost, duration)
		"enemy_atk_down":
			if enemy:
				var debuff = float(item_data.get("debuff_percent", 0)) / 100.0
				if debuff > 0:
					enemy.apply_stat_modifier("atk", 1.0 - debuff, duration)
		"remove_all_debuffs":
			player_fish.clear_status_effects()
			player_fish.reset_stat_modifiers()
		"auto_revive":
			if player_fish.is_fainted():
				var revive_hp = int(item_data.get("revive_hp", 1))
				player_fish.current_hp = max(1, revive_hp)
		"invincible":
			player_fish.apply_status_effect("invincible", duration)
		_:
			return false

	return true

func _register_item_use_tags(item_id: String) -> void:
	var item_data = DataLoader.get_item_by_id(item_id)
	var item_type = str(item_data.get("type", "")) if not item_data.is_empty() else ""
	_register_item_used("any_bread")
	_register_item_used(item_id)
	if item_type != "":
		_register_item_used(item_type)

func _get_bread_multiplier() -> float:
	var multiplier = 1.0
	if GameState.story_flags.get("miracle_loaves_and_fishes_active", false):
		multiplier = float(GameState.story_flags.get("miracle_loaves_and_fishes_multiplier", 3))
	if GameState.story_flags.get("apostle_multiplication_active", false):
		multiplier = max(multiplier, 3.0)
	return multiplier

func _clear_menu_children(container: Control) -> void:
	for child in container.get_children():
		child.queue_free()


func _get_first_available_apostle_ability(player: Player) -> Dictionary:
	for apostle_id in player.recruited_apostles:
		var ability = ApostleManager.get_ability(apostle_id)
		if ability and ability.is_ready():
			return {"apostle_id": apostle_id, "ability": ability}
	return {}

func _tick_timed_effects() -> void:
	var keys = GameState.story_flags.keys()
	for key in keys:
		if not str(key).ends_with("_turns"):
			continue
		var remaining = int(GameState.story_flags.get(key, 0))
		if remaining <= 0:
			continue
		remaining -= 1
		GameState.story_flags[key] = remaining
		if remaining == 0:
			_handle_effect_expired(key)

	if GameState.player:
		for fish in GameState.player.active_party:
			fish.tick_temporary_effects()
	if enemy:
		enemy.tick_temporary_effects()

func _handle_effect_expired(flag: String) -> void:
	if flag == "miracle_loaves_and_fishes_turns":
		GameState.story_flags["miracle_loaves_and_fishes_active"] = false
	if flag == "apostle_multiplication_turns":
		GameState.story_flags["apostle_multiplication_active"] = false
	if flag == "miracle_resurrection_immunity_turns":
		for fish in GameState.player.active_party:
			fish.remove_status_effect("immunity")

func _advance_active_quests() -> void:
	if not QuestManager:
		return
	for quest_id in GameState.active_quests:
		QuestManager.advance_quest(quest_id)

func _get_first_available_miracle() -> String:
	for miracle_id in GameState.unlocked_miracles:
		if MiracleSystem.can_perform_miracle(miracle_id):
			return miracle_id
	return ""

func _get_miracle_battle_text(miracle_id: String) -> String:
	var miracle_data = DataLoader.get_miracle_by_id(miracle_id)
	if miracle_data.is_empty():
		return "Miracle performed!"
	var battle_text = miracle_data.get("battle_text", {})
	if TextManager:
		return TextManager.get_text(battle_text)
	return str(battle_text)

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
