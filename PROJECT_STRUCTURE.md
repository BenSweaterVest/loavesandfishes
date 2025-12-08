# Project Structure

```
loavesandfishes/
├── README.md                 # Main project documentation
├── PROJECT_STRUCTURE.md      # This file
├── .gitignore               # Git ignore rules
│
├── src/                     # Source code
│   ├── data/                # Game data (fish, apostles, towns, items)
│   │   ├── fish.json        # All fish stats, moves, properties
│   │   ├── apostles.json    # Apostle abilities and powers
│   │   ├── towns.json       # Town data and progression
│   │   ├── items.json       # Bread items and equipment
│   │   ├── enemies.json     # Enemy bestiary
│   │   ├── bosses.json      # Boss battle data
│   │   ├── quests.json      # Side quest definitions
│   │   └── parables.json    # Collectible parables
│   │
│   ├── engine/              # Core game engine
│   │   ├── battle.py        # Battle system logic
│   │   ├── overworld.py     # Overworld navigation
│   │   ├── progression.py   # XP, leveling, stats
│   │   ├── inventory.py     # Fish party & item management
│   │   └── save_load.py     # Save/load system
│   │
│   ├── ui/                  # User interface
│   │   ├── menus.py         # Menu systems
│   │   ├── battle_ui.py     # Battle interface
│   │   ├── shop_ui.py       # Shop interfaces
│   │   └── hud.py           # Heads-up display
│   │
│   └── utils/               # Utility functions
│       ├── constants.py     # Game constants
│       ├── helpers.py       # Helper functions
│       └── data_loader.py   # Data loading utilities
│
├── assets/                  # Game assets (to be created)
│   ├── sprites/             # Pixel art sprites
│   │   ├── characters/      # Jesus, apostles, NPCs
│   │   ├── fish/            # Fish sprites
│   │   ├── enemies/         # Enemy sprites
│   │   └── ui/              # UI elements
│   │
│   ├── music/               # Music tracks (.ogg, .mp3)
│   │   ├── overworld/       # Overworld themes
│   │   ├── battle/          # Battle music
│   │   └── towns/           # Town themes
│   │
│   ├── sfx/                 # Sound effects
│   │   ├── menu/            # Menu sounds
│   │   ├── battle/          # Battle sounds
│   │   └── ambient/         # Ambient sounds
│   │
│   └── maps/                # Map data and tilesets
│       ├── overworld/       # Overworld map
│       └── towns/           # Town maps
│
├── docs/                    # Documentation
│   ├── DESIGN_DOC.md        # Complete game design document
│   ├── FISH_GUIDE.md        # Fish reference
│   ├── APOSTLE_GUIDE.md     # Apostle reference
│   └── DEVELOPMENT.md       # Development notes
│
└── saves/                   # Player save files
    └── .gitkeep
```

## Development Phases

### Phase 1: Data & Core Systems (Current)
- ✅ Project structure setup
- 🔄 Create all JSON data files
- 🔄 Implement core battle system
- 🔄 Basic menu and UI

### Phase 2: Content Implementation
- ⏳ Implement all 20+ fish
- ⏳ Implement 12 apostles
- ⏳ Create 13 towns
- ⏳ Program boss battles

### Phase 3: Art & Audio
- ⏳ Create pixel art sprites
- ⏳ Compose music tracks
- ⏳ Record sound effects

### Phase 4: Polish & Testing
- ⏳ Balance testing
- ⏳ Bug fixes
- ⏳ UI/UX refinement
- ⏳ Content completion

### Phase 5: Release
- ⏳ Platform builds
- ⏳ Marketing
- ⏳ Launch!

## Tech Stack Options

### Option 1: Python + Pygame (Recommended for prototyping)
- **Pros**: Fast development, easy to learn, great for prototypes
- **Cons**: Performance limitations, harder to distribute

### Option 2: JavaScript/TypeScript + Phaser
- **Pros**: Web-based (easy distribution), good performance
- **Cons**: Larger codebase, more complex setup

### Option 3: Godot Engine
- **Pros**: Built for games, great 2D support, visual editor
- **Cons**: Learning curve, GDScript language

### Option 4: Unity
- **Pros**: Professional engine, wide platform support
- **Cons**: Overkill for 2D, larger file sizes

**Current Choice**: Starting with Python + JSON data for rapid prototyping. Engine can be changed later!
