# The Bark Facts — Site Audit Report

## 1. Facts Data

Each fact in `dog_facts.json` has **four fields**:

| Field | Values |
|---|---|
| `fact_number` | 1–365 |
| `category` | Sensory, Biology, Anatomy, Behavior, Intelligence, History, Breeds |
| `fact` | The fact text |
| `breed` | An **explicit string tag** (e.g. `"greyhound"`) or `null` |

Breed association is an **explicit field, not text-scanned** — the `breed` key is set directly in the data. 132 of 365 facts have a breed; 233 have `null`.

---

## 2. Photos

`images/photo_tags.json` gives each photo: `file`, `breeds[]` (array, always one entry currently), `tags[]`, and `caption`.

At runtime, JS indexes all photos into a `photosByBreed` dictionary. **Photo selection** is deterministic: `pool[factNum % pool.length]` — it rotates through the breed's photos based on fact number, with a fallback to 15 generic photos when there's no breed match.

### Photo counts per breed (non-generic)

| Breed | Photos |
|---|---|
| greyhound | 12 |
| rottweiler | 8 |
| beagle | 7 |
| bloodhound | 7 |
| bulldog | 7 |
| chihuahua | 7 |
| dachshund | 7 |
| siberian husky | 7 |
| akita | 6 |
| australian shepherd | 6 |
| border collie | 6 |
| boxer | 6 |
| corgi | 6 |
| dalmatian | 6 |
| german shepherd | 6 |
| jack russell terrier | 6 |
| papillon | 6 |
| poodle | 6 |
| saluki | 6 |
| samoyed | 6 |
| basset hound | 5 |
| chow chow | 5 |
| great dane | 5 |
| mastiff | 5 |
| newfoundland | 5 |
| pug | 5 |
| saint bernard | 5 |
| whippet | 5 |
| great pyrenees | 2 |
| pekingese | 2 |
| shiba inu | 2 |
| (30+ breeds) | 1 each |
| generic (fallback) | 15 |

---

## 3. Page Structure & Navigation

There are **three HTML files** — `index.html`, `browse.html`, `daily.html` — and **zero links between them**. No `<a href>` navigation exists; the pages are isolated islands.

| File | Behavior |
|---|---|
| `index.html` | One fact at a time, ← Back / Next → navigation, loads today's fact on open |
| `browse.html` | 3 facts per page, 67 pages total, same day-of-year landing |
| `daily.html` | Fact-of-the-day only view |

All data (the full 365-fact array and the full photo array) is **inlined as JSON blobs** directly in each file's `<script>` block — there is no `fetch()` call to the `.json` files at runtime.

**Where new pages link in:** A `<nav>` bar needs to be added to the header of every page (none exists yet) and breed pages linked from there.

---

## 4. Styling

CSS is **embedded in a `<style>` block** in each file's `<head>` — no external stylesheet. The same rules are duplicated across all three files.

### Palette

| Role | Color |
|---|---|
| Page background | `#FAF0DC` (warm cream) |
| Header / footer | `#5C3D11` (dark walnut) |
| Accent (buttons, tags) | `#C05621` (burnt orange) |
| Fact card background | `#FFF8EC` |
| Fact card border | `#E0C090` |
| Body text | `#3D2B1F` (dark brown) |
| Secondary text | `#D4B483`, `#9A6B3A` |

Caption style is punchy 3–7 word fragments with dry wit (e.g. "Greyhound. 45mph. Also napping. Mostly napping.").

---

## Breed Pages — Proposed Plan

### Architecture

Follow the existing pattern: static HTML files with the breed's filtered facts and photos inlined in the `<script>` block. No build step, no server, fully consistent with the current site.

### URL Structure

```
breeds/greyhound.html
breeds/corgi.html
breeds/great-dane.html
breeds/index.html   (future directory page — good for SEO)
```

### What Goes on Each Breed Page

- Same header/footer/CSS palette
- Hero photo section rotating through the breed's photos
- All breed-specific facts listed as `.fact-card` cards
- A witty breed intro line in the header subtitle slot
- Breadcrumb / back link to home

### Navigation Change Needed First

Add a minimal `<nav>` to the header across all existing pages before building breed pages, so they're linked on day one. Suggested: "Home | Browse All | Breeds ▾"

### Which 3 Breeds to Build First

Ranked by facts × photos (both ingredients needed for a full page):

| Rank | Breed | Facts | Photos | Score |
|---|---|---|---|---|
| 1 | **Greyhound** | 8 | 12 | 96 — clear winner |
| 2 | **Corgi** | 5 | 6 | 30 |
| 3 | **Great Dane** | 5 | 5 | 25 |

German Shepherd (4 facts, 6 photos, score 24) is an honorable mention — slightly behind Great Dane on score but likely higher search volume.
