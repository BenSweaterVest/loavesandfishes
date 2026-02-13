extends Node
class_name Constants

const TYPE_CHART: Dictionary = {
	"Holy": {
		"Holy": 1.0,
		"Water": 1.0,
		"Earth": 1.0,
		"Spirit": 1.0,
		"Dark": 2.0
	},
	"Water": {
		"Holy": 1.0,
		"Water": 0.5,
		"Earth": 2.0,
		"Spirit": 1.0,
		"Dark": 1.0
	},
	"Earth": {
		"Holy": 1.0,
		"Water": 0.5,
		"Earth": 1.0,
		"Spirit": 1.0,
		"Dark": 1.0
	},
	"Spirit": {
		"Holy": 1.5,
		"Water": 1.0,
		"Earth": 1.0,
		"Spirit": 1.0,
		"Dark": 1.5
	},
	"Dark": {
		"Holy": 0.5,
		"Water": 1.0,
		"Earth": 1.0,
		"Spirit": 0.5,
		"Dark": 1.0
	}
}

func get_type_effectiveness(attack_type: String, defend_type: String) -> float:
	if TYPE_CHART.has(attack_type):
		var row = TYPE_CHART[attack_type]
		if row is Dictionary and row.has(defend_type):
			return float(row[defend_type])
	return 1.0
