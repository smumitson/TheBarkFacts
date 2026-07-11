"""Builds deep-dive pages for batch 3 and updates index + breed CTAs."""
import os, re, openpyxl

BREEDS = [
    (
        'great-pyrenees', 'Great Pyrenees',
        'Mountain guardian. Works nights. Barking included.',
        'great_pyrenees_2.jpg',
        'An independent livestock guardian &mdash; the nighttime barking and stubbornness are features, not bugs.',
    ),
    (
        'irish-terrier', 'Irish Terrier',
        'Red coat. Fiery heart. Not interested in backing down.',
        'irish_terrier_1.jpg',
        'A fearless, loyal terrier &mdash; small enough to underestimate, bold enough to make that a mistake.',
    ),
    (
        'irish-wolfhound', 'Irish Wolfhound',
        'Tallest dog alive. Gentlest soul in the room. Shortest run together.',
        'irish_wolfhound_2.jpg',
        'An ancient gentle giant &mdash; the lifespan is short and worth sitting with before committing.',
    ),
    (
        'jack-russell-terrier', 'Jack Russell Terrier',
        'Tiny. Relentless. Currently dismantling your garden.',
        'jack_russell_terrier_4.jpg',
        'One of the most demanding small breeds alive &mdash; not the apartment dog the size suggests.',
    ),
    (
        'japanese-chin', 'Japanese Chin',
        'Imperial origins. Cat-like independence. Silently critiquing your home.',
        'japanese_chin_dog_2.jpg',
        'A calm, elegant toy breed &mdash; easier than it looks, with health caveats worth knowing.',
    ),
    (
        'kerry-blue-terrier', 'Kerry Blue Terrier',
        'Blue coat. Terrier soul. Has opinions about other dogs.',
        'kerry_blue_terrier_1.jpg',
        'A versatile working terrier &mdash; the grooming commitment surprises people expecting a low-maintenance dog.',
    ),
    (
        'leonberger', 'Leonberger',
        'Bred to look like a lion. Acts like your best friend. Leaves hair everywhere.',
        'leonberger_3.jpg',
        'A gentle giant with genuine warmth &mdash; and all the giant-breed tradeoffs that come with it.',
    ),
    (
        'lhasa-apso', 'Lhasa Apso',
        'Temple guardian. Small but serious. That coat is a commitment.',
        'lhasa_apso_3.jpg',
        'An ancient sentinel breed with real independence underneath the flowing coat &mdash; not just a lap dog.',
    ),
    (
        'mastiff', 'Mastiff',
        '200 pounds of gentle. Currently on your couch.',
        'mastiff_4.jpg',
        'The gentle giant of gentle giants &mdash; the temperament is easy, the physical realities are not.',
    ),
    (
        'newfoundland', 'Newfoundland',
        'Nanny dog. Swimming champion. Drool machine. Extraordinary package.',
        'newfoundland_dog_3.jpg',
        'Genuinely one of the best dogs with children &mdash; the coat, drool, and size are the honest caveats.',
    ),
]

SCALE_BADGE = {'Low':'badge-low','Moderate':'badge-moderate','High':'badge-high','Very High':'badge-very-high'}
TRAINABILITY_BADGE = {'Easy':'badge-yes','Moderate':'badge-moderate','Independent-Minded':'badge-with-exp'}
BEGINNER_BADGE = {'Yes':'badge-yes','With Experience':'badge-with-exp','Not Recommended':'badge-no'}
APARTMENT_BADGE = {'Yes':'badge-yes','With Enough Exercise':'badge-with-exp','No':'badge-no'}

wb = openpyxl.load_workbook('dog_facts_7.3.2026.xlsx')
ws = wb['deep_dive_profiles']
headers = [ws.cell(1, c).value for c in range(1, 15)]
profiles = {}
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0]:
        profiles[row[0].lower()] = dict(zip(headers, row))

