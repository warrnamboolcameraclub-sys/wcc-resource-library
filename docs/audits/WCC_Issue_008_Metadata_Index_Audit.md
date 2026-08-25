# Issue 008 Metadata Index Audit

**Publication:** Warrnambool Camera Club Weekly Update  
**Issue:** 008  
**Published:** 27 July 2026  
**Metadata standard:** WCC Weekly Update Metadata Index Standard v1  
**Historical-content rule:** Published wording, chronology and historical state have been preserved. Metadata was added around the existing content.

| Indexed item | Category / type | Series / code | Key metadata |
|---|---|---|---|
| From the Editor | club-news / article | — | AGM, rules, mat cutting, Craig Richards |
| Welcome New Members | club-news / article | — | Andrew & Debbie Iverach, Luke Annett, Sandi Uren |
| More Than Just a Meeting – Why Our AGM Matters | club-news / article | — | AGM, Club Rules, governance, competition |
| Mat Cutting Workshop Returns | events / event | — | 3 August 2026, 7:00 PM onwards, confirmed |
| Proposed Club Rule Amendments | club-news / article | — | Club Rules, AGM, member feedback |
| Warrnambool Photography Walk for Wellness Turns Two | community / article | — | anniversary, Civic Green, community photography |
| Bob & Kerrie Reach Cape York | members-on-the-move / article | — | Cape York, member travel |
| Craig & Sharon Discover Ireland | members-on-the-move / article | — | Ireland, Blarney Stone, member travel |
| Building a Stable Foundation | education / article | Mastering Long Exposure Photography · Part 4 | Ian van der Wolde, tripod, stability, geared head |
| Improve Colour & Contrast in Five Minutes | editing / article | Lightroom Basics · Part 1 | exposure, contrast, colour, vibrance |
| Beginner Tip: Keep Your Horizons Level | photography-tips / tip | B004 | horizon, landscape, composition |
| Intermediate Tip: Look for Natural Leading Lines | photography-tips / tip | I004 | leading lines, composition |
| Advanced Tip: Look Beyond the Subject | photography-tips / tip | A004 | backgrounds, distractions, simplification |
| Leading Lines | challenge / article | — | weekly camera challenge, composition |
| Walk for Wellness 2nd Anniversary | community / event | — | 1 August 2026, confirmed |
| Annual General Meeting event | club-news / event | — | 6 August 2026, confirmed |
| Craig Richards Landscape Photography Presentation | education / event | — | 6 August 2026, confirmed |
| Craig Richards Landscape Photography Workshop | events / event | — | 15 August 2026, confirmed |
| Lightroom Part 1 downloadable guide | editing / resource | Lightroom Basics · Part 1 | PDF resource |

## Important historical/indexing notes

1. **Tip codes B004, I004 and A004** were not printed in the Issue 008 HTML. They have been added from the established sequence immediately before Issue 009's B005/I005/A005.
2. **Mastering Long Exposure Photography Part 4** is explicitly indexed under `mastering-long-exposure-photography`.
3. **Lightroom Basics Part 1** is explicitly indexed under `lightroom-basics`, and its PDF is indexed separately as a resource.
4. The article's “Looking Ahead” references **Ethical Bird Photography Part 4**, but Issue 008 does not itself contain that bird article. No bird-series item has therefore been created for this issue.
5. The **Mat Cutting Workshop** section is the canonical indexed event for 3 August. Its duplicate “Coming Up” row carries date/status metadata but intentionally no `data-index`.
6. The 6 August “Coming Up” row combines the AGM and Craig Richards presentation. Separate hidden metadata spans were inserted so an automated index can extract the two events independently without altering what members see.
7. The **Walk for Wellness anniversary event** is indexed for 1 August 2026 because that exact date is shown in “Coming Up”; the feature text also states the anniversary walk begins at 9.00 am at Civic Green.
8. The historical email spelling `stanmcculalgh@gmail.com` in the Mat Cutting Workshop has been preserved exactly as published.
9. The generic `.footer` class has been renamed to `.wcc-newsletter-footer` to avoid Zenfolio footer-style collisions. Visible footer wording remains unchanged.
10. Existing short navigation IDs were replaced with permanent global IDs and the “In this issue” links were updated.

## Result

Issue 008 is now suitable for automated extraction into the future GitHub resource index while preserving the newsletter as published.
