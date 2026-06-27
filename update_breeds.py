import json, re

# ── 1. Update photo_tags.json ─────────────────────────────────────────────
with open('E:/ClaudeCode/dog_facts/images/photo_tags.json', encoding='utf-8') as f:
    data = json.load(f)

new_photos = [
    {'file': 'alaskan_malamute_1.jpg',     'breeds': ['alaskan malamute'],       'tags': ['working dog', 'sled dog', 'large breed', 'fluffy'],           'caption': 'Alaskan Malamute. Built for blizzards. Currently melting hearts.'},
    {'file': 'besenji_1.jpg',              'breeds': ['basenji'],                'tags': ['hound', 'barkless', 'small breed', 'ancient breed'],          'caption': 'Basenji. Cannot bark. Has other ways of making his feelings known.'},
    {'file': 'borzoi_1.jpg',               'breeds': ['borzoi'],                 'tags': ['sighthound', 'elegant', 'large breed', 'russian'],            'caption': 'Borzoi. Long nose. Longer legs. Infinite elegance.'},
    {'file': 'bull_terrier_1.jpg',         'breeds': ['bull terrier'],           'tags': ['terrier', 'medium breed', 'muscular', 'playful'],             'caption': 'Bull Terrier. Egg-shaped head. Triangle eyes. Zero regrets.'},
    {'file': 'doberman_1.jpg',             'breeds': ['doberman'],               'tags': ['working dog', 'guardian', 'large breed', 'loyal'],            'caption': 'Doberman. Sleek. Fierce. Also sleeping on your couch.'},
    {'file': 'great_pryenesse_1.jpg',      'breeds': ['great pyrenees'],         'tags': ['working dog', 'fluffy', 'giant breed', 'guardian'],          'caption': 'Great Pyrenees. Royal Dog of France. Knows it.'},
    {'file': 'great_pyrenesse_2.jpg',      'breeds': ['great pyrenees'],         'tags': ['working dog', 'fluffy', 'giant breed', 'guardian'],          'caption': 'White floof. Mountain guardian. Unimpressed by everything.'},
    {'file': 'grey_hound_1.jpg',           'breeds': ['greyhound'],              'tags': ['sighthound', 'racing dog', 'large breed', 'athletic'],        'caption': 'Greyhound. Fastest dog on Earth. Napping competitively.'},
    {'file': 'grey_hound_2.jpg',           'breeds': ['greyhound'],              'tags': ['sighthound', 'racing dog', 'large breed', 'athletic'],        'caption': 'Lean machine. Off duty. Do not disturb.'},
    {'file': 'grey_hound_3.jpg',           'breeds': ['greyhound'],              'tags': ['sighthound', 'racing dog', 'large breed', 'athletic'],        'caption': 'Born to run. Currently declining.'},
    {'file': 'grey_hound_4.jpg',           'breeds': ['greyhound'],              'tags': ['sighthound', 'racing dog', 'large breed', 'athletic'],        'caption': '45mph potential. 0mph current speed. Balance achieved.'},
    {'file': 'grey_hound_5.jpg',           'breeds': ['greyhound'],              'tags': ['sighthound', 'racing dog', 'large breed', 'athletic'],        'caption': 'Retired racer. Professional lounge expert.'},
    {'file': 'grey_hound_five.jpg',        'breeds': ['greyhound'],              'tags': ['sighthound', 'racing dog', 'large breed', 'athletic'],        'caption': 'Greyhound. Sees the treat. Will absolutely sprint for it.'},
    {'file': 'irish_wolf_hound_1.jpg',     'breeds': ['irish wolfhound'],        'tags': ['sighthound', 'giant breed', 'gentle giant', 'historic'],     'caption': 'Irish Wolfhound. Taller than your furniture. Gentler than your cat.'},
    {'file': 'leonberger_1.jpg',           'breeds': ['leonberger'],             'tags': ['working dog', 'giant breed', 'fluffy', 'gentle giant'],      'caption': 'Leonberger. Bred to look like a lion. Behaves like a labrador.'},
    {'file': 'lhasa_alpso_1.jpg',          'breeds': ['lhasa apso'],             'tags': ['companion dog', 'small breed', 'fluffy', 'ancient breed'],   'caption': 'Lhasa Apso. Temple guardian. Tiny. Takes the job seriously.'},
    {'file': 'otter_hound_1.jpg',          'breeds': ['otterhound'],             'tags': ['hound', 'rare breed', 'medium breed', 'scruffy'],            'caption': 'Otterhound. Rare. Shaggy. Absolutely magnificent.'},
    {'file': 'pekingese_1.jpg',            'breeds': ['pekingese'],              'tags': ['toy breed', 'companion dog', 'ancient breed', 'imperial'],   'caption': 'Pekingese. Carried in sleeves. Still expects that treatment.'},
    {'file': 'pekingese_2.jpg',            'breeds': ['pekingese'],              'tags': ['toy breed', 'companion dog', 'ancient breed', 'imperial'],   'caption': 'Imperial breed. Imperial attitude. Non-negotiable.'},
    {'file': 'portuguese_water_dog_1.jpg', 'breeds': ['portuguese water dog'],   'tags': ['working dog', 'water dog', 'medium breed', 'curly'],         'caption': 'Portuguese Water Dog. Herded fish once. Would do it again.'},
    {'file': 'shiba_inu_1.jpg',            'breeds': ['shiba inu'],              'tags': ['spitz type', 'small breed', 'japanese breed', 'bold'],       'caption': 'Shiba Inu. Much wow. Very dog. Such attitude.'},
    {'file': 'shiba_inu_2.jpg',            'breeds': ['shiba inu'],              'tags': ['spitz type', 'small breed', 'japanese breed', 'bold'],       'caption': 'Shiba Inu. Fox face. Cat personality. Dog rules.'},
    {'file': 'viszla_1.jpg',               'breeds': ['vizsla'],                 'tags': ['sporting dog', 'medium breed', 'loyal', 'energetic'],        'caption': 'Vizsla. Velcro dog. Currently attached to its person.'},
    {'file': 'weimaraner_1.jpg',           'breeds': ['weimaraner'],             'tags': ['sporting dog', 'large breed', 'silver', 'elegant'],          'caption': 'Weimaraner. The Gray Ghost. Haunting your kitchen for scraps.'},
]

