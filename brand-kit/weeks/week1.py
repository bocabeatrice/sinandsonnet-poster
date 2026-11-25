"""
Week 1 (Nov 23-29 2026) -- the worked example. Copy this file to start a new week.

Run from the repo root:   python3 brand-kit/weeks/week1.py

Naming: '1a','1b','1c' = slides of carousel 1. Plain '2' = a single image.
How it performed: the 5-slide carousel ('1a'-'1e', "House rules") got ~925
views on TikTok vs ~150-180 for the single images. Favour carousels.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from render import *  # noqa: F401,F403

OUT = 'out/week1'
P = {}

# 1 - House rules carousel (5 slides) -- the top performer
P['1a'] = ('ink', FEED, kicker('the library', 'ink') + head('House<br>rules', 'ink', 120)
           + rule() + ital('well read · barely behaved', 'ink', 58), {'sym': 170})
P['1b'] = ('ivory', FEED, kicker('rule nº 1', 'ivory') + ital('We read the spicy ones', 'ivory', 100)
           + head('in public.', 'ivory', 92), {})
P['1c'] = ('bur', FEED, kicker('rule nº 2', 'bur') + ital('We dog-ear.', 'bur', 110)
           + rule() + head("Don't @ us.", 'bur', 84), {})
P['1d'] = ('ink', FEED, kicker('rule nº 3', 'ink') + head('Book<br>boyfriends', 'ink', 96)
           + ital('count.', 'ink', 130), {})
P['1e'] = ('ink', FEED, kicker('rule nº 4', 'ink') + head('Chapter one', 'ink', 88)
           + ital('is coming.', 'ink', 110) + rule() + small('follow to be first', 'ink', 30), {})

# 2 - story, confession
P['2'] = ('bur', STORY, kicker('a confession', 'bur') + ital('“Just one<br>more chapter”', 'bur', 124)
          + rule() + head('is a lie we<br>tell together.', 'bur', 64), {'sym': 230})

# 3 - slogan teaser, boxed
P['3'] = ('ink', FEED, kicker('chapter one · first look', 'ink')
          + f'<div style="border:1.5px solid {GOLD};padding:80px 70px">'
          + head('Bound', 'ink', 118) + ital('&amp;', 'ink', 120) + head('bookmarked', 'ink', 96)
          + '</div><div style="margin-top:44px">'
          + small('coming soon · slogan on the back', 'ink', 28) + '</div>', {})

# 4 - Thanksgiving
P['4'] = ('ivory', FEED, kicker('happy thanksgiving', 'ivory') + head('Grateful for', 'ivory', 84)
          + rule() + ital('a long weekend,<br>a full Kindle,<br>&amp; zero plans.', 'ivory', 92), {})

# 5 - story, Black Friday anti-sale
P['5'] = ('ink', STORY, kicker('black friday', 'ink') + head('No sale.', 'ink', 110)
          + ital("We're still writing<br>chapter one.", 'ink', 100) + rule()
          + small('follow to be first', 'ink', 34), {'sym': 230})

# 6 - vote carousel (4 slides)
P['6a'] = ('bur', FEED, kicker('help us write chapter one', 'bur') + head('Vote', 'bur', 150)
           + ital('for the slogans<br>that make the cut', 'bur', 84) + rule()
           + small('swipe · then comment 1, 2 or 3', 'bur', 30), {})
P['6b'] = ('ink', FEED, numeral('1', 'ink') + head("F*ck off,", 'ink', 100)
           + ital("I'm reading.", 'ink', 112), {})
P['6c'] = ('ivory', FEED, numeral('2', 'ivory') + head('Wake up,', 'ivory', 96)
           + ital("it's time to sin.", 'ivory', 104), {})
P['6d'] = ('bur', FEED, numeral('3', 'bur') + head('Strict rules,', 'bur', 90)
           + ital('loose morals.', 'bur', 112), {})

# 7 - story, weekend roll call
P['7'] = ('ivory', STORY, kicker('weekend roll call', 'ivory') + head("What are<br>you reading?", 'ivory', 96)
          + rule() + ital('reply &amp; tell us.<br>no judgment. (some judgment.)', 'ivory', 72), {'sym': 230})


if __name__ == '__main__':
    build(P, outdir=OUT)
    sheet(['1a', '1b', '1c', '1d', '1e'], f'{OUT}/preview-1-carousel.png', outdir=OUT)
    sheet(['2', '3', '4', '5'], f'{OUT}/preview-2-midweek.png', outdir=OUT)
    sheet(['6a', '6b', '6c', '6d', '7'], f'{OUT}/preview-3-weekend.png', outdir=OUT)
    print('done ->', OUT)