PAGE_CSS = """\
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: #FAF0DC;
      font-family: Georgia, "Times New Roman", serif;
      color: #3D2B1F;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      background: #5C3D11;
      color: #FAF0DC;
      text-align: center;
      padding: 18px 24px 14px;
    }
    header h1 {
      font-size: 4rem;
      letter-spacing: 0.04em;
      font-weight: normal;
    }
    header .subtitle {
      font-size: 0.85rem;
      color: #D4B483;
      margin-top: 4px;
      font-style: italic;
    }

    .site-nav {
      background: #4A2E0A;
      display: flex;
      justify-content: center;
      gap: 4px;
      padding: 0 12px;
      flex-wrap: wrap;
    }
    .site-nav a {
      color: #C8A87A;
      text-decoration: none;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 0.82rem;
      padding: 9px 20px;
      display: inline-block;
      letter-spacing: 0.03em;
      border-bottom: 2px solid transparent;
      transition: color 0.15s, border-color 0.15s;
    }
    .site-nav a:hover,
    .site-nav a.active {
      color: #FAF0DC;
      border-bottom-color: #C05621;
    }

    .main {
      flex: 1;
      max-width: 680px;
      width: 100%;
      margin: 0 auto;
      padding: 28px 20px 40px;
      display: flex;
      flex-direction: column;
      gap: 22px;
    }

    .deep-hero {
      text-align: center;
      padding: 8px 0 4px;
    }
    .deep-hero h2 {
      font-size: 2.4rem;
      font-weight: normal;
      color: #5C3D11;
      letter-spacing: 0.04em;
    }
    .breed-tagline {
      font-size: 0.95rem;
      color: #9A6B3A;
      font-style: italic;
      margin-top: 6px;
    }
    .deep-dives-label {
      display: inline-block;
      font-size: 0.7rem;
      background: #5C3D11;
      color: #D4B483;
      padding: 3px 10px;
      border-radius: 10px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 10px;
    }

    .breadcrumb {
      font-size: 0.82rem;
    }
    .breadcrumb a {
      color: #C05621;
      text-decoration: none;
    }
    .breadcrumb a:hover { text-decoration: underline; }

    .stat-panel {
      background: #FFF8EC;
      border: 2px solid #E0C090;
      border-radius: 10px;
      padding: 22px 26px 26px;
      box-shadow: 0 2px 8px rgba(92,61,17,0.10);
    }
    .panel-heading {
      font-size: 0.78rem;
      color: #7A4F2A;
      font-style: italic;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      margin-bottom: 18px;
    }
    .stat-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px 12px;
    }
    .stat-item {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }
    .stat-label {
      font-size: 0.64rem;
      color: #9A6B3A;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      line-height: 1.4;
    }
    .stat-badge {
      display: inline-block;
      font-size: 0.78rem;
      font-weight: bold;
      padding: 4px 10px;
      border-radius: 20px;
      line-height: 1.35;
      width: fit-content;
    }

    .badge-low      { background: #E4CFA0; color: #4A2E0A; }
    .badge-moderate { background: #C8A870; color: #3D2B1F; }
    .badge-high     { background: #C05621; color: #FFF8EC; }
    .badge-very-high{ background: #5C3D11; color: #FAF0DC; }
    .badge-neutral  { background: #7A4F2A; color: #FAF0DC; }
    .badge-yes      { background: #6B7C45; color: #F5F0E8; }
    .badge-with-exp { background: #B8880A; color: #FFF8EC; }
    .badge-no       { background: #8B3A1A; color: #FAF0DC; }

    .narrative-section {
      background: #FFF8EC;
      border: 2px solid #E0C090;
      border-radius: 10px;
      padding: 28px 30px;
      box-shadow: 0 2px 8px rgba(92,61,17,0.12);
      overflow: hidden;
    }
    .narrative-heading {
      font-size: 0.78rem;
      color: #7A4F2A;
      font-style: italic;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      margin-bottom: 14px;
    }
    .narrative-body {
      font-size: 1.05rem;
      line-height: 1.78;
      color: #3D2B1F;
    }
    .narrative-body p + p {
      margin-top: 14px;
    }

    .narrative-img {
      float: right;
      width: 150px;
      margin: 4px 0 14px 18px;
      border-radius: 8px;
      border: 2px solid #E0C090;
      box-shadow: 0 2px 8px rgba(92,61,17,0.12);
      display: block;
    }

    .narrative-section.honest-take {
      border-left: 4px solid #C05621;
    }
    .narrative-section.honest-take .narrative-heading {
      color: #C05621;
    }

    @media (max-width: 520px) {
      header h1 { font-size: 2.8rem; }
      .stat-grid { grid-template-columns: repeat(2, 1fr); gap: 12px 10px; }
      .stat-badge { font-size: 0.74rem; }
      .narrative-img {
        float: none;
        display: block;
        width: 180px;
        margin: 0 auto 16px;
      }
    }

    footer {
      background: #5C3D11;
      color: #A07840;
      text-align: center;
      font-size: 0.78rem;
      padding: 10px;
    }"""


