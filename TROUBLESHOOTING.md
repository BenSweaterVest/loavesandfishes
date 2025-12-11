# Troubleshooting Guide - Loaves and Fishes

Common issues and solutions for developing and playing Loaves and Fishes.

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [JSON Data Issues](#json-data-issues)
3. [Asset Loading Issues](#asset-loading-issues)
4. [Battle System Issues](#battle-system-issues)
5. [Save/Load Issues](#save-load-issues)
6. [Performance Issues](#performance-issues)
7. [Godot Migration Issues](#godot-migration-issues)
8. [Development Environment](#development-environment)

---

## Installation Issues

### Python Version Mismatch

**Symptoms:**
- Import errors
- Syntax errors about f-strings or type hints
- `ModuleNotFoundError`

**Cause:** Python version too old (requires 3.8+)

**Solution:**
```bash
# Check Python version
python --version

# Should show Python 3.8 or higher
# If not, install Python 3.8+

# On Ubuntu/Debian
sudo apt install python3.8

# On macOS with Homebrew
brew install python@3.8

# On Windows
# Download from python.org
```

### Missing Dependencies

**Symptoms:**
- `ModuleNotFoundError: No module named 'pygame'`
- Game won't start

**Cause:** Dependencies not installed

**Solution:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install pygame

# If using virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Permission Errors

**Symptoms:**
- `PermissionError` when saving files
- Can't create save directory

**Cause:** Insufficient file permissions

**Solution:**
```bash
# Make saves directory writable
chmod 755 saves/

# On Windows, run as administrator or check folder permissions
```

---

## JSON Data Issues

### JSON Syntax Errors

**Symptoms:**
- `json.JSONDecodeError: Expecting ',' delimiter`
- Game crashes on startup
- Data not loading

**Cause:** Invalid JSON syntax (missing comma, bracket, quote)

**Common mistakes:**
```json
// ❌ WRONG: Trailing comma
{
  "fish": [
    {"id": "fish1"},
    {"id": "fish2"},  // ← Remove this comma!
  ]
}

// ✅ CORRECT: No trailing comma
{
  "fish": [
    {"id": "fish1"},
    {"id": "fish2"}
  ]
}

// ❌ WRONG: Missing quotes
{
  id: "fish1"  // ← id needs quotes
}

// ✅ CORRECT: Quoted keys
{
  "id": "fish1"
}
```

**Solution:**
1. Use a JSON validator: https://jsonlint.com/
2. Check for:
   - Missing commas between items
   - Trailing commas before closing brackets
   - Missing quotes around keys
   - Missing closing brackets/braces

### Dual-Text Field Missing

**Symptoms:**
- `KeyError: 'default'` or `KeyError: 'christian_edition'`
- Text not displaying correctly

**Cause:** Text field doesn't have both dual-text versions

**Wrong:**
```json
{
  "flavor_text": "Just a string"  // ❌ Missing dual-text structure
}
```

**Correct:**
```json
{
  "flavor_text": {
    "default": "Irreverent version here",
    "christian_edition": "Reverent version here"
  }
}
```

**Solution:**
All user-facing text must have dual-text structure. Check `TONE_GUIDE.md` for guidelines.

### Fish/Enemy ID Not Found

**Symptoms:**
- `None` returned when getting fish
- "Fish not found" errors
- Enemies not appearing

**Cause:** ID mismatch between code and JSON

**Example:**
```python
# Code tries to load:
fish = get_fish("holy_mackerel")

# But JSON has:
{
  "id": "Holy_Mackerel"  // ❌ Wrong capitalization!
}
```

**Solution:**
1. IDs are **case-sensitive**
2. Use **lowercase** with underscores: `holy_mackerel`
3. Search JSON file for exact ID
4. Verify spelling

### Type Effectiveness Missing

**Symptoms:**
- All attacks deal 1.0x damage
- No super-effective messages

**Cause:** `TYPE_CHART` incomplete or types misspelled

**Solution:**
```python
# Check constants.py TYPE_CHART
# Verify type names match exactly

# ❌ WRONG
fish_type = "water"  # Lowercase
TYPE_CHART["Water"]["Holy"]  # ← KeyError!

# ✅ CORRECT
fish_type = "Water"  # Capitalized
TYPE_CHART["Water"]["Holy"]  # Works!
```

All types must be capitalized: `Holy`, `Water`, `Earth`, `Spirit`, `Dark`

---

## Asset Loading Issues

### Image Not Displaying

**Symptoms:**
- Black square where sprite should be
- `pygame.error: Couldn't open file`
- Missing visuals

**Cause:** File path incorrect or file missing

**Solution:**

1. **Check file exists:**
   ```bash
   ls assets/images/fish/holy_mackerel.png
   # Should show file, not "No such file"
   ```

2. **Check path in JSON:**
   ```json
   {
     "sprite": "assets/images/fish/holy_mackerel.png"
     // ❌ NOT: "assets/images/fish/Holy_Mackerel.PNG"
     // ❌ NOT: "assets/fish/holy_mackerel.png"
   }
   ```

3. **Check capitalization:**
   - Linux/Mac are case-sensitive
   - `holy_mackerel.png` ≠ `Holy_Mackerel.png`

4. **Verify format:**
   - Must be PNG (not BMP, GIF, etc.)
   - Check actual format: `file holy_mackerel.png`

### Audio Not Playing

**Symptoms:**
- No sound
- `pygame.error: Couldn't open audio file`
- Music not looping

**Cause:** Audio file format issues or mixer not initialized

**Solution:**

1. **Initialize mixer before loading:**
   ```python
   import pygame
   pygame.init()
   pygame.mixer.init()  # ← Must call this!

   # Now load audio
   pygame.mixer.music.load("assets/audio/music/battle_theme.ogg")
   ```

2. **Use correct format:**
   - Music: OGG Vorbis (not MP3)
   - SFX: WAV or OGG

3. **Check file integrity:**
   ```bash
   # Try playing in media player
   vlc assets/audio/music/battle_theme.ogg

   # If corrupted, re-export from audio editor
   ```

4. **Volume issues:**
   ```python
   # Set volume (0.0 to 1.0)
   pygame.mixer.music.set_volume(0.5)

   # Check not muted
   if pygame.mixer.music.get_volume() == 0:
       pygame.mixer.music.set_volume(0.7)
   ```

### Asset File Too Large

**Symptoms:**
- Slow loading times
- Game stutters when loading
- High memory usage

**Cause:** Asset files too large (4K images, uncompressed audio)

**Solution:**

**For images:**
```bash
# Resize oversized images
convert huge_image.png -resize 128x128 optimized.png

# Check file size
ls -lh assets/images/fish/*.png
# Should be <100KB per sprite
```

**For audio:**
```bash
# Convert WAV to OGG (much smaller)
ffmpeg -i music.wav -q:a 5 music.ogg

# Reduce bitrate if still too large
ffmpeg -i music.ogg -b:a 128k music_compressed.ogg
```

**Recommended maximum sizes:**
- Fish/enemy sprites: 100KB
- Backgrounds: 500KB
- Music: 5MB per track
- SFX: 100KB

---

## Battle System Issues

### Damage Always 1

**Symptoms:**
- All attacks deal exactly 1 damage
- No variance in damage

**Cause:** Defense formula capping damage at minimum

**Solution:**

Check fish/enemy stats:
```python
# If defense is VERY high, damage gets capped
# Defense 100 + damage 10 = actual damage 1

# Verify stats are reasonable
print(f"Fish ATK: {fish.atk}")
print(f"Enemy DEF: {enemy.defense}")

# Expected ranges (level 1):
# ATK: 15-30
# DEF: 10-25
```

### Infinite Loop in Battle

**Symptoms:**
- Battle never ends
- Turn count keeps increasing
- No victory/defeat

**Cause:** Victory/defeat condition not checked

**Solution:**

```python
# In battle.py, verify these are called:
if self.active_enemy.is_defeated():
    self._handle_enemy_defeat()  # ← Must call this

if self.active_fish.is_fainted():
    self._handle_fish_faint()    # ← Must call this
```

### XP Not Gained

**Symptoms:**
- Fish never level up
- XP stays at 0

**Cause:** XP not awarded or formula incorrect

**Solution:**

```python
# Check XP is awarded in battle.py
self.active_fish.gain_xp(actual_damage)  # ← Should be called

# Check XP formula in fish.py
def gain_xp(self, amount: int) -> bool:
    self.xp += amount  # ← Verify this line exists

# Check XP display
print(f"Fish XP: {fish.xp}/{fish.xp_to_next_level}")
```

### Miracle Meter Not Filling

**Symptoms:**
- Miracle meter stays at 0
- Can never use miracles

**Cause:** Meter gain rates too low or not being called

**Solution:**

```python
# Check in battle.py after dealing damage
self.player.add_miracle_meter(actual_damage * 0.1)

# Check in battle.py after taking damage
self.player.add_miracle_meter(actual_damage * 0.2)

# Verify constants.py values
MIRACLE_GAIN_PER_DAMAGE_DEALT = 0.1   # Not 0.01!
MIRACLE_GAIN_PER_DAMAGE_TAKEN = 0.2   # Not 0.02!
```

### Fish Can't Use Moves

**Symptoms:**
- "Fish cannot use that move!" message
- All moves disabled

**Cause:** Status effect preventing moves or move index out of range

**Solution:**

```python
# Check status effects
print(fish.status_effects)  # Should be []

# If frozen/asleep, fish can't act
if "frozen" in fish.status_effects:
    fish.remove_status_effect("frozen")

# Check move index
print(f"Known moves: {len(fish.known_moves)}")  # Should be 1-4
# If trying to use move 2 but only have 1 move → Error

# Check move level requirements
for move in fish.all_moves:
    print(f"{move['name']}: Level {move['level']}")
# Fish must be high enough level to know move
```

---

## Save/Load Issues

### Can't Save Game

**Symptoms:**
- `PermissionError` when saving
- Save file not created
- Progress not persisted

**Cause:** Saves directory doesn't exist or no permissions

**Solution:**

```bash
# Create saves directory
mkdir -p saves

# Set permissions
chmod 755 saves

# On Windows, check folder isn't read-only
# Right-click saves folder → Properties → Uncheck "Read-only"
```

### Save File Corrupted

**Symptoms:**
- `json.JSONDecodeError` when loading
- Game crashes on load
- "Save file corrupted" error

**Cause:** Save file has invalid JSON (game crashed during save)

**Solution:**

1. **Try loading backup:**
   ```bash
   # Rename corrupted save
   mv saves/save1.loaves saves/save1.loaves.corrupted

   # If backup exists, use it
   cp saves/save1.loaves.backup saves/save1.loaves
   ```

2. **Manually fix JSON:**
   ```bash
   # Open in text editor
   nano saves/save1.loaves

   # Validate at jsonlint.com
   # Fix syntax errors
   # Save
   ```

3. **If unfixable, start new game:**
   ```bash
   rm saves/save1.loaves
   # Game will create fresh save
   ```

### Fish Stats Wrong After Loading

**Symptoms:**
- Loaded fish have wrong stats
- HP higher/lower than expected
- Stats don't match level

**Cause:** Save file has old stats (not recalculated)

**Solution:**

This is actually **correct behavior**! When loading:
```python
# Stats are recalculated from base stats + level
# This ensures balance changes in fish.json apply to old saves

fish = Fish.from_dict(saved_data, fish_data)
# ↑ Recalculates stats based on current fish.json
```

If stats seem wrong:
1. Check `fish.json` - did you change base stats?
2. Verify level is correct in save file
3. Check for stat modifiers (buffs/debuffs)

---

## Performance Issues

### Game Running Slow

**Symptoms:**
- Low FPS
- Stuttering
- Laggy UI

**Causes & Solutions:**

1. **Too many assets loaded at once**
   ```python
   # ❌ WRONG: Load everything at start
   all_images = [load(f) for f in all_files]

   # ✅ CORRECT: Load only what's needed
   current_scene_images = load_scene_assets(scene_name)
   ```

2. **No FPS cap**
   ```python
   # Add FPS limit in main loop
   clock = pygame.time.Clock()

   while running:
       clock.tick(60)  # ← Cap at 60 FPS
       # ... game loop
   ```

3. **Inefficient rendering**
   ```python
   # ❌ WRONG: Redraw everything every frame
   screen.fill(BLACK)
   draw_all_sprites()

   # ✅ CORRECT: Only redraw changed areas
   dirty_rects = update_sprites()
   pygame.display.update(dirty_rects)
   ```

### Memory Leak

**Symptoms:**
- Memory usage grows over time
- Game eventually crashes
- Slowdown after playing for a while

**Cause:** Objects not being garbage collected

**Solution:**

```python
# Clear references when done
def end_battle(self):
    self.log.clear()      # Clear battle log
    self.enemies = []     # Clear enemy list
    self.active_fish = None
    self.active_enemy = None

# Use weak references for callbacks
import weakref
callback = weakref.ref(some_object)
```

### Slow JSON Loading

**Symptoms:**
- Long startup time
- Delay when changing scenes

**Cause:** Re-loading JSON files every time

**Solution:**

Use the DataLoader cache system (already implemented):
```python
# ✅ CORRECT: Uses cache
loader = get_data_loader()  # Singleton
fish_data = loader.get_fish_data()  # Cached after first call

# ❌ WRONG: Manual loading
with open("fish.json") as f:
    fish_data = json.load(f)  # Loads from disk every time
```

Cache is automatic if using `get_data_loader()`!

---

## Godot Migration Issues

### Python Code Won't Run in Godot

**Symptoms:**
- Syntax errors in GDScript
- Python imports don't work

**Cause:** Godot uses GDScript, not Python

**Solution:**

You must **translate** Python code to GDScript. They're similar but not identical.

**Python:**
```python
class Fish:
    def __init__(self, fish_id, fish_data, level):
        self.fish_id = fish_id
        self.level = level
```

**GDScript:**
```gdscript
extends Node
class_name Fish

var fish_id: String
var level: int

func _init(p_fish_id: String, fish_data: Dictionary, p_level: int):
    fish_id = p_fish_id
    level = p_level
```

See `GODOT_MIGRATION.md` for full translation guide.

### JSON Not Loading in Godot

**Symptoms:**
- `FileAccess` errors
- Data not found

**Cause:** Different file loading in Godot

**Solution:**

**Python:**
```python
with open("src/data/fish.json") as f:
    data = json.load(f)
```

**GDScript:**
```gdscript
var file = FileAccess.open("res://src/data/fish.json", FileAccess.READ)
var json = JSON.new()
var data = json.parse_string(file.get_as_text())
```

Paths use `res://` instead of relative paths.

### Assets Not Importing

**Symptoms:**
- Images/audio not appearing
- "Failed to load resource" errors

**Cause:** Assets not in Godot project folder

**Solution:**

1. **Place assets in project:**
   ```
   project/
   ├── assets/
   │   ├── images/
   │   └── audio/
   └── project.godot
   ```

2. **Wait for import:**
   - Godot auto-imports on file add
   - Check `.import` files created
   - Check Import tab in editor

3. **Check import settings:**
   - Select asset in FileSystem
   - Check Import tab
   - Reimport if needed

---

## Development Environment

### IDE Autocomplete Not Working

**Symptoms:**
- No code completion
- Type hints not recognized

**Cause:** IDE doesn't recognize Python version or virtual environment

**Solution:**

**VS Code:**
```json
// .vscode/settings.json
{
  "python.pythonPath": "venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

**PyCharm:**
1. File → Settings → Project → Python Interpreter
2. Select virtual environment interpreter
3. Apply

### Import Errors in IDE

**Symptoms:**
- Red underlines on imports
- "Module not found" warnings
- Code runs fine but IDE complains

**Cause:** IDE doesn't recognize project structure

**Solution:**

**Mark source root:**
- Right-click `src/` folder
- Mark Directory As → Sources Root

**Or add to PYTHONPATH:**
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/loavesandfishes/src"
```

### Git Issues

**Symptoms:**
- Can't commit
- Merge conflicts
- Accidental commits

**Common fixes:**

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD

# Resolve merge conflict
git status  # See conflicted files
# Edit files, remove <<<<<<< ======= >>>>>>> markers
git add .
git commit

# Revert to previous commit
git log  # Find commit hash
git revert <commit-hash>
```

---

## Getting More Help

If your issue isn't covered here:

1. **Check existing docs:**
   - `README.md` - Project overview
   - `DEVELOPER_GUIDE.md` - Architecture and patterns
   - `ASSETS_GUIDE.md` - Asset creation and loading
   - `CONTRIBUTING.md` - Code standards
   - `GODOT_MIGRATION.md` - Godot-specific issues

2. **Search codebase:**
   ```bash
   # Find where something is defined
   grep -r "def calculate_damage" src/

   # Find where something is used
   grep -r "get_fish_by_id" src/
   ```

3. **Add debug logging:**
   ```python
   # Temporary debugging
   print(f"DEBUG: fish_id={fish_id}, data={fish_data}")

   # Or use logging module
   import logging
   logging.debug(f"Loading fish: {fish_id}")
   ```

4. **Check Python docs:**
   - https://docs.python.org/3/
   - https://www.pygame.org/docs/

5. **Check Godot docs:**
   - https://docs.godotengine.org/en/stable/

6. **File an issue:**
   - Describe problem clearly
   - Include error messages
   - Share relevant code snippets
   - Note what you've already tried

---

## Quick Diagnostic Checklist

When something goes wrong, check these first:

- [ ] Python 3.8+ installed?
- [ ] Dependencies installed? (`pip list`)
- [ ] Running from project root? (`pwd`)
- [ ] JSON files valid? (jsonlint.com)
- [ ] Asset files exist and spelled correctly?
- [ ] IDs match between JSON and code?
- [ ] Dual-text structure used for all user-facing text?
- [ ] Data loader initialized? (`get_data_loader()`)
- [ ] Pygame mixer initialized for audio?
- [ ] Latest code pulled? (`git pull`)
- [ ] Tried clearing cache? (restart game/IDE)

**Still stuck? Add debug logging and trace the issue step-by-step!**

---

Happy debugging! 🐛🔨