data['photos'].extend(new_photos)

with open('E:/ClaudeCode/dog_facts/images/photo_tags.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f'photo_tags.json updated — now {len(data["photos"])} photos')

# ── 2. Update dog_facts.json breed detection ──────────────────────────────
extra_breeds = {
    'alaskan malamute':     ['malamute', 'alaskan malamute'],
    'basenji':              ['basenji'],
    'borzoi':               ['borzoi'],
    'bull terrier':         ['bull terrier'],
    'doberman':             ['doberman'],
    'great pyrenees':       ['great pyrenees'],
    'irish wolfhound':      ['irish wolfhound'],
    'leonberger':           ['leonberger'],
    'lhasa apso':           ['lhasa apso'],
    'otterhound':           ['otterhound'],
    'pekingese':            ['pekingese'],
    'portuguese water dog': ['portuguese water dog'],
    'shiba inu':            ['shiba inu'],
    'vizsla':               ['vizsla'],
    'weimaraner':           ['weimaraner'],
}

with open('E:/ClaudeCode/dog_facts/dog_facts.json', encoding='utf-8') as f:
    facts_data = json.load(f)

updated = 0
for fact in facts_data['facts']:
    if fact['breed'] is None:
        text = fact['fact'].lower()
        for breed, patterns in extra_breeds.items():
            if any(re.search(r'\b' + re.escape(p) + r'\b', text) for p in patterns):
                fact['breed'] = breed
                updated += 1
                print(f'  Tagged #{fact["fact_number"]} -> {breed}')
                break

with open('E:/ClaudeCode/dog_facts/dog_facts.json', 'w', encoding='utf-8') as f:
    json.dump(facts_data, f, indent=2, ensure_ascii=False)

print(f'dog_facts.json updated — {updated} new breed tags')
