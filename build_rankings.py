#!/usr/bin/env python3
"""Generate the Breed Rankings section for The Bark Facts.

Writes:
  Rankings/index.html               - the Breed Rankings landing page
  Rankings/fastest-dog-breeds.html  - breeds ranked by top running speed

Speeds are top sprint speed in mph. Figures with `est=True` have no reliable
published number (mostly toy and giant breeds); those are honest estimates from
size, build, and what the breed was made to do, and are marked with a * on the
page. Everything else is drawn from published breed-speed sources.

Re-run whenever the data below changes, then run build_sitemap.py.
Only breeds that already have a Deep Dive page belong here. Add new breeds to
FASTEST as their Deep Dives go live.
"""
from pathlib import Path

ROOT = Path(__file__).parent
OUT_DIR = ROOT / "Rankings"
DOMAIN = "https://thebarkfacts.com"

# (name, deep-dive slug, mph, estimate?, whimsical comment)
# Ordered fastest to slowest. km/h is computed.
FASTEST = [
    ("Greyhound", "greyhound", 45, False,
     "The undisputed champ. Forty-five miles an hour, then eighteen hours asleep on your couch."),
    ("Saluki", "saluki", 42, False,
     "Ancient royalty with a Guinness record to back it up. It only just lost the crown to the Greyhound."),
    ("Vizsla", "vizsla", 40, False,
     "Velcro at rest, rocket in a field. Blink and it's a dot on the horizon."),
    ("Irish Wolfhound", "irish-wolfhound", 40, False,
     "Yes, this much dog moves that fast. Alarming for about six seconds, then it's over."),
    ("Dalmatian", "dalmatian", 37, False,
     "Bred to run under carriages all day. Your morning jog is a warm-up."),
    ("Borzoi", "borzoi", 36, False,
     "Built like a Greyhound that went to finishing school. Quietly, deceptively quick."),
    ("Whippet", "whippet", 35, False,
     "The Greyhound's smaller cousin, and pound for pound maybe the better deal."),
    ("Weimaraner", "weimaraner", 35, False,
     "The Gray Ghost earns the name. Usually gone before you've registered it left."),
    ("Jack Russell Terrier", "jack-russell-terrier", 35, False,
     "All that speed crammed into a dog that flatly refuses to acknowledge its size."),
    ("Doberman", "doberman", 32, False,
     "Fast, and it looks fast. The kind of fast that ends arguments."),
    ("Pointer", "pointer", 32, True,
     "Built to sweep a field for hours. The speed is almost a side effect."),
    ("Boxer", "boxer", 31, False,
     "Goofy right up until it decides to run laps around the yard for no reason."),
    ("Border Collie", "border-collie", 30, False,
     "Could probably go faster if it weren't so busy managing everyone."),
    ("German Shepherd", "german-shepherd", 30, False,
     "Fast, precise, and annoyingly good at this like it's good at everything."),
    ("Great Dane", "great-dane", 30, False,
     "Thirty miles an hour of horse-sized dog. Give it room."),
    ("Standard Poodle", "poodle", 30, False,
     "Under the ridiculous haircut is a real athlete. People keep forgetting that."),
    ("Australian Shepherd", "australian-shepherd", 30, False,
     "Will run this fast around livestock, around your kids, or around nothing at all."),
    ("Siberian Husky", "siberian-husky", 30, False,
     "Quick in a sprint, tireless over distance, and gone the instant the gate opens."),
    ("Irish Terrier", "irish-terrier", 30, True,
     "The daredevil of the terrier world. Quicker than a dog that size has any right to be."),
    ("Bull Terrier", "bull-terrier", 30, True,
     "That egg-shaped head is hiding a surprisingly serious engine."),
    ("Kerry Blue Terrier", "kerry-blue-terrier", 28, True,
     "A working terrier under all that grooming. Faster than the show ring lets on."),
    ("Portuguese Water Dog", "portuguese-water-dog", 28, True,
     "Quick on land, quicker in the water. It was bred to keep up with boats."),
    ("Basenji", "basenji", 25, False,
     "The barkless one. Moves like a cat, then bolts like a hare."),
    ("Shiba Inu", "shiba-inu", 25, False,
     "Plenty fast, but only when it personally sees the point. Recall sold separately."),
    ("Akita", "akita", 25, True,
     "Dignified and unhurried, right up until it isn't. Then, briefly, quick."),
    ("Norwegian Elkhound", "norwegian-elkhound", 25, True,
     "Built to track moose across cold country. Sturdy and steady more than fast."),
    ("Rottweiler", "rottweiler", 25, True,
     "More power than speed, but you'd still lose the footrace."),
    ("Samoyed", "samoyed", 25, True,
     "That smile hides a sled dog. Endurance is the gift here, not the sprint."),
    ("Finnish Lapphund", "finnish-lapphund", 25, True,
     "A herder built to dodge reindeer. Nimble more than flat-out fast."),
    ("Corgi", "corgi", 24, True,
     "Those little legs turn over shockingly fast. Physics is as confused as you are."),
    ("Bloodhound", "bloodhound", 22, True,
     "The nose sets the pace, and the nose is in no particular hurry."),
    ("Otterhound", "otterhound", 22, True,
     "A big shaggy hound that ambles along until there's water. Then it commits."),
    ("Leonberger", "leonberger", 22, True,
     "A lot of dog moving at a gentleman's pace. No reason to rush."),
    ("Beagle", "beagle", 20, False,
     "Follows its nose at a steady trot. Speed was never the assignment."),
    ("Alaskan Malamute", "alaskan-malamute", 20, True,
     "Built to haul freight over distance, not to sprint. Truck, not sports car."),
    ("Great Pyrenees", "great-pyrenees", 20, True,
     "Guardians hold ground, they don't chase. Fast enough when it truly counts."),
    ("Newfoundland", "newfoundland", 20, True,
     "Slow on land, unstoppable in water. Wrong element for a footrace."),
    ("Papillon", "papillon", 18, False,
     "The butterfly ears do more than decorate. Tiny, springy, quicker than you'd guess."),
    ("Chow Chow", "chow-chow", 18, True,
     "That stilted walk was not built for speed. It was built for judging you."),
    ("Dachshund", "dachshund", 18, True,
     "Short legs, long body, one gear. Charming, not fast."),
    ("Mastiff", "mastiff", 18, True,
     "Two hundred pounds of no thank you. It will sit this one out."),
    ("Saint Bernard", "saint-bernard", 18, True,
     "Rescues people from snowbanks. Nobody ever said quickly."),
    ("Chihuahua", "chihuahua", 15, True,
     "The effort of a racehorse, roughly the output of a brisk walk."),
    ("Bichon Frise", "bichon-frise", 15, True,
     "The zoomies are real. The top speed is not. Adorable blur, very small radius."),
    ("Bulldog", "bulldog", 15, True,
     "Sprints in theory. In practice it prefers the shade and a solid nap."),
    ("Japanese Chin", "japanese-chin", 14, True,
     "Elegant, cat-like, and completely uninterested in hurrying anywhere."),
    ("Basset Hound", "basset-hound", 12, True,
     "Low to the ground and powered mostly by vibes. Those ears are basically drag."),
    ("Brussels Griffon", "brussels-griffon", 12, True,
     "Big personality, short stride. It'll supervise the race, not enter it."),
    ("English Toy Spaniel", "english-toy-spaniel", 12, True,
     "Bred for laps, not for laps of the track. Perfectly happy with the trade."),
    ("Lhasa Apso", "lhasa-apso", 12, True,
     "An ancient sentinel, not a sprinter. It patrols the walls, slowly."),
    ("Pug", "pug", 12, True,
     "The spirit is willing. The airway and the little legs are still negotiating."),
    ("Skye Terrier", "skye-terrier", 12, True,
     "All that coat over those short legs. Style over velocity, every time."),
    ("Pekingese", "pekingese", 10, True,
     "Bred for palace laps at a palace pace. The dignified anchor of this whole list."),
]


