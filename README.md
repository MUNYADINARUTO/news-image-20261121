# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/MUNYADINARUTO/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/MUNYADINARUTO/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper-style front page that sums up Saturday, 21 November 2026 in a
single 1024×1024 image: Russian missiles landing in Poland — called a
deliberate provocation by Warsaw and a grave violation by NATO — a Russian
strike on Kryvyi Rih killing 2 and injuring 42, the EU adopting €1 billion
in military aid for Ukraine, Cyclone Akvan's floods on the Odisha coast,
and COP31 climate talks entering their final hours — plus a ticker with US
sanctions on four Iranians over oil revenues, the S&P 500 sliding into
correction, Mongolia's president quitting, India fighting back in the
Wellington Test, and Ebola hitting children in Congo.

The date is printed large at the top, and every story is named on the page,
so the image stands on its own as a record of that one day.

## Run it

```sh
python3 main.py
# writes /output/entry.png (1024x1024 PNG, < 1 MiB)
```

`main.py` deterministically writes the finished image to `/output/entry.png`
(a byte-for-byte copy of the bundled `entry.png` asset — no network, no
randomness, so repeated runs produce identical bytes). The finished front
page is the bundled `entry.png` itself, composed from AI-generated news
photography in `assets/` with crisp PIL typography into the 1024×1024
layout (see `build_frontpage.py`).

## What the image shows

The front page leads with the day's most consequential story: Russian
missiles landing in Poland. Warsaw called the incursion a deliberate
provocation; NATO called it a grave violation. The page carries that
tension in its headline and in the map panel that places the strikes.

The second lead is the Russian strike on Kryvyi Rih, in central Ukraine:
two people killed and forty-two injured. The photograph panel shows the
rescue work in the aftermath, and the caption gives the toll as it was
reported that day, without embellishment.

The third panel covers the European Union's decision to adopt one
billion euros in military aid for Ukraine — the institutional answer to
the day's attacks, shown as a council chamber rather than a battlefield.

Below the fold, the page turns to Cyclone Akvan's landfall on the
Odisha coast: flooded streets, evacuated villages, and the storm's
track drawn across the Bay of Bengal. The storm is the day's reminder
that the news is not only about wars and summits.

The last panel follows the COP31 climate talks into their final hours,
with negotiators still short of an agreement as the deadline approached.

A ticker along the bottom carries the rest of the day in short: United
States sanctions on four Iranians over oil revenues, the S&P 500 sliding
into correction territory, Mongolia's president quitting, India fighting
back in the Wellington Test, and Ebola reaching children in Congo.

## How the picture was put together

Each photograph panel started as an AI-generated news-style image, made
from a written brief for that one story and saved under `assets/` with
its generation record beside it. The front-page script then laid the
panels out in a newspaper grid, set the headlines and captions in a
heavy serif face, and printed the date large at the top so the image
names the day it sums up. Nothing in the image was photographed: every
panel is an illustration of a reported event, labelled as the story it
belongs to, so a reader can tell what happened from the page alone.

The image is licensed under the MIT license in this repository, like
the code beside it. The stories it names are the public record of
21 November 2026 as reported that day; the page does not invent
events, only selects and arranges them.

---

<sub>Entered on [make.fun](https://make.fun/?ref=9w6wee9v&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
