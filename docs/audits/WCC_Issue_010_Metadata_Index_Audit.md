# Issue 010 Metadata Index Audit

**Publication:** Warrnambool Camera Club Weekly Update  
**Issue:** 010  
**Published:** 10 August 2026  
**Metadata standard:** WCC Weekly Update Metadata Index Standard v1  
**Historical-content rule:** Published wording, chronology and historical state have been preserved. Metadata was added around the existing content.

| Indexed item | Category / type | Series / code | Key metadata |
|---|---|---|---|
| From the Editor | club-news / article | — | weekly update, AGM, website, Club activity |
| AGM Wrap-Up | club-news / article | — | AGM, Club Rules, AI guidance, governance |
| Meet Your 2026–27 Committee | club-news / article | — | committee, President, governance, named committee members |
| Refreshed Website | club-news / article | — | website, Club Rules, resources, activities |
| A Great Night with Craig Richards | education / article | — | Craig Richards, landscape photography, presentation |
| Craig Richards Landscape Photography Workshop | events / event | — | 15 August 2026, Middle Island, confirmed |
| World Photography Week is Almost Here | feature / article | — | World Photography Week, World Photography Day |
| Craig & Sharon Reach Iceland | members-on-the-move / article | — | Grundarfjörður, Iceland, member travel |
| Bob & Kerrie Keep Moving | members-on-the-move / article | — | Cape York, Karumba, Alice Springs |
| Neutral Density Filters – Unlocking the Magic of Long Exposure | education / article | Mastering Long Exposure Photography · Part 5 | Ian van der Wolde, ND filters, shutter speed, light leaks |
| Understanding the Histogram | editing / article | Lightroom Basics · Part 3 | histogram, exposure, clipping, highlights, shadows |
| Beginner Tip: Check Your Shutter Speed | photography-tips / tip | B006 | beginner, shutter speed, motion blur |
| Intermediate Tip: Use Negative Space | photography-tips / tip | I006 | composition, negative space |
| Advanced Tip: Watch Where the Brightest Area Falls | photography-tips / tip | A006 | brightness, visual attention, tonal control |
| Find the Foreground | challenge / article | — | foreground, landscape, composition |
| World Photography Day | feature / event | — | 19 August 2026, confirmed |
| Competition judging with Johanna Botman | competition / event | — | September only; no exact date back-filled |
| Warrnambool Marathon | community / event | — | 19–20 September; indexed from 19 September |
| Flash Trigger Workshop | events / event | — | 24 September 2026, confirmed |
| Potential Werribee Open Range Zoo outing | events / event | — | planning; October only; no exact date |
| Warrnambool Show Photography Competition | competition / event | — | October only; no exact date |
| Lightroom Part 3 downloadable guide | editing / resource | Lightroom Basics · Part 3 | PDF resource |

## Important historical/indexing notes

1. **Tip codes B006, I006 and A006** were not printed in the Issue 010 HTML. They have been added from the established sequence immediately preceding Issue 011's B007/I007/A007 and following Issue 009's B005/I005/A005.
2. **Werribee Open Range Zoo** remains `planning` because Issue 010 explicitly called it a “Potential” outing with details to be confirmed. No later date has been back-filled.
3. **Competition judging with Johanna Botman** remains September-only because that is all this issue stated.
4. **Warrnambool Show Photography Competition** remains October-only because no exact date appeared in the issue.
5. **Warrnambool Marathon** is shown in the source as 19–20 September. Metadata uses `data-event-date="2026-09-19"` as the starting date because Metadata Standard v1 currently has a single event-date field rather than start/end fields.
6. **World Photography Week (12–26 August)** is not separately indexed as an event because Metadata Standard v1 does not yet have start/end date fields. The feature article remains fully searchable under World Photography Week tags.
7. The duplicate Craig Richards workshop row in “Coming Up” is intentionally **not** given `data-index="event"` because the full workshop callout earlier in the issue is already the canonical indexed event.
8. The generic `.footer` class has been renamed to `.wcc-newsletter-footer` to avoid Zenfolio footer-style collisions. Visible footer wording is unchanged.
9. Existing short navigation IDs were replaced with permanent global IDs and the “In this issue” links were updated.
10. The Lightroom Part 3 PDF is indexed as a `resource` while retaining the original published URL.

## Result

Issue 010 is now suitable for automated extraction into the future GitHub resource index while preserving the historical newsletter as published.
