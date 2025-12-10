# TONE GUIDE
## Dual-Text Content System for Loaves and Fishes

**Last Updated**: December 10, 2025

---

## OVERVIEW

Loaves and Fishes supports **two distinct tones** for the same content:

1. **DEFAULT** (Free Version): Irreverent, darkly funny, secular mythology game
2. **CHRISTIAN_EDITION** (Paid DLC): Reverent, educational, suitable for churches/schools

All game content uses a dual-text system where both versions are maintained side-by-side.

---

## TONE COMPARISON

### DEFAULT VERSION (Free Game)

**Target Audience**: Indie game fans 18-40, atheists/agnostics welcome
**Inspiration**: Dark religious roguelikes, cute dark comedy games, campy B-movies
**Tone**: Irreverent, snarky, self-aware, darkly funny

**Characteristics:**
- Casual, modern language
- Self-aware humor and meta-commentary
- Characters with personality and flaws
- Biblical references treated as mythology (like Greek/Norse myths)
- Puns, jokes, and sarcasm
- "Holy Mackerel" energy

**Example:**
> "Peter: Look, we fished ALL NIGHT. Nothing. My back hurts, I smell like disappointment, and I'm pretty sure a seagull judged me. But... *sigh* ...if you insist, let's do this again."

---

### CHRISTIAN EDITION (Paid DLC)

**Target Audience**: Churches, Sunday schools, Christian homeschoolers, parents
**Inspiration**: VeggieTales, educational Christian games
**Tone**: Reverent, respectful, educational, inspiring

**Characteristics:**
- Formal, Biblical language
- Respectful treatment of scripture
- Educational focus
- Inspirational messages
- No sarcasm or irreverence
- Suitable for all ages

**Example:**
> "Simon Peter: Master, we have worked hard all night and haven't caught anything. But because you say so, I will let down the nets."

---

## IMPLEMENTATION GUIDE

### JSON Structure

All text content should use this structure:

```json
{
  "text_field": {
    "default": "Irreverent, funny version",
    "christian_edition": "Reverent, educational version"
  }
}
```

Or for simple flavor text:

```json
{
  "flavor_text": {
    "default": "Snarky version with jokes",
    "christian_edition": "Inspirational, educational version"
  }
}
```

---

## CONTENT TYPE GUIDELINES

### 1. FISH

**Flavor Text:**
- **Default**: Punny, snarky, self-aware
- **Christian Edition**: Inspirational, biblical significance

**Example:**
```json
{
  "flavor_text": {
    "default": "Started from the bottom, now we're... still pretty small, honestly. But we try!",
    "christian_edition": "Even small beginnings can lead to great things with faith and perseverance."
  }
}
```

---

### 2. QUESTS

**Dialogue:**
- **Default**: Casual speech, personality, complaints, humor
- **Christian Edition**: Formal, respectful, faithful

**Example:**
```json
{
  "dialogue": {
    "start": {
      "default": "Peter: Okay, real talk? We fished ALL NIGHT. Caught absolutely nothing. My hands are blistered and I smell like regret. But... you're the boss. Let's do this.",
      "christian_edition": "Simon Peter: Master, we have worked hard all night and haven't caught anything. But because you say so, I will let down the nets."
    },
    "complete": {
      "default": "Peter: HOLY—sorry, I mean—LOOK AT ALL THESE FISH! The nets are about to BREAK! I've never seen anything like this! Okay, I'm in. From now on, I'm catching PEOPLE. ...That sounded better in my head.",
      "christian_edition": "Simon Peter: Master, this is a miracle! The nets are full! I have never seen such a catch! From now on, I will be a fisher of men, as you have called me."
    }
  }
}
```

---

### 3. APOSTLES

**Personality:**
- **Default**: Flaws, quirks, humor, realistic struggles
- **Christian Edition**: Biblical virtues, lessons, growth