def kmh(mph: int) -> int:
    return round(mph * 1.60934)


HEAD_STYLE = """  <style>
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
    header .site-brand {
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
      max-width: 720px;
      width: 100%;
      margin: 0 auto;
      padding: 36px 20px 20px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    .page-heading { text-align: center; }
    .page-heading h1 {
      font-size: 2.1rem;
      font-weight: normal;
      color: #5C3D11;
      letter-spacing: 0.02em;
    }
    .page-heading p {
      font-size: 0.95rem;
      color: #9A6B3A;
      font-style: italic;
      margin-top: 8px;
      line-height: 1.6;
    }

    .note {
      background: #FFF8EC;
      border: 2px solid #E0C090;
      border-left: 6px solid #C05621;
      border-radius: 10px;
      padding: 14px 18px;
      font-size: 0.9rem;
      line-height: 1.6;
      color: #3D2B1F;
      box-shadow: 0 2px 8px rgba(92,61,17,0.10);
    }
    .note strong { color: #5C3D11; }

    .rank-list { display: flex; flex-direction: column; gap: 10px; }

    .rank-row {
      background: #FFF8EC;
      border: 2px solid #E0C090;
      border-radius: 10px;
      padding: 16px 18px;
      display: flex;
      align-items: center;
      gap: 16px;
      box-shadow: 0 2px 8px rgba(92,61,17,0.10);
      transition: border-color 0.15s, box-shadow 0.15s;
    }
    .rank-row:hover {
      border-color: #C05621;
      box-shadow: 0 3px 12px rgba(192,86,33,0.18);
    }
    .rank-row.champ { border-color: #C05621; }

    .rank-num {
      font-size: 1.5rem;
      color: #C05621;
      min-width: 2.4rem;
      text-align: center;
      flex-shrink: 0;
    }
    .rank-body { flex: 1; min-width: 0; }
    .rank-name {
      font-size: 1.2rem;
      color: #5C3D11;
      text-decoration: none;
      border-bottom: 1px solid transparent;
    }
    .rank-name:hover { color: #C05621; border-bottom-color: #C05621; }
    .rank-comment {
      font-size: 0.9rem;
      color: #9A6B3A;
      font-style: italic;
      margin-top: 4px;
      line-height: 1.5;
    }

    .rank-speed { text-align: right; flex-shrink: 0; min-width: 5rem; }
    .rank-mph { font-size: 1.35rem; color: #5C3D11; white-space: nowrap; }
    .rank-mph .unit { font-size: 0.68rem; color: #9A6B3A; }
    .rank-mph .est { color: #C05621; }
    .rank-kmh { font-size: 0.75rem; color: #9A6B3A; margin-top: 2px; white-space: nowrap; }

    .rank-grid { display: flex; flex-direction: column; gap: 12px; }
    .rank-card {
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
    .rank-card:hover {
      border-color: #C05621;
      box-shadow: 0 3px 12px rgba(192,86,33,0.18);
    }
    .rank-card-name { font-size: 1.2rem; color: #5C3D11; }
    .rank-card-teaser { font-size: 0.8rem; color: #9A6B3A; font-style: italic; margin-top: 3px; }
    .rank-card-arrow { color: #C05621; font-size: 1.1rem; }
    .rank-soon {
      font-size: 0.85rem;
      color: #9A6B3A;
      font-style: italic;
      text-align: center;
      padding: 4px 0 0;
    }

    .breadcrumb { font-size: 0.82rem; }
    .breadcrumb a { color: #C05621; text-decoration: none; }
    .breadcrumb a:hover { text-decoration: underline; }

    .sources {
      font-size: 0.78rem;
      color: #9A6B3A;
      line-height: 1.6;
      border-top: 1px solid #E0C090;
      padding-top: 14px;
    }
    .sources a { color: #C05621; text-decoration: none; }
    .sources a:hover { text-decoration: underline; }

    footer {
      background: #5C3D11;
      color: #A07840;
      text-align: center;
      font-size: 0.78rem;
      padding: 10px;
    }

    @media (max-width: 520px) {
      .rank-row { padding: 14px 14px; gap: 10px; }
      .rank-num { font-size: 1.25rem; min-width: 1.9rem; }
      .rank-mph { font-size: 1.15rem; }
      .rank-speed { min-width: 4.4rem; }
    }
  </style>"""

