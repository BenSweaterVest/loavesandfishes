@tool
extends EditorScript

const INPUT_DIR = "res://assets/raw/"
const OUTPUT_DIR = "res://assets/sprites/fish/"
const TARGET_SIZE = Vector2i(128, 128)
const CHROMA_KEY = Color(1.0, 0.0, 1.0) # Pure magenta
const TOLERANCE = 0.15

func _run() -> void:
	print("Starting Batch Image Processing...")

	# Create directories if they don't exist
	if not DirAccess.dir_exists_absolute(INPUT_DIR):
		DirAccess.make_dir_absolute(INPUT_DIR)
	if not DirAccess.dir_exists_absolute(OUTPUT_DIR):
		DirAccess.make_dir_absolute(OUTPUT_DIR)

	var dir = DirAccess.open(INPUT_DIR)
	if dir:
		dir.list_dir_begin()
		var file_name = dir.get_next()
		while file_name != "":
			var is_image = file_name.ends_with(".png") or file_name.ends_with(".jpg")
			if not dir.current_is_dir() and is_image:
				var input_path = INPUT_DIR + file_name
				var output_path = OUTPUT_DIR + file_name.get_basename() + ".png"
				_process_image(input_path, output_path)
			file_name = dir.get_next()
		print("Batch Processing Complete!")

func _process_image(in_path: String, out_path: String) -> void:
	var img = Image.load_from_file(in_path)
	if img == null:
		push_error("Failed to load: " + in_path)
		return

	# Downscale using NEAREST interpolation for a crisp, retro pixel-art look
	img.resize(TARGET_SIZE.x, TARGET_SIZE.y, Image.INTERPOLATE_NEAREST)

	# Add alpha channel for transparency
	if img.get_format() != Image.FORMAT_RGBA8:
		img.convert(Image.FORMAT_RGBA8)

	# Chroma key (remove magenta background)
	for y in range(img.get_height()):
		for x in range(img.get_width()):
			var pixel_color = img.get_pixel(x, y)
			# If the pixel is close to magenta, make it fully transparent
			if pixel_color.distance_to(CHROMA_KEY) < TOLERANCE:
				img.set_pixel(x, y, Color(0, 0, 0, 0))

	# Save the finalized sprite
	img.save_png(out_path)
	print("Saved clean sprite: ", out_path)
