import json

with open('E:/ClaudeCode/dog_facts/dog_facts.json', 'r', encoding='utf-8') as f:
    facts_data = json.load(f)
with open('E:/ClaudeCode/dog_facts/images/photo_tags.json', 'r', encoding='utf-8') as f:
    photos_data = json.load(f)

fact_breeds = {}
for f in facts_data['facts']:
    if f.get('breed'):
        fact_breeds.setdefault(f['breed'], []).append(f)

photo_breeds = {}
for p in photos_data['photos']:
    for b in p.get('breeds', []):
        if b != 'generic':
            photo_breeds.setdefault(b, []).append(p)

breeds = [
    # Originally hand-built pages — now rebuilt from new data
    ('greyhound',           'greyhound',             'Greyhound',             '45 mph. Naps included. No brakes.'),
    ('corgi',               'corgi',                 'Corgi',                 'Royal blood. Tiny legs. Zero self-awareness.'),
    ('great dane',          'great-dane',            'Great Dane',            "Gentle giant. Thinks it's a lap dog. It's not."),
    ('german shepherd',     'german-shepherd',       'German Shepherd',       'Smartest dog in the room. Knows it. Judges you.'),
    ('boxer',               'boxer',                 'Boxer',                 'Wiggles first. Questions later. No off switch.'),
    # Previously built by this script
    ('akita',               'akita',                 'Akita',                 'Ancient. Loyal. Not interested in your opinion.'),
    ('border collie',       'border-collie',         'Border Collie',         'Smartest dog alive. Already judged your efficiency.'),
    ('borzoi',              'borzoi',                'Borzoi',                'Russian elegance. Nose of legend. Deeply unbothered.'),
    ('bulldog',             'bulldog',               'Bulldog',               'Maximum wrinkles. Minimum effort. Zero regrets.'),
    ('chihuahua',           'chihuahua',             'Chihuahua',             'Five pounds. Zero fear. Infinite attitude.'),
    ('dalmatian',           'dalmatian',             'Dalmatian',             'Born spotty. Stays spotty. Energetic about it.'),
    ('great pyrenees',      'great-pyrenees',        'Great Pyrenees',        'Royal dog of France. Mountain guardian. Never off duty.'),
    ('newfoundland',        'newfoundland',          'Newfoundland',          'Gentle giant. World-class drooler. Born to swim.'),
    ('pekingese',           'pekingese',             'Pekingese',             'Imperial. Ancient. Will not be rushed.'),
    ('pointer',             'pointer',               'Pointer',               'Born to point. Wired to hunt. Always on.'),
    ('poodle',              'poodle',                'Poodle',                'Smarter than you. Fluffier too. Not sorry.'),
    ('saint bernard',       'saint-bernard',         'Saint Bernard',         'Rescue dog by trade. Couch hog by choice.'),
    ('shiba inu',           'shiba-inu',             'Shiba Inu',             "Japan's national treasure. Knows it. Isn't telling."),
    # New breeds from updated facts file
    ('alaskan malamute',    'alaskan-malamute',      'Alaskan Malamute',      "Built for blizzards. Currently stealing your couch."),
    ('australian shepherd', 'australian-shepherd',   'Australian Shepherd',   'No job too big. No sheep too fast. No off switch.'),
    ('basenji',             'basenji',               'Basenji',               "Doesn't bark. Communicates through soul stare."),
    ('basset hound',        'basset-hound',          'Basset Hound',          'Low rider. Excellent nose. Zero urgency.'),
    ('beagle',              'beagle',                'Beagle',                "Nose first. Brain second. Heart always."),
    ('bichon frise',        'bichon-frise',          'Bichon Frise',          'Cotton ball. With opinions.'),
    ('bloodhound',          'bloodhound',            'Bloodhound',            "World's best nose. Attached to world-class wrinkles."),
    ('brussels griffon',    'brussels-griffon',      'Brussels Griffon',      'Tiny face. Enormous feelings.'),
    ('bull terrier',        'bull-terrier',          'Bull Terrier',          'Egg head. Triangle eyes. Unstoppable charm.'),
    ('chow chow',           'chow-chow',             'Chow Chow',             'Purple tongue. Independent soul. Do not rush.'),
    ('dachshund',           'dachshund',             'Dachshund',             'Long body. Short legs. Infinite stubbornness.'),
    ('doberman',            'doberman',              'Doberman',              'Sleek. Fast. Deeply loyal. Slightly judging you.'),
    ('english toy spaniel', 'english-toy-spaniel',   'English Toy Spaniel',   'Lap dog by trade. Royal by heritage.'),
    ('finnish lapphund',    'finnish-lapphund',      'Finnish Lapphund',      'Herded reindeer once. Now herds your schedule.'),
    ('irish terrier',       'irish-terrier',         'Irish Terrier',         'Red coat. Red-hot attitude. No regrets.'),
    ('irish wolfhound',     'irish-wolfhound',       'Irish Wolfhound',       'Tallest dog alive. Gentlest soul in the room.'),
    ('jack russell terrier','jack-russell-terrier',  'Jack Russell Terrier',  'Tiny. Tireless. Terminally enthusiastic.'),
    ('japanese chin',       'japanese-chin',         'Japanese Chin',         'Imperial origins. Eternal elegance.'),
    ('kerry blue terrier',  'kerry-blue-terrier',    'Kerry Blue Terrier',    'Blue coat. Bold heart. Very Irish.'),
    ('leonberger',          'leonberger',            'Leonberger',            "Bred to look like a lion. Acts like your best friend."),
    ('lhasa apso',          'lhasa-apso',            'Lhasa Apso',            'Temple guardian. Ancient. Takes the job seriously.'),
    ('mastiff',             'mastiff',               'Mastiff',               'Enormous. Devoted. Currently on your furniture.'),
    ('norwegian elkhound',  'norwegian-elkhound',    'Norwegian Elkhound',    'Viking dog. Still on duty.'),
    ('otterhound',          'otterhound',            'Otterhound',            'Rare. Shaggy. Born for the water.'),
    ('papillon',            'papillon',              'Papillon',              'Butterfly ears. Butterfly speed. Butterfly soul.'),
    ('portuguese water dog','portuguese-water-dog',  'Portuguese Water Dog',  'Herded fish once. Would absolutely do it again.'),
    ('pug',                 'pug',                   'Pug',                   'Smooshed face. Loud breathing. Pure love.'),
    ('rottweiler',          'rottweiler',            'Rottweiler',            'Tough face. Soft heart. Zero personal space.'),
    ('saluki',              'saluki',                'Saluki',                'Fastest ancient breed. Resting at the speed of light.'),
    ('samoyed',             'samoyed',               'Samoyed',               'The Samoyed smile. Non-negotiable.'),
    ('siberian husky',      'siberian-husky',        'Siberian Husky',        'Opinions: maximum. Volume: also maximum.'),
    ('skye terrier',        'skye-terrier',          'Skye Terrier',          'Long coat. Long memory. Loyal forever.'),
    ('vizsla',              'vizsla',                'Vizsla',                'Velcro dog. Currently attached to its human.'),
    ('weimaraner',          'weimaraner',            'Weimaraner',            'The Gray Ghost. Haunting your kitchen.'),
    ('whippet',             'whippet',               'Whippet',               '35 mph. Then immediately back to the couch.'),
]

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} Facts — The Bark Facts</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background: #FAF0DC;
      font-family: Georgia, "Times New Roman", serif;
      color: #3D2B1F;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    header {{
      background: #5C3D11;
      color: #FAF0DC;
      text-align: center;
      padding: 18px 24px 14px;
    }}
    header h1 {{
      font-size: 4rem;
      letter-spacing: 0.04em;
      font-weight: normal;
    }}
    header .subtitle {{
      font-size: 0.85rem;
      color: #D4B483;
      margin-top: 4px;
      font-style: italic;
    }}

    .site-nav {{
      background: #4A2E0A;
      display: flex;
      justify-content: center;
      gap: 4px;
      padding: 0 12px;
    }}
    .site-nav a {{
      color: #C8A87A;
      text-decoration: none;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 0.82rem;
      padding: 9px 20px;
      display: inline-block;
      letter-spacing: 0.03em;
      border-bottom: 2px solid transparent;
      transition: color 0.15s, border-color 0.15s;
    }}
    .site-nav a:hover,
    .site-nav a.active {{
      color: #FAF0DC;
      border-bottom-color: #C05621;
    }}

    .main {{
      flex: 1;
      max-width: 680px;
      width: 100%;
      margin: 0 auto;
      padding: 28px 20px 20px;
      display: flex;
      flex-direction: column;
      gap: 22px;
    }}

    .breed-hero {{
      text-align: center;
      padding: 8px 0 4px;
    }}
    .breed-hero h2 {{
      font-size: 2.4rem;
      font-weight: normal;
      color: #5C3D11;
      letter-spacing: 0.04em;
    }}
    .breed-tagline {{
      font-size: 0.95rem;
      color: #9A6B3A;
      font-style: italic;
      margin-top: 6px;
    }}

    .photo-section {{
      background: #3a2509;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 3px 12px rgba(92,61,17,0.25);
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .photo-section img {{
      width: 100%;
      max-height: 380px;
      object-fit: contain;
      background: #3a2509;
      display: block;
    }}
    .photo-caption {{
      color: #F5E6C8;
      font-style: italic;
      font-size: 0.95rem;
      padding: 10px 18px 10px;
      text-align: center;
      background: #5C3D11;
      width: 100%;
    }}
    .photo-nav {{
      background: #4A2E0A;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 16px;
    }}
    .photo-nav button {{
      background: #C05621;
      color: white;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 0.85rem;
      font-family: Georgia, serif;
      cursor: pointer;
      transition: background 0.15s;
    }}
    .photo-nav button:hover {{
      background: #9E4418;
    }}
    .photo-counter {{
      font-size: 0.82rem;
      color: #C8A87A;
      font-style: italic;
    }}

    .breadcrumb {{
      font-size: 0.82rem;
    }}
    .breadcrumb a {{
      color: #C05621;
      text-decoration: none;
    }}
    .breadcrumb a:hover {{
      text-decoration: underline;
    }}

    .facts-heading {{
      font-size: 0.82rem;
      color: #7A4F2A;
      font-style: italic;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}

    .fact-card {{
      background: #FFF8EC;
      border: 2px solid #E0C090;
      border-radius: 10px;
      padding: 28px 30px;
      box-shadow: 0 2px 8px rgba(92,61,17,0.12);
    }}
    .fact-number {{
      font-size: 0.75rem;
      font-weight: bold;
      color: #C05621;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 6px;
    }}
    .fact-category {{
      font-size: 0.8rem;
      color: #9A6B3A;
      margin-bottom: 14px;
      font-style: italic;
    }}
    .fact-text {{
      font-size: 1.2rem;
      line-height: 1.7;
      color: #3D2B1F;
    }}
    .fact-breed-tag {{
      display: inline-block;
      font-size: 0.75rem;
      background: #C05621;
      color: white;
      padding: 3px 10px;
      border-radius: 10px;
      text-transform: capitalize;
    }}
    .fact-footer {{
      display: flex;
      align-items: center;
      margin-top: 14px;
    }}

    footer {{
      background: #5C3D11;
      color: #A07840;
      text-align: center;
      font-size: 0.78rem;
      padding: 10px;
    }}
  </style>
</head>
<body>

<header>
  <h1>The Bark Facts</h1>
  <div class="subtitle">one fact, one dog, one day at a time</div>
</header>
<nav class="site-nav">
  <a href="../index.html">Home</a>
  <a href="index.html" class="active">Browse Facts</a>
  <a href="../deep-dives/index.html">Breeds</a>
</nav>

<div class="main">

  <div class="breed-hero">
    <h2>{title}</h2>
    <p class="breed-tagline">{tagline}</p>
  </div>

  <div class="photo-section">
    <img id="dog-photo" src="" alt="" />
    <div id="photo-caption" class="photo-caption"></div>
    <div class="photo-nav">
      <button onclick="prevPhoto()">← Prev</button>
      <span id="photo-counter" class="photo-counter">1 / {photo_count}</span>
      <button onclick="nextPhoto()">Next →</button>
    </div>
  </div>

  <div class="breadcrumb"><a href="../index.html">← Back to Home</a> &nbsp;&middot;&nbsp; <a href="index.html">← Back to Browse Facts</a></div>

  <div class="facts-heading">{fact_count} facts about the {title}</div>

  <div id="facts-section"></div>

</div>

<footer>Dog Facts &mdash; a fun project</footer>

<script>
const PHOTOS = {photos_js};

const FACTS = {facts_js};

let currentPhoto = 0;

function showPhoto(idx) {{
  const p = PHOTOS[idx];
  document.getElementById('dog-photo').src = '../images/' + p.file;
  document.getElementById('dog-photo').alt = p.caption;
  document.getElementById('photo-caption').textContent = p.caption;
  document.getElementById('photo-counter').textContent = (idx + 1) + ' / ' + PHOTOS.length;
}}

function nextPhoto() {{
  currentPhoto = (currentPhoto + 1) % PHOTOS.length;
  showPhoto(currentPhoto);
}}

function prevPhoto() {{
  currentPhoto = (currentPhoto - 1 + PHOTOS.length) % PHOTOS.length;
  showPhoto(currentPhoto);
}}

const section = document.getElementById('facts-section');
FACTS.forEach(function(fact) {{
  const card = document.createElement('div');
  card.className = 'fact-card';
  card.innerHTML =
    '<div class="fact-number">Fact #' + fact.fact_number + '</div>' +
    '<div class="fact-category">' + fact.category + '</div>' +
    '<div class="fact-text">' + fact.fact + '</div>' +
    '<div class="fact-footer"><span class="fact-breed-tag">{breed_tag}</span></div>';
  section.appendChild(card);
}});

showPhoto(0);
</script>
</body>
</html>
"""

for breed_key, slug, title, tagline in breeds:
    facts = fact_breeds[breed_key]
    photos = photo_breeds[breed_key]

    html = TEMPLATE.format(
        title=title,
        tagline=tagline,
        photo_count=len(photos),
        fact_count=len(facts),
        photos_js=json.dumps(photos, ensure_ascii=False),
        facts_js=json.dumps(facts, ensure_ascii=False),
        breed_tag=breed_key,
    )

    path = f'E:/ClaudeCode/dog_facts/breeds/{slug}.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Built: {slug}.html  ({len(facts)} facts, {len(photos)} photos)')
