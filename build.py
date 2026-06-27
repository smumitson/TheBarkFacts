import json

with open('E:/ClaudeCode/dog_facts/dog_facts.json', encoding='utf-8') as f:
    facts_data = json.load(f)

with open('E:/ClaudeCode/dog_facts/images/photo_tags.json', encoding='utf-8') as f:
    photo_data = json.load(f)

facts_js = json.dumps(facts_data['facts'], ensure_ascii=False)
photos_js = json.dumps(photo_data['photos'], ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>The Bark Facts</title>
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

    .main {{
      flex: 1;
      max-width: 780px;
      width: 100%;
      margin: 0 auto;
      padding: 28px 20px 20px;
      display: flex;
      flex-direction: column;
      gap: 22px;
    }}

    .photo-section {{
      background: #5C3D11;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 3px 12px rgba(92,61,17,0.25);
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .photo-section img {{
      width: 100%;
      max-height: 320px;
      object-fit: cover;
      display: block;
    }}
    .photo-caption {{
      color: #F5E6C8;
      font-style: italic;
      font-size: 0.95rem;
      padding: 10px 18px 12px;
      text-align: center;
      background: #5C3D11;
      width: 100%;
    }}

    .facts-section {{
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .fact-card {{
      background: #FFF8EC;
      border: 1px solid #E0C090;
      border-radius: 8px;
      padding: 16px 20px;
      box-shadow: 0 2px 6px rgba(92,61,17,0.1);
    }}
    .fact-card.today-highlight {{
      border-color: #C05621;
      border-width: 2px;
      background: #FFF3E0;
    }}
    .fact-number {{
      font-size: 0.75rem;
      font-weight: bold;
      color: #C05621;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 4px;
    }}
    .fact-category {{
      font-size: 0.75rem;
      color: #9A6B3A;
      margin-bottom: 8px;
      font-style: italic;
    }}
    .fact-text {{
      font-size: 1rem;
      line-height: 1.6;
      color: #3D2B1F;
    }}
    .fact-breed-tag {{
      display: inline-block;
      margin-top: 8px;
      font-size: 0.72rem;
      background: #C05621;
      color: white;
      padding: 2px 8px;
      border-radius: 10px;
      text-transform: capitalize;
    }}

    .today-banner {{
      background: #C05621;
      color: white;
      text-align: center;
      font-size: 0.85rem;
      padding: 8px 12px;
      border-radius: 6px;
      letter-spacing: 0.02em;
    }}

    .nav-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 0 20px;
      gap: 12px;
    }}
    .nav-bar button {{
      background: #C05621;
      color: white;
      border: none;
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 0.95rem;
      font-family: Georgia, serif;
      cursor: pointer;
      transition: background 0.15s;
      min-width: 70px;
    }}
    .nav-bar button:hover:not(:disabled) {{
      background: #9E4418;
    }}
    .nav-bar button:disabled {{
      background: #C8A87A;
      cursor: default;
    }}
    .page-counter {{
      font-size: 0.9rem;
      color: #7A4F2A;
      text-align: center;
      flex: 1;
    }}
    .page-counter strong {{
      color: #5C3D11;
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
  <h1><img src="images/the_bark_facts_2.jpg" alt="The Bark Facts" style="height:1.8em;vertical-align:middle;margin-right:10px;border-radius:4px;"> The Bark Facts</h1>
  <div class="subtitle">200 facts about man's best friend</div>
</header>

<div class="main">
  <div id="today-banner" class="today-banner" style="display:none"></div>

  <div class="photo-section">
    <img id="dog-photo" src="" alt="Dog photo" />
    <div id="photo-caption" class="photo-caption"></div>
  </div>

  <div class="facts-section" id="facts-section"></div>

  <div class="nav-bar">
    <button id="btn-first" onclick="goToPage(1)">&#171; First</button>
    <button id="btn-back" onclick="changePage(-1)">&#8592; Back</button>
    <div class="page-counter">
      Page <strong id="page-num">1</strong> of <strong id="page-total">67</strong>
    </div>
    <button id="btn-next" onclick="changePage(1)">Next &#8594;</button>
    <button id="btn-last" onclick="goToPage(TOTAL_PAGES)">Last &#187;</button>
  </div>
</div>

<footer>Dog Facts &mdash; a fun project</footer>

<script>
const FACTS = {facts_js};
const PHOTOS = {photos_js};

const FACTS_PER_PAGE = 3;
const TOTAL_PAGES = Math.ceil(FACTS.length / FACTS_PER_PAGE);

// Index photos by breed
const photosByBreed = {{}};
PHOTOS.forEach(p => {{
  p.breeds.forEach(b => {{
    if (!photosByBreed[b]) photosByBreed[b] = [];
    photosByBreed[b].push(p);
  }});
}});

function getDayOfYear() {{
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 1);
  return Math.ceil((now - start) / 86400000);
}}

const todayFactNum = Math.min(getDayOfYear(), FACTS.length);
const todayPage = Math.ceil(todayFactNum / FACTS_PER_PAGE);
let currentPage = todayPage;

function pickPhoto(pageNum, pageFacts) {{
  const breeds = pageFacts.map(f => f.breed).filter(Boolean);
  let pool = [];
  for (const breed of breeds) {{
    if (photosByBreed[breed]) pool = pool.concat(photosByBreed[breed]);
  }}
  if (pool.length === 0) pool = photosByBreed['generic'] || [];
  if (pool.length === 0) return null;
  return pool[pageNum % pool.length];
}}

function render(pageNum) {{
  const startIdx = (pageNum - 1) * FACTS_PER_PAGE;
  const pageFacts = FACTS.slice(startIdx, startIdx + FACTS_PER_PAGE);

  // Photo
  const photo = pickPhoto(pageNum, pageFacts);
  if (photo) {{
    document.getElementById('dog-photo').src = 'images/' + photo.file;
    document.getElementById('dog-photo').alt = photo.caption;
    document.getElementById('photo-caption').textContent = photo.caption;
  }}

  // Today banner
  const banner = document.getElementById('today-banner');
  if (pageNum === todayPage) {{
    const months = ['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec'];
    const now = new Date();
    banner.textContent = '\\u2605 Fact of the Day \\u2014 ' +
      months[now.getMonth()] + ' ' + now.getDate() + ', ' + now.getFullYear() +
      ' \\u2014 Fact #' + todayFactNum;
    banner.style.display = 'block';
  }} else {{
    banner.style.display = 'none';
  }}

  // Facts
  const section = document.getElementById('facts-section');
  section.innerHTML = '';
  pageFacts.forEach(fact => {{
    const card = document.createElement('div');
    card.className = 'fact-card' + (fact.fact_number === todayFactNum ? ' today-highlight' : '');
    card.innerHTML =
      '<div class="fact-number">Fact #' + fact.fact_number + '</div>' +
      '<div class="fact-category">' + fact.category + '</div>' +
      '<div class="fact-text">' + fact.fact + '</div>' +
      (fact.breed ? '<span class="fact-breed-tag">' + fact.breed + '</span>' : '');
    section.appendChild(card);
  }});

  // Navigation
  document.getElementById('page-num').textContent = pageNum;
  document.getElementById('page-total').textContent = TOTAL_PAGES;
  document.getElementById('btn-first').disabled = pageNum <= 1;
  document.getElementById('btn-back').disabled = pageNum <= 1;
  document.getElementById('btn-next').disabled = pageNum >= TOTAL_PAGES;
  document.getElementById('btn-last').disabled = pageNum >= TOTAL_PAGES;

  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function changePage(delta) {{
  const next = currentPage + delta;
  if (next >= 1 && next <= TOTAL_PAGES) {{
    currentPage = next;
    render(currentPage);
  }}
}}

function goToPage(n) {{
  if (n >= 1 && n <= TOTAL_PAGES) {{
    currentPage = n;
    render(currentPage);
  }}
}}

render(currentPage);
</script>
</body>
</html>"""

with open('E:/ClaudeCode/dog_facts/browse.html', 'w', encoding='utf-8') as f:
    f.write(html)

# ── index.html — one fact per page ───────────────────────────────────────────

daily_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>The Bark Facts</title>
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
      padding: 10px 18px 12px;
      text-align: center;
      background: #5C3D11;
      width: 100%;
    }}

    .today-banner {{
      background: #C05621;
      color: white;
      text-align: center;
      font-size: 0.85rem;
      padding: 8px 12px;
      border-radius: 6px;
      letter-spacing: 0.02em;
    }}

    .fact-card {{
      background: #FFF8EC;
      border: 2px solid #E0C090;
      border-radius: 10px;
      padding: 28px 30px;
      box-shadow: 0 2px 8px rgba(92,61,17,0.12);
    }}
    .fact-card.today-highlight {{
      border-color: #C05621;
      background: #FFF3E0;
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
      justify-content: space-between;
      margin-top: 14px;
    }}
    .share-btn {{
      background: none;
      border: 1px solid #C05621;
      color: #C05621;
      border-radius: 6px;
      padding: 5px 12px;
      font-size: 0.78rem;
      font-family: Georgia, serif;
      cursor: pointer;
      transition: background 0.15s, color 0.15s;
    }}
    .share-btn:hover {{
      background: #C05621;
      color: white;
    }}

    .nav-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 0 20px;
      gap: 12px;
    }}
    .nav-bar button {{
      background: #C05621;
      color: white;
      border: none;
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 0.95rem;
      font-family: Georgia, serif;
      cursor: pointer;
      transition: background 0.15s;
      min-width: 70px;
    }}
    .nav-bar button:hover:not(:disabled) {{
      background: #9E4418;
    }}
    .nav-bar button:disabled {{
      background: #C8A87A;
      cursor: default;
    }}
    .page-counter {{
      font-size: 0.9rem;
      color: #7A4F2A;
      text-align: center;
      flex: 1;
    }}
    .page-counter strong {{
      color: #5C3D11;
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
  <h1><img src="images/the_bark_facts_2.jpg" alt="The Bark Facts" style="height:1.8em;vertical-align:middle;margin-right:10px;border-radius:4px;"> The Bark Facts</h1>
  <div class="subtitle">one fact, one dog, one day at a time</div>
</header>

<div class="main">
  <div id="today-banner" class="today-banner" style="display:none"></div>

  <div class="photo-section">
    <img id="dog-photo" src="" alt="Dog photo" />
    <div id="photo-caption" class="photo-caption"></div>
  </div>

  <div id="fact-card"></div>

  <div class="nav-bar">
    <button id="btn-first" onclick="goToFact(1)">&#171; First</button>
    <button id="btn-back" onclick="changeFact(-1)">&#8592; Back</button>
    <div class="page-counter">
      Fact <strong id="fact-num">1</strong> of <strong>{len(facts_data['facts'])}</strong>
    </div>
    <button id="btn-next" onclick="changeFact(1)">Next &#8594;</button>
    <button id="btn-last" onclick="goToFact(TOTAL)">Last &#187;</button>
  </div>
</div>

<footer>Dog Facts &mdash; a fun project</footer>

<script>
const FACTS = {facts_js};
const PHOTOS = {photos_js};
const TOTAL = FACTS.length;

const photosByBreed = {{}};
PHOTOS.forEach(p => {{
  p.breeds.forEach(b => {{
    if (!photosByBreed[b]) photosByBreed[b] = [];
    photosByBreed[b].push(p);
  }});
}});

function getDayOfYear() {{
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 1);
  return Math.ceil((now - start) / 86400000);
}}

const todayFactNum = Math.min(getDayOfYear(), TOTAL);
let current = todayFactNum;

function pickPhoto(factNum, breed) {{
  let pool = breed && photosByBreed[breed] ? photosByBreed[breed] : [];
  if (pool.length === 0) pool = photosByBreed['generic'] || [];
  if (pool.length === 0) return null;
  return pool[factNum % pool.length];
}}

function render(factNum) {{
  const fact = FACTS[factNum - 1];

  // Photo
  const photo = pickPhoto(factNum, fact.breed);
  if (photo) {{
    document.getElementById('dog-photo').src = 'images/' + photo.file;
    document.getElementById('dog-photo').alt = photo.caption;
    document.getElementById('photo-caption').textContent = photo.caption;
  }}

  // Today banner
  const banner = document.getElementById('today-banner');
  if (factNum === todayFactNum) {{
    const months = ['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec'];
    const now = new Date();
    banner.textContent = '\\u2605 Fact of the Day \\u2014 ' +
      months[now.getMonth()] + ' ' + now.getDate() + ', ' + now.getFullYear();
    banner.style.display = 'block';
  }} else {{
    banner.style.display = 'none';
  }}

  // Fact card
  const card = document.getElementById('fact-card');
  card.className = 'fact-card' + (factNum === todayFactNum ? ' today-highlight' : '');
  card.innerHTML =
    '<div class="fact-number">Fact #' + fact.fact_number + '</div>' +
    '<div class="fact-category">' + fact.category + '</div>' +
    '<div class="fact-text">' + fact.fact + '</div>' +
    '<div class="fact-footer">' +
      (fact.breed ? '<span class="fact-breed-tag">' + fact.breed + '</span>' : '<span></span>') +
      '<button class="share-btn" onclick="shareFact(' + fact.fact_number + ')">&#8679; Share</button>' +
    '</div>';

  // Counter & buttons
  document.getElementById('fact-num').textContent = factNum;
  document.getElementById('btn-first').disabled = factNum <= 1;
  document.getElementById('btn-back').disabled = factNum <= 1;
  document.getElementById('btn-next').disabled = factNum >= TOTAL;
  document.getElementById('btn-last').disabled = factNum >= TOTAL;

  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function shareFact(factNum) {{
  const fact = FACTS[factNum - 1];
  const text = 'Fact #' + factNum + ': ' + fact.fact + ' \u2014 The Bark Facts';
  if (navigator.share) {{
    navigator.share({{ title: 'The Bark Facts', text: text }});
  }} else {{
    navigator.clipboard.writeText(text).then(function() {{
      const btn = document.querySelector('.share-btn');
      const orig = btn.innerHTML;
      btn.textContent = 'Copied!';
      setTimeout(function() {{ btn.innerHTML = orig; }}, 1500);
    }});
  }}
}}

function changeFact(delta) {{
  const next = current + delta;
  if (next >= 1 && next <= TOTAL) {{
    current = next;
    render(current);
  }}
}}

function goToFact(n) {{
  if (n >= 1 && n <= TOTAL) {{
    current = n;
    render(current);
  }}
}}

render(current);
</script>
</body>
</html>"""

with open('E:/ClaudeCode/dog_facts/index.html', 'w', encoding='utf-8') as f:
    f.write(daily_html)

import math, datetime
day = datetime.date.today().timetuple().tm_yday
today_fact = min(day, 200)
print(f"index.html written  — 200 pages, 1 fact each")
print(f"browse.html written — {math.ceil(200/3)} pages, 3 facts each")
print(f"Today is day {day} -> Fact #{today_fact}")
