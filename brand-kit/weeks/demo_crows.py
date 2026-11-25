"""Demo: Sharon's own words about Hello Stranger, paced across slides.
The escalating metaphor IS the open loop — each slide earns the next swipe.
Zero plot detail. Slogan lands last.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from render import *

OUT = 'out/demo'
P = {}

P['c1'] = ('ink', FEED, kicker('dark romance', 'ink') + head('Hello<br>Stranger', 'ink', 104)
           + small('Jade West', 'ink', 30) + rule()
           + ital('let me tell you what<br>it did to my heart.', 'ink', 62), {})
P['c2'] = ('ivory', FEED, ital('It destroyed<br>my heart.', 'ivory', 104), {})
P['c3'] = ('bur', FEED, ital('Then it threw<br>my heart out.', 'bur', 100), {})
P['c4'] = ('ink', FEED, ital('Then it called<br>the crows.', 'ink', 104), {})
P['c5'] = ('ivory', FEED, kicker('and still', 'ivory') + head('Six stars.', 'ivory', 104)
           + rule() + ital('I would hand it<br>to you anyway.', 'ivory', 76), {})
P['c6'] = ('bur', FEED, kicker('for books like this one', 'bur')
           + ital('Don\'t handle<br>with care.', 'bur', 104)
           + rule() + small('on the back · sin & sonnet', 'bur', 28), {})

if __name__ == '__main__':
    build(P, outdir=OUT)
    sheet(['c1', 'c2', 'c3', 'c4', 'c5', 'c6'], f'{OUT}/demo-crows.png', outdir=OUT, cols=6, tile=330)
    print('done')
