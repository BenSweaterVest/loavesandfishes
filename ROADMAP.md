# Loaves and Fishes - Development Roadmap

> **Last Updated**: December 8, 2025
> **Current Phase**: Phase 2 - Integration & Polish (75% Complete)

This roadmap outlines the planned development trajectory for the Loaves and Fishes JRPG. The project is divided into four major phases, each building upon the previous to create a complete, polished gaming experience.

---

## Table of Contents

1. [Phase Overview](#phase-overview)
2. [Phase 1: Foundation (COMPLETE)](#phase-1-foundation-complete)
3. [Phase 2: Integration & Polish (IN PROGRESS)](#phase-2-integration--polish-in-progress)
4. [Phase 3: Content Expansion](#phase-3-content-expansion)
5. [Phase 4: Final Polish & Release](#phase-4-final-polish--release)
6. [Post-Release Plans](#post-release-plans)
7. [Timeline Estimates](#timeline-estimates)
8. [Stretch Goals](#stretch-goals)

---

## Phase Overview

| Phase | Status | Completion | Focus | Est. Hours |
|-------|--------|-----------|-------|-----------|
| **Phase 1** | ✅ Complete | 100% | Core systems and content creation | 80 hrs |
| **Phase 2** | 🚧 In Progress | 75% | Integration and polish | 40 hrs |
| **Phase 3** | ❌ Not Started | 0% | Content expansion and balance | 60 hrs |
| **Phase 4** | ❌ Not Started | 0% | Final polish and release prep | 30 hrs |

**Total Estimated Development Time**: 210 hours

---

## Phase 1: Foundation (COMPLETE)

**Status**: ✅ **100% Complete**
**Time Invested**: ~80 hours

### Goals
Create all core game systems and foundational content to make a playable game loop.

### Completed Features

#### Core Systems (100%)
- ✅ **Turn-based Battle System** - Full Pokémon-style combat
- ✅ **Type Effectiveness** - 5 types with strategic matchups
- ✅ **Status Effects** - 6 effects (Blessed, Burn, Poison, Paralysis, Sleep, Confusion)
- ✅ **Leveling System** - XP gain, level up, stat growth
- ✅ **Party Management** - 4 active fish + unlimited storage
- ✅ **Inventory System** - Items with categorization
- ✅ **Save/Load System** - Complete JSON serialization
- ✅ **Game State Management** - Scene-based state machine
- ✅ **UI Framework** - Text-based display system

#### Content Creation (100%)
- ✅ **21 Fish Species** - Fully balanced with unique stats
- ✅ **40 Enemies** - Organized in 5 tiers
- ✅ **13 Bosses** - One per town with unique mechanics
- ✅ **12 Apostles** - Each with unique abilities
- ✅ **50 Quests** - Main story, side quests, fetch quests, battle challenges
- ✅ **25 Parables** - Interactive storytelling collectibles
- ✅ **30 Items** - Healing, buffs, fishing equipment

#### World Building (100%)
- ✅ **13 Towns** - Nazareth to Jerusalem progression
- ✅ **World Map** - ASCII representation with coordinates
- ✅ **Town Exploration** - Locations and NPCs
- ✅ **Dialogue System** - Branching conversations
- ✅ **Cutscene System** - Story event sequences

#### Advanced Systems (100%)
- ✅ **Apostle Abilities** - 12 unique once-per-battle abilities
- ✅ **Miracle System** - 4 limit break abilities with meter
- ✅ **Combo Attacks** - 13 fish+apostle combinations
- ✅ **Fishing Mini-game** - Rhythm-based fish catching

### Key Achievements
- Complete game loop from title screen to credits
- All major systems integrated and functional
- Playable alpha ready for testing

---

## Phase 2: Integration & Polish (IN PROGRESS)

**Status**: 🚧 **75% Complete**
**Estimated Remaining Time**: 10 hours

### Goals
Connect all systems, integrate advanced features into gameplay, and polish the user experience.

### Completed Work (75%)
- ✅ **Documentation** - README, STATUS, ROADMAP, ARCHITECTURE, CONTRIBUTING
- ✅ **Main Game Loop** - Fully playable from start to finish
- ✅ **Town System Integration** - NPCs, locations, shops working
- ✅ **World Map Integration** - Travel and fast travel functional

### In Progress (20%)
- 🚧 **Apostle Ability Integration** (8 hrs remaining)
  - [ ] Add ability UI to battle screen
  - [ ] Implement cooldown tracking per battle
  - [ ] Add visual feedback for ability effects
  - [ ] Test all 12 apostle abilities in battle
  - [ ] Balance power levels and cooldowns

- 🚧 **Miracle System Integration** (6 hrs remaining)
  - [ ] Add miracle meter to battle UI
  - [ ] Implement meter gain events
  - [ ] Add miracle selection menu in battle
  - [ ] Test all 4 miracles
  - [ ] Balance meter costs

- 🚧 **Combo Attack Integration** (6 hrs remaining)
  - [ ] Add combo menu option in battle
  - [ ] Check requirements (fish + apostle + meter)
  - [ ] Implement special effects
  - [ ] Test all 13 combos
  - [ ] Balance damage and costs

### Not Started (5%)
- ❌ **Fishing Integration** (4 hrs)
  - [ ] Add fishing spots to towns
  - [ ] Integrate mini-game with town exploration
  - [ ] Connect to fish acquisition
  - [ ] Test difficulty scaling

- ❌ **Quest System Integration** (6 hrs)
  - [ ] Add quest tracking to UI
  - [ ] Implement quest triggers (dialogue, locations, battles)
  - [ ] Add quest rewards
  - [ ] Test quest progression
  - [ ] Balance XP and item rewards

- ❌ **Parable Collection Integration** (4 hrs)
  - [ ] Add parable discovery to exploration
  - [ ] Implement parable reading UI
  - [ ] Track collected parables
  - [ ] Test all 25 parables

- ❌ **Story Progression Integration** (6 hrs)
  - [ ] Connect story flags to events
  - [ ] Implement apostle recruitment cutscenes
  - [ ] Add boss victory cutscenes
  - [ ] Test story flow from start to end

### Success Criteria
- All advanced systems (apostle abilities, miracles, combos) functional in battles
- Quest system fully operational with tracking
- Fishing mini-game accessible from towns
- Story progression triggers working correctly
- No critical bugs in core gameplay loop

---

## Phase 3: Content Expansion

**Status**: ❌ **Not Started**
**Estimated Time**: 60 hours

### Goals
Expand content, improve balance, and enhance the gameplay experience.

### Planned Features

#### New Content (35 hrs)
- [ ] **10 Additional Fish Species** (8 hrs)
  - Design new fish with unique stat distributions
  - Add to appropriate fishing spots
  - Integrate with combo system
  - Create new evolution chains

- [ ] **20 More Enemies** (6 hrs)
  - Fill out enemy tiers
  - Add more variety to encounters
  - Create themed enemy groups

- [ ] **5 Optional Superbosses** (10 hrs)
  - Design endgame challenges
  - Unique mechanics for each
  - Legendary fish rewards
  - Place in hidden locations

- [ ] **25 Additional Quests** (8 hrs)
  - Apostle-specific side quests
  - Town-specific storylines
  - Endgame content
  - Hidden secrets and Easter eggs

- [ ] **10 New Parables** (3 hrs)
  - Lesser-known Biblical stories
  - More interactive elements
  - Reward system integration

#### Game Balance (15 hrs)
- [ ] **Enemy Stat Balancing** (4 hrs)
  - Adjust HP/ATK/DEF/SPD values
  - Test difficulty progression
  - Ensure fair challenge curves

- [ ] **Fish Stat Balancing** (4 hrs)
  - Balance growth rates
  - Adjust type distributions
  - Ensure no overpowered fish

- [ ] **Item Balance** (3 hrs)
  - Adjust healing amounts
  - Balance buff durations
  - Price optimization

- [ ] **XP Curve Refinement** (2 hrs)
  - Test leveling speed
  - Adjust XP rewards
  - Ensure smooth progression

- [ ] **Economy Balance** (2 hrs)
  - Adjust shop prices
  - Balance money rewards
  - Prevent grinding exploits

#### Quality of Life (10 hrs)
- [ ] **Battle Speed Options** (2 hrs)
  - Fast text mode
  - Animation skip
  - Turbo mode toggle

- [ ] **Auto-Battle System** (3 hrs)
  - AI for party members
  - Strategy settings
  - Override controls

- [ ] **Quick Save** (1 hr)
  - Save anywhere option
  - Multiple save slots
  - Autosave feature

- [ ] **Map Improvements** (2 hrs)
  - Enhanced ASCII art
  - Town descriptions
  - Travel time display

- [ ] **Help System** (2 hrs)
  - In-game tutorials
  - Type chart reference
  - Status effect guide

### Success Criteria
- 31 total fish species
- 60+ unique enemies
- 75+ quests
- Balanced difficulty throughout
- Smooth, enjoyable pacing

---

## Phase 4: Final Polish & Release

**Status**: ❌ **Not Started**
**Estimated Time**: 30 hours

### Goals
Polish all systems, fix bugs, optimize performance, and prepare for release.

### Planned Work

#### Bug Fixing & Testing (12 hrs)
- [ ] **Comprehensive Playtesting** (6 hrs)
  - Full game playthrough
  - Test all systems thoroughly
  - Document all bugs
  - Edge case testing

- [ ] **Bug Fixes** (4 hrs)
  - Fix critical bugs
  - Address gameplay issues
  - Polish rough edges

- [ ] **Save/Load Testing** (2 hrs)
  - Test save file compatibility
  - Verify state persistence
  - Handle corrupted saves

#### Performance Optimization (6 hrs)
- [ ] **Code Optimization** (3 hrs)
  - Profile performance
  - Optimize slow sections
  - Reduce memory usage

- [ ] **Load Time Optimization** (2 hrs)
  - Optimize JSON loading
  - Cache frequently used data
  - Lazy load when possible

- [ ] **Battle Performance** (1 hr)
  - Optimize combat calculations
  - Speed up animations
  - Reduce input lag

#### UI/UX Polish (8 hrs)
- [ ] **Visual Consistency** (3 hrs)
  - Standardize formatting
  - Consistent color scheme
  - Unified spacing

- [ ] **Text Polish** (3 hrs)
  - Proofread all dialogue
  - Fix typos and grammar
  - Improve flavor text

- [ ] **Menu Improvements** (2 hrs)
  - Better navigation
  - Clearer tooltips
  - Keyboard shortcuts

#### Release Preparation (4 hrs)
- [ ] **Final Documentation** (2 hrs)
  - Update all docs
  - Write release notes
  - Create installation guide

- [ ] **Package for Distribution** (1 hr)
  - Create release build
  - Test on clean system
  - Prepare distribution files

- [ ] **Launch Materials** (1 hr)
  - Screenshots
  - Feature highlights
  - Trailer script (text-based)

### Success Criteria
- Zero critical bugs
- Smooth gameplay throughout
- Professional presentation
- Ready for public release

---

## Post-Release Plans

Features and improvements planned after initial 1.0 release:

### Version 1.1 - Quality of Life Update
- [ ] Cloud save support
- [ ] Achievement system
- [ ] Statistics tracking
- [ ] New Game+ mode
- [ ] Difficulty modes (Easy, Normal, Hard, Miracle)

### Version 1.2 - Endgame Update
- [ ] Post-game content
- [ ] Battle Tower challenge mode
- [ ] Shiny fish variants
- [ ] Breeding system
- [ ] Online leaderboards (theoretical)

### Version 2.0 - New Testament Expansion
- [ ] Acts of the Apostles storyline
- [ ] New regions (Rome, Greece, Asia Minor)
- [ ] Expanded apostle stories
- [ ] New fish species and types
- [ ] More miracles and combos

### Community Features
- [ ] Modding support
- [ ] Custom quest creator
- [ ] Fish editor
- [ ] Share save files
- [ ] Community challenges

---

## Timeline Estimates

### Optimistic Timeline (Full-time development)
- **Phase 2 Completion**: 1-2 weeks
- **Phase 3 Completion**: 2-3 weeks
- **Phase 4 Completion**: 1 week
- **Total to Release**: 4-6 weeks

### Realistic Timeline (Part-time development)
- **Phase 2 Completion**: 3-4 weeks
- **Phase 3 Completion**: 6-8 weeks
- **Phase 4 Completion**: 2-3 weeks
- **Total to Release**: 11-15 weeks (~3 months)

### Conservative Timeline (Hobby development)
- **Phase 2 Completion**: 6-8 weeks
- **Phase 3 Completion**: 10-12 weeks
- **Phase 4 Completion**: 4-5 weeks
- **Total to Release**: 20-25 weeks (~5-6 months)

---

## Stretch Goals

Features that would be amazing but aren't required for 1.0:

### High Priority Stretch Goals
- [ ] **Multiplayer Trading** - Trade fish with other players
- [ ] **PvP Battles** - Battle other players' parties
- [ ] **Daily Challenges** - New quests each day
- [ ] **Seasonal Events** - Special content for holidays
- [ ] **Voice Acting** - Text-to-speech integration

### Medium Priority Stretch Goals
- [ ] **Animated Battle Sprites** - ASCII art animations
- [ ] **Music System** - MIDI or chiptune soundtrack
- [ ] **Sound Effects** - Terminal beep effects
- [ ] **Color Customization** - User-selectable themes
- [ ] **Localization** - Multiple language support

### Low Priority Stretch Goals
- [ ] **Mobile Version** - iOS/Android port
- [ ] **Web Version** - Browser-based game
- [ ] **GUI Version** - Graphical interface option
- [ ] **Discord Integration** - Rich presence and commands
- [ ] **Twitch Integration** - Stream-interactive features

---

## Development Priorities

### Must-Have for 1.0
1. All Phase 2 integration complete
2. Zero critical bugs
3. Balanced gameplay start to finish
4. Complete documentation
5. Smooth user experience

### Should-Have for 1.0
1. Phase 3 content expansion complete
2. Quality of life features
3. Help system
4. Achievement framework

### Nice-to-Have for 1.0
1. Auto-battle system
2. New Game+ mode
3. Statistics tracking
4. Battle speed options

### Post-1.0
1. All stretch goals
2. Community features
3. Major expansions
4. Platform ports

---

## Contributing to the Roadmap

Want to help shape the future of Loaves and Fishes?

1. **Vote on Features** - Let us know what you want most
2. **Suggest Ideas** - Propose new features or content
3. **Report Issues** - Help us prioritize fixes
4. **Submit Contributions** - See CONTRIBUTING.md

---

## Version History

### Planned Releases

- **v0.5.0 (Current)** - Playable Alpha
  - All core systems complete
  - Main story playable
  - Integration in progress

- **v0.8.0** - Beta Release
  - Phase 2 complete
  - All systems integrated
  - Full testing pass

- **v0.9.0** - Release Candidate
  - Phase 3 complete
  - Content expansion done
  - Balance finalized

- **v1.0.0** - Official Release
  - Phase 4 complete
  - Fully polished
  - Production ready

---

## Contact & Feedback

- **Issues**: Use GitHub issues for bug reports
- **Discussions**: GitHub discussions for feature requests
- **Development**: Follow STATUS.md for progress updates

---

*"Give a man a fish, and you feed him for a day. Teach a man to fish, and he'll catch a Holy Mackerel!"*
