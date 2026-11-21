#!/usr/bin/env python3
"""Build the news front page for 21 November 2026 (1024x1024).

Composes AI-generated news photos (assets/) with crisp PIL typography
into a single newspaper-style front page: entry.png.

Stories (all reported on Saturday 21 November 2026, or overnight into it):
- Lead: Russian missiles land in Poland; NATO calls it a grave violation.
- Kryvyi Rih strike: 2 dead, 42 injured, including four children.
- EU Council adopts EUR 1bn in military aid for Ukraine.
- Cyclone Akvan's aftermath on the Odisha coast.
- COP31 climate talks in Turkey enter their final stage.
Ticker: US sanctions four Iranians over oil revenues; S&P 500 slides into
correction; Mongolia's president quits; India fight back in Wellington;
Ebola crisis hits children in Congo.

Run:  python3 build_frontpage.py
Out:  entry.png  (1024x1024, PNG)
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

W, H = 1024, 1024

PAPER = (246, 241, 231)      # warm newsprint
INK = (17, 17, 17)
NAVY = (12, 26, 46)
RED = (192, 57, 43)
GREY = (70, 70, 70)
WHITE = (255, 255, 255)
GOLD = (255, 210, 90)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_w):
    """Largest size (<= start) at which text fits max_w."""
    size = start
    while size > 8:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 8)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cover(path, size, cy=0.5, cx=0.5):
    """Crop/resize an image to exactly fill size (center crop)."""
    im = Image.open(path).convert("RGB")
    return ImageOps.fit(im, size, method=Image.LANCZOS, centering=(cx, cy))


def bottom_shade(im, height):
    """Dark gradient at the bottom of an RGB image for legible white text."""
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for y in range(height):
        a = int(200 * (y / height) ** 1.4)
        d.line([(0, im.size[1] - height + y), (im.size[0], im.size[1] - height + y)],
               fill=(0, 0, 0, a))
    base = im.convert("RGBA")
    base.alpha_composite(overlay)
    return base.convert("RGB")


def panel(page, x, y, w, h, img_path, img_h, tag, headline, sub, hl_size=30):
    """One story panel: photo on top, tag, headline, subline below."""
    d = ImageDraw.Draw(page)
    img = cover(img_path, (w, img_h))
    page.paste(img, (x, y))
    # red tag bar over the photo's top-left corner
    ft = font(SANS_B, 16)
    tw = d.textlength(tag, font=ft)
    d.rectangle([x + 12, y + 10, x + 12 + tw + 20, y + 10 + 28], fill=RED)
    d.text((x + 12 + 10, y + 10 + 5), tag, font=ft, fill=WHITE)
    ty = y + img_h + 10
    fh = fit_font(d, headline, SANS_B, hl_size, w - 16)
    d.text((x + 8, ty), headline, font=fh, fill=INK)
    fs = font(SANS, 17)
    lines = wrap(d, sub, fs, w - 16)
    ly = ty + fh.size + 6
    for ln in lines[:2]:
        d.text((x + 8, ly), ln, font=fs, fill=GREY)
        ly += 21
    return ly


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---------- Masthead ----------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    kicker = "W O R L D   N E W S   \u2022   T H E   D A Y   I N   O N E   I M A G E"
    fk = font(SANS_B, 17)
    d.text(((W - d.textlength(kicker, font=fk)) / 2, 12), kicker, font=fk, fill=GOLD)
    date = "SATURDAY 21 NOVEMBER 2026"
    fd = fit_font(d, date, SERIF_B, 64, W - 60)
    d.text(((W - d.textlength(date, font=fd)) / 2, 40), date, font=fd, fill=WHITE)
    d.rectangle([0, 118, W, 122], fill=RED)

    # ---------- Lead story: Russian missiles land in Poland ----------
    lead = cover(os.path.join(ASSETS, "media-generation-poland-missile-site-0-fb9a5143-84bd-4d49-84a8-c2b70649e7ba.webp"),
                 (W, 350), cy=0.5)
    lead = bottom_shade(lead, 175)
    page.paste(lead, (0, 130))
    dl = ImageDraw.Draw(page)
    tag = "TOP STORY"
    ft = font(SANS_B, 20)
    tw = dl.textlength(tag, font=ft)
    dl.rectangle([24, 148, 24 + tw + 28, 148 + 36], fill=RED)
    dl.text((24 + 14, 148 + 6), tag, font=ft, fill=WHITE)
    fh = fit_font(dl, "RUSSIAN MISSILES LAND IN POLAND", SANS_B, 44, W - 48)
    dl.text((24, 480 - 98), "RUSSIAN MISSILES LAND IN POLAND", font=fh, fill=WHITE)
    fs = font(SANS, 20)
    dl.text((24, 480 - 46),
            "Tusk calls it a deliberate provocation; NATO calls it",
            font=fs, fill=(235, 235, 235))
    dl.text((24, 480 - 20),
            "a grave violation of allied airspace \u2014 no one hurt",
            font=fs, fill=(235, 235, 235))

    # ---------- Row 2: Kryvyi Rih | EU aid ----------
    y2, h2 = 488, 258
    panel(page, 0, y2, 508, h2,
          os.path.join(ASSETS, "media-generation-kryvyi-rih-strike-0-a04a1c62-fd4b-4c3c-ba42-cb028c0b8eb1.webp"),
          160, "UKRAINE",
          "KRYVYI RIH HIT: 2 DEAD, 42 HURT",
          "Russian strike on the city kills two and injures 42, including four children")
    panel(page, 516, y2, 508, h2,
          os.path.join(ASSETS, "media-generation-eu-aid-ukraine-0-844b4a12-31f2-4a39-9b32-1ee066d7bfb2.webp"),
          160, "BRUSSELS",
          "EU ARMS UKRAINE WITH \u20ac1BN",
          "Council adopts \u20ac1 billion in military aid; Kyiv says Russia has rejected peace")

    # ---------- Row 3: Cyclone photo | COP31 text panel ----------
    y3, h3 = 754, 192
    panel(page, 0, y3, 508, h3,
          os.path.join(ASSETS, "media-generation-cyclone-akvan-0-b7b9bb9f-e173-499a-9606-347a314d39c4.webp"),
          104, "INDIA",
          "AKVAN'S AFTERMATH",
          "Floods swamp the Odisha coast after the cyclone crosses land",
          hl_size=26)
    # Text-only sidebar: COP31, no photo needed
    d = ImageDraw.Draw(page)
    gx = 516
    d.rectangle([gx, y3, gx + 508, y3 + h3], outline=(150, 140, 120), width=2)
    ft = font(SANS_B, 16)
    d.rectangle([gx + 12, y3 + 10, gx + 12 + d.textlength("CLIMATE", font=ft) + 20, y3 + 10 + 28], fill=RED)
    d.text((gx + 12 + 10, y3 + 10 + 5), "CLIMATE", font=ft, fill=WHITE)
    fh = fit_font(d, "COP31 IN FINAL HOURS", SANS_B, 26, 508 - 16)
    d.text((gx + 8, y3 + 48), "COP31 IN FINAL HOURS", font=fh, fill=INK)
    fs = font(SANS, 17)
    bullets = [
        "Climate talks in Turkey reach their final",
        "stage \u2014 fossil fuels and climate finance",
        "still the sticking points.",
    ]
    ly = y3 + 48 + fh.size + 8
    for ln in bullets:
        d.text((gx + 8, ly), ln, font=fs, fill=GREY)
        ly += 21

    # ---------- Footer ticker ----------
    d.rectangle([0, 954, W, H], fill=NAVY)
    f1 = font(SANS_B, 17)
    f2 = font(SANS, 17)
    d.text((16, 962), "ALSO TODAY", font=f1, fill=GOLD)
    ticker = "US sanctions four Iranians over oil revenues  \u2022  S&P 500 slides into correction  \u2022  Mongolia's president quits  \u2022  India fight back in Wellington Test  \u2022  Ebola hits Congo's children"
    ftick = fit_font(d, ticker, SANS, 17, W - 32)
    d.text((16, 986), ticker, font=ftick, fill=WHITE)

    out = os.path.join(BASE, "entry.png")
    # Palette PNG (256 colours, dithered) keeps the file under the 1 MiB
    # limit while staying a valid PNG; RGB would exceed it.
    page = page.convert("P", palette=Image.ADAPTIVE, colors=256)
    page.save(out, "PNG", optimize=True)
    print(f"Wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
