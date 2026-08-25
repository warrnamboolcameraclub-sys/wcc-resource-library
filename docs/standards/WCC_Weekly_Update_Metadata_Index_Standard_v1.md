# WCC Weekly Update Metadata Index Standard v1

**Project:** Warrnambool Camera Club Weekly Update  
**Status:** Locked working standard  
**Effective from:** Issue 012  
**First implemented:** 24 August 2026  
**Purpose:** Provide a consistent metadata structure for indexing, searching, grouping and reusing individual Weekly Update articles, tips, series items, events, people, locations and resources.

---

## 1. Core Principle

The Weekly Update HTML is the source of truth.

Metadata is embedded directly in the HTML around the page, article, tip or event that it describes. This allows future indexing without maintaining a separate manual database for every article.

Visible headings should remain consistent with the metadata wherever practical.

---

## 2. Page-Level Metadata

Every Weekly Update page should use the main wrapper:

```html
<div class="wcc-weekly"
     data-publication="weekly-update"
     data-issue="012"
     data-published="2026-08-24">
```

### Required page fields

| Field | Purpose | Example |
|---|---|---|
| `data-publication` | Publication identifier | `weekly-update` |
| `data-issue` | Three-digit issue number | `012` |
| `data-published` | Publication date in ISO format | `2026-08-24` |

Do not add separate year or month fields. These can be derived from `data-published`.

---

## 3. Standard Item Metadata Fields

Use only the fields relevant to the item.

```text
data-index
data-category
data-series
data-part
data-code
data-level
data-tags
data-people
data-locations
data-event-date
data-event-status
```

### Field definitions

| Field | Purpose |
|---|---|
| `data-index` | Item type, such as `article`, `tip` or `event` |
| `data-category` | Controlled primary category |
| `data-series` | Stable series identifier |
| `data-part` | Part number within a series |
| `data-code` | Permanent code such as `B008` |
| `data-level` | Beginner, intermediate or advanced |
| `data-tags` | Searchable topic keywords |
| `data-people` | Material people associated with the item |
| `data-locations` | Material locations associated with the item |
| `data-event-date` | Event date in ISO format |
| `data-event-status` | Event status such as `confirmed` or `planning` |

---

## 4. Controlled Categories

Use the following category values unless the standard is deliberately revised:

```text
club-news
education
editing
photography-tips
challenge
competition
events
community
members-on-the-move
feature
```

### Category intent

| Category | Used for |
|---|---|
| `club-news` | Committee, AGM, surveys, website, membership |
| `education` | Long exposure, camera skills, ethics, presentations |
| `editing` | Lightroom and post-processing |
| `photography-tips` | Beginner, intermediate and advanced tips |
| `challenge` | Weekly camera challenges |
| `competition` | Judging, competitions, competition rules |
| `events` | Meetings, outings and workshops |
| `community` | Fundraising, Wellness Walk, community activity |
| `members-on-the-move` | Member travel stories |
| `feature` | Standalone photographic features and galleries |

Each item should normally have one principal category. Use tags for finer detail.

---

## 5. Unique HTML IDs

Every indexed article, tip or event must have a permanent unique HTML `id`.

### Recommended format

```text
wcc-YYYY-ISSUE-topic
```

Examples:

```text
wcc-2026-012-world-photography-day
wcc-2026-012-long-exposure-006
wcc-2026-012-lightroom-005
wcc-2026-012-survey
wcc-event-2026-09-03-judging
wcc-tip-b008
```

Once published, do not casually rename an ID. It may later be used as an index target or anchor.

---

## 6. Tags

Use approximately **3–7 meaningful tags per item**.

Good:

```text
long-exposure,focus,nd-filters,tripod,landscape
```

Avoid keyword stuffing:

```text
camera,photography,photo,photos,image,picture,photographer
```

### Tag rules

- lower-case
- use hyphens between words
- comma-separated
- use one agreed form consistently
- do not create plural/singular variants for the same concept without reason

Example: use `long-exposure`, not a mixture of `long-exposure`, `long-exposures` and `longexposure`.

---

## 7. Educational Series

Series articles should carry both the stable series identifier and part number.

Example:

```html
<section
    id="wcc-2026-012-long-exposure-006"
    data-index="article"
    data-category="education"
    data-series="mastering-long-exposure-photography"
    data-part="6"
    data-tags="long-exposure,focus,nd-filters,tripod,landscape">
```

### Current series identifiers

```text
mastering-long-exposure-photography
ethical-bird-photography
lightroom-basics
using-your-camera
```

Add new identifiers only when a genuine recurring series is created.

---

## 8. Photographer's Tips

Each tip is indexed individually, even though all three are displayed together.

Example:

```html
<article class="tip"
         id="wcc-tip-b008"
         data-index="tip"
         data-category="photography-tips"
         data-level="beginner"
         data-code="B008"
         data-tags="iso,exposure,noise,camera-basics">
```

### Level values

```text
beginner
intermediate
advanced
```

### Code structure

```text
Bxxx = Beginner
Ixxx = Intermediate
Axxx = Advanced
```

Codes are permanent once published.

---

## 9. Events

Events should carry the date and status where known.

Example, confirmed event:

```html
<article
    id="wcc-event-2026-09-03-judging"
    data-index="event"
    data-category="competition"
    data-event-date="2026-09-03"
    data-event-status="confirmed"
    data-tags="judging,competition,johanna-botman">
```

Example, event still being planned:

```html
<article
    id="wcc-event-2026-10-24-werribee-zoo"
    data-index="event"
    data-category="events"
    data-event-date="2026-10-24"
    data-event-status="planning"
    data-tags="outing,werribee-open-range-zoo,bus,photography">
```

### Event status values currently used

