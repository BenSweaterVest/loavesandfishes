# Godot 4.3 - GDScript
class_name MiracleSystem
extends Node

signal miracle_performed(miracle_id: String)

const DEFAULT_MIRACLE_COSTS = {
	"healing_miracle": 50,
	"loaves_and_fishes": 40,
	"divine_judgment": 75,
	"resurrection_power": 100
}

func can_perform_miracle(miracle_id: String) -> bool:
	if GameState.player == null:
		return false
	if not GameState.unlocked_miracles.has(miracle_id):
		return false

	var cost = _get_miracle_cost(miracle_id)
	if cost < 0:
		return false

	return float(GameState.player.miracle_meter) >= float(cost)

func perform_miracle(miracle_id: String) -> bool:
	if not can_perform_miracle(miracle_id):
		return false

	var cost = _get_miracle_cost(miracle_id)
	GameState.player.miracle_meter = max(0.0, GameState.player.miracle_meter - float(cost))

	match miracle_id:
		"healing_miracle":
			_apply_healing_miracle()
		"loaves_and_fishes":
			_apply_loaves_and_fishes()
		"divine_judgment":
			_apply_divine_judgment()
		"resurrection_power":
			_apply_resurrection_power()
		_:
			return false

	miracle_performed.emit(miracle_id)
	return true

func _get_miracle_cost(miracle_id: String) -> int:
	var miracle_data = DataLoader.get_miracle_by_id(miracle_id)
	if not miracle_data.is_empty():
		return int(miracle_data.get("meter_cost", DEFAULT_MIRACLE_COSTS.get(miracle_id, -1)))
	return int(DEFAULT_MIRACLE_COSTS.get(miracle_id, -1))

func _apply_healing_miracle() -> void:
	var player = GameState.player
	if player == null:
		return

	for fish in player.active_party:
		if fish:
			fish.current_hp = fish.max_hp
			fish.clear_status_effects()

func _apply_loaves_and_fishes() -> void:
	GameState.story_flags["miracle_loaves_and_fishes_active"] = true
	GameState.story_flags["miracle_loaves_and_fishes_multiplier"] = 3

func _apply_divine_judgment() -> void:
	if GameState.current_battle and GameState.current_battle.has_method("apply_divine_judgment"):
		GameState.current_battle.apply_divine_judgment(300, 0.5, 3)
		return

	GameState.story_flags["miracle_divine_judgment_damage"] = 300
	GameState.story_flags["miracle_divine_judgment_debuff"] = 0.5
	GameState.story_flags["miracle_divine_judgment_turns"] = 3

func _apply_resurrection_power() -> void:
	var player = GameState.player
	if player == null:
		return

	for fish in player.active_party:
		if fish and fish.is_fainted():
			fish.current_hp = fish.max_hp
			fish.apply_status_effect("immunity")

	GameState.story_flags["miracle_resurrection_immunity_turns"] = 2
