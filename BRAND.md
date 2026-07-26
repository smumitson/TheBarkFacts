# The Bark Facts — Brand Guide

Persistent brand reference for The Bark Facts. Read this before designing a new
page, writing copy, or making a graphic, so everything stays consistent.

- **Name:** The Bark Facts
- **Domain:** https://thebarkfacts.com
- **Tagline:** Real facts and honest takes on the dogs we love.
- **What it is:** A dog facts and breed site. Quirky true facts, plus honest,
  in-depth breed deep dives.

---

## Voice and tone

The whole brand runs on one idea: honest. We love dogs and we say the true
thing, even when the true thing is "this breed is not for you."

**How it sounds:**

- Warm, but with a dry sense of humor. Fond of dogs, never syrupy about them.
- Plainspoken. Short sentences are good. Contractions always.
- Specific over general. A real detail beats a vague claim.
- Willing to be blunt. The "Honest Take" on each breed exists to tell people
  what they won't hear from a breeder trying to make a sale.
- Punchy fragments are on-brand for captions and taglines. Think "Ancient.
  Loyal. Not interested in your opinion." That clipped, declarative rhythm is
  part of the personality.

**Hard rules:**

- **No em dashes, ever.** They read as AI writing. Use a comma, a colon, a
  period, or restructure the sentence.
- No AI filler: skip "dive in," "unpack," "delve," "leverage," "robust,"
  "seamless," "elevate," "in today's world."
- Don't open a paragraph by restating the question or heading.
- Don't pad with three-item lists just for rhythm. Two is fine when two is true.
- For health and breed advice, stay honest about limits: we're dog lovers, not
  veterinarians. When it matters, point people to their vet.

---

## Color palette

Warm and earthy: browns, cream, and a rust-orange accent. Everything leans warm.

### Core

| Color | Hex | Use |
|---|---|---|
| Rust orange (accent) | `#C05621` | Primary accent. Links, active states, CTAs, key highlights. |
| Highlight orange | `#E8863B` | Lighter accent. Paw mark, share-image art. |
| Primary brown | `#5C3D11` | Header, footer, main headings. The brand's anchor color. |
| Darkest brown | `#4A2E0A` | Nav bar background. |
| Near-black brown | `#3A2509` | Photo frame background. |
| Cream (page) | `#FAF0DC` | Page background. |
| Card cream | `#FFF8EC` | Card and panel backgrounds. |
| Body text | `#3D2B1F` | Default text on cream. |
| Card border tan | `#E0C090` | Borders on cards and panels. |
| Label brown | `#7A4F2A` | Small section labels, muted headings. |
| Caption brown | `#9A6B3A` | Taglines, captions. |
| Nav link tan | `#C8A87A` | Inactive nav links. |
| Subtitle tan | `#D4B483` | Header subtitle. |
| Footer text | `#A07840` | Footer text on brown. |

### Semantic badges (deep-dive "Quick Glance" stats)

These carry meaning, so keep the mapping consistent. Text color in parentheses.

| Badge | Background | Meaning |
|---|---|---|
| low | `#E4CFA0` (`#4A2E0A`) | Low / easy |
| moderate | `#C8A870` (`#3D2B1F`) | Moderate |
| high | `#C05621` (`#FFF8EC`) | High |
| very-high | `#5C3D11` (`#FAF0DC`) | Very high |
| neutral | `#7A4F2A` (`#FAF0DC`) | Descriptive, no scale |
| yes | `#6B7C45` (`#F5F0E8`) | Yes / good (the one sage green) |
| with-exp | `#B8880A` (`#FFF8EC`) | Qualified yes (amber) |
| no | `#8B3A1A` (`#FAF0DC`) | No / not recommended (dark rust) |

---

## Typography

- **Typeface:** Georgia, `"Times New Roman"`, serif. Serif throughout, no sans.
  It reads warm and a little old-fashioned, which fits.
- **Scale:**
  - Site name (header): `4rem`
  - Page / breed title (`h1`): `2.4rem`, weight normal
  - Section labels (uppercase, italic, letter-spaced): `0.78rem`
  - Body: `1.05rem` to `1.2rem`, line-height `1.7`–`1.8`
  - Nav / subtitle: `0.82`–`0.85rem`, subtitle italic
- Headings use `letter-spacing: 0.04em` and normal (not bold) weight for that
  understated, classic look.

---

## Logo and assets

- **Mascot / logo:** a cartoon dog holding a megaphone (`images/the_bark_facts_2.jpg`).
  The megaphone is the brand's little joke: barking the facts. Keep the full-size
  original as the source for share graphics.
- **Header logo:** `images/logo-header.jpg` (400x256), a small version of the
  mascot used at the top of the home page. Don't use the full-size file in the
  header.
- **Favicon:** a paw print, highlight orange `#E8863B` on a primary-brown
  rounded tile. Simple on purpose so it reads at 16px.
- **Social share image:** `images/og-cover.jpg` (1200x630), brown card with the
  paw mark, the wordmark, the tagline, and the mascot framed on the right.

---

## UI patterns

- **Header:** primary-brown bar, centered cream site name, italic tan subtitle.
- **Nav:** darkest-brown bar, tan links, rust-orange underline on the active or
  hovered link.
- **Cards / sections:** card-cream background, tan border, `10px` radius, soft
  brown shadow (`rgba(92,61,17,0.12)`). This is the workhorse container.
- **Honest Take callout:** same card with a `4px` rust-orange left border and a
  rust-orange heading, to set the blunt section apart.
- **Buttons / CTAs:** rust-orange background, cream text, darker orange
  (`#9E4418`) on hover.
- **Related-breed chips:** pill shape, cream background, rust-orange border and
  text, filling to rust-orange on hover.
- **Footer:** primary-brown bar, muted `#A07840` text.

---

## Using this with the SEO skill

When running the `seo-static-site` skill on this site, the `seo.config.json`
brand block maps to the core palette:

```json
"brand": {
  "primary": "#5C3D11",
  "accent":  "#C05621",
  "bg":      "#FAF0DC",
  "on_primary": "#FAF0DC"
},
"theme_color": "#5C3D11"
```

---

*Keep this current. If a color, rule, or asset changes on the site, update it
here so this stays the single source of truth.*
