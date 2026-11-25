# Sin & Sonnet brand kit — weekly mock-up template

Everything needed to render Sin & Sonnet social posts that match the existing
look. Self-contained: fonts and artwork are in this folder, nothing to download
or install. Used by the weekly Sunday scheduled task.

## Make a week

```bash
git clone https://github.com/bocabeatrice/sinandsonnet-poster.git
cd sinandsonnet-poster
cp brand-kit/weeks/week1.py brand-kit/weeks/week2.py   # then edit the posts
python3 brand-kit/weeks/week2.py
```

Renders go to `out/week2/`, plus `preview-*.png` contact sheets to send Sharon.

`brand-kit/weeks/week1.py` is the worked example — read it first. Running it
reproduces week 1 byte-for-byte, so it doubles as a self-test.

## Writing a post

Each entry is `key: (palette, size, inner_html, opts)`.

```python
P['2a'] = ('bur', FEED,
           kicker('rule nº 1','bur') + head('Book','bur',110) + ital('boyfriends.','bur',120),
           {'sym': 170})
```

- **palette** — `'ink'` (near-black), `'ivory'` (cream), `'bur'` (deep burgundy).
  Alternate them across a carousel; don't run two of the same back to back.
- **size** — `FEED` (1080×1350, grid and carousels) or `STORY` (1080×1920,
  stories and reels).
- **opts** — `{'sym': 170}` puts the ribbon-S mark at the top (170 for feed,
  230 for story). `{'footer': False}` drops the bottom lockup; rarely wanted.

Text pieces, in the order they normally stack:

| piece | what it is |
|---|---|
| `kicker(t, pal)` | small spaced label above the headline |
| `head(t, pal, size)` | Montserrat ExtraLight uppercase headline |
| `ital(t, pal, size)` | Cormorant italic accent line, in the accent colour |
| `rule()` | gold hairline divider |
| `small(t, pal, size)` | Jost caption / call-to-action |
| `numeral(n, pal)` | big italic number, for vote and listicle slides |

Use `<br>` for line breaks and `&amp;` for an ampersand inside text.

## Naming

`'3a'`, `'3b'`, `'3c'` are slides of carousel 3, in order. A plain `'4'` is a
single image. Keep the numbers in posting order across the week.

## Rules that don't change

- Logo lockup, `@sinandsonnet`, and the gold hairline sit at the bottom of every
  post — that's what `foot()` does automatically. Leave it on.
- Burgundy `&` always larger than SIN and SONNET.
- Tagline is *well read · barely behaved* — lowercase, middle dot, never a hyphen.
- No script or handwritten fonts, no Bodoni. See the Brand Bible for the
  rejected list.
- Slogans live on the **back** of garments; fronts get the small monogram. The
  mock-ups here are social posts, not garment art — don't mix the two up.

**Don't restyle the template.** Colours, fonts and layout are the brand. If a
week needs a format this template can't do, build it and flag it to Sharon
rather than quietly changing the look.

## What performed (keep this updated each week)

- **Week 1 (Nov 23–29):** the 5-slide "House rules" carousel got ~925 TikTok
  views; single images got ~150–180. Carousels win by a wide margin — favour
  multi-slide posts, and put the hook on slide 1.
