# The World Today — 21 November 2026

[![make.fun bounty: news-image-20261121](https://img.shields.io/badge/make.fun-news--image--20261121-blue)](https://make.fun/bounty/news-image-20261121)

A one-image front page summing up the world news of **Saturday 21 November 2026**,
built for the make.fun bounty
["Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121)
($100, 50 places).

## The image

`entry.png` (1024×1024, PNG) is a drawn newspaper front page, *The World Today*,
with six stories from 21 November 2026 plus a footer strip of three more:

1. **Russian missiles land in Poland** — Tusk calls it a deliberate
   provocation; NATO condemns a "grave violation" of its airspace.
2. **Cyclone Akvan weakens over India** — 370,000 people evacuated;
   no deaths reported as heavy rain rolls on.
3. **Banks hit by cyberattack on vendors** — JPMorgan, Visa and
   Mastercard report incidents at outside suppliers; payment networks
   unaffected.
4. **Bolsonaro taken to hospital** — Brazil's ex-president in severe
   abdominal pain.
5. **Suicide bombing kills five in Pakistan** — car bomb at a security
   checkpoint; 13 injured.
6. **Trump: no AI data centres abroad** — the president says US firms
   must not build them overseas.

Also today: India fight back in the Wellington Test; the UN warns
hunger-aid funding is running short; Hyundai unveils the 2027 Elantra
in Los Angeles.

Every story was checked against news reported on 21 November 2026.
The picture is drawn from scratch with vector-style shapes — no photos,
no downloaded assets.

## How it is built

`tools/draw_frontpage.py` draws the front page with Pillow (stdlib-style
shapes and text only) and writes `entry.png`. `main.ts` (Node 22,
standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`, refusing to run if the file is not a
PNG or exceeds the 1 MiB limit.

Run it:

```sh
python3 tools/draw_frontpage.py
MAKEFUN_OUTPUT_DIR=out node main.ts
```

Two runs write byte-identical output (verified with sha256).

## License

MIT — see [LICENSE](LICENSE).
