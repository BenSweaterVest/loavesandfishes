extends Node
class_name GameState

# --- SIGNALS (For event-driven UI updates) ---
signal scene_changed(new_scene: GameScene)
signal town_changed(new_town: String)
signal story_flag_updated(flag: String, value: bool)
signal quest_started(quest_id: String)
signal quest_completed(quest_id: String)

enum GameScene {
	TITLE,
	TOWN,
	WORLD_MAP,
	BATTLE,
	MENU,
	SHOP,
	DIALOGUE,
	CUTSCENE,
	FISHING,
	GAME_OVER,
	CREDITS
}

enum EncounterType {
	NONE,
	WILD_BATTLE,
	NPC_DIALOGUE,
	TREASURE,
	PARABLE
}

# --- STATE VARIABLES ---
var player

var current_scene: GameScene = GameScene.TITLE
var previous_scene: GameScene = GameScene.TITLE
var current_town: String = "Nazareth"

var current_shop = null
var current_battle = null
var current_dialogue = null
var current_cutscene = null

var active_quests: Array[String] = []
var completed_quests: Array[String] = []
var collected_parables: Array[String] = []
var parables_seen: Array[String] = []

var story_flags: Dictionary = {
	"game_started": false,
	"first_fish_caught": false,
	"first_battle_won": false,
	"first_apostle_recruited": false,
	"cana_wedding_complete": false,
	"five_thousand_fed": false,
	"lazarus_raised": false,
	"temple_cleansed": false,
	"final_battle_unlocked": false,
	"game_completed": false
}

var unlocked_towns: Array[String] = ["Nazareth"]
var unlocked_fast_travel: Array[String] = []
var unlocked_miracles: Array[String] = []

var encounter_rate: float = 0.1
var steps_since_encounter: int = 0

var playtime: float = 0.0
var total_steps: int = 0
var fish_caught: int = 0
var battles_won: int = 0
var battles_fled: int = 0

func change_scene(new_scene: GameScene, params: Dictionary = {}) -> void:
	previous_scene = current_scene
	current_scene = new_scene
	if new_scene == GameScene.TOWN:
		var next_town = params.get("town", current_town)
		if next_town != current_town:
			current_town = next_town
			town_changed.emit(current_town)
	elif new_scene == GameScene.SHOP:
		current_shop = params.get("shop", null)
	elif new_scene == GameScene.BATTLE:
		current_battle = params.get("battle", null)
	elif new_scene == GameScene.DIALOGUE:
		current_dialogue = params.get("dialogue", null)
	elif new_scene == GameScene.CUTSCENE:
		current_cutscene = params.get("cutscene", null)

	scene_changed.emit(current_scene)

func return_to_previous_scene() -> void:
	var temp = current_scene
	current_scene = previous_scene
	previous_scene = temp
	if current_scene == GameScene.TOWN:
		town_changed.emit(current_town)
	scene_changed.emit(current_scene)

func take_step() -> EncounterType:
	total_steps += 1
	steps_since_encounter += 1

	if randf() < encounter_rate:
		steps_since_encounter = 0
		var roll = randf()
		if roll < 0.7:
			return EncounterType.WILD_BATTLE
		if roll < 0.85:
			return EncounterType.NPC_DIALOGUE
		if roll < 0.95:
			return EncounterType.TREASURE
		return EncounterType.PARABLE

	return EncounterType.NONE

func unlock_town(town: String) -> void:
	if not unlocked_towns.has(town):
		unlocked_towns.append(town)

func unlock_fast_travel(town: String) -> void:
	if not unlocked_fast_travel.has(town) and unlocked_towns.has(town):
		unlocked_fast_travel.append(town)

func unlock_miracle(miracle: String) -> void:
	if not unlocked_miracles.has(miracle):
		unlocked_miracles.append(miracle)

func set_story_flag(flag: String, value: bool = true) -> void:
	if story_flags.has(flag):
		story_flags[flag] = value
		story_flag_updated.emit(flag, value)

func get_story_flag(flag: String) -> bool:
	return bool(story_flags.get(flag, false))

func start_quest(quest_id: String) -> void:
	if not active_quests.has(quest_id) and not completed_quests.has(quest_id):
		active_quests.append(quest_id)
		quest_started.emit(quest_id)

func complete_quest(quest_id: String) -> void:
	if active_quests.has(quest_id):
		active_quests.erase(quest_id)
		completed_quests.append(quest_id)
		quest_completed.emit(quest_id)

func collect_parable(parable_id: String) -> void:
	if not collected_parables.has(parable_id):
		collected_parables.append(parable_id)

func can_access_town(town: String) -> bool:
	return unlocked_towns.has(town)

func get_current_region() -> String:
	var region_map = {
		"Nazareth": "Galilee",
		"Cana": "Galilee",
		"Capernaum": "Galilee",
		"Bethsaida": "Coastal",
		"Magdala": "Coastal",
		"Chorazin": "Coastal",
		"Tiberias": "Coastal",
		"Gadara": "Gentile",
		"Samaria": "Gentile",
		"Jericho": "Judean",
		"Bethany": "Judean",
		"Bethlehem": "Judean",
		"Jerusalem": "Jerusalem"
	}

	return str(region_map.get(current_town, "Unknown"))

func get_available_encounters() -> Array:
	return []

func to_dict() -> Dictionary:
	return {
		"current_scene": current_scene,
		"current_town": current_town,
		"active_quests": active_quests,
		"completed_quests": completed_quests,
		"collected_parables": collected_parables,
		"story_flags": story_flags,
		"unlocked_towns": unlocked_towns,
		"unlocked_fast_travel": unlocked_fast_travel,
		"unlocked_miracles": unlocked_miracles,
		"playtime": playtime,
		"total_steps": total_steps,
		"fish_caught": fish_caught,
		"battles_won": battles_won,
		"battles_fled": battles_fled
	}

func from_dict(data: Dictionary) -> void:
	var scene_value = data.get("current_scene", GameScene.TITLE)
	if scene_value is int:
		current_scene = scene_value
	else:
		current_scene = GameScene.TITLE

	current_town = str(data.get("current_town", current_town))
	active_quests = data.get("active_quests", [])
	completed_quests = data.get("completed_quests", [])
	collected_parables = data.get("collected_parables", [])
	story_flags = data.get("story_flags", story_flags)
	unlocked_towns = data.get("unlocked_towns", unlocked_towns)
	unlocked_fast_travel = data.get("unlocked_fast_travel", unlocked_fast_travel)
	unlocked_miracles = data.get("unlocked_miracles", unlocked_miracles)
	playtime = float(data.get("playtime", 0.0))
	total_steps = int(data.get("total_steps", 0))
	fish_caught = int(data.get("fish_caught", 0))
	battles_won = int(data.get("battles_won", 0))
	battles_fled = int(data.get("battles_fled", 0))
