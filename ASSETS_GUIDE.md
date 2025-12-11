# Assets Guide - Images and Audio for Loaves and Fishes

This guide explains how to work with visual and audio assets in Loaves and Fishes, both for the current Python implementation and the future Godot 4.x migration.

---

## Table of Contents

1. [Asset Organization](#asset-organization)
2. [Image Assets](#image-assets)
3. [Audio Assets](#audio-assets)
4. [File Naming Conventions](#file-naming-conventions)
5. [Godot 4.x Integration](#godot-4x-integration)
6. [Creating New Assets](#creating-new-assets)
7. [Asset Specifications](#asset-specifications)
8. [Tools and Resources](#tools-and-resources)

---

## Asset Organization

All game assets are stored in the `assets/` directory, organized by type:

```
assets/
├── images/
│   ├── fish/           # Fish sprites (battle weapons)
│   ├── enemies/        # Enemy sprites
│   ├── apostles/       # Apostle character portraits
│   ├── items/          # Bread item icons
│   ├── backgrounds/    # Battle backgrounds, town scenes
│   ├── ui/             # UI elements, buttons, borders
│   └── icons/          # Game icon, menu icons
├── audio/
│   ├── music/          # Background music tracks
│   ├── sfx/            # Sound effects
│   └── voice/          # Voice lines (future feature)
└── fonts/              # Custom fonts for UI
```

**Design Philosophy:**
- **Organized by category** for easy navigation
- **Separate files** (not sprite sheets) for clarity and modding
- **Descriptive names** that match data IDs in JSON files

---

## Image Assets

### Current Python Implementation

In the Python version, images are referenced by file path in JSON data:

```json
{
  "id": "holy_mackerel",
  "name": "Holy Mackerel",
  "sprite": "assets/images/fish/holy_mackerel.png"
}
```

**Loading images:**
```python
import pygame

# Load image
sprite = pygame.image.load("assets/images/fish/holy_mackerel.png")

# Scale if needed
sprite = pygame.transform.scale(sprite, (64, 64))

# Display
screen.blit(sprite, (x, y))
```

### Image Types

#### 1. **Fish Sprites** (`assets/images/fish/`)
- **Purpose:** Visual representation of fish in battle and menus
- **Recommended size:** 128x128 pixels
- **Format:** PNG with transparency
- **Style:** Pixel art or hand-drawn, colorful and expressive

**Example files:**
- `holy_mackerel.png` - Holy type fish
- `sardine_of_faith.png` - Holy type starter
- `leviathan.png` - Water type legendary

**Naming:** Must match fish ID from `fish.json`

#### 2. **Enemy Sprites** (`assets/images/enemies/`)
- **Purpose:** Visual representation of enemies in battle
- **Recommended size:** 128x128 to 256x256 pixels
- **Format:** PNG with transparency
- **Style:** Match fish style, slightly more detailed for bosses

**Example files:**
- `pharisee.png` - Regular enemy
- `herod_antipas.png` - Boss enemy
- `money_changer.png` - Common enemy

**Naming:** Must match enemy ID from `enemies.json`

#### 3. **Apostle Portraits** (`assets/images/apostles/`)
- **Purpose:** Character portraits for dialogue and menus
- **Recommended size:** 256x256 pixels (face/bust shot)
- **Format:** PNG with transparency or solid background
- **Style:** Higher detail than fish/enemies, shows personality

**Example files:**
- `peter.png` - Peter the Rock
- `john.png` - John the Beloved
- `judas.png` - Judas Iscariot

**Naming:** Must match apostle ID from `apostles.json`

#### 4. **Item Icons** (`assets/images/items/`)
- **Purpose:** Small icons for bread items in inventory
- **Recommended size:** 64x64 pixels
- **Format:** PNG with transparency
- **Style:** Simple, recognizable at small size

**Example files:**
- `manna_bread.png` - Healing item
- `unleavened_bread.png` - Status cure item
- `fish_bread.png` - Revive item

**Naming:** Must match item ID from `items.json`

#### 5. **Backgrounds** (`assets/images/backgrounds/`)
- **Purpose:** Battle backgrounds, town scenes, world map
- **Recommended size:** 1280x720 pixels (16:9 ratio)
- **Format:** PNG or JPEG
- **Style:** Atmospheric, not too busy (doesn't distract from combat)

**Example files:**
- `battle_desert.png` - Desert battle scene
- `battle_sea_of_galilee.png` - Water battle scene
- `town_nazareth.png` - Nazareth town view

#### 6. **UI Elements** (`assets/images/ui/`)
- **Purpose:** Buttons, borders, text boxes, menus
- **Recommended size:** Varies by element
- **Format:** PNG with transparency
- **Style:** Clean, readable, thematic (biblical/ancient)

**Example files:**
- `button_normal.png` - Standard button
- `button_hover.png` - Button hover state
- `textbox_border.png` - Dialogue box border
- `hp_bar.png` - Health bar graphic

---

## Audio Assets

### Music (`assets/audio/music/`)

**Purpose:** Background music for battles, towns, menus

**Format:**
- **Development:** OGG Vorbis (open format, good compression)
- **Alternative:** MP3 (wider compatibility)

**Specifications:**
- **Sample rate:** 44.1kHz
- **Bitrate:** 128-192 kbps (balance quality/file size)
- **Loop-friendly:** Seamless loops for continuous play

**Example files:**
- `battle_theme.ogg` - Standard battle music
- `boss_battle.ogg` - Epic boss music
- `town_peaceful.ogg` - Calm town exploration
- `menu_theme.ogg` - Main menu music

**Naming Convention:**
- Descriptive of where/when it plays
- Match scene names from `towns.json` if applicable

**Loading in Python:**
```python
import pygame

# Load and play music
pygame.mixer.music.load("assets/audio/music/battle_theme.ogg")
pygame.mixer.music.play(-1)  # -1 = loop forever
```

### Sound Effects (`assets/audio/sfx/`)

**Purpose:** Battle sounds, menu interactions, events

**Format:** WAV (uncompressed, instant playback) or OGG

**Specifications:**
- **Sample rate:** 44.1kHz
- **Mono or stereo:** Mono preferred (smaller files)
- **Short duration:** 0.1s - 2s typically

**Example files:**
- `attack_hit.wav` - Attack lands
- `attack_miss.wav` - Attack misses
- `critical_hit.wav` - Critical hit sound
- `fish_faint.wav` - Fish faints
- `heal.wav` - Healing sound
- `menu_select.wav` - Menu navigation
- `menu_confirm.wav` - Confirm selection

**Naming Convention:**
- Action-based: what triggers the sound
- Lowercase with underscores

**Loading in Python:**
```python
import pygame

# Load sound effect
hit_sound = pygame.mixer.Sound("assets/audio/sfx/attack_hit.wav")

# Play sound
hit_sound.play()
```

### Voice Lines (`assets/audio/voice/`) - Future Feature

**Purpose:** Character voice lines, narration

**Format:** OGG Vorbis
**Specifications:** Same as music
**Note:** Not implemented yet, reserved for future expansion

---

## File Naming Conventions

**Golden Rules:**
1. **Use lowercase** for all filenames
2. **Use underscores** instead of spaces: `holy_mackerel.png` not `Holy Mackerel.png`
3. **Match JSON IDs exactly** (critical for data-driven system)
4. **Be descriptive** but concise
5. **Include type suffix** for variants: `_front`, `_back`, `_icon`

**Examples:**
- ✅ `holy_mackerel.png` (matches fish ID)
- ✅ `battle_desert_day.png` (descriptive)
- ✅ `button_normal.png` (shows state)
- ❌ `Holy Mackerel.PNG` (uppercase, spaces)
- ❌ `img001.png` (not descriptive)
- ❌ `holy-mackerel.png` (hyphens instead of underscores)

**ID Matching:**
Your asset filenames **must match** the IDs in JSON files:

```json
// fish.json
{
  "id": "holy_mackerel",  // ← matches holy_mackerel.png
  "sprite": "assets/images/fish/holy_mackerel.png"
}
```

If IDs don't match, images won't load!

---

## Godot 4.x Integration

When migrating to Godot 4.x, assets will be handled differently but the organization remains the same.

### Import Settings

Godot automatically imports assets when placed in the project folder.

**For Images:**
1. Place PNG files in `assets/images/` subdirectories
2. Godot creates `.import` files automatically
3. Configure import settings in Godot Inspector:
   - **Filter:** Enable for smooth scaling (sprites)
   - **Mipmaps:** Disable for pixel art, enable for 3D
   - **Compression:** Lossless for UI, Lossy for backgrounds

**For Audio:**
1. Place OGG/WAV files in `assets/audio/` subdirectories
2. Godot imports automatically
3. Configure:
   - **Loop:** Enable for music, disable for SFX
   - **Compression:** Vorbis for music, WAV for short SFX

### Loading Assets in GDScript

```gdscript
# Load image
var sprite_texture = load("res://assets/images/fish/holy_mackerel.png")
$Sprite2D.texture = sprite_texture

# Load and play music
var music = load("res://assets/audio/music/battle_theme.ogg")
$AudioStreamPlayer.stream = music
$AudioStreamPlayer.play()

# Play sound effect
var sfx = load("res://assets/audio/sfx/attack_hit.wav")
$SFXPlayer.stream = sfx
$SFXPlayer.play()
```

### Resource Preloading

For frequently used assets, preload at compile-time:

```gdscript
# Preload (compiled into game)
const FISH_SPRITE = preload("res://assets/images/fish/holy_mackerel.png")

# Use instantly (no loading delay)
$Sprite2D.texture = FISH_SPRITE
```

---

## Creating New Assets

### Adding a New Fish

1. **Create sprite:**
   - Size: 128x128 pixels
   - Format: PNG with transparency
   - Style: Match existing fish art

2. **Save file:**
   - Location: `assets/images/fish/`
   - Filename: `[fish_id].png` (e.g., `rainbow_trout.png`)

3. **Update JSON:**
   ```json
   // src/data/fish.json
   {
     "id": "rainbow_trout",
     "name": "Rainbow Trout",
     "sprite": "assets/images/fish/rainbow_trout.png",
     // ... other fish data
   }
   ```

4. **Test:** Load game, catch fish, verify sprite appears

### Adding a New Sound Effect

1. **Create/find sound:**
   - Format: WAV or OGG
   - Length: 0.1-2 seconds
   - Quality: 44.1kHz, mono

2. **Save file:**
   - Location: `assets/audio/sfx/`
   - Filename: `[action].wav` (e.g., `level_up.wav`)

3. **Code integration:**
   ```python
   # In battle.py or relevant module
   level_up_sound = pygame.mixer.Sound("assets/audio/sfx/level_up.wav")

   # Play when fish levels up
   if fish.level_up():
       level_up_sound.play()
   ```

4. **Test:** Trigger action, verify sound plays

---

## Asset Specifications

### Image Formats

| Asset Type | Size | Format | Notes |
|------------|------|--------|-------|
| Fish Sprite | 128x128 | PNG | Transparency required |
| Enemy Sprite | 128-256 | PNG | Transparency required |
| Boss Sprite | 256x256 | PNG | Larger, more detailed |
| Apostle Portrait | 256x256 | PNG | Face/bust shot |
| Item Icon | 64x64 | PNG | Small, simple |
| Background | 1280x720 | PNG/JPEG | 16:9 aspect ratio |
| UI Element | Varies | PNG | Transparency for borders |
| Button | 200x50 | PNG | Multiple states (normal/hover/pressed) |

### Audio Formats

| Asset Type | Format | Sample Rate | Bitrate | Notes |
|------------|--------|-------------|---------|-------|
| Music | OGG | 44.1kHz | 128-192kbps | Loop-friendly |
| SFX (Long) | OGG | 44.1kHz | 96kbps | >2 seconds |
| SFX (Short) | WAV | 44.1kHz | N/A | <2 seconds, instant playback |
| Voice | OGG | 44.1kHz | 128kbps | Future feature |

### Color Guidelines

**Type-Based Color Coding** (match `constants.py` TYPE_CHART):

- **Holy:** Gold (#FFD700), white, light yellow
- **Water:** Blue (#1E90FF), cyan, aqua
- **Earth:** Brown (#8B4513), green, tan
- **Spirit:** Purple (#9370DB), magenta, lavender
- **Dark:** Dark purple (#4B0082), black, deep red

Fish should incorporate their type's color prominently.

---

## Tools and Resources

### Image Creation/Editing

**Free Tools:**
- **GIMP** - Full-featured image editor (Photoshop alternative)
- **Krita** - Digital painting, great for hand-drawn sprites
- **Aseprite** - Pixel art editor (paid but affordable)
- **Piskel** - Free online pixel art editor

**Pixel Art Resources:**
- **Lospec Palette List** - Curated color palettes
- **OpenGameArt.org** - Free game assets (CC-licensed)

### Audio Creation/Editing

**Free Tools:**
- **Audacity** - Audio editing, perfect for SFX
- **LMMS** - Music creation (FL Studio alternative)
- **Bfxr** - Retro SFX generator (great for game sounds)

**Music Resources:**
- **OpenGameArt.org** - Free music tracks (CC-licensed)
- **Incompetech** - Royalty-free music by Kevin MacLeod

### Asset Conversion

**ImageMagick** (command-line):
```bash
# Resize image
convert input.png -resize 128x128 output.png

# Convert to PNG with transparency
convert input.jpg -transparent white output.png

# Batch convert all JPGs to PNG
mogrify -format png *.jpg
```

**FFmpeg** (audio conversion):
```bash
# Convert MP3 to OGG
ffmpeg -i input.mp3 -c:a libvorbis -q:a 5 output.ogg

# Convert WAV to OGG
ffmpeg -i input.wav output.ogg

# Normalize audio levels
ffmpeg -i input.wav -af "loudnorm" output.wav
```

### Testing Assets

**Python Quick Test:**
```python
import pygame
pygame.init()

# Test image load
try:
    img = pygame.image.load("assets/images/fish/holy_mackerel.png")
    print(f"✅ Image loaded: {img.get_size()}")
except:
    print("❌ Image failed to load")

# Test audio load
try:
    pygame.mixer.music.load("assets/audio/music/battle_theme.ogg")
    print("✅ Music loaded")
except:
    print("❌ Music failed to load")
```

---

## Common Issues

### Image Not Loading

**Symptoms:** Black square, error message, or nothing appears

**Causes & Fixes:**
1. **Wrong file path**
   - Check spelling: `holy_mackerel.png` not `Holy_Mackerel.png`
   - Check location: Must be in correct `assets/` subfolder

2. **JSON mismatch**
   - Verify `sprite` field in JSON matches actual filename
   - IDs must match exactly: `"id": "holy_mackerel"` → `holy_mackerel.png`

3. **Corrupt file**
   - Try opening in image editor to verify
   - Re-export from original source

4. **Wrong format**
   - Must be PNG (not BMP, GIF, etc.)
   - Check file extension is `.png` not `.PNG`

### Audio Not Playing

**Symptoms:** Silence, error message, or game crash

**Causes & Fixes:**
1. **Wrong format**
   - Music: Use OGG (not MP3 in some cases)
   - SFX: Use WAV for short sounds

2. **File corrupted**
   - Play file in media player to verify
   - Re-export from audio editor

3. **Path issues**
   - Same as images: check spelling and location

4. **Mixer not initialized**
   ```python
   # Must call before loading audio
   pygame.mixer.init()
   ```

### Performance Issues

**Symptoms:** Lag, stuttering, slow loading

**Causes & Fixes:**
1. **Images too large**
   - Resize to recommended sizes (128x128 for sprites)
   - Don't use 4K images for small sprites!

2. **Too many assets loaded**
   - Only load assets when needed
   - Unload assets when switching scenes

3. **Uncompressed audio**
   - Convert WAV to OGG for music (much smaller)
   - Keep WAV only for short SFX

---

## Modding Support

The asset system is designed to be **mod-friendly**!

### Creating an Asset Mod

1. **Create mod folder:**
   ```
   mods/my_mod/
   ├── assets/
   │   ├── images/
   │   │   └── fish/
   │   │       └── custom_fish.png
   │   └── audio/
   │       └── music/
   │           └── custom_track.ogg
   └── data/
       └── fish.json
   ```

2. **Override assets:**
   - Place same-named files in mod folder
   - Game loads mod assets instead of default

3. **Add new content:**
   - Add new JSON entries with mod asset paths
   - Game loads both default and mod content

### Asset Mod Best Practices

- **Match style:** Keep art style consistent with base game
- **Same sizes:** Use same dimensions as default assets
- **Credit artists:** Include CREDITS.txt in mod folder
- **License clearly:** Specify license (CC-BY, CC0, etc.)

---

## Future: Advanced Features

**Planned features** for asset system:

### Sprite Animations
- **Idle animations** (fish bobbing)
- **Attack animations** (fish lunging)
- **Damage animations** (fish recoiling)

**Implementation:** Sprite sheets (8 frames per animation)

### Dynamic Music
- **Adaptive music** (changes based on battle state)
- **Layered tracks** (add instruments as battle intensifies)
- **Smooth transitions** (crossfade between themes)

### Localized Assets
- **Different images per language** (text-in-image support)
- **Localized audio** (voice acting in multiple languages)

---

## Summary

**Key Takeaways:**

1. ✅ **Organize assets** in `assets/` subdirectories by type
2. ✅ **Name files** to match JSON IDs exactly (lowercase, underscores)
3. ✅ **Use correct formats:** PNG for images, OGG/WAV for audio
4. ✅ **Follow size guidelines:** 128x128 for sprites, 1280x720 for backgrounds
5. ✅ **Test assets** before committing to repository
6. ✅ **Document custom assets** for other developers

**Questions?** Check `DEVELOPER_GUIDE.md` for code integration details or `TROUBLESHOOTING.md` for common issues.

---

**Happy asset creation! 🎨🎵**
