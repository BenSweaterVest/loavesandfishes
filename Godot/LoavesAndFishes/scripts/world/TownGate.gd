extends Area2D

func _ready() -> void:
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
	if body.name == "PlayerCharacter":
		var current_town_id = String(GameState.current_town).to_lower()
		var current_loc = WorldMapManager.get_location(current_town_id)
		if current_loc and current_loc.connected_to.size() > 0:
			var next_town = current_loc.connected_to[0]
			GameState.unlock_town(next_town)
			print("Leaving " + current_town_id + "... Traveling to: " + next_town)
			WorldMapManager.travel_to(next_town)
