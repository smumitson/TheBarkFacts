import json, re

# ── 1. New photos to add ───────────────────────────────────────────────────
new_photos = [
    {
        'file': 'Norwegian_elkhound_1.jpg',
        'breeds': ['norwegian elkhound'],
        'tags': ['spitz type', 'working dog', 'medium breed', 'nordic'],
        'caption': 'Norwegian Elkhound. Viking dog. Still on duty.'
    },
    {
        'file': 'bichon_frise_.jpg',
        'breeds': ['bichon frise'],
        'tags': ['toy breed', 'companion dog', 'fluffy', 'non-shedding'],
        'caption': 'Bichon Frise. Cotton ball with opinions.'
    },
    {
        'file': 'brussels_griffon_1.jpg',
        'breeds': ['brussels griffon'],
        'tags': ['toy breed', 'companion dog', 'small breed', 'wiry'],
        'caption': 'Brussels Griffon. Big personality. Very small dog.'
    },
    {
        'file': 'english_toy_spaniel_1.jpg',
        'breeds': ['english toy spaniel'],
        'tags': ['toy breed', 'companion dog', 'small breed', 'spaniel'],
        'caption': 'English Toy Spaniel. Lap dog. Knows the lap is earned.'
    },
    {
        'file': 'finnish_lapphund_1.jpg',
        'breeds': ['finnish lapphund'],
        'tags': ['spitz type', 'herding dog', 'medium breed', 'fluffy'],
        'caption': 'Finnish Lapphund. Herded reindeer. Now herds your schedule.'
    },
    {
        'file': 'irish_terrier_1.jpg',
        'breeds': ['irish terrier'],
        'tags': ['terrier', 'medium breed', 'red coat', 'bold'],
        'caption': 'Irish Terrier. Red coat. Redder attitude.'
    },
    {
        'file': 'japanese_chin_dog_1.jpg',
        'breeds': ['japanese chin'],
        'tags': ['toy breed', 'companion dog', 'small breed', 'japanese breed'],
        'caption': 'Japanese Chin. Imperial origins. Eternal elegance.'
    },
    {
        'file': 'kerry_blue_terrier_1.jpg',
        'breeds': ['kerry blue terrier'],
        'tags': ['terrier', 'medium breed', 'irish breed', 'blue coat'],
        'caption': 'Kerry Blue Terrier. Blue coat. Bold heart.'
    },
    {
        'file': 'pointer_1.jpg',
        'breeds': ['pointer'],
        'tags': ['sporting dog', 'medium breed', 'hunting dog', 'athletic'],
        'caption': 'Pointer. Spots the bird. Holds the pose. Awaits applause.'
    },
    {
        'file': 'skye_terrier_1.jpg',
        'breeds': ['skye terrier'],
        'tags': ['terrier', 'small breed', 'scottish breed', 'long coat'],
        'caption': 'Skye Terrier. Long coat. Longer memory.'
    },
]

# ── 2. Update photo_tags.json ──────────────────────────────────────────────
with open('E:/ClaudeCode/dog_facts/images/photo_tags.json', encoding='utf-8') as f:
    photo_data = json.load(f)

existing_files = {p['file'] for p in photo_data['photos']}
added = []
for photo in new_photos:
    if photo['file'] not in existing_files:
        photo_data['photos'].append(photo)
        added.append(photo['file'])

with open('E:/ClaudeCode/dog_facts/images/photo_tags.json', 'w', encoding='utf-8') as f:
    json.dump(photo_data, f, indent=2, ensure_ascii=False)

print(f"photo_tags.json: added {len(added)} photos -> now {len(photo_data['photos'])} total")
for f in added:
    print(f"  + {f}")

# ── 3. Update dog_facts.json breed detection ───────────────────────────────
new_breed_patterns = {
    'norwegian elkhound':  ['norwegian elkhound', 'elkhound'],
    'bichon frise':        ['bichon frise', 'bichon'],
    'brussels griffon':    ['brussels griffon'],
    'english toy spaniel': ['english toy spaniel'],
    'finnish lapphund':    ['finnish lapphund', 'lapphund'],
    'irish terrier':       ['irish terrier'],
    'japanese chin':       ['japanese chin'],
    'kerry blue terrier':  ['kerry blue terrier'],
    'pointer':             ['pointer'],
    'skye terrier':        ['skye terrier'],
}

with open('E:/ClaudeCode/dog_facts/dog_facts.json', encoding='utf-8') as f:
    facts_data = json.load(f)

updated = 0
for fact in facts_data['facts']:
    if fact['breed'] is None:
        text = fact['fact'].lower()
        for breed, patterns in new_breed_patterns.items():
            if any(re.search(r'\b' + re.escape(p) + r'\b', text) for p in patterns):
                fact['breed'] = breed
                updated += 1
                print(f"  Tagged fact #{fact['fact_number']} -> {breed}: {fact['fact'][:60]}...")
                break

with open('E:/ClaudeCode/dog_facts/dog_facts.json', 'w', encoding='utf-8') as f:
    json.dump(facts_data, f, indent=2, ensure_ascii=False)

print(f"\ndog_facts.json: {updated} new breed tags applied")