**Example:**
```json
{
  "personality": {
    "default": "Wants proof of literally everything. Yes, EVERYTHING. The guy wouldn't believe the sky is blue without a peer-reviewed study. Gets really annoying about it, but once he's convinced, he's ALL IN. You love him anyway.",
    "christian_edition": "Thomas is thoughtful and seeks evidence before believing. His honest questions lead to deeper understanding. When he finally believes, his faith becomes unshakeable. He teaches us that doubt can lead to stronger faith."
  },
  "recruitment_dialogue": {
    "default": "Thomas: Unless I see the nail marks, I will NOT believe. I've been fooled before. Show me evidence. *sees miracle* ...Okay, I believe. I REALLY believe. Sorry for being difficult.",
    "christian_edition": "Thomas: Unless I see the nail marks in his hands and put my finger where the nails were, I will not believe. *sees miracle* My Lord and my God! I believe."
  }
}
```

---

### 4. ENEMIES

**Flavor Text:**
- **Default**: Satirical, funny, exaggerated
- **Christian Edition**: Educational, represents obstacles

**Example:**
```json
{
  "flavor_text": {
    "default": "This guy REALLY wants to see your permits. All of them. In triplicate. He has a rulebook and he's not afraid to use it. Yes, there ARE 613 rules. Yes, he's memorized them all. Yes, you're already breaking three of them.",
    "christian_edition": "The Pharisees were religious leaders bound by hundreds of laws. They represent legalism and the danger of valuing rules over compassion. Jesus challenged them to see beyond tradition."
  }
}
```

---

### 5. ITEMS (Already Good!)

**Flavor Text** (items are already punny, just need reverent versions):
- **Default**: Keep the puns!
- **Christian Edition**: Explain the biblical significance

**Example:**
```json
{
  "name": "Rye-demption Roll",
  "flavor_text": {
    "default": "Rise again with restored health! Get it? RYE-demption? We're not sorry.",
    "christian_edition": "Bread that restores and renews. Redemption brings us back to wholeness and health."
  }
}
```

---

### 6. BOSSES

**Dialogue:**
- **Default**: Personality, snark, dramatic
- **Christian Edition**: Symbolic, explanatory, serious

**Example:**
```json
{
  "intro_dialogue": {
    "default": "Steward: This wine is *hic* absolutely UNACCEPTABLE! Who serves this SWILL at a WEDDING?! I have STANDARDS! *wobbles* HIGH standards!",
    "christian_edition": "Steward: This wine is not suitable for such an important celebration. The quality must be maintained for our honored guests."
  },
  "defeat_dialogue": {
    "default": "Steward: Wait... this new wine is... *sniff* ...magnificent? This is the BEST wine I've ever tasted! My apologies! I may have judged too harshly! *hic*",
    "christian_edition": "Steward: This new wine is of exceptional quality! You have saved the best wine for last! This is truly remarkable!"
  }
}
```

---

### 7. PARABLES

**Framing:**
- **Default**: Self-aware intro, casual delivery
- **Christian Edition**: Traditional presentation

**Example:**
```json
{
  "intro": {
    "default": "Okay, story time. There's this farmer, right? And he's absolutely terrible at aiming. Just throwing seeds EVERYWHERE. Let me explain...",
    "christian_edition": "Jesus taught in parables to help us understand spiritual truths. Listen carefully to this teaching about the Kingdom of Heaven."
  },
  "moral": {
    "default": "Be good soil. Don't be the path (too hard), the rocks (too shallow), or the thorns (too distracted). Actually absorb the message. Revolutionary concept, we know.",
    "christian_edition": "We must be like good soil: receptive to God's word, rooted deeply in faith, and free from worldly distractions that would choke our spiritual growth."
  }
}
```

---

## WRITING GUIDELINES

### DEFAULT VERSION (Irreverent) - DO's

✅ Use casual, modern language
✅ Add personality and flaws to characters
✅ Include complaints, struggles, realistic reactions
✅ Self-aware humor and meta-commentary
✅ Pop culture references (sparingly)
✅ Puns and wordplay
✅ Acknowledge the absurdity
✅ Characters can be frustrated, tired, sarcastic
✅ "Show don't tell" - let actions speak

**Good Examples:**
- "Look, I'm not saying I doubted you, but I DEFINITELY doubted you."
- "This fish is judging me. I can feel it."
- "Upon this Bass I will build my church. *pause* Did I just say Bass?"

---

### DEFAULT VERSION - DON'Ts

❌ Don't mock faith itself (mock the situation, not belief)
❌ Don't be mean-spirited or cruel
❌ Don't make it ONLY jokes (balance with genuine moments)
❌ Don't use modern slang excessively (no "yeet" or "sus")
❌ Don't break immersion with 4th-wall breaks (except rare occasions)
❌ Don't be edgy for edgy's sake

