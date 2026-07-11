"""Rewrites deep-dives/index.html cleanly with all 45 cards."""
import re, os

ALL_CARDS = [
    ('akita',                 'Akita',                 'A dignified, one-family dog &mdash; loyal on its own terms and no one else&rsquo;s.'),
    ('alaskan-malamute',      'Alaskan Malamute',      'Tundra-bred strength and a friendly face &mdash; hiding an escape artist underneath.'),
    ('australian-shepherd',   'Australian Shepherd',   'The velcro herding dog &mdash; extraordinary partner if you can keep up.'),
    ('basenji',               'Basenji',               'The barkless dog &mdash; independent, cat-like, and very much on its own terms.'),
    ('basset-hound',          'Basset Hound',          'Low to the ground, high on vibes &mdash; a forgiving breed with a stubborn streak.'),
    ('beagle',                'Beagle',                'Nose-led, food-motivated, and louder than expected &mdash; loveable with caveats.'),
    ('bichon-frise',          'Bichon Frise',          'Small, cheerful, and low-shed &mdash; but that coat is a real commitment.'),
    ('bloodhound',            'Bloodhound',            'The world&rsquo;s best nose attached to a sweet, stubborn, drool-forward dog.'),
    ('border-collie',         'Border Collie',         'Extraordinary intelligence with extraordinary demands &mdash; not for the low-key household.'),
    ('borzoi',                'Borzoi',                'Serene indoors, electric on a trail &mdash; and that coat needs real upkeep.'),
    ('boxer',                 'Boxer',                 'Looks tough, acts goofy &mdash; a demanding dog that&rsquo;s easy to underestimate.'),
    ('brussels-griffon',      'Brussels Griffon',      'A velcro companion in a tiny, opinionated package &mdash; more emotionally demanding than it looks.'),
    ('bull-terrier',          'Bull Terrier',          'The class clown with a stubborn streak &mdash; funny until training gets ignored.'),
    ('bulldog',               'Bulldog',               'The original couch potato &mdash; charming, low-key, and carrying real health tradeoffs.'),
    ('chihuahua',             'Chihuahua',             'Tiny body, outsized personality &mdash; needs real training despite the small packaging.'),
    ('chow-chow',             'Chow Chow',             'Reserved, serious, and deeply independent &mdash; not a dog for everyone.'),
    ('corgi',                 'Corgi',                 'A working dog in a footstool&rsquo;s body &mdash; more demanding than the memes suggest.'),
    ('dachshund',             'Dachshund',             'A surprisingly bold hunting dog in a hot-dog shape &mdash; that spine needs protecting.'),
    ('dalmatian',             'Dalmatian',             'The endurance athlete behind the Disney image &mdash; demanding and diet-specific.'),
    ('doberman',              'Doberman',              'Loyal, sensitive, and misunderstood &mdash; the real challenge is cardiac health, not temperament.'),
    ('english-toy-spaniel',   'English Toy Spaniel',   'A calm, devoted companion &mdash; genuinely easy to live with, with health caveats worth knowing.'),
    ('finnish-lapphund',      'Finnish Lapphund',      'A friendly, trainable Arctic breed &mdash; sociable, vocal, and surprisingly easygoing.'),
    ('german-shepherd',       'German Shepherd',       'One of the most capable breeds alive &mdash; and exactly why it ends up in the wrong hands.'),
    ('great-dane',            'Great Dane',            'Room-filling loyalty and a shorter run together than you&rsquo;d like.'),
    ('great-pyrenees',        'Great Pyrenees',        'An independent livestock guardian &mdash; the nighttime barking and stubbornness are features, not bugs.'),
    ('greyhound',             'Greyhound',             'Gentle at home, electric outside &mdash; and more apartment-friendly than you&rsquo;d think.'),
    ('irish-terrier',         'Irish Terrier',         'A fearless, loyal terrier &mdash; small enough to underestimate, bold enough to make that a mistake.'),
    ('irish-wolfhound',       'Irish Wolfhound',       'An ancient gentle giant &mdash; the lifespan is short and worth sitting with before committing.'),
    ('jack-russell-terrier',  'Jack Russell Terrier',  'One of the most demanding small breeds alive &mdash; not the apartment dog the size suggests.'),
    ('japanese-chin',         'Japanese Chin',         'A calm, elegant toy breed &mdash; easier than it looks, with health caveats worth knowing.'),
    ('kerry-blue-terrier',    'Kerry Blue Terrier',    'A versatile working terrier &mdash; the grooming commitment surprises people expecting a low-maintenance dog.'),
    ('leonberger',            'Leonberger',            'A gentle giant with genuine warmth &mdash; and all the giant-breed tradeoffs that come with it.'),
    ('lhasa-apso',            'Lhasa Apso',            'An ancient sentinel breed with real independence underneath the flowing coat &mdash; not just a lap dog.'),
    ('mastiff',               'Mastiff',               'The gentle giant of gentle giants &mdash; the temperament is easy, the physical realities are not.'),
    ('newfoundland',          'Newfoundland',          'Genuinely one of the best dogs with children &mdash; the coat, drool, and size are the honest caveats.'),
    ('norwegian-elkhound',    'Norwegian Elkhound',    'An ancient, vocal Nordic hunter &mdash; loyal to family, loud about everything else.'),
    ('otterhound',            'Otterhound',            'One of the rarest breeds alive &mdash; a boisterous, water-loving hound that needs serious exercise.'),
    ('papillon',              'Papillon',              'An underrated toy breed &mdash; genuinely trainable, athletic, and nothing like the fragile lap dog it looks.'),
    ('pekingese',             'Pekingese',             'Ancient palace companion &mdash; the flat face is a real health consideration, not just a look.'),
    ('pointer',               'Pointer',               'A stamina athlete built for all-day field work &mdash; not a casual-exercise breed.'),
    ('poodle',                'Poodle',                'The intelligent athlete behind the show-dog reputation &mdash; demanding, trainable, and not low-maintenance.'),
    ('portuguese-water-dog',  'Portuguese Water Dog',  'An athletic, water-loving working dog &mdash; needs more than a walk to be genuinely content.'),
    ('pug',                   'Pug',                   'Genuinely charming &mdash; and the brachycephalic health realities are just as real as the personality.'),
    ('rottweiler',            'Rottweiler',            'A misunderstood, deeply loyal family dog &mdash; the work is socialization, not managing aggression.'),
    ('saint-bernard',         'Saint Bernard',         'The gentle giant rescue dog &mdash; patient with everyone, less so about personal space.'),
]

