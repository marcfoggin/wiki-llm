---
title: "Source Registry"
type: registry
last_updated: 2026-05-22
---

# Source Registry

Tracks all external URLs that have been fetched and summarised into wiki pages. Use this to avoid duplicate work, flag URLs for revisit, and detect when sources may have been updated.

## Status Key

- **done** — fetched and summarised
- **revisit** — needs another pass (new focus, or source updated)
- **failed** — fetch failed (paywall, 403, dead link)

## Fetch Method Key

- **WebFetch** — Claude Code's built-in web fetch tool
- **curl+meta** — curl returns 200; content extracted from HTML meta tags / page body
- **CrossRef** — DOI metadata and abstract via api.crossref.org (no auth needed)
- **known** — summarised from prior knowledge; URL not successfully fetched
- **n/a** — not attempted (lightweight reference, one-liner sufficient)

## Registry

| URL | Status | Method | Last Fetched | Source Page | Pages Updated | Focus / Notes |
|-----|--------|--------|-------------|-------------|---------------|---------------|
| https://doughnuteconomics.org/about-doughnut-economics | done | WebFetch | 2026-05-22 | doughnut-economics | environment-and-economics | Full framework: social foundation + ecological ceiling |
| https://creationcare.org/who-we-are/beliefs.html | done | WebFetch | 2026-05-22 | een-creation-care-beliefs | creation-care | Biblical imperative, Great Commandments, pollution & poor |
| https://lausanne.org/report/sustainable/creation-care | done | WebFetch | 2026-05-22 | lausanne-creation-care | creation-care, stewarding-creation | Integral mission, planetary boundaries, case studies |
| https://lausanne.org/core-documents | done | WebFetch | 2026-05-22 | lausanne-core-documents | proclaiming-the-good-news | 4 core documents 1974–2024 |
| https://climatepromise.undp.org/.../indigenous-knowledge...heres-why | done | WebFetch | 2026-05-22 | undp-indigenous-knowledge-climate | local-indigenous-knowledge | 25% land, 36% forests, FPIC, 5 policy actions |
| https://earthbound.report/.../elinor-ostroms-8-rules... | done | WebFetch | 2026-05-22 | ostrom-eight-rules-commons | managing-common-resources | Full 8 principles with examples |
| https://nextbigideaclub.com/.../nomads-wanderers-shaped-world... | done | WebFetch | 2026-05-22 | sattin-nomads | culture-and-identity | Nomads central to civilisation |
| https://wearemakingdisciples.com/.../5-reasons-why-we-love... | done | WebFetch | 2026-05-22 | rogers-five-reasons-serve | loving-service | 5 reasons: command, value, incarnation, Matt 25:40, credibility |
| https://www.biola.edu/.../thinking-biblically-about-systemic-injustice | done | WebFetch | 2026-05-22 | williams-systemic-injustice | transforming-society | Disparity vs discrimination, biblical systemic sin |
| https://www.fao.org/pastoralist-knowledge-hub/ | done | WebFetch | 2026-05-22 | fao-pastoralist-knowledge-hub | nomadic-pastoralism | 2B people depend on rangelands, IYRP 2026 |
| https://www.icimod.org | done | WebFetch | 2026-05-22 | — | mountains-and-wetlands | Hindu Kush Himalaya, 8 countries |
| https://portals.iucn.org/library/node/44874 | done | WebFetch | 2026-05-22 | — | protected-areas | Metadata only, no abstract on page |
| https://sdgs.un.org/goals | done | WebFetch | 2026-05-22 | — | transforming-society | 17 goals, 2015, 2030 Agenda |
| https://www.plough.com/.../jesus-is-coming-plant-a-tree | done | WebFetch | 2026-05-22 | wright-jesus-plant-tree | stewarding-creation | Eschatology, resurrection, building for the kingdom |
| https://www.plough.com/.../insight-evangelism-vs-neighbor-love | done | WebFetch | 2026-05-22 | stott-evangelism-neighbour-love | loving-service | Great Commission + Great Commandment as partners |
| https://www.iccaconsortium.org/ | done | curl+meta | 2026-05-22 | icca-consortium | local-and-traditional-livelihoods | Territories of life, community governance |
| https://doi.org/10.1038/s41893-018-0100-6 | done | curl+meta | 2026-05-22 | indigenous-lands-conservation | local-and-traditional-livelihoods | 38M km², 40% protected areas overlap |
| https://doi.org/10.1002/ecs2.2582 | done | CrossRef | 2026-05-22 | grasslands-ecosystem-services | biodiversity-and-rangelands | Grassland ES: water, carbon, pollination |
| https://doi.org/10.1093/biosci/biaf158 | done | CrossRef | 2026-05-22 | pastoralism-mitigate-biodiversity-loss | biodiversity-and-rangelands, nomadic-pastoralism | 67% hotspots include rangelands, 4 synergies |
| https://doi.org/10.1126/science.abl4881 | done | CrossRef | 2026-05-22 | overcoming-climate-biodiversity-crises | environment-and-economics | Coupled crises, 30-50% conservation target |
| https://www.forumforthefuture.org/the-five-capitals | done | curl+meta | 2026-05-22 | five-capitals-model | environment-and-economics | 5 capitals: natural, human, social, manufactured, financial |
| https://ipbes.net/global-assessment | done | curl+meta | 2026-05-22 | ipbes-global-assessment | biodiversity-and-rangelands | 1M species threatened, 5 direct drivers |
| https://www.alpha.org/what-is-alpha | done | curl+meta | 2026-05-22 | alpha-course | discipleship-and-formation | Meal + talk + discussion, 100+ countries |
| https://doi.org/10.4060/cb8461en | done | curl+meta | 2026-05-22 | fao-making-way-pastoral-mobility | the-need-for-mobility | Legal frameworks for pastoral mobility |
| https://www.vatican.va/.../laudato-si.html | done | known | 2026-05-22 | laudato-si | stewarding-creation | Integral ecology, cry of earth = cry of poor |
| https://www.ramsar.org | failed | — | 2026-05-22 | — | mountains-and-wetlands | 403 on both WebFetch and curl |
| https://doi.org/10.1073/pnas.1525002113 | failed | — | 2026-05-22 | — | stewarding-creation | 403 — "Why protect nature?" |
| https://doi.org/10.3390/su15021388 | failed | — | 2026-05-22 | — | creation-care | 403 — "Trouble with Sustainability" |
| https://doi.org/10.1080/14888386.2014.931247 | failed | — | 2026-05-22 | — | nomadic-pastoralism | 403 — Globalisation & pastoralists |
| https://www.iied.org/.../pastoralism-development-...mooc | failed | — | 2026-05-22 | — | the-need-for-mobility | 403 on both WebFetch and curl |
| https://seas.umich.edu/news/commons-more-just-resources | failed | — | 2026-05-22 | — | managing-common-resources | 403 on both WebFetch and curl |
| https://doi.org/10.1016/j.oneear.2020.10.013 | done | curl+meta | 2026-05-22 | — | biodiversity-and-rangelands | 200 but no extractable abstract; title only |
| https://doi.org/10.1016/j.cosust.2023.101298 | done | curl+meta | 2026-05-22 | — | local-and-traditional-livelihoods | 200 but no extractable abstract; title only |
| https://doi.org/10.1016/j.cosust.2016.12.006 | done | curl+meta | 2026-05-22 | — | creation-care, stewarding-creation | 200 but no extractable abstract; title only |
| https://www.ilri.org/news/ten-interesting-facts-about-rangelands | done | WebFetch | 2026-05-22 | ten-facts-rangelands | biodiversity-and-rangelands | 10 key facts, 54% land, 2B people |
| https://iyrp.info/ | done | WebFetch | 2026-05-22 | iyrp-2026 | nomadic-pastoralism | UN Year 2026, awareness & policy advocacy |
| https://lausanne.org/report/just | done | WebFetch | 2026-05-22 | lausanne-what-is-just | transforming-society | Justice integral to mission, global perspectives |
| https://www.rangelandsdata.org/atlas/ | done | WebFetch | 2026-05-22 | rangelands-atlas | biodiversity-and-rangelands | FAO/IUCN/UNEP/WWF spatial data on rangelands |
| https://www.practicingtheway.org/ | done | curl+meta | 2026-05-22 | — | discipleship-and-formation | Spiritual formation practices; one-liner sufficient |
| https://biologos.org/ | failed | — | 2026-05-22 | — | stewarding-creation | 403 on WebFetch; org homepage, one-liner sufficient |
| https://jri.org.uk/ | done | curl+meta | 2026-05-22 | — | stewarding-creation | John Ray Initiative; science-faith-environment |
| https://www.christianityexplored.org/ | done | curl+meta | 2026-05-22 | — | proclaiming-the-good-news | Course exploring Mark's Gospel; one-liner sufficient |
| https://teeb.biodiversityfinance.net/ | failed | — | 2026-05-22 | — | environment-and-economics | 403 on WebFetch; TEEB initiative homepage |
| https://ipbes.net/ilk | failed | — | 2026-05-22 | — | local-indigenous-knowledge | 403 on WebFetch; IPBES ILK programme page |