**Bad Examples:**
- "LOL religion is dumb" ← Mean-spirited
- "This is so cringe fr fr no cap" ← Too much modern slang
- "Player, you should press the A button now" ← 4th wall break

---

### CHRISTIAN EDITION - DO's

✅ Use respectful, age-appropriate language
✅ Explain biblical context and significance
✅ Include moral lessons clearly
✅ Show character growth and virtue
✅ Reference scripture accurately
✅ Educational tone
✅ Inspirational messages
✅ Suitable for church/school settings

---

### CHRISTIAN EDITION - DON'Ts

❌ Don't be preachy or condescending
❌ Don't oversimplify complex theology
❌ Don't contradict scripture
❌ Don't be boring (keep it engaging!)
❌ Don't talk down to the audience

---

## TONE SPECTRUM

Think of tone on a spectrum:

```
REVERENT ←------------------------→ IRREVERENT
(Christian Edition)        (Default)

|------------|---------------|---------------|
Kids' shows   Fantasy novels  Mythology games  Dark religious indies
```

**Christian Edition**: Aim for educational kids' media / reverent fantasy
**Default Version**: Aim for mythology-based games (treating source material as entertainment, not scripture)

---

## CHECKLIST FOR NEW CONTENT

When adding new content, ensure:

- [ ] All text fields have BOTH `default` and `christian_edition` versions
- [ ] Default version is irreverent, self-aware, has personality
- [ ] Christian Edition version is respectful, educational, age-appropriate
- [ ] Both versions tell the same story/convey same gameplay info
- [ ] Puns work in both contexts (or are adapted)
- [ ] No mean-spirited mockery in default version
- [ ] No boring "preachiness" in Christian Edition

---

## EXAMPLES BY CONTENT TYPE

### NPC Dialogue
```json
{
  "npc_greeting": {
    "default": "Innkeeper: Welcome! You look exhausted. Long journey? Or did Peter's snoring keep you up again?",
    "christian_edition": "Innkeeper: Welcome, traveler! You look weary from your journey. Please, come in and rest."
  }
}
```

### Battle Victory Text
```json
{
  "victory_text": {
    "default": "You won! Your fish are looking pretty smug about it. Especially that one. You know which one.",
    "christian_edition": "Victory! Your faith and strategy have prevailed. Your fish have grown stronger through this trial."
  }
}
```

### Location Descriptions
```json
{
  "location_description": {
    "default": "The Sea of Galilee. Looks peaceful. Smells like fish. Lot of fishing going on. You'd think they'd have caught them all by now.",
    "christian_edition": "The Sea of Galilee, where Jesus called his first disciples and performed many miracles. The waters are calm and full of life."
  }
}
```

---

## QUALITY ASSURANCE

### Before Committing Content:

1. **Read both versions aloud** - Does each sound natural for its audience?
2. **Check for consistency** - Do both versions convey the same information?
3. **Test with different audiences** - Would this work for a church? For an indie gamer?
4. **Look for tone violations** - Any mean-spirited jokes? Any boring sermons?
5. **Verify Biblical accuracy** - Christian Edition should be theologically sound

---

## FUTURE: DYNAMIC TEXT SYSTEM

Eventually, implement a text system that:

```python
def get_text(content, field, edition="default"):
    """Get text based on current game edition setting."""
    if isinstance(content[field], dict):
        return content[field].get(edition, content[field]["default"])
    return content[field]  # Fallback for non-dual text
```

This allows:
- Player selection of edition at start
- On-the-fly switching (for testing)
- Easy modding and translations

---

## CONTACT

Questions about tone? Check these examples or ask:
- Is it funny but not mean? → Good for Default
- Is it educational but not boring? → Good for Christian Edition
- Does it fit the source material? → Check MANUAL.md vs MANUAL_CHRISTIAN.md

---

**Remember**: The best content works for BOTH audiences. The Default version entertains secular gamers, the Christian Edition educates believers. Both should be high quality!

---

*"Give a man a fish, and you feed him for a day. Give a man two versions of every fish, and you've got a DLC strategy."* 🐟✨
