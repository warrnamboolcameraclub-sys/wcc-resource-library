# Issue 007 Metadata Index Audit

**Publication:** Warrnambool Camera Club Weekly Update  
**Issue:** 007  
**Published:** Tuesday, 21 July 2026  
**Metadata standard:** WCC Weekly Update Metadata Index Standard v1  
**Historical-content rule:** Published wording, chronology and historical state have been preserved. Metadata was added around the existing content.

| Indexed item | Category / type | Series / code | Key metadata |
|---|---|---|---|
| From the Editor | club-news / article | — | Craig Richards, Competition Rules, Walk for Wellness, bird series |
| Craig Richards Visits the Warrnambool Camera Club | education / article | — | landscape, astrophotography, seascapes, guest speaker |
| Craig Richards Club Presentation | education / event | — | 6 August 2026, confirmed |
| Craig Richards Landscape Photography Workshop | events / event | — | 15 August 2026, confirmed |
| Mat Cutting Workshop – Learning the Art of Presentation | education / article | — | mat cutting, print presentation, competition |
| Competition Rules Update | competition / article | — | competition rules, AI guidance, member feedback |
| Competition Rules downloadable guide | competition / resource | — | PDF resource |
| Photography Walk for Wellness – Celebrating Two Years | community / article | — | anniversary, wellbeing, community photography |
| Walk for Wellness Anniversary | community / event | — | 1 August 2026, confirmed |
| The Four P's: Finding Beauty in Everyday Behaviour | education / article | Ethical Bird Photography · Part 3 | Kim Wormald, Four P's, ethics, wildlife |
| Beginner Tip: Choose a Single Focus Point | photography-tips / tip | B003 | autofocus, focus point, sharpness |
| Intermediate Tip: Use Foreground Interest to Add Depth | photography-tips / tip | I003 | foreground, landscape, depth |
| Advanced Tip: Wait for the Right Moment | photography-tips / tip | A003 | timing, decisive moment, patience |
| Capture the Landscape You Know Best | challenge / article | — | local landscape, foreground, light, composition |
| Mat Cutting Workshop – week beginning 3 August | events / event | — | planning; exact date not known in Issue 007 |
| Dinner at The Liebig Thai Restaurant | events / event | — | 15 August 2026, 7:00 pm, confirmed |

## Important historical/indexing notes

1. **Issue 007 was published Tuesday, 21 July 2026**, not Monday. The metadata preserves the date shown in the issue.
2. **B003, I003 and A003** are printed directly in the source, so no historical tip-code inference was required.
3. **Ethical Bird Photography Part 3** is explicitly indexed as `ethical-bird-photography`, Part 3. The article itself describes this as the final instalment of a three-part series. Later newsletters subsequently extended the topic to Parts 4 and 5; this historical wording has not been altered.
4. The **Craig Richards presentation and workshop** are exposed as separate hidden machine-readable events inside the Craig preview article so they can be indexed without changing the visible layout. Duplicate rows in Upcoming Events deliberately carry no second `data-index`.
5. The **Mat Cutting Workshop** future session remains `planning` because Issue 007 says only “week beginning 3 August” and that the final date would be confirmed shortly. No later date has been back-filled.
6. The **RSVP closing date** is given a stable HTML ID/date for automation hygiene, but is not separately indexed into the photography resource library.
7. The **Dinner at The Liebig Thai Restaurant** is indexed as an event because the source provides a definite date and time.
8. The **Competition Rules PDF** is indexed separately as a resource while retaining its original published URL.
9. The generic `.footer` class has been renamed to `.wcc-newsletter-footer` to avoid Zenfolio footer-style collisions. Visible footer wording remains unchanged.
10. Existing short navigation IDs were replaced with permanent global IDs and the “In this issue” links were updated.

## Result

Issue 007 is now suitable for automated extraction into the future GitHub resource index while preserving the newsletter as published.