```text
confirmed
planning
```

Additional status values should only be added when a real need arises.

---

## 10. People and Locations

Use these fields only when the person or location is material to the article.

Example:

```html
data-people="craig-homberg,sharon-homberg"
data-locations="iceland,singapore"
```

Example:

```html
data-people="bob-artis,kerrie-artis"
data-locations="karumba,alice-springs"
```

Do not add every incidental name mentioned in an article.

---

## 11. Zenfolio Photo ID Workflow

Where the Zenfolio Photo ID is available, insert the image directly into the HTML master rather than inserting a Zenfolio `<zentobox>` first.

### Current working image path pattern

```html
<img src="/img/s/v-10/p1585012085-3.jpg" ... />
```

General form:

```text
/img/s/v-10/p[ZENFOLIO-PHOTO-ID]-3.jpg
```

### Image workflow

1. Upload photographs to Zenfolio.
2. Export or obtain the Zenfolio Photo ID index.
3. Match filename to Photo ID.
4. Insert the Photo ID directly into the HTML image path.
5. Add meaningful `alt` text.
6. Add the visible caption separately.
7. Use responsive image CSS.
8. Correct image orientation in Zenfolio itself where necessary rather than using CSS rotation.

This removes the previous insert → retrieve `<zentobox>` → clean HTML cycle.

---

## 12. Image Presentation Rules

Images must not crop on mobile.

Core responsive rule:

```css
.wcc-weekly .rollup img,
.wcc-weekly section img {
    display:block !important;
    width:auto !important;
    max-width:100% !important;
    height:auto !important;
    max-height:none !important;
    object-fit:contain !important;
    object-position:center center !important;
    margin:20px auto !important;
    box-sizing:border-box !important;
}
```

Relevant mobile protection should also be repeated inside the `@media (max-width:760px)` rule.

For galleries, use framed `.photo-card` containers consistently.

Do not put Zenfolio `<zentobox>` markup inside `<details>` elements.

---

## 13. Downloadable Guides

Download links should be full-width buttons beneath the explanatory feature card, not overlaid inside it.

Example:

```html
<div class="feature-card">
    <p><strong>📄 This Week's Guide:</strong> ...</p>
</div>

<a class="button teal"
   href="..."
   target="_blank"
   rel="noopener">
   Download ...
</a>
```

---

## 14. Newsletter Footer

Use a unique class so Zenfolio's own footer styles do not interfere.

```html
<div class="wcc-newsletter-footer">
    <strong>Warrnambool Camera Club</strong><br />
    Weekly Update | Issue 012<br /><br />
    <strong>Compiled &amp; edited by Stan McCullagh</strong><br /><br />
    Learn &bull; Create &bull; Share &bull; Inspire
</div>
```

Do **not** use the generic class name `.footer`.

The WCC newsletter footer appears immediately above Zenfolio's own site footer.

---

## 15. Issue 012 Seed Index

Issue 012 is the first edition built to this standard.

| Item | Category | Series / Code | Key Tags |
|---|---|---|---|
| From the Editor | `club-news` | — | weekly-update |
| World Photography Day – What Our Members Saw | `feature` | — | world-photography-day,member-images |
| Member Survey Update | `club-news` | — | survey,committee,member-feedback |
| Getting the Focus Right | `education` | Long Exposure Part 6 | long-exposure,focus,nd-filters,tripod |
| Sharpening Without Halos | `editing` | Lightroom Basics Part 5 | lightroom,sharpening,masking,halos |
| Understand What ISO Does | `photography-tips` | B008 | iso,exposure,noise,camera-basics |
| Use the Direction of Movement | `photography-tips` | I008 | composition,movement,gaze |
| Look for Tonal Separation | `photography-tips` | A008 | tone,monochrome,composition |
| Make the Ordinary Interesting | `challenge` | — | seeing,composition,creativity |
| Craig & Sharon – Iceland / Singapore | `members-on-the-move` | — | iceland,singapore,travel |
| Bob & Kerrie – Karumba to Alice Springs | `members-on-the-move` | — | karumba,alice-springs,travel |
| September Judging Night | `competition` | — | judging,competition,johanna-botman |
| Warrnambool Running Festival | `community` | — | volunteering,fundraising,running-festival |
| Werribee Open Range Zoo Outing | `events` | — | outing,werribee-open-range-zoo,bus |

---

## 16. Publication Workflow

The standard Weekly Update production flow is:

```text
1. Build and approve individual sections
2. Assemble the complete Weekly Update HTML
3. Add metadata to each indexable item
4. Upload photographs to Zenfolio
5. Obtain Zenfolio Photo IDs
6. Insert image paths directly into the HTML master
7. Add guide/download URLs
8. Check desktop and mobile layout
9. Check roll-ups and image framing
10. Check newsletter footer/sign-off
11. Publish the Zenfolio page
12. Send the short summary email linking prominently to the full page
13. Retain the published HTML as the master copy
```

---

## 17. Historical Issues

Issues 001–011 may be progressively brought into this metadata structure as they are converted or reviewed.

Historical conversions must preserve the wording, chronology and facts of the original edition. Metadata may be added without rewriting historical content.

---

## 18. Change Control

This document is:

**WCC Weekly Update Metadata Index Standard v1**

Any structural change should be deliberate and should result in a new version number when it affects how existing indexed content is interpreted.

Minor additions such as a genuinely necessary new tag do not require a new version.

Changes to:
- core field names
- category definitions
- ID structure
- event-status interpretation
- tip coding
- series identifiers

should be recorded in an updated version of this file.

---

## 19. Guiding Rule

The metadata exists to make the Weekly Update easier to search and reuse.

It should remain:

**consistent, compact, meaningful and invisible to normal readers.**
