"""Check available photos and facts for batch 5 breeds."""
import json, os

photo_list = json.load(open('images/photo_tags.json', encoding='utf-8'))['photos']
facts_list = json.load(open('dog_facts.json', encoding='utf-8'))

BREEDS = ['saluki', 'samoyed', 'shiba inu', 'siberian husky', 'skye terrier', 'vizsla', 'weimaraner', 'whippet']

for breed in BREEDS:
    slug = breed.replace(' ', '-')
    breed_photos = [p['file'] for p in photo_list
                    if isinstance(p, dict) and breed in [b.lower() for b in p.get('breeds', [])]]
    breed_facts = [f for f in facts_list
                   if isinstance(f, dict) and (f.get('breed') or '').lower() == breed]
    page_exists = os.path.exists(f'breeds/{slug}.html')
    print(f'{breed}:')
    print(f'  photos: {breed_photos}')
    print(f'  facts count: {len(breed_facts)}')
    print(f'  breeds/{slug}.html: {"exists" if page_exists else "MISSING"}')
    print()
