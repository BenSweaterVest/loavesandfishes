class_name Boss
extends Enemy

@export var boss_id: String = ""
@export var title: String = ""
@export var phases: int = 1
@export var current_phase: int = 1

@export var gimmick: String = ""
@export var special_conditions: Array = []
@export var intro_dialogue: Variant
@export var defeat_dialogue: Variant
@export var phase_transitions: Dictionary = {}
@export var biblical_reference: String = ""

func _init(boss_data: Dictionary = {}, level_param: int = 1) -> void:
	if boss_data.is_empty():
		return
	super(boss_data, level_param)
	boss_id = str(boss_data.get("id", ""))
	title = str(boss_data.get("title", ""))
	phases = int(boss_data.get("phases", 1))
	current_phase = 1

	gimmick = str(boss_data.get("gimmick", ""))
	special_conditions = boss_data.get("special_conditions", [])
	intro_dialogue = boss_data.get("intro_dialogue", {})
	defeat_dialogue = boss_data.get("defeat_dialogue", {})
	phase_transitions = boss_data.get("phase_transitions", {})
	biblical_reference = str(boss_data.get("biblical_reference", ""))

func check_phase_transition() -> bool:
	if current_phase >= phases:
		return false

	var hp_percent = 0.0
	if max_hp > 0:
		hp_percent = (float(current_hp) / float(max_hp)) * 100.0

	if phases == 2 and hp_percent <= 50.0 and current_phase == 1:
		transition_phase()
		return true
	if phases == 3:
		if hp_percent <= 66.0 and current_phase == 1:
			transition_phase()
			return true
		if hp_percent <= 33.0 and current_phase == 2:
			transition_phase()
			return true

	return false

func transition_phase() -> void:
	current_phase += 1

	var heal_amount = int(max_hp * 0.1)
	heal(heal_amount)
	reset_stat_modifiers()
	stat_modifiers["atk"] = float(stat_modifiers.get("atk", 1.0)) * 1.2
	stat_modifiers["def"] = float(stat_modifiers.get("def", 1.0)) * 1.1

func get_phase_dialogue() -> Variant:
	var key = str(current_phase)
	if phase_transitions.has(key):
		return phase_transitions[key]
	return null
