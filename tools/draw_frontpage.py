#!/usr/bin/env python3
"""Draw the front page for news-image-20261121.

A 1024x1024 PNG newspaper front page summing up the world news of
Saturday 21 November 2026. Every shape is drawn with Pillow primitives;
no photos, no downloaded assets, no copied artwork.

Layout is a fixed grid: masthead, one lead story, two mid panels, three
small panels, a footer strip. Each panel has fixed zones (kicker,
headline, art strip, deck) so nothing overlaps.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (176, 42, 42)
NAVY = (31, 58, 95)
TEAL = (23, 110, 110)
GOLD = (201, 141, 32)
GREY = (110, 106, 96)
LIGHT = (255, 255, 255)
SKY = (214, 231, 240)
DARK = (30, 34, 40)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, label, color=RED):
    draw.text((x, y), label, font=font(SANS_B, 20), fill=color)


def panel(draw, x, y, w, h, fill=LIGHT):
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=INK, width=2)


def starburst(draw, cx, cy, r1, r2, n=12, fill=GOLD):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def arc_curve(draw, p0, p1, lift, fill, width=3, steps=24):
    """A smooth arc from p0 to p1 rising `lift` px above the chord."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t - lift * 4 * t * (1 - t)
        pts.append((x, y))
    draw.line(pts, fill=fill, width=width)


def jet(draw, x, y, s, color, flip=False):
    d = -1 if flip else 1
    draw.polygon([(x, y), (x + 34 * s * d, y - 6 * s), (x + 44 * s * d, y),
                  (x + 34 * s * d, y + 6 * s)], fill=color)
    draw.polygon([(x + 8 * s * d, y - 4 * s), (x + 18 * s * d, y - 16 * s),
                  (x + 22 * s * d, y - 4 * s)], fill=color)
    draw.polygon([(x + 8 * s * d, y + 4 * s), (x + 18 * s * d, y + 16 * s),
                  (x + 22 * s * d, y + 4 * s)], fill=color)


