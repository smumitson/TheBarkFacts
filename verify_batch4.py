import os, re

BASE = r'E:\ClaudeCode\dog_facts'

BATCH4 = [
    ('norwegian-elkhound', 'Norwegian Elkhound', 'norwegian_elkhound_1.jpg'),
    ('otterhound',          'Otterhound',          'otterhound_3.jpg'),
    ('papillon',            'Papillon',             'papillon_1.jpg'),
    ('pekingese',           'Pekingese',            'pekingese_3.jpg'),
    ('pointer',             'Pointer',              'pointer_2.jpg'),
    ('poodle',              'Poodle',               'poodle_4.jpg'),
    ('portuguese-water-dog','Portuguese Water Dog', 'portuguese_water_dog_1.jpg'),
    ('pug',                 'Pug',                  'pug_5.jpg'),
    ('rottweiler',          'Rottweiler',            'rottweiler_1.jpg'),
    ('saint-bernard',       'Saint Bernard',        'saint_bernard_3.jpg'),
]

idx = open(os.path.join(BASE, 'deep-dives', 'index.html'), encoding='utf-8').read()

all_ok = True
for slug, name, photo in BATCH4:
    errs = []
    dive = os.path.join(BASE, 'deep-dives', f'{slug}.html')
    if not os.path.exists(dive):
        errs.append('MISSING deep-dive file')
    else:
        content = open(dive, encoding='utf-8').read()
        if f'href="../breeds/{slug}.html"' not in content:
            errs.append('breadcrumb href wrong')
        if photo not in content:
            errs.append(f'photo {photo} not in page')
    if not os.path.exists(os.path.join(BASE, 'images', photo)):
        errs.append('photo missing from disk')
    breed = os.path.join(BASE, 'breeds', f'{slug}.html')
    if not os.path.exists(breed):
        errs.append('MISSING breed page')
    else:
        bc = open(breed, encoding='utf-8').read()
        if f'../deep-dives/{slug}.html' not in bc:
            errs.append('CTA missing in breed page')
    if f'href="{slug}.html"' not in idx:
        errs.append('missing from index')
    if errs:
        all_ok = False
    print(f'{slug:<28} {"OK" if not errs else "FAIL: " + " | ".join(errs)}')

cards = re.findall(r'class="dive-card"', idx)
print(f'\nTotal index cards: {len(cards)}')
print('All checks passed!' if all_ok else 'Some checks FAILED.')
