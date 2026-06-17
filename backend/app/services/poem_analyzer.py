import re

# Database of popular poems/quotes
POEM_DATABASE = {
    "two roads diverged in a yellow wood": {
        "intention": "Choices",
        "suitable_age_group": "Teens & Adults",
        "moral": "Decisions shape our destiny; choose wisely and stand by the less traveled path with conviction.",
        "meaning": "An exploration of human choice, the nature of regret, and individuality in the journey of life.",
        "real_life_example": "Choosing to pursue an unconventional, risky passion or a startup role over a secure, standard corporate path, which ultimately leads to profound self-discovery.",
        "suggested_poems": [
            {"title": "Stopping by Woods on a Snowy Evening", "author": "Robert Frost"},
            {"title": "The Journey", "author": "Mary Oliver"},
            {"title": "Invictus", "author": "William Ernest Henley"}
        ],
        "emotions": {"Nostalgia": 0.84, "Awe": 0.45, "Melancholy": 0.30},
        "poetic_devices": ["Extended Metaphor", "Imagery", "Antithesis"]
    },
    "hope is the thing with feathers": {
        "intention": "Resilience",
        "suitable_age_group": "All Ages",
        "moral": "Hope is a quiet, resilient force inside us that never fades and asks for nothing in return.",
        "meaning": "A beautiful metaphor depicting hope as a bird that sings in the soul, staying strong through life's storms.",
        "real_life_example": "Rebounding from a serious health diagnosis or academic setback by focusing on the belief that better days are ahead, which provides the quiet strength to keep trying.",
        "suggested_poems": [
            {"title": "Still I Rise", "author": "Maya Angelou"},
            {"title": "Don't Quit", "author": "Edgar A. Guest"},
            {"title": "Ode to the West Wind", "author": "Percy Bysshe Shelley"}
        ],
        "emotions": {"Joy": 0.90, "Awe": 0.65, "Nostalgia": 0.20},
        "poetic_devices": ["Metaphor", "Personification", "Imagery"]
    },
    "i wandered lonely as a cloud": {
        "intention": "Nature",
        "suitable_age_group": "All Ages",
        "moral": "Finding joy in the simple beauty of nature provides lasting comfort and cures loneliness.",
        "meaning": "The poem praises the healing power of natural scenes and the joy of keeping those memories to brighten future dark days.",
        "real_life_example": "Recalling the quiet peace of a sunset walk on a beach or park during a high-stress exam week to help calm the nerves.",
        "suggested_poems": [
            {"title": "To Autumn", "author": "John Keats"},
            {"title": "Lines Written in Early Spring", "author": "William Wordsworth"},
            {"title": "Trees", "author": "Joyce Kilmer"}
        ],
        "emotions": {"Joy": 0.95, "Awe": 0.80, "Nostalgia": 0.50},
        "poetic_devices": ["Simile", "Personification", "Hyperbole"]
    }
}

def analyze_poem_text(text: str) -> dict:
    cleaned = text.strip().lower()
    
    # Check for exact or partial matches of popular lines in database
    for key, data in POEM_DATABASE.items():
        if key in cleaned:
            return data.copy()
            
    # Fallback dynamic generator based on keywords
    # Detect emotions
    joy_hits = len(re.findall(r'\b(joy|happy|gold|light|sing|feather|hope|rise|sun|dance)\b', cleaned))
    sad_hits = len(re.findall(r'\b(dark|tear|grief|sad|lost|grave|night|shadow|alone|weep)\b', cleaned))
    nature_hits = len(re.findall(r'\b(wood|cloud|flower|sea|river|star|wind|leaf|nature|lake)\b', cleaned))
    
    emotions = {"Awe": 0.40, "Nostalgia": 0.30}
    if joy_hits >= sad_hits and joy_hits > 0:
        emotions["Joy"] = round(0.50 + 0.05 * min(10, joy_hits), 2)
        emotions["Melancholy"] = 0.15
        intention = "Optimism"
        suitable_age_group = "All Ages"
        moral = "Find light and hope within small moments; optimism is the quiet seed of positive change."
        meaning = "A poetic expression highlighting the beauty of hope, joy, and new beginnings."
        real_life_example = "Encouraging a teammate after a project failure by focusing on what was learned and celebrating the potential of the next idea."
        suggested_poems = [
            {"title": "A Psalm of Life", "author": "Henry Wadsworth Longfellow"},
            {"title": "Pippa's Song", "author": "Robert Browning"}
        ]
    elif sad_hits > joy_hits:
        emotions["Melancholy"] = round(0.50 + 0.05 * min(10, sad_hits), 2)
        emotions["Joy"] = 0.10
        intention = "Grief"
        suitable_age_group = "Teens & Adults"
        moral = "Allow yourself to feel sorrow fully; expressing grief is a necessary path to healing."
        meaning = "An introspective look at the passage of time, loss, and the heavy moments of human emotion."
        real_life_example = "Sharing a quiet, supportive conversation with a family member who is missing a loved one during the holidays, acknowledging their absence."
        suggested_poems = [
            {"title": "O Captain! My Captain!", "author": "Walt Whitman"},
            {"title": "Annabel Lee", "author": "Edgar Allan Poe"}
        ]
    elif nature_hits > 0:
        emotions["Awe"] = round(0.50 + 0.05 * min(10, nature_hits), 2)
        emotions["Nostalgia"] = 0.40
        intention = "Tranquility"
        suitable_age_group = "All Ages"
        moral = "Step back from technology and reconnect with nature to restore peace to your mind."
        meaning = "A contemplative verse highlighting the enduring cycles and visual wonders of the natural world."
        real_life_example = "Going offline for a weekend hike in the forest to decompress and recharge your energy."
        suggested_poems = [
            {"title": "The Lake Isle of Innisfree", "author": "W.B. Yeats"},
            {"title": "Sea Fever", "author": "John Masefield"}
        ]
    else:
        # General default fallback
        intention = "Reflection"
        suitable_age_group = "Teens & Adults"
        moral = "Self-reflection on our decisions and the paths we choose is the key to true personal wisdom."
        meaning = "A thoughtful examination of identity, human connections, and the quiet spaces in between actions."
        real_life_example = "Spending ten minutes writing in a personal journal before sleeping to reflect on your day and set clean intentions."
        suggested_poems = [
            {"title": "If—", "author": "Rudyard Kipling"},
            {"title": "A Psalm of Life", "author": "Henry Wadsworth Longfellow"}
        ]
        
    # Standard poetic devices
    poetic_devices = []
    if len(text.split('\n')) > 3:
        poetic_devices.append("Rhyme Scheme")
    if any(w in cleaned for w in ["like", "as"]):
        poetic_devices.append("Simile")
    else:
        poetic_devices.append("Metaphor")
    if re.search(r'\b(\w)\w*\s+\1', cleaned):
        poetic_devices.append("Alliteration")
    else:
        poetic_devices.append("Imagery")
        
    return {
        "intention": intention,
        "suitable_age_group": suitable_age_group,
        "moral": moral,
        "meaning": meaning,
        "real_life_example": real_life_example,
        "suggested_poems": suggested_poems,
        "emotions": emotions,
        "poetic_devices": poetic_devices
    }
