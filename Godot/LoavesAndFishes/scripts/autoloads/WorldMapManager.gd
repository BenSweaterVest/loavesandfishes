extends Node

enum TravelMethod { WALK, FAST_TRAVEL, BOAT, MIRACLE }

class WorldLocation:
	var location_id: String
	var name: String
	var location_type: String
	var position: Vector2i
	var connected_to: Array[String] = []
	var region: String = ""
	var description: String = ""

	func _init(id: String, d_name: String, type: String, pos: Vector2i) -> void:
		location_id = id
		name = d_name
		location_type = type
		position = pos

var locations: Dictionary = {}

func _ready() -> void:
	_build_default_map()

func _build_default_map() -> void:
	var towns = [
		["nazareth", 5, 3, "Galilee"],
		["cana", 6, 4, "Galilee"],
		["capernaum", 8, 2, "Galilee"],
		["bethsaida", 10, 1, "Coastal"],
		["magdala", 9, 3, "Coastal"],
		["chorazin", 11, 2, "Coastal"],
		["tiberias", 9, 4, "Coastal"],
		["gadara", 12, 3, "Gentile"],
		["samaria", 7, 7, "Gentile"],
		["jericho", 9, 10, "Judean"],
		["bethany", 8, 11, "Judean"],
		["bethlehem", 7, 12, "Judean"],
		["jerusalem", 8, 12, "Jerusalem"]
	]

	for town_data in towns:
		var town_id = str(town_data[0])
		var town_name = town_id.capitalize()
		var loc = WorldLocation.new(
			town_id,
			town_name,
			"town",
			Vector2i(int(town_data[1]), int(town_data[2]))
		)
		loc.region = str(town_data[3])
		loc.description = "The town of " + town_name
		locations[town_id] = loc

	var connections = [
		["nazareth", "cana"],
		["cana", "capernaum"],
		["capernaum", "bethsaida"],
		["capernaum", "magdala"],
		["bethsaida", "chorazin"],
		["magdala", "tiberias"],
		["tiberias", "gadara"],
		["cana", "samaria"],
		["samaria", "jericho"],
		["jericho", "bethany"],
		["bethany", "bethlehem"],
		["bethlehem", "jerusalem"],
		["bethany", "jerusalem"]
	]

	for conn in connections:
		var loc1 = str(conn[0])
		var loc2 = str(conn[1])
		if locations.has(loc1) and locations.has(loc2):
			var location1: WorldLocation = locations[loc1]
			var location2: WorldLocation = locations[loc2]
			location1.connected_to.append(loc2)
			location2.connected_to.append(loc1)

func get_location(location_id: String) -> WorldLocation:
	if locations.has(location_id):
		return locations[location_id]
	return null

func can_travel_to(location_id: String) -> bool:
	var target = get_location(location_id)
	if target == null:
		return false
	if not GameState.unlocked_towns.has(location_id):
		return false

	var current_town_id = String(GameState.current_town).to_lower()

	if GameState.unlocked_fast_travel.has(location_id):
		return true

	var current = get_location(current_town_id)
	if current and location_id in current.connected_to:
		return true

	return false

func travel_to(location_id: String, method: TravelMethod = TravelMethod.WALK) -> bool:
	if not can_travel_to(location_id):
		return false
	if method == TravelMethod.FAST_TRAVEL and not GameState.unlocked_fast_travel.has(location_id):
		return false

	GameState.change_scene(GameState.GameScene.TOWN, {"town": location_id})
	return true

func get_path(from_id: String, to_id: String) -> Array[String]:
	if not locations.has(from_id) or not locations.has(to_id):
		return []

	var queue: Array = [[from_id, [from_id]]]
	var visited: Dictionary = {from_id: true}

	while queue.size() > 0:
		var entry = queue.pop_front()
		var current_id: String = entry[0]
		var path: Array[String] = []
		path.assign(entry[1])

		if current_id == to_id:
			return path

		var current_loc: WorldLocation = locations[current_id]
		for neighbor in current_loc.connected_to:
			if not visited.has(neighbor):
				visited[neighbor] = true
				var new_path = path.duplicate()
				new_path.append(neighbor)
				queue.append([neighbor, new_path])

	return []
