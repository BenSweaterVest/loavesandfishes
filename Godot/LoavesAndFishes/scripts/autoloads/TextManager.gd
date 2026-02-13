extends Node
class_name TextManager

signal edition_changed(new_edition: Edition)

enum Edition { DEFAULT, CHRISTIAN }
var current_edition: Edition = Edition.DEFAULT

func get_text(text_data: Variant) -> String:
	if typeof(text_data) == TYPE_DICTIONARY:
		if current_edition == Edition.CHRISTIAN and text_data.has("christian_edition"):
			return str(text_data["christian_edition"])
		if text_data.has("default"):
			return str(text_data["default"])
		return ""
	if typeof(text_data) == TYPE_STRING:
		return str(text_data)
	return str(text_data)

func set_edition(edition: Edition) -> void:
	if current_edition == edition:
		return
	current_edition = edition
	emit_signal("edition_changed", current_edition)