FAVICON = """  <!-- FAVICON:BEGIN (generated by add_favicon_links.py) -->
  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#5C3D11" />
  <!-- FAVICON:END -->"""


def nav(active: str) -> str:
    """Site nav for pages one directory deep (Rankings/)."""
    def cls(name):
        return ' class="active"' if name == active else ""
    return f"""<nav class="site-nav">
  <a href="../index.html">Home</a>
  <a href="../breeds/index.html">Browse Facts</a>
  <a href="../deep-dives/index.html">Breeds</a>
  <a href="index.html"{cls('rankings')}>Breed Rankings</a>
  <a href="../about.html">About</a>
</nav>"""


HEADER = """<header>
  <div class="site-brand">The Bark Facts</div>
  <div class="subtitle">Real facts and honest takes on the dogs we love.</div>
</header>"""

FOOTER = "<footer>The Bark Facts &middot; Real facts and honest takes on the dogs we love.</footer>"


def build_fastest():
    rows = []
    for i, (name, slug, mph, est, comment) in enumerate(FASTEST, start=1):
        champ = " champ" if i == 1 else ""
        star = '<span class="est">*</span>' if est else ""
        rows.append(f"""    <div class="rank-row{champ}">
      <div class="rank-num">{i}</div>
      <div class="rank-body">
        <a class="rank-name" href="../deep-dives/{slug}.html">{name}</a>
        <div class="rank-comment">{comment}</div>
      </div>
      <div class="rank-speed">
        <div class="rank-mph">{mph}{star} <span class="unit">mph</span></div>
        <div class="rank-kmh">{kmh(mph)} km/h</div>
      </div>
    </div>""")
    rows_html = "\n".join(rows)

    # JSON-LD ItemList of the ranking.
    items = []
    for i, (name, slug, mph, est, comment) in enumerate(FASTEST, start=1):
        items.append(f"""    {{
      "@type": "ListItem",
      "position": {i},
      "name": "{name}",
      "url": "{DOMAIN}/deep-dives/{slug}.html"
    }}""")
    itemlist = ",\n".join(items)

    desc = ("All 53 dog breeds in our Deep Dives, ranked from fastest to slowest "
            "by top running speed in mph and km/h, with an honest, funny take on each.")
    url = f"{DOMAIN}/Rankings/fastest-dog-breeds.html"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fastest Dog Breeds, Ranked by Speed &middot; The Bark Facts</title>
{HEAD_STYLE}
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="index, follow" />
  <meta property="og:site_name" content="The Bark Facts" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="Fastest Dog Breeds, Ranked by Speed" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{DOMAIN}/images/og-cover.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Fastest Dog Breeds, Ranked by Speed" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{DOMAIN}/images/og-cover.jpg" />
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Fastest Dog Breeds, Ranked by Speed",
  "description": "{desc}",
  "url": "{url}",
  "numberOfItems": {len(FASTEST)},
  "itemListOrder": "https://schema.org/ItemListOrderDescending",
  "itemListElement": [
{itemlist}
  ]
}}
  </script>
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{DOMAIN}/" }},
    {{ "@type": "ListItem", "position": 2, "name": "Breed Rankings", "item": "{DOMAIN}/Rankings/" }},
    {{ "@type": "ListItem", "position": 3, "name": "Fastest Dog Breeds", "item": "{url}" }}
  ]
}}
  </script>
{FAVICON}
</head>
<body>

