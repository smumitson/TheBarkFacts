import json

with open('E:/ClaudeCode/dog_facts/images/photo_tags.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Remove bad entry for bichon_frise_.jpg (file doesn't exist on disk)
data['photos'] = [p for p in data['photos'] if p['file'] != 'bichon_frise_.jpg']

# Get set of already-registered filenames
registered = {p['file'] for p in data['photos']}

new_entries = [
    # alaskan_malamute 2-5
    {"file": "alaskan_malamute_2.jpg", "breeds": ["alaskan malamute"], "tags": ["working dog", "sled dog", "large breed", "fluffy"], "caption": "Alaskan Malamute. Bred for the tundra. Tolerating the suburbs."},
    {"file": "alaskan_malamute_3.jpg", "breeds": ["alaskan malamute"], "tags": ["working dog", "sled dog", "large breed", "fluffy"], "caption": "Big dog. Bigger personality. Biggest paws."},
    {"file": "alaskan_malamute_4.jpg", "breeds": ["alaskan malamute"], "tags": ["working dog", "sled dog", "large breed", "fluffy"], "caption": "Could pull a sled. Prefers to pull your arm."},
    {"file": "alaskan_malamute_5.jpg", "breeds": ["alaskan malamute"], "tags": ["working dog", "sled dog", "large breed", "fluffy"], "caption": "Malamute. Floof champion. Currently shedding everywhere."},

    # basenji 2-6
    {"file": "basenji_2.jpg", "breeds": ["basenji"], "tags": ["hound", "barkless", "small breed", "ancient breed"], "caption": "No bark. Plenty of attitude. Problem solved differently."},
    {"file": "basenji_3.jpg", "breeds": ["basenji"], "tags": ["hound", "barkless", "small breed", "ancient breed"], "caption": "Ancient Egyptian hunting dog. Still on the hunt."},
    {"file": "basenji_4.jpg", "breeds": ["basenji"], "tags": ["hound", "barkless", "small breed", "ancient breed"], "caption": "Self-grooming like a cat. Running like a cheetah."},
    {"file": "basenji_5.jpg", "breeds": ["basenji"], "tags": ["hound", "barkless", "small breed", "ancient breed"], "caption": "Silence. Speed. Judgment. All at once."},
    {"file": "basenji_6.jpg", "breeds": ["basenji"], "tags": ["hound", "barkless", "small breed", "ancient breed"], "caption": "Basenji. Doesn't bark. Communicates through soul stare."},

    # bichon_frise 1-3 (replacing old broken entry)
    {"file": "bichon_frise_1.jpg", "breeds": ["bichon frise"], "tags": ["toy breed", "companion dog", "fluffy", "non-shedding"], "caption": "Bichon Frise. Cotton ball with opinions."},
    {"file": "bichon_frise_2.jpg", "breeds": ["bichon frise"], "tags": ["toy breed", "companion dog", "fluffy", "non-shedding"], "caption": "Cloud dog. Zero shedding. Maximum fluff."},
    {"file": "bichon_frise_3.jpg", "breeds": ["bichon frise"], "tags": ["toy breed", "companion dog", "fluffy", "non-shedding"], "caption": "Small. Cheerful. Refuses to have a bad day."},

    # borzoi 2-5
    {"file": "borzoi_2.jpg", "breeds": ["borzoi"], "tags": ["sighthound", "elegant", "large breed", "russian"], "caption": "Borzoi. Aristocratic. Slightly dismissive of your presence."},
    {"file": "borzoi_3.jpg", "breeds": ["borzoi"], "tags": ["sighthound", "elegant", "large breed", "russian"], "caption": "Nose: imperial. Speed: extraordinary. Snack interest: eternal."},
    {"file": "borzoi_4.jpg", "breeds": ["borzoi"], "tags": ["sighthound", "elegant", "large breed", "russian"], "caption": "Russian wolfhound. Silky. Statuesque. Oddly photogenic."},
    {"file": "borzoi_5.jpg", "breeds": ["borzoi"], "tags": ["sighthound", "elegant", "large breed", "russian"], "caption": "Borzoi. Born to run. Also born to pose dramatically."},

    # brussels_griffon 2-4
    {"file": "brussels_griffon_2.jpg", "breeds": ["brussels griffon"], "tags": ["toy breed", "companion dog", "small breed", "wiry"], "caption": "Brussels Griffon. Looks like a Muppet. Totally owns it."},
    {"file": "brussels_griffon_3.jpg", "breeds": ["brussels griffon"], "tags": ["toy breed", "companion dog", "small breed", "wiry"], "caption": "Tiny face. Enormous feelings. Non-negotiable."},
    {"file": "brussels_griffon_4.jpg", "breeds": ["brussels griffon"], "tags": ["toy breed", "companion dog", "small breed", "wiry"], "caption": "Distinguished. Bearded. Deeply opinionated about everything."},

    # bull_terrier 2-4
    {"file": "bull_terrier_2.jpg", "breeds": ["bull terrier"], "tags": ["terrier", "medium breed", "muscular", "playful"], "caption": "Bull Terrier. Egg head. Maximum personality."},
    {"file": "bull_terrier_3.jpg", "breeds": ["bull terrier"], "tags": ["terrier", "medium breed", "muscular", "playful"], "caption": "Clown. Athlete. Best friend you didn't expect."},
    {"file": "bull_terrier_4.jpg", "breeds": ["bull terrier"], "tags": ["terrier", "medium breed", "muscular", "playful"], "caption": "Bull Terrier. Unique face. Even more unique spirit."},

    # doberman 2-3
    {"file": "doberman_2.jpg", "breeds": ["doberman"], "tags": ["working dog", "guardian", "large breed", "loyal"], "caption": "Doberman. Precision machine. Runs on loyalty."},
    {"file": "doberman_3.jpg", "breeds": ["doberman"], "tags": ["working dog", "guardian", "large breed", "loyal"], "caption": "Vigilant. Elegant. Would die for you and also steal your seat."},

    # english_toy_spaniel 2-3
    {"file": "english_toy_spaniel_2.jpg", "breeds": ["english toy spaniel"], "tags": ["toy breed", "companion dog", "small breed", "spaniel"], "caption": "English Toy Spaniel. Royal companion. Taking the role very seriously."},
    {"file": "english_toy_spaniel_3.jpg", "breeds": ["english toy spaniel"], "tags": ["toy breed", "companion dog", "small breed", "spaniel"], "caption": "Silky. Sweet. Historically sat on the laps of royalty."},

    # finnish_lapphund 2-3
    {"file": "finnish_lapphund_2.jpg", "breeds": ["finnish lapphund"], "tags": ["spitz type", "herding dog", "medium breed", "fluffy"], "caption": "Finnish Lapphund. Arctic floof. Warm heart. Cold nose."},
    {"file": "finnish_lapphund_3.jpg", "breeds": ["finnish lapphund"], "tags": ["spitz type", "herding dog", "medium breed", "fluffy"], "caption": "Reindeer herder on sabbatical. Enjoying the warmth."},

    # great_dane_6
    {"file": "great_dane_6.jpg", "breeds": ["great dane"], "tags": ["giant breed", "gentle giant", "working dog", "elegant"], "caption": "Great Dane. World's tallest dog. Still wants to be a lapdog."},

    # great_pyrenees 3-4
    {"file": "great_pyrenees_3.jpg", "breeds": ["great pyrenees"], "tags": ["working dog", "fluffy", "giant breed", "guardian"], "caption": "Great Pyrenees. Mountain floof. Would block a wolf. Also the door."},
    {"file": "great_pyrenees_4.jpg", "breeds": ["great pyrenees"], "tags": ["working dog", "fluffy", "giant breed", "guardian"], "caption": "Nocturnal guardian. Loud barker. Excellent napper by day."},

    # irish_terrier 2-3
    {"file": "irish_terrier_2.jpg", "breeds": ["irish terrier"], "tags": ["terrier", "medium breed", "red coat", "bold"], "caption": "Irish Terrier. Spirited. Stubborn. Absolutely worth it."},
    {"file": "irish_terrier_3.jpg", "breeds": ["irish terrier"], "tags": ["terrier", "medium breed", "red coat", "bold"], "caption": "Daredevil dog. Fiery coat. Even fierier personality."},

    # irish_wolfhound 2-3
    {"file": "irish_wolfhound_2.jpg", "breeds": ["irish wolfhound"], "tags": ["sighthound", "giant breed", "gentle giant", "historic"], "caption": "Irish Wolfhound. Gentle. Enormous. Would not harm a fly."},
    {"file": "irish_wolfhound_3.jpg", "breeds": ["irish wolfhound"], "tags": ["sighthound", "giant breed", "gentle giant", "historic"], "caption": "Historic breed. Ancient nobility. Currently napping."},

    # japanese_chin_dog 2-3
    {"file": "japanese_chin_dog_2.jpg", "breeds": ["japanese chin"], "tags": ["toy breed", "companion dog", "small breed", "japanese breed"], "caption": "Japanese Chin. Elegant. Refined. Absolutely judging your decor."},
    {"file": "japanese_chin_dog_3.jpg", "breeds": ["japanese chin"], "tags": ["toy breed", "companion dog", "small breed", "japanese breed"], "caption": "Temple dog. Still expecting temple-level treatment."},

    # kerry_blue_terrier 2-3
    {"file": "kerry_blue_terrier_2.jpg", "breeds": ["kerry blue terrier"], "tags": ["terrier", "medium breed", "irish breed", "blue coat"], "caption": "Kerry Blue Terrier. Stunning coat. Even more stunning stubbornness."},
    {"file": "kerry_blue_terrier_3.jpg", "breeds": ["kerry blue terrier"], "tags": ["terrier", "medium breed", "irish breed", "blue coat"], "caption": "Irish through and through. Bold, brave, and curly."},

    # leonberger 2-3
    {"file": "leonberger_2.jpg", "breeds": ["leonberger"], "tags": ["working dog", "giant breed", "fluffy", "gentle giant"], "caption": "Leonberger. Part lion. Part lapdog. All heart."},
    {"file": "leonberger_3.jpg", "breeds": ["leonberger"], "tags": ["working dog", "giant breed", "fluffy", "gentle giant"], "caption": "Mane like a lion. Temperament like a golden."},

    # lhasa_apso 2-3
    {"file": "lhasa_apso_2.jpg", "breeds": ["lhasa apso"], "tags": ["companion dog", "small breed", "fluffy", "ancient breed"], "caption": "Lhasa Apso. Small in size. Large in confidence."},
    {"file": "lhasa_apso_3.jpg", "breeds": ["lhasa apso"], "tags": ["companion dog", "small breed", "fluffy", "ancient breed"], "caption": "Monk approved. Palace raised. Currently judging your home."},

    # norwegian_elkhound 2-3
    {"file": "norwegian_elkhound_2.jpg", "breeds": ["norwegian elkhound"], "tags": ["spitz type", "working dog", "medium breed", "nordic"], "caption": "Norwegian Elkhound. Survived Vikings. Can handle your schedule."},
    {"file": "norwegian_elkhound_3.jpg", "breeds": ["norwegian elkhound"], "tags": ["spitz type", "working dog", "medium breed", "nordic"], "caption": "Ancient Nordic hunter. Thick coat. Thick determination."},

    # otterhound 2-3
    {"file": "otterhound_2.jpg", "breeds": ["otterhound"], "tags": ["hound", "rare breed", "medium breed", "scruffy"], "caption": "Otterhound. One of the rarest breeds. Worth every rarity point."},
    {"file": "otterhound_3.jpg", "breeds": ["otterhound"], "tags": ["hound", "rare breed", "medium breed", "scruffy"], "caption": "Shaggy. Lovable. Swimming optional but preferred."},

    # pekingese 3-4
    {"file": "pekingese_3.jpg", "breeds": ["pekingese"], "tags": ["toy breed", "companion dog", "ancient breed", "imperial"], "caption": "Pekingese. Descended from palace dogs. Has not forgotten."},
    {"file": "pekingese_4.jpg", "breeds": ["pekingese"], "tags": ["toy breed", "companion dog", "ancient breed", "imperial"], "caption": "Small. Fluffy. Carrying 2000 years of dignified history."},

    # pointer 2-4
    {"file": "pointer_2.jpg", "breeds": ["pointer"], "tags": ["sporting dog", "medium breed", "hunting dog", "athletic"], "caption": "Pointer. Locked in. Target acquired. Waiting for your signal."},
    {"file": "pointer_3.jpg", "breeds": ["pointer"], "tags": ["sporting dog", "medium breed", "hunting dog", "athletic"], "caption": "Precision nose. Sculptural pose. Born to hunt."},
    {"file": "pointer_4.jpg", "breeds": ["pointer"], "tags": ["sporting dog", "medium breed", "hunting dog", "athletic"], "caption": "Pointer. Elegant. Athletic. Always pointing at something."},

    # portuguese_water_dog 2-3
    {"file": "portuguese_water_dog_2.jpg", "breeds": ["portuguese water dog"], "tags": ["working dog", "water dog", "medium breed", "curly"], "caption": "Portuguese Water Dog. Loves the water. Tolerates the bath."},
    {"file": "portuguese_water_dog_3.jpg", "breeds": ["portuguese water dog"], "tags": ["working dog", "water dog", "medium breed", "curly"], "caption": "Curly. Energetic. Ready to jump in at any moment."},

    # shiba_inu 3-4
    {"file": "shiba_inu_3.jpg", "breeds": ["shiba inu"], "tags": ["spitz type", "small breed", "japanese breed", "bold"], "caption": "Shiba Inu. Not your average dog. Never your average dog."},
    {"file": "shiba_inu_4.jpg", "breeds": ["shiba inu"], "tags": ["spitz type", "small breed", "japanese breed", "bold"], "caption": "Ancient Japanese breed. Modern internet icon."},

    # skye_terrier 2-3
    {"file": "skye_terrier_2.jpg", "breeds": ["skye terrier"], "tags": ["terrier", "small breed", "scottish breed", "long coat"], "caption": "Skye Terrier. Hair everywhere. Heart even bigger."},
    {"file": "skye_terrier_3.jpg", "breeds": ["skye terrier"], "tags": ["terrier", "small breed", "scottish breed", "long coat"], "caption": "Scottish legend. Coat like a waterfall. Loyalty like a rock."},

    # vizsla 2-3
    {"file": "vizsla_2.jpg", "breeds": ["vizsla"], "tags": ["sporting dog", "medium breed", "loyal", "energetic"], "caption": "Vizsla. Velcro dog. The 'where are you going' breed."},
    {"file": "vizsla_3.jpg", "breeds": ["vizsla"], "tags": ["sporting dog", "medium breed", "loyal", "energetic"], "caption": "Golden rust coat. Golden retriever energy. No, not related."},

    # weimaraner 2-3
    {"file": "weimaraner_2.jpg", "breeds": ["weimaraner"], "tags": ["sporting dog", "large breed", "silver", "elegant"], "caption": "Weimaraner. Silver ghost. Currently haunting your kitchen."},
    {"file": "weimaraner_3.jpg", "breeds": ["weimaraner"], "tags": ["sporting dog", "large breed", "silver", "elegant"], "caption": "Sleek. Fast. Deeply attached to one specific human."},
]

added = 0
for entry in new_entries:
    if entry['file'] not in registered:
        data['photos'].append(entry)
        registered.add(entry['file'])
        added += 1
        print(f"Added: {entry['file']}")
    else:
        print(f"Already registered: {entry['file']}")

with open('E:/ClaudeCode/dog_facts/images/photo_tags.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nDone. Added {added} new entries. Removed bichon_frise_.jpg entry.")
print(f"Total photos registered: {len(data['photos'])}")
