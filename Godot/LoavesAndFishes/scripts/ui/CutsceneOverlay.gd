extends ColorRect

@export var default_fade_duration: float = 1.0
@export var default_color: Color = Color(0, 0, 0, 1)

func _ready() -> void:
	_load_project_defaults()
	color = default_color
	modulate.a = 0.0
	visible = false
	if DialogueManager and not DialogueManager.cutscene_action_requested.is_connected(
		_on_cutscene_action_requested
	):
		DialogueManager.cutscene_action_requested.connect(
			_on_cutscene_action_requested
		)

func _on_cutscene_action_requested(action: int, data: Dictionary) -> void:
	if action == DialogueManager.CutsceneAction.ActionType.FADE_OUT:
		var duration = float(data.get("duration", default_fade_duration))
		_set_color_override(data)
		_start_fade(1.0, duration)
	elif action == DialogueManager.CutsceneAction.ActionType.FADE_IN:
		var duration = float(data.get("duration", default_fade_duration))
		_set_color_override(data)
		_start_fade(0.0, duration)

func _set_color_override(data: Dictionary) -> void:
	if data.has("color") and data["color"] is Color:
		color = data["color"]
	else:
		color = default_color

func _load_project_defaults() -> void:
	var duration_setting = ProjectSettings.get_setting(
		"cutscene/fade_default_duration",
		default_fade_duration
	)
	default_fade_duration = float(duration_setting)
	var color_setting = ProjectSettings.get_setting(
		"cutscene/fade_default_color",
		default_color
	)
	if color_setting is Color:
		default_color = color_setting

func _start_fade(target_alpha: float, duration: float) -> void:
	visible = true
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", target_alpha, duration)
	await tween.finished
	if target_alpha <= 0.0:
		visible = false
