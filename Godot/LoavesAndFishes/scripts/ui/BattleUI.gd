extends Control
class_name BattleUI

@onready var player_effects_label: RichTextLabel = $EffectBackground/EffectPanel/PlayerEffects
@onready var enemy_effects_label: RichTextLabel = $EffectBackground/EffectPanel/EnemyEffects
@onready var player_status_icons: HBoxContainer = $EffectBackground/EffectPanel/PlayerStatusIcons
@onready var enemy_status_icons: HBoxContainer = $EffectBackground/EffectPanel/EnemyStatusIcons

func update_effects(player_fish: Fish, enemy: Enemy) -> void:
	player_effects_label.text = _format_label("Player", player_fish)
	enemy_effects_label.text = _format_label("Enemy", enemy)
	player_effects_label.parse_bbcode(player_effects_label.text)
	enemy_effects_label.parse_bbcode(enemy_effects_label.text)
	_populate_status_icons(player_status_icons, player_fish)
	_populate_status_icons(enemy_status_icons, enemy)

func _format_label(title: String, target) -> String:
	return "[b]" + title + ":[/b] " + _format_effects(target)

func _format_effects(target) -> String:
	if target == null:
		return "none"

	var parts: Array[String] = []
	var seen_statuses: Dictionary = {}

	if target.status_effects is Array:
		for status in target.status_effects:
			seen_statuses[status] = true
			parts.append(_format_status(status, _get_status_turns(target, status)))

	if target.status_durations is Dictionary:
		for status in target.status_durations.keys():
			var turns = int(target.status_durations.get(status, 0))
			if turns > 0:
				if not seen_statuses.has(status):
					parts.append(_format_status(status, turns))

	if target.timed_stat_modifiers is Dictionary:
		for stat in target.timed_stat_modifiers.keys():
			var entries: Array = target.timed_stat_modifiers[stat]
			for entry in entries:
				var turns = int(entry.get("turns", 0))
				var multiplier = float(entry.get("multiplier", 1.0))
				if turns > 0 and multiplier != 1.0:
					parts.append(_format_stat_modifier(stat, multiplier, turns))

	if parts.is_empty():
		return "[color=#9aa0a6]none[/color]"
	return ", ".join(parts)

func _format_multiplier(multiplier: float) -> String:
	return String.num(multiplier, 2)

func _get_status_turns(target, status: String) -> int:
	if target.status_durations is Dictionary and target.status_durations.has(status):
		return int(target.status_durations.get(status, 0))
	return 0

func _format_status(status: String, turns: int) -> String:
	var abbrev = _status_abbreviation(status)
	var color = _status_color(status)
	var label = "[color=" + color + "]" + abbrev + "[/color]"
	if turns > 0:
		return label + "(" + str(turns) + "T)"
	return label

func _format_stat_modifier(stat: String, multiplier: float, turns: int) -> String:
	var percent = int(abs(multiplier - 1.0) * 100.0)
	var sign = "+" if multiplier >= 1.0 else "-"
	var color = "#7adf8f" if multiplier >= 1.0 else "#ff8b8b"
	var label = str(stat).to_upper() + sign + str(percent) + "%"
	return "[color=" + color + "]" + label + "[/color]" + "(" + str(turns) + "T)"

func _status_abbreviation(status: String) -> String:
	match status:
		"poisoned":
			return "POI"
		"burned":
			return "BRN"
		"frozen":
			return "FRZ"
		"asleep":
			return "SLP"
		"silenced":
			return "SIL"
		"confused":
			return "CONF"
		"invincible":
			return "INV"
		"immunity":
			return "IMM"
		_:
			return status.to_upper()

func _status_color(status: String) -> String:
	match status:
		"poisoned":
			return "#7adf8f"
		"burned":
			return "#ff8b8b"
		"frozen":
			return "#8cc8ff"
		"asleep":
			return "#c2b5ff"
		"silenced":
			return "#ffd28a"
		"confused":
			return "#f3b6ff"
		"invincible":
			return "#ffe17a"
		"immunity":
			return "#b8f4ff"
		_:
			return "#d6d6d6"

func _populate_status_icons(container: HBoxContainer, target) -> void:
	for child in container.get_children():
		child.queue_free()

	if target == null or not (target.status_effects is Array):
		_add_empty_icon_label(container)
		return

	var statuses: Array = []
	for status in target.status_effects:
		if not statuses.has(status):
			statuses.append(status)

	if statuses.is_empty():
		_add_empty_icon_label(container)
		return

	for status in statuses:
		var icon = ColorRect.new()
		icon.color = Color(_status_color(status))
		icon.custom_minimum_size = Vector2(14, 14)
		icon.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
		icon.size_flags_vertical = Control.SIZE_SHRINK_CENTER
		var turns = _get_status_turns(target, status)
		if turns > 0:
			icon.tooltip_text = status + " (" + str(turns) + "T)"
		else:
			icon.tooltip_text = status
		container.add_child(icon)

func _add_empty_icon_label(container: HBoxContainer) -> void:
	var label = Label.new()
	label.text = "none"
	label.modulate = Color("#9aa0a6")
	container.add_child(label)