def paras(text):
    parts = [p.strip() for p in text.strip().split('\n\n') if p.strip()]
    return '\n      '.join(f'<p>{p}</p>' for p in parts)


def build_page(slug, title, tagline, photo, p):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} &mdash; Deep Dive &mdash; The Bark Facts</title>
  <style>
{PAGE_CSS}
  </style>
</head>
<body>

<header>
  <h1>The Bark Facts</h1>
  <div class="subtitle">one fact, one dog, one day at a time</div>
</header>
<nav class="site-nav">
  <a href="../index.html">Home</a>
  <a href="../breeds/index.html">Browse Facts</a>
  <a href="index.html" class="active">Breeds</a>
</nav>

<div class="main">

  <div class="deep-hero">
    <div class="deep-dives-label">Deep Dive</div>
    <h2>{title}</h2>
    <p class="breed-tagline">{tagline}</p>
  </div>

  <div class="breadcrumb">
    <a href="../index.html">&#8592; Back to Home</a>
    &nbsp;&middot;&nbsp;
    <a href="index.html">&#8592; Back to Breeds</a>
    &nbsp;&middot;&nbsp;
    <a href="../breeds/{slug}.html">See Breed Facts Page</a>
  </div>

  <!-- Quick-Glance Panel -->
  <section class="stat-panel">
    <div class="panel-heading">Quick Glance</div>
    <div class="stat-grid">

      <div class="stat-item">
        <div class="stat-label">Primary Role</div>
        <span class="stat-badge badge-neutral">{p['primary_role']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Physical Activity Needs</div>
        <span class="stat-badge {SCALE_BADGE[p['physical_activity_needs']]}">{p['physical_activity_needs']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Mental Stimulation Needs</div>
        <span class="stat-badge {SCALE_BADGE[p['mental_stimulation_needs']]}">{p['mental_stimulation_needs']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Size</div>
        <span class="stat-badge badge-neutral">{p['size']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Grooming Needs</div>
        <span class="stat-badge {SCALE_BADGE[p['grooming_needs']]}">{p['grooming_needs']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Trainability</div>
        <span class="stat-badge {TRAINABILITY_BADGE[p['trainability']]}">{p['trainability']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Good For Beginners</div>
        <span class="stat-badge {BEGINNER_BADGE[p['good_for_beginners']]}">{p['good_for_beginners']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Apartment Friendly</div>
        <span class="stat-badge {APARTMENT_BADGE[p['apartment_friendly']]}">{p['apartment_friendly']}</span>
      </div>

    </div>
  </section>

  <!-- Temperament -->
  <section class="narrative-section">
    <div class="narrative-heading">Temperament</div>
    <div class="narrative-body">
      <img class="narrative-img" src="../images/{photo}" alt="{title}" />
      {paras(p['temperament_narrative'])}
    </div>
  </section>

  <!-- Health & Lifespan -->
  <section class="narrative-section">
    <div class="narrative-heading">Health &amp; Lifespan</div>
    <div class="narrative-body">
      {paras(p['health_lifespan_narrative'])}
    </div>
  </section>

  <!-- Nutrition Needs -->
  <section class="narrative-section">
    <div class="narrative-heading">Nutrition Needs</div>
    <div class="narrative-body">
      {paras(p['nutrition_narrative'])}
    </div>
  </section>

  <!-- Family Fit -->
  <section class="narrative-section">
    <div class="narrative-heading">Family Fit</div>
    <div class="narrative-body">
      {paras(p['family_fit_narrative'])}
    </div>
  </section>

  <!-- The Honest Take -->
  <section class="narrative-section honest-take">
    <div class="narrative-heading">The Honest Take</div>
    <div class="narrative-body">
      {paras(p['honest_take_narrative'])}
    </div>
  </section>

</div>

<footer>Dog Facts &mdash; a fun project</footer>

</body>
</html>
"""


# Build pages
for slug, title, tagline, photo, _teaser in BREEDS:
    profile = profiles[title.lower()]
    with open(f'deep-dives/{slug}.html', 'w', encoding='utf-8') as f:
        f.write(build_page(slug, title, tagline, photo, profile))
    print(f'Built: deep-dives/{slug}.html')


# Full alphabetical index — 35 breeds
ALL_CARDS = [
    ('akita',                'Akita',                'A dignified, one-family dog &mdash; loyal on its own terms and no one else&rsquo;s.'),
    ('alaskan-malamute',     'Alaskan Malamute',     'Tundra-bred strength and a friendly face &mdash; hiding an escape artist underneath.'),
    ('australian-shepherd',  'Australian Shepherd',  'The velcro herding dog &mdash; extraordinary partner if you can keep up.'),
    ('basenji',              'Basenji',              'The barkless dog &mdash; independent, cat-like, and very much on its own terms.'),
    ('basset-hound',         'Basset Hound',         'Low to the ground, high on vibes &mdash; a forgiving breed with a stubborn streak.'),
    ('beagle',               'Beagle',               'Nose-led, food-motivated, and louder than expected &mdash; loveable with caveats.'),
    ('bichon-frise',         'Bichon Frise',         'Small, cheerful, and low-shed &mdash; but that coat is a real commitment.'),
    ('bloodhound',           'Bloodhound',           'The world&rsquo;s best nose attached to a sweet, stubborn, drool-forward dog.'),
    ('border-collie',        'Border Collie',        'Extraordinary intelligence with extraordinary demands &mdash; not for the low-key household.'),
    ('borzoi',               'Borzoi',               'Serene indoors, electric on a trail &mdash; and that coat needs real upkeep.'),
    ('boxer',                'Boxer',                'Looks tough, acts goofy &mdash; a demanding dog that&rsquo;s easy to underestimate.'),
    ('brussels-griffon',     'Brussels Griffon',     'A velcro companion in a tiny, opinionated package &mdash; more emotionally demanding than it looks.'),
    ('bull-terrier',         'Bull Terrier',         'The class clown with a stubborn streak &mdash; funny until training gets ignored.'),
    ('bulldog',              'Bulldog',              'The original couch potato &mdash; charming, low-key, and carrying real health tradeoffs.'),
    ('chihuahua',            'Chihuahua',            'Tiny body, outsized personality &mdash; needs real training despite the small packaging.'),
    ('chow-chow',            'Chow Chow',            'Reserved, serious, and deeply independent &mdash; not a dog for everyone.'),
    ('corgi',                'Corgi',                'A working dog in a footstool&rsquo;s body &mdash; more demanding than the memes suggest.'),
    ('dachshund',            'Dachshund',            'A surprisingly bold hunting dog in a hot-dog shape &mdash; that spine needs protecting.'),
    ('dalmatian',            'Dalmatian',            'The endurance athlete behind the Disney image &mdash; demanding and diet-specific.'),
    ('doberman',             'Doberman',             'Loyal, sensitive, and misunderstood &mdash; the real challenge is cardiac health, not temperament.'),
    ('english-toy-spaniel',  'English Toy Spaniel',  'A calm, devoted companion &mdash; genuinely easy to live with, with health caveats worth knowing.'),
    ('finnish-lapphund',     'Finnish Lapphund',     'A friendly, trainable Arctic breed &mdash; sociable, vocal, and surprisingly easygoing.'),
    ('german-shepherd',      'German Shepherd',      'One of the most capable breeds alive &mdash; and exactly why it ends up in the wrong hands.'),
    ('great-dane',           'Great Dane',           'Room-filling loyalty and a shorter run together than you&rsquo;d like.'),
    ('great-pyrenees',       'Great Pyrenees',       'An independent livestock guardian &mdash; the nighttime barking and stubbornness are features, not bugs.'),
    ('greyhound',            'Greyhound',            'Gentle at home, electric outside &mdash; and more apartment-friendly than you&rsquo;d think.'),
    ('irish-terrier',        'Irish Terrier',        'A fearless, loyal terrier &mdash; small enough to underestimate, bold enough to make that a mistake.'),
    ('irish-wolfhound',      'Irish Wolfhound',      'An ancient gentle giant &mdash; the lifespan is short and worth sitting with before committing.'),
    ('jack-russell-terrier', 'Jack Russell Terrier', 'One of the most demanding small breeds alive &mdash; not the apartment dog the size suggests.'),
    ('japanese-chin',        'Japanese Chin',        'A calm, elegant toy breed &mdash; easier than it looks, with health caveats worth knowing.'),
    ('kerry-blue-terrier',   'Kerry Blue Terrier',   'A versatile working terrier &mdash; the grooming commitment surprises people expecting a low-maintenance dog.'),
    ('leonberger',           'Leonberger',           'A gentle giant with genuine warmth &mdash; and all the giant-breed tradeoffs that come with it.'),
    ('lhasa-apso',           'Lhasa Apso',           'An ancient sentinel breed with real independence underneath the flowing coat &mdash; not just a lap dog.'),
    ('mastiff',              'Mastiff',              'The gentle giant of gentle giants &mdash; the temperament is easy, the physical realities are not.'),
    ('newfoundland',         'Newfoundland',         'Genuinely one of the best dogs with children &mdash; the coat, drool, and size are the honest caveats.'),
]

cards_html = '\n\n'.join(
    f'    <a class="dive-card" href="{slug}.html">\n'
    f'      <div>\n'
    f'        <div class="dive-card-name">{name}</div>\n'
    f'        <div class="dive-card-teaser">{teaser}</div>\n'
    f'      </div>\n'
    f'      <span class="dive-card-arrow">&#8594;</span>\n'
    f'    </a>'
    for slug, name, teaser in ALL_CARDS
)

with open('deep-dives/index.html', encoding='utf-8') as f:
    idx = f.read()
new_grid = f'  <div class="dive-grid">\n\n{cards_html}\n\n  </div>'
idx = re.sub(r'<div class="dive-grid">.*?</div>', new_grid, idx, flags=re.DOTALL)
with open('deep-dives/index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print('Updated: deep-dives/index.html')


# CTA buttons on breed pages
CTA_CSS = """\
    .deep-dive-cta {
      display: inline-block;
      background: #FFF8EC;
      border: 2px solid #C05621;
      border-radius: 10px;
      padding: 16px 24px;
      text-decoration: none;
      color: #C05621;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 0.95rem;
      font-style: italic;
      box-shadow: 0 2px 8px rgba(92,61,17,0.12);
      transition: background 0.15s, color 0.15s, box-shadow 0.15s;
      align-self: flex-start;
    }
    .deep-dive-cta:hover {
      background: #C05621;
      color: #FFF8EC;
      box-shadow: 0 3px 12px rgba(192,86,33,0.22);
    }
"""
OLD_FOOTER_CSS = "    footer {\n      background: #5C3D11;"
FACTS_CLOSE = '<div id="facts-section"></div>\n\n</div>'

for slug, title, *_ in BREEDS:
    breed_path = f'breeds/{slug}.html'
    if not os.path.exists(breed_path):
        print(f'MISSING breed page: {breed_path}')
        continue
    with open(breed_path, encoding='utf-8') as f:
        content = f.read()
    if '.deep-dive-cta' not in content:
        content = content.replace(OLD_FOOTER_CSS, CTA_CSS + OLD_FOOTER_CSS, 1)
    cta_link = (
        f'  <a class="deep-dive-cta" href="../deep-dives/{slug}.html">'
        'There&rsquo;s more to this dog than facts. Deep dive &rarr;</a>'
    )
    if cta_link not in content:
        content = content.replace(
            FACTS_CLOSE,
            f'<div id="facts-section"></div>\n\n{cta_link}\n\n</div>',
            1
        )
    with open(breed_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'CTA added: {breed_path}')

print('\nAll done.')