{HEADER}
{nav('rankings')}

<div class="main">

  <div class="page-heading">
    <h1>Fastest Dog Breeds, Ranked</h1>
    <p>Every breed in our Deep Dives, lined up from flat-out fastest to proudly<br>slowest. A few of these will surprise you. A few really won't.</p>
  </div>

  <div class="note">
    Speeds are top sprint speed. Numbers marked with a <strong>*</strong> are our
    own estimate. Where no reliable published figure exists, mostly the toy and
    giant breeds, we estimated from size, build, and what the dog was made to do.
    We marked those so you always know which is which.
  </div>

  <div class="rank-list">
{rows_html}
  </div>

  <div class="sources">
    Published speeds drawn from
    <a href="https://basepaws.com/blog/top-15-fastest-dog-breeds" rel="nofollow noopener" target="_blank">Basepaws</a>,
    <a href="https://highlandcanine.com/blog/the-fastest-dog-breeds-in-the-world/" rel="nofollow noopener" target="_blank">Highland Canine</a>, and
    <a href="https://www.lovetoknowpets.com/life-with-pets/how-fast-can-dogs-run-13-fastest-10-slowest-breeds" rel="nofollow noopener" target="_blank">LoveToKnow Pets</a>.
    Individual dogs vary. Your couch potato is not disqualified.
  </div>

  <div class="breadcrumb"><a href="index.html">&#8592; All Breed Rankings</a></div>

