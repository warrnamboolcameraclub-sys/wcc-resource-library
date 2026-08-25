# Issue 009 Metadata Index Audit

**Publication:** Warrnambool Camera Club Weekly Update  
**Issue:** 009  
**Published:** 3 August 2026  
**Metadata standard:** WCC Weekly Update Metadata Index Standard v1  
**Historical-content rule:** Published wording, chronology and historical state have been preserved. Metadata was added around the existing content.

| Indexed item | Category / type | Series / code | Key metadata |
|---|---|---|---|
| From the Editor | club-news / article | — | Weekly Update, Walk for Wellness, AGM, Craig Richards |
| Photography Walk for Wellness Celebrates Two Years | community / article | — | 25th walk, anniversary, community, ABC South West Victoria |
| Craig Richards Visits the Club | education / article | — | landscape photography, guest speaker, presentation |
| Annual General Meeting | club-news / article | — | Club Rules, governance, competition, member feedback |
| Mat Cutting Workshop | events / event | — | 3 August 2026, confirmed |
| The Photographer's Greatest Tool Isn't a Longer Lens | education / article | Ethical Bird Photography · Part 4 | Kim Wormald, patience, fieldcraft, bird behaviour |
| Cropping for Better Composition | editing / article | Lightroom Basics · Part 2 | crop, aspect ratio, composition, straightening |
| Beginner Tip: Hold Your Camera Steady | photography-tips / tip | B005 | stability, sharpness, camera holding |
| Intermediate Tip: Use Natural Frames | photography-tips / tip | I005 | natural frames, depth, composition |
| Advanced Tip: Balance the Visual Weight | photography-tips / tip | A005 | visual weight, balance, brightness, colour |
| Use Natural Frames | challenge / article | — | weekly camera challenge, composition |
| Bob & Kerrie Conquer the Tip of Australia | members-on-the-move / article | — | Cape York, Atherton Tablelands, Alice Springs |
| Craig & Sharon Continue Their European Adventure | members-on-the-move / article | — | London, Ireland, Germany, Iceland |
| Annual General Meeting event | club-news / event | — | 6 August 2026, confirmed |
| Craig Richards Landscape Photography Presentation | education / event | — | 6 August 2026, confirmed |
| Craig Richards Landscape Photography Workshop | events / event | — | 15 August 2026, confirmed |
| Lightroom Part 2 downloadable guide | editing / resource | Lightroom Basics · Part 2 | PDF resource |

## Important historical/indexing notes

1. **Tip codes B005, I005 and A005** were not printed in the Issue 009 HTML. They have been added from the established tip sequence used by the project.
2. **Ethical Bird Photography Part 4** is now explicitly indexed under the `ethical-bird-photography` series.
3. **Lightroom Basics Part 2** is explicitly indexed under the `lightroom-basics` series, and its PDF is indexed separately as a resource.
4. The **Mat Cutting Workshop** section is the canonical indexed event for 3 August. The duplicate row in “What's Coming Up” has date/status metadata but intentionally no `data-index`.
5. The 6 August “What's Coming Up” row contains both the AGM and Craig Richards presentation. Two invisible metadata spans were inserted so an automated index can extract them as separate events without changing the visible newsletter.
6. No later information has been back-filled into the historical newsletter. Dates and statuses come from Issue 009 itself.
7. The generic `.footer` class has been renamed to `.wcc-newsletter-footer` to avoid Zenfolio footer-style collisions. Visible footer wording remains unchanged.
8. Existing short navigation IDs were replaced with permanent global IDs and the “In this issue” links were updated.
9. The visible historical wording, photographs and publication layout remain intact.

## Result

Issue 009 is now suitable for automated extraction into the future GitHub resource index while preserving the newsletter as published.
