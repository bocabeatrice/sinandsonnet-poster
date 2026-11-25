"""Demo: a book carousel built with ZERO plot recall required.
Every line comes from her own rating, not from any claim about the story.
Slogan lands on the last slide as the punchline.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from render import *

OUT = 'out/demo'
P = {}

# Hook — "dark military romance" sits in the on-screen text for search.
P['d1'] = ('ink', FEED, kicker('dark military romance', 'ink')
           + head('Four books', 'ink', 112) + ital('that got my<br>rarest rating.', 'ink', 92)
           + rule() + small('out of 240 · swipe', 'ink', 28), {'sym': 150})

# The books. No plot claims — only her rating and her reaction.
P['d2'] = ('ivory', FEED, kicker('nº 1', 'ivory') + head('Bulletproof', 'ivory', 88)
           + small('K.M. Moronova', 'ivory', 30) + rule()
           + ital('I would give up<br>remembering it<br>just to read it again.', 'ivory', 62), {})
P['d3'] = ('bur', FEED, kicker('nº 2', 'bur') + head('Dark Forces', 'bur', 88)
           + small('K.M. Moronova', 'bur', 30) + rule()
           + ital('same author. yes,<br>that is the point.', 'bur', 64), {})
P['d4'] = ('ink', FEED, kicker('nº 3', 'ink') + head('Leave Me<br>Behind', 'ink', 88)
           + small('K.M. Moronova', 'ink', 30) + rule()
           + ital('three for three.<br>nobody else is close.', 'ink', 62), {})
P['d5'] = ('ivory', FEED, kicker('nº 4', 'ivory') + head('Mariposa', 'ivory', 96)
           + small('Lexie Axelson', 'ivory', 30) + rule()
           + ital('the one I hand people<br>who say they<br>don\'t read military.', 'ivory', 60), {})

# Payoff — the slogan is the punchline, and it is a Chapter One shirt.
P['d6'] = ('bur', FEED, kicker('the whole genre in two words', 'bur')
           + ital('Yes, Sir.', 'bur', 170) + rule()
           + small('on the back. chapter one.', 'bur', 30), {})

if __name__ == '__main__':
    build(P, outdir=OUT)
    sheet(['d1', 'd2', 'd3', 'd4', 'd5', 'd6'], f'{OUT}/demo-military.png', outdir=OUT, cols=6, tile=330)
    print('done')
