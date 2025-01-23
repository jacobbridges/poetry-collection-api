# Brainstorming Document

I like to pen down my thoughts so in the future I can look back and understand why I made those decisions.


## What to do with the dataset on `legacy` branch?

This is an odd one. The repo has a full dataset of the poetryfoundation.org from 2015 -- well before the era of AI. Perhaps that can be used as a starting point.


## How to build the automated collection system?

My mind goes several directions when I see "create an automated fleet of web scrapers", but first I want to set this tone. This is a small, hobby project. It does not need a "fleet" of anything. "Scouring the web" is a goal for the future, right now I can start by building web scrapers for these sites:

- [Poetry Foundation](https://www.poetryfoundation.org/) - a long-standing archive of poetry.
- [Academy of American Poets](https://poets.org/poems) - another staple. Offers 

## What data to collect?

- Title
- Poem
  - Split out by line.
  - Try to preserve whitespace. (This can help follow the flow of some passages)
- Poet
- Source Tags (tags extracted from the source, if the source supports tags)
- AI Tags (tags applied by the poetry collection service)
- Source Address (URL)
- Source Publish Date (Any timestamp from the source for when the poem was published)

## Need a system for matching the same poem across multiple sources.

If the same poem is found in two sources, ideally they would match. However, this is rarely the case. Different line lengths, whitespace, tags, metadata, etc. How should the system resolve this?

My initial thoughts:

1. A poem should be unique based on name + author.
2. A poem can have many versions (poetryfoundation.org version vs poets.org version)
3. Each version must have source information.
4. System will deliver the most recent version by default, but provide a way to browse all versions.

A tool like [splink](https://github.com/moj-analytical-services/splink) could be useful to detect when two scraped records should actually be different versions of the same poem.
