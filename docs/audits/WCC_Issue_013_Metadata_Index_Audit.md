# Issue 013 Metadata and Build Audit

Source authority: `weekly newsletter issue 013.docx`

## Build rules applied
- Word document treated as the editorial master.
- Public web edition preserves the newsletter wording and order.
- The non-newsletter editorial comment appearing after `Until Next Week` in the Word file was not published because `Until Next Week` is explicitly the closing section.
- Long sections use teaser paragraphs before roll-ups.
- Members on the Move remains one top-level section with Bob & Kerrie, Craig & Sharon, and the Lyn & Phil handover nested beneath it.
- Standard responsive `<img>` elements are used for all supplied Zenfolio photographs.
- Dark body text is explicitly forced to avoid Zenfolio theme overrides.
- Mobile image CSS uses `height:auto`, `max-width:100%`, `object-fit:contain` and no maximum height.
- The Monday email is a separate file and links prominently to the full online issue.

## Images
- Jason Carter `waterdrop.jpg` → Zenfolio Photo ID 1592700773
- Jason Carter `chicken.jpg` → Zenfolio Photo ID 1592700781
- Jason Carter `mushroom.jpg` → Zenfolio Photo ID 1592700782
- Bob Artis `ghost gum over 100 years old.jpg` → Zenfolio Photo ID 1592700760
- Bob Artis `eagle in flight.jpg` → Zenfolio Photo ID 1592700770

## Running Festival map
The 42 km course is embedded using Plotaroute's route-player page and a separate button links to:
`https://www.plotaroute.com/route/2739212?units=km`

## Editing Corner link
The Noise Reduction Editing Corner button uses the URL supplied by the user:
`https://warrnamboolcameraclub.zenfolio.com/lr_006_noise_reduction.pdf`

## Machine-readable fields
Page:
- `data-publication`
- `data-issue`
- `data-published`
- `data-url`

Indexed content:
- `data-index`
- `data-category`
- `data-title`
- `data-series`
- `data-part`
- `data-code`
- `data-level`
- `data-event-date`
- `data-event-status`
- `data-tags`
- `data-people`
- `data-locations`

## Validation summary
- Indexed elements: 23
- Photographer's Tips: 3
- Images: 5
- Tip codes: B009, I009, A009
- Members on the Move nested items: 3
- Until Next Week section present: yes
- Standard delayed deep-link helper present: yes