</div>

{FOOTER}

</body>
</html>
"""


def build_landing():
    desc = ("The Bark Facts breed rankings: our Deep Dive breeds sorted by the "
            "numbers and by our honest read of them. Starting with top speed.")
    url = f"{DOMAIN}/Rankings/"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Breed Rankings &middot; The Bark Facts</title>
{HEAD_STYLE}
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="index, follow" />
  <meta property="og:site_name" content="The Bark Facts" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Breed Rankings &mdash; The Bark Facts" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{DOMAIN}/images/og-cover.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Breed Rankings &mdash; The Bark Facts" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{DOMAIN}/images/og-cover.jpg" />
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Breed Rankings",
  "description": "{desc}",
  "url": "{url}",
  "isPartOf": {{ "@type": "WebSite", "name": "The Bark Facts", "url": "{DOMAIN}/" }}
}}
  </script>
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{DOMAIN}/" }},
    {{ "@type": "ListItem", "position": 2, "name": "Breed Rankings", "item": "{url}" }}
  ]
}}
  </script>
{FAVICON}
</head>
<body>

{HEADER}
{nav('rankings')}

<div class="main">

  <div class="page-heading">
    <h1>Breed Rankings</h1>
    <p>We line up the breeds in our Deep Dives by the numbers, and by our honest<br>read of them. One list so far. More on the way.</p>
  </div>

  <div class="rank-grid">
    <a class="rank-card" href="fastest-dog-breeds.html">
      <div>
        <div class="rank-card-name">Fastest Dog Breeds</div>
        <div class="rank-card-teaser">Every breed we cover, ranked from flat-out fastest to proudly slowest.</div>
      </div>
      <span class="rank-card-arrow">&#8594;</span>
    </a>
  </div>

  <div class="rank-soon">More rankings coming. Hungriest, biggest, and a few you won't see anywhere else.</div>

  <div class="breadcrumb"><a href="../index.html">&#8592; Back to Home</a></div>

</div>

{FOOTER}

</body>
</html>
"""


def main():
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "fastest-dog-breeds.html").write_text(build_fastest(), encoding="utf-8")
    (OUT_DIR / "index.html").write_text(build_landing(), encoding="utf-8")
    print(f"Wrote Rankings/index.html and Rankings/fastest-dog-breeds.html "
          f"({len(FASTEST)} breeds ranked)")


if __name__ == "__main__":
    main()