cards_html = '\n'.join(
    f'    <a class="dive-card" href="{slug}.html">\n'
    f'      <div>\n'
    f'        <div class="dive-card-name">{name}</div>\n'
    f'        <div class="dive-card-teaser">{teaser}</div>\n'
    f'      </div>\n'
    f'      <span class="dive-card-arrow">&#8594;</span>\n'
    f'    </a>'
    for slug, name, teaser in ALL_CARDS
)

html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Deep Dives &mdash; The Bark Facts</title>
  <style>
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
      padding: 36px 20px 20px;
      display: flex;
      flex-direction: column;
      gap: 28px;
    }

    .page-heading {
      text-align: center;
    }
    .page-heading h2 {
      font-size: 1.9rem;
      font-weight: normal;
      color: #5C3D11;
    }
    .page-heading p {
      font-size: 0.9rem;
      color: #9A6B3A;
      font-style: italic;
      margin-top: 6px;
      line-height: 1.6;
    }

    .dive-grid {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .dive-card {
      background: #FFF8EC;
      border: 2px solid #E0C090;
      border-radius: 10px;
      padding: 20px 24px;
      text-decoration: none;
      color: #3D2B1F;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(92,61,17,0.10);
      transition: border-color 0.15s, box-shadow 0.15s;
    }
    .dive-card:hover {
      border-color: #C05621;
      box-shadow: 0 3px 12px rgba(192,86,33,0.18);
    }
    .dive-card-name {
      font-size: 1.2rem;
      color: #5C3D11;
    }
    .dive-card-teaser {
      font-size: 0.8rem;
      color: #9A6B3A;
      font-style: italic;
      margin-top: 3px;
    }
    .dive-card-arrow {
      color: #C05621;
      font-size: 1.1rem;
    }

    .breadcrumb {
      font-size: 0.82rem;
    }
    .breadcrumb a {
      color: #C05621;
      text-decoration: none;
    }
    .breadcrumb a:hover { text-decoration: underline; }

    footer {
      background: #5C3D11;
      color: #A07840;
      text-align: center;
      font-size: 0.78rem;
      padding: 10px;
    }
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

  <div class="page-heading">
    <h2>Deep Dives</h2>
    <p>Beyond the facts &mdash; temperament, health, nutrition, and an honest take<br>on what it&rsquo;s actually like to live with these dogs.</p>
  </div>

  <div class="dive-grid">

CARDS_PLACEHOLDER

  </div>

  <div class="breadcrumb"><a href="../index.html">&#8592; Back to Home</a></div>

</div>

<footer>Dog Facts &mdash; a fun project</footer>

</body>
</html>
"""

html = html.replace('CARDS_PLACEHOLDER', cards_html)

out = os.path.join(os.path.dirname(__file__), 'deep-dives', 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

check = open(out, encoding='utf-8').read()
import re
cards = re.findall(r'class="dive-card"', check)
print(f"Cards written: {len(cards)}")
