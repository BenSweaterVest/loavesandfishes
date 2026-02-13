class_name Player
extends Resource

@export var player_name: String = "Jesus"
@export var level: int = 1
@export var xp: int = 0
@export var xp_to_next_level: int = 100

@export var base_hp: int = 50
@export var max_hp: int
@export var current_hp: int

@export var active_party: Array[Fish] = []
@export var fish_storage: Array[Fish] = []
@export var recruited_apostles: Array[String] = []

@export var bread_items: Dictionary = {}
@export var money: int = 0
@export var equipped_robe: Variant = null
@export var equipped_accessory: Variant = null

@export var current_town: String = "nazareth"
@export var visited_towns: Array[String] = ["nazareth"]
@export var completed_quests: Array[String] = []
@export var found_parables: Array[String] = []

@export var miracle_meter: float = 0.0
@export var battles_won: int = 0
@export var battles_lost: int = 0
@export var difficulty: String = "normal"

func _init(p_name: String = "Jesus") -> void:
	player_name = p_name
	max_hp = calculate_stat(base_hp, level)
	current_hp = max_hp

func calculate_stat(base_stat: int, level_value: int) -> int:
	var growth_rate := 0.05
	return int(base_stat * (1.0 + growth_rate * (level_value - 1)))

func add_fish_to_party(fish: Fish) -> bool:
	if active_party.size() >= 4:
		return false
	active_party.append(fish)
	return true

func add_fish_to_storage(fish: Fish) -> void:
	fish_storage.append(fish)

func remove_fish_from_party(index: int) -> Fish:
	if index >= 0 and index < active_party.size():
		return active_party.pop_at(index)
	return null

func swap_fish(party_index: int, storage_index: int) -> bool:
	if party_index < 0 or party_index >= active_party.size():
		return false
	if storage_index < 0 or storage_index >= fish_storage.size():
		return false

	var temp = active_party[party_index]
	active_party[party_index] = fish_storage[storage_index]
	fish_storage[storage_index] = temp
	return true

func get_active_fish() -> Array[Fish]:
	var usable: Array[Fish] = []
	for fish in active_party:
		if not fish.is_fainted():
			usable.append(fish)
	return usable

func has_usable_fish() -> bool:
	return get_active_fish().size() > 0

func add_bread_item(item_id: String, quantity: int = 1) -> void:
	if bread_items.has(item_id):
		bread_items[item_id] = int(bread_items[item_id]) + quantity
	else:
		bread_items[item_id] = quantity

func remove_bread_item(item_id: String, quantity: int = 1) -> bool:
	if not bread_items.has(item_id) or int(bread_items[item_id]) < quantity:
		return false

	bread_items[item_id] = int(bread_items[item_id]) - quantity
	if int(bread_items[item_id]) <= 0:
		bread_items.erase(item_id)
	return true

func has_item(item_id: String, quantity: int = 1) -> bool:
	return bread_items.has(item_id) and int(bread_items[item_id]) >= quantity

func add_money(amount: int) -> void:
	money += amount

func spend_money(amount: int) -> bool:
	if money >= amount:
		money -= amount
		return true
	return false

func recruit_apostle(apostle_id: String) -> void:
	if not recruited_apostles.has(apostle_id):
		recruited_apostles.append(apostle_id)

func has_apostle(apostle_id: String) -> bool:
	return recruited_apostles.has(apostle_id)

func equip_robe(robe: Dictionary) -> void:
	equipped_robe = robe

func equip_accessory(accessory: Dictionary) -> void:
	equipped_accessory = accessory

func get_defense() -> int:
	var base_def = 10
	if equipped_robe is Dictionary:
		base_def += int(equipped_robe.get("def_bonus", 0))
	return base_def

func take_damage(damage: int) -> int:
	var defense = get_defense()
	var actual_damage = max(1, damage - int(defense / 2))
	current_hp = max(0, current_hp - actual_damage)
	return actual_damage

