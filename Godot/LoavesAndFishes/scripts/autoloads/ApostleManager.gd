extends Node

func execute_overworld_ability(apostle_id: String) -> bool:
	match apostle_id.to_lower():
		"bartholomew":
			return true
		"peter":
			return true
		"andrew":
			return true
		"james_zebedee", "james":
			return true
		"john":
			return true
		"philip":
			return true
		"matthew":
			return true
		"simon_zealot":
			return true
		"james_alphaeus":
			return true
		"thomas":
			return true
		"thaddaeus":
			return true
		"judas":
			return true
		_:
			return false

func execute_battle_ability(apostle_id: String, _context: Dictionary = {}) -> bool:
	match apostle_id.to_lower():
		"bartholomew":
			return true
		"peter":
			return true
		"andrew":
			return true
		"james_zebedee", "james":
			return true
		"john":
			return true
		"philip":
			return true
		"matthew":
			return true
		"simon_zealot":
			return true
		"james_alphaeus":
			return true
		"thomas":
			return true
		"thaddaeus":
			return true
		"judas":
			return true
		_:
			return false
