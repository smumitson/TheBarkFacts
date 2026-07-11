"""Fix CTA injection for batch 5 breed pages."""
import os

BASE = r'E:\ClaudeCode\dog_facts'

SLUGS = [
    'saluki', 'samoyed', 'shiba-inu', 'siberian-husky',
    'skye-terrier', 'vizsla', 'weimaraner', 'whippet',
]

CTA_CSS = """
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
    }"""

for slug in SLUGS:
    path = os.path.join(BASE, 'breeds', f'{slug}.html')
    content = open(path, encoding='utf-8').read()

    # Check if CTA already present
    if f'../deep-dives/{slug}.html' in content:
        print(f'Already done: {slug}')
        continue

    # 1. Add CSS before 'footer {' if not already present
    if 'deep-dive-cta' not in content:
        content = content.replace('    footer {', CTA_CSS + '\n    footer {', 1)

    # 2. Insert CTA HTML after <div id="facts-section"></div>
    cta_html = f'\n\n  <a class="deep-dive-cta" href="../deep-dives/{slug}.html">There&rsquo;s more to this dog than facts. Deep dive &rarr;</a>'
    content = content.replace(
        '<div id="facts-section"></div>',
        '<div id="facts-section"></div>' + cta_html,
        1
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Fixed: {slug}')
