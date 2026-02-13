extends Node

func _ready() -> void:
	print("DataLoader fish count:", DataLoader.get_all_fish().size())
	var sample = DataLoader.get_fish_by_id("holy_mackerel")
	print("Sample fish:", sample.get("name", ""))
	print("Sample flavor:", TextManager.get_text(sample.get("flavor_text", {})))
