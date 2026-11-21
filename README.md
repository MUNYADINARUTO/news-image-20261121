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

---

<sub>Entered on [make.fun](https://make.fun/?ref=9w6wee9v&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
