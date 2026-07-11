"""Full site-wide check: all 53 breeds have both a facts page and a deep dive,
   cross-links are correct in both directions, and the index lists all 53.
"""
import os, re

BASE = r'E:\ClaudeCode\dog_facts'

ALL_BREEDS = [
    ('akita',                 'Akita'),
    ('alaskan-malamute',      'Alaskan Malamute'),
    ('australian-shepherd',   'Australian Shepherd'),
    ('basenji',               'Basenji'),
    ('basset-hound',          'Basset Hound'),
    ('beagle',                'Beagle'),
    ('bichon-frise',          'Bichon Frise'),
    ('bloodhound',            'Bloodhound'),
    ('border-collie',         'Border Collie'),
    ('borzoi',                'Borzoi'),
    ('boxer',                 'Boxer'),
    ('brussels-griffon',      'Brussels Griffon'),
    ('bull-terrier',          'Bull Terrier'),
    ('bulldog',               'Bulldog'),
    ('chihuahua',             'Chihuahua'),
    ('chow-chow',             'Chow Chow'),
    ('corgi',                 'Corgi'),
    ('dachshund',             'Dachshund'),
    ('dalmatian',             'Dalmatian'),
    ('doberman',              'Doberman'),
    ('english-toy-spaniel',   'English Toy Spaniel'),
    ('finnish-lapphund',      'Finnish Lapphund'),
    ('german-shepherd',       'German Shepherd'),
    ('great-dane',            'Great Dane'),
    ('great-pyrenees',        'Great Pyrenees'),
    ('greyhound',             'Greyhound'),
    ('irish-terrier',         'Irish Terrier'),
    ('irish-wolfhound',       'Irish Wolfhound'),
    ('jack-russell-terrier',  'Jack Russell Terrier'),
    ('japanese-chin',         'Japanese Chin'),
    ('kerry-blue-terrier',    'Kerry Blue Terrier'),
    ('leonberger',            'Leonberger'),
    ('lhasa-apso',            'Lhasa Apso'),
    ('mastiff',               'Mastiff'),
    ('newfoundland',          'Newfoundland'),
    ('norwegian-elkhound',    'Norwegian Elkhound'),
    ('otterhound',            'Otterhound'),
    ('papillon',              'Papillon'),
    ('pekingese',             'Pekingese'),
    ('pointer',               'Pointer'),
    ('poodle',                'Poodle'),
    ('portuguese-water-dog',  'Portuguese Water Dog'),
    ('pug',                   'Pug'),
    ('rottweiler',            'Rottweiler'),
    ('saint-bernard',         'Saint Bernard'),
    ('saluki',                'Saluki'),
    ('samoyed',               'Samoyed'),
    ('shiba-inu',             'Shiba Inu'),
    ('siberian-husky',        'Siberian Husky'),
    ('skye-terrier',          'Skye Terrier'),
    ('vizsla',                'Vizsla'),
    ('weimaraner',            'Weimaraner'),
    ('whippet',               'Whippet'),
]

idx = open(os.path.join(BASE, 'deep-dives', 'index.html'), encoding='utf-8').read()

fails = []
for slug, name in ALL_BREEDS:
    errs = []

    # 1. Breed facts page exists
    breed_path = os.path.join(BASE, 'breeds', f'{slug}.html')
    if not os.path.exists(breed_path):
        errs.append('MISSING breeds page')
    else:
        bc = open(breed_path, encoding='utf-8').read()
        # 2. CTA from breed page -> deep dive
        if f'../deep-dives/{slug}.html' not in bc:
            errs.append('CTA missing in breeds page')

    # 3. Deep-dive page exists
    dive_path = os.path.join(BASE, 'deep-dives', f'{slug}.html')
    if not os.path.exists(dive_path):
        errs.append('MISSING deep-dive page')
    else:
        dc = open(dive_path, encoding='utf-8').read()
        # 4. Breadcrumb from deep dive -> breed page
        if f'href="../breeds/{slug}.html"' not in dc:
            errs.append('breadcrumb href wrong in deep-dive')

    # 5. Slug in index
    if f'href="{slug}.html"' not in idx:
        errs.append('missing from index')

    status = 'OK' if not errs else 'FAIL: ' + ' | '.join(errs)
    if errs:
        fails.append(slug)
    print(f'{slug:<28} {status}')

# Index card count
cards = re.findall(r'class="dive-card"', idx)
print(f'\nTotal index cards: {len(cards)}')
print(f'Expected: 53')
print(f'Match: {"YES" if len(cards) == 53 else "NO — mismatch!"}')
print(f'\nTotal fails: {len(fails)}')
if fails:
    print(f'Failed slugs: {fails}')
else:
    print('All 53 breeds fully verified.')