func heal(amount: int) -> int:
	var old_hp = current_hp
	current_hp = min(max_hp, current_hp + amount)
	return current_hp - old_hp

func is_defeated() -> bool:
	return current_hp <= 0 or not has_usable_fish()

func gain_xp(amount: int) -> bool:
	xp += amount
	if xp >= xp_to_next_level:
		return level_up()
	return false

func level_up() -> bool:
	if level >= 50:
		return false

	level += 1
	xp -= xp_to_next_level

	var old_max_hp = max_hp
	max_hp = calculate_stat(base_hp, level)
	current_hp += (max_hp - old_max_hp)
	return true

func add_miracle_meter(amount: float) -> void:
	miracle_meter = min(100.0, miracle_meter + amount)

func is_miracle_ready() -> bool:
	return miracle_meter >= 100.0

func use_miracle() -> void:
	miracle_meter = 0.0

func visit_town(town_id: String) -> void:
	current_town = town_id
	if not visited_towns.has(town_id):
		visited_towns.append(town_id)

func complete_quest(quest_id: String) -> void:
	if not completed_quests.has(quest_id):
		completed_quests.append(quest_id)

func find_parable(parable_id: String) -> void:
	if not found_parables.has(parable_id):
		found_parables.append(parable_id)

func get_parable_count() -> int:
	return found_parables.size()

func rest_at_inn() -> void:
	current_hp = max_hp
	for fish in active_party:
		fish.current_hp = fish.max_hp
		fish.clear_status_effects()

func to_dict() -> Dictionary:
	var active_list: Array = []
	var storage_list: Array = []
	for fish in active_party:
		active_list.append(fish.to_dict())
	for fish in fish_storage:
		storage_list.append(fish.to_dict())

	return {
		"name": player_name,
		"level": level,
		"xp": xp,
		"current_hp": current_hp,
		"active_party": active_list,
		"fish_storage": storage_list,
		"recruited_apostles": recruited_apostles,
		"bread_items": bread_items,
		"money": money,
		"equipped_robe": equipped_robe,
		"equipped_accessory": equipped_accessory,
		"current_town": current_town,
		"visited_towns": visited_towns,
		"completed_quests": completed_quests,
		"found_parables": found_parables,
		"miracle_meter": miracle_meter,
		"battles_won": battles_won,
		"battles_lost": battles_lost,
		"difficulty": difficulty
	}

static func from_dict(data: Dictionary) -> Player:
	var player = Player.new(str(data.get("name", "Jesus")))
	player.level = int(data.get("level", 1))
	player.xp = int(data.get("xp", 0))
	player.max_hp = player.calculate_stat(player.base_hp, player.level)
	player.current_hp = int(data.get("current_hp", player.max_hp))

	var loaded_party: Array[Fish] = []
	var loaded_storage: Array[Fish] = []
	for fish_data in data.get("active_party", []):
		var fish = Fish.from_dict(fish_data)
		if fish:
			loaded_party.append(fish)
	for fish_data in data.get("fish_storage", []):
		var fish = Fish.from_dict(fish_data)
		if fish:
			loaded_storage.append(fish)

	player.active_party.assign(loaded_party)
	player.fish_storage.assign(loaded_storage)
	player.recruited_apostles.assign(data.get("recruited_apostles", []))
	player.bread_items = data.get("bread_items", {})
	player.money = int(data.get("money", 0))
	player.equipped_robe = data.get("equipped_robe", null)
	player.equipped_accessory = data.get("equipped_accessory", null)
	player.current_town = str(data.get("current_town", "nazareth"))
	player.visited_towns.assign(data.get("visited_towns", []))
	player.completed_quests.assign(data.get("completed_quests", []))
	player.found_parables.assign(data.get("found_parables", []))
	player.miracle_meter = float(data.get("miracle_meter", 0.0))
	player.battles_won = int(data.get("battles_won", 0))
	player.battles_lost = int(data.get("battles_lost", 0))
	player.difficulty = str(data.get("difficulty", "normal"))

	return player