def draw_lead_art(draw, x, y, w, h):
    """Stylised map: Poland above Ukraine, missile arcs, NATO jets."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # Poland (upper land) and Ukraine (lower land), box-relative
    draw.polygon([(x + 0.10 * w, y + 0.10 * h), (x + 0.52 * w, y + 0.06 * h),
                  (x + 0.62 * w, y + 0.30 * h), (x + 0.55 * w, y + 0.50 * h),
                  (x + 0.30 * w, y + 0.55 * h), (x + 0.12 * w, y + 0.40 * h)],
                 fill=(196, 214, 178), outline=NAVY, width=2)
    draw.polygon([(x + 0.12 * w, y + 0.60 * h), (x + 0.58 * w, y + 0.56 * h),
                  (x + 0.64 * w, y + 0.82 * h), (x + 0.40 * w, y + 0.92 * h),
                  (x + 0.16 * w, y + 0.86 * h)],
                 fill=(222, 205, 160), outline=NAVY, width=2)
    f = font(SANS_B, 18)
    draw.text((x + 0.16 * w, y + 0.26 * h), "POLAND", font=f, fill=NAVY)
    draw.text((x + 0.20 * w, y + 0.68 * h), "UKRAINE", font=f, fill=NAVY)
    # missile arcs arriving from the east edge
    impacts = [(x + 0.60 * w, y + 0.28 * h), (x + 0.56 * w, y + 0.46 * h)]
    for (ex, ey) in impacts:
        arc_curve(draw, (x + w - 6, ey - 46), (ex, ey), 42, RED, width=3)
        draw.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=RED)
    starburst(draw, impacts[0][0], impacts[0][1], 17, 8, fill=GOLD)
    starburst(draw, impacts[1][0], impacts[1][1], 13, 6, fill=(230, 120, 40))
    # one jet patrolling the sky at right
    jet(draw, x + 0.80 * w, y + 0.52 * h, 1.3, NAVY, flip=True)
    # NATO compass
    cx, cy = x + w - 36, y + h - 34
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=NAVY, width=2)
    draw.polygon([(cx, cy - 16), (cx + 4, cy), (cx, cy + 16), (cx - 4, cy)],
                 fill=NAVY)
    draw.text((cx - 22, cy + 24), "NATO", font=font(SANS_B, 14), fill=NAVY)


def draw_cyclone_art(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 238, 244))
    # sea and coastline
    draw.rectangle([x, y + 0.78 * h, x + w, y + h], fill=(120, 165, 200))
    draw.polygon([(x, y + 0.78 * h), (x + 0.45 * w, y + 0.66 * h),
                  (x + w, y + 0.80 * h), (x + w, y + h), (x, y + h)],
                 fill=(196, 190, 150))
    # spiral, left of centre
    cx, cy = x + 0.28 * w, y + 0.42 * h
    for r in (38, 29, 20, 11):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=TEAL, width=4)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=TEAL)
    # rain drops, right side
    for (rx, ry) in [(0.62, 0.18), (0.74, 0.30), (0.86, 0.16), (0.92, 0.42),
                     (0.68, 0.48)]:
        px, py = x + rx * w, y + ry * h
        draw.line([(px, py), (px - 4, py + 10)], fill=NAVY, width=3)
    draw.text((x + 0.60 * w, y + 0.62 * h), "ODISHA COAST",
              font=font(SANS_B, 15), fill=INK)


def draw_cyber_art(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=DARK)
    for i in range(4):
        yy = y + 0.16 * h + i * 0.20 * h
        draw.line([(x + 12, yy), (x + w - 12, yy)], fill=(60, 90, 70), width=2)
        draw.ellipse([x + w - 24, yy - 4, x + w - 16, yy + 4],
                     fill=(80, 200, 120))
    # bank columns
    for i in range(3):
        bx = x + 0.10 * w + i * 0.24 * w
        draw.rectangle([bx, y + 0.42 * h, bx + 0.16 * w, y + 0.86 * h],
                       fill=(150, 160, 175))
        draw.rectangle([bx - 6, y + 0.36 * h, bx + 0.16 * w + 6, y + 0.42 * h],
                       fill=(200, 208, 216))
    # warning triangle
    tx, ty = x + 0.82 * w, y + 0.58 * h
    draw.polygon([(tx, ty - 24), (tx + 26, ty + 16), (tx - 26, ty + 16)],
                 fill=GOLD, outline=INK)
    draw.text((tx - 4, ty - 14), "!", font=font(SANS_B, 24), fill=INK)


def draw_hospital_art(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 240, 244))
    # building
    draw.rectangle([x + 0.10 * w, y + 0.30 * h, x + 0.90 * w, y + 0.92 * h],
                   fill=LIGHT, outline=NAVY, width=2)
    # red-cross sign on the roof
    cx = x + 0.50 * w
    draw.rectangle([cx - 15, y + 0.04 * h, cx + 15, y + 0.30 * h], fill=RED)
    draw.rectangle([cx - 5, y - 2, cx + 5, y + 0.34 * h], fill=RED)
    # windows
    for i in range(3):
        wx = x + 0.16 * w + i * 0.28 * w
        draw.rectangle([wx, y + 0.46 * h, wx + 0.16 * w, y + 0.68 * h],
                       fill=SKY, outline=NAVY, width=2)
    # bed
    draw.rectangle([x + 0.14 * w, y + 0.80 * h, x + 0.86 * w, y + 0.88 * h],
                   fill=NAVY)
    draw.ellipse([x + 0.16 * w, y + 0.72 * h, x + 0.24 * w, y + 0.82 * h],
                 fill=(240, 200, 170))
    draw.rectangle([x + 0.24 * w, y + 0.74 * h, x + 0.80 * w, y + 0.82 * h],
                   fill=(90, 140, 200))


def draw_blast_art(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 228, 210))
    # road
    draw.rectangle([x, y + 0.72 * h, x + w, y + 0.84 * h], fill=(120, 118, 112))
    for i in range(5):
        lx = x + 0.06 * w + i * 0.19 * w
        draw.rectangle([lx, y + 0.76 * h, lx + 0.09 * w, y + 0.80 * h],
                       fill=(250, 240, 200))
    # checkpoint barrier
    draw.rectangle([x + 0.06 * w, y + 0.42 * h, x + 0.30 * w, y + 0.52 * h],
                   fill=RED)
    draw.rectangle([x + 0.08 * w, y + 0.52 * h, x + 0.10 * w, y + 0.72 * h],
                   fill=INK)
    draw.rectangle([x + 0.26 * w, y + 0.52 * h, x + 0.28 * w, y + 0.72 * h],
                   fill=INK)
    # blast
    bx, by = x + 0.72 * w, y + 0.42 * h
    starburst(draw, bx, by, 30, 14, fill=(230, 120, 40))
    starburst(draw, bx, by, 19, 9, fill=GOLD)
    draw.ellipse([bx - 52, by - 30, bx - 30, by - 8], fill=(90, 88, 84))
    draw.ellipse([bx + 18, by - 34, bx + 40, by - 12], fill=(120, 118, 112))


def draw_datacentre_art(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 234, 240))
    # server racks
    for i in range(3):
        rx = x + 0.08 * w + i * 0.24 * w
        draw.rectangle([rx, y + 0.14 * h, rx + 0.18 * w, y + 0.88 * h],
                       fill=DARK)
        for j in range(4):
            yy = y + 0.20 * h + j * 0.18 * h
            draw.rectangle([rx + 4, yy, rx + 0.18 * w - 4, yy + 0.08 * h],
                           fill=(50, 60, 72))
            draw.ellipse([rx + 7, yy + 1, rx + 12, yy + 6],
                         fill=(80, 220, 120) if j % 2 else (230, 180, 60))
    # globe, top right
    cx, cy = x + 0.88 * w, y + 0.22 * h
    r = 0.16 * h
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 180, 220),
                 outline=NAVY, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=2)
    # red "no" ring over the racks
    cx2, cy2 = x + 0.44 * w, y + 0.50 * h
    rr = 0.46 * h
    draw.ellipse([cx2 - rr, cy2 - rr, cx2 + rr, cy2 + rr], outline=RED, width=5)
    draw.line([(cx2 - rr * 0.7, cy2 + rr * 0.7),
               (cx2 + rr * 0.7, cy2 - rr * 0.7)], fill=RED, width=5)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.text((512, 8), "THE WORLD TODAY", font=font(SERIF_B, 62),
           fill=INK, anchor="ma")
    d.text((512, 76), "Saturday, 21 November 2026", font=font(SERIF_B, 30),
           fill=RED, anchor="ma")
    rule(d, 24, 116, 1000, 3)
    d.text((24, 122), "ONE DAY  •  ONE WORLD  •  ONE PICTURE",
           font=font(SANS_B, 15), fill=GREY)
    d.text((1000, 122), "No. 325", font=font(SANS_B, 15), fill=GREY, anchor="ra")

    # ---------- lead story ----------
    panel(d, 24, 148, 976, 264)
    draw_lead_art(d, 600, 162, 384, 236)
    kicker(d, 40, 162, "LEAD STORY — EUROPE")
    y = text_block(d, 40, 192, "Russian missiles land in Poland",
                   font(SERIF_B, 40), INK, 540, leading=46)
    y = text_block(d, 40, y + 6,
                   "Tusk calls it a deliberate provocation as NATO "
                   "condemns a “grave violation” of its airspace.",
                   font(SANS, 23), INK, 540, leading=29)
    d.text((40, 384), "No injuries reported; NATO jets scrambled.",
           font=font(SANS_B, 19), fill=NAVY)

    # ---------- row 2: two panels ----------
    # Cyclone Akvan
    panel(d, 24, 428, 482, 236)
    kicker(d, 40, 442, "ASIA — WEATHER")
    text_block(d, 40, 468, "Cyclone Akvan weakens over India",
               font(SERIF_B, 26), INK, 450, leading=30)
    draw_cyclone_art(d, 40, 534, 450, 74)
    d.text((40, 620), "370,000 evacuated; no deaths reported.",
           font=font(SANS, 19), fill=INK)
    # Cyberattack
    panel(d, 518, 428, 482, 236)
    kicker(d, 534, 442, "BUSINESS — TECH")
    text_block(d, 534, 468, "Banks hit by cyberattack on vendors",
               font(SERIF_B, 26), INK, 450, leading=30)
    draw_cyber_art(d, 534, 534, 450, 74)
    d.text((534, 620), "JPMorgan, Visa, Mastercard report breaches.",
           font=font(SANS, 19), fill=INK)

    # ---------- row 3: three panels ----------
    # Bolsonaro
    panel(d, 24, 680, 318, 208)
    kicker(d, 40, 692, "AMERICAS")
    text_block(d, 40, 716, "Bolsonaro taken to hospital",
               font(SERIF_B, 23), INK, 286, leading=27)
    draw_hospital_art(d, 40, 770, 286, 56)
    text_block(d, 40, 834, "Brazil’s ex-president in severe abdominal pain.",
               font(SANS, 16), INK, 286, leading=19)
    # Pakistan
    panel(d, 353, 680, 318, 208)
    kicker(d, 369, 692, "ASIA — SECURITY")
    text_block(d, 369, 716, "Suicide bombing kills five in Pakistan",
               font(SERIF_B, 23), INK, 286, leading=27)
    draw_blast_art(d, 369, 770, 286, 56)
    text_block(d, 369, 834, "Car bomb at a checkpoint; 13 injured.",
               font(SANS, 16), INK, 286, leading=19)
    # Trump / AI data centres
    panel(d, 682, 680, 318, 208)
    kicker(d, 698, 692, "UNITED STATES")
    text_block(d, 698, 716, "Trump: no AI data centres abroad",
               font(SERIF_B, 23), INK, 286, leading=27)
    draw_datacentre_art(d, 698, 770, 286, 56)
    text_block(d, 698, 834, "President says US firms must not build them overseas.",
               font(SANS, 16), INK, 286, leading=19)

    # ---------- footer strip ----------
    panel(d, 24, 904, 976, 76, fill=(232, 226, 208))
    d.text((40, 912), "ALSO TODAY", font=font(SANS_B, 18), fill=RED)
    text_block(d, 40, 934,
               "India fight back in the Wellington Test  •  UN warns "
               "hunger-aid funding is running short  •  Hyundai unveils "
               "the 2027 Elantra in Los Angeles",
               font(SANS, 18), INK, 944, leading=21)

    # ---------- bottom credit ----------
    d.text((512, 990), "Drawn from reports of 21 November 2026  •  make.fun  news-image-20261121",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
