import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from render import *

OUT = 'out/vote'
P = {}

# Option 1 — honest + minimal change. States plainly that ch.1 is done.
P['opt1'] = ('bur', FEED, kicker('chapter two · you decide', 'bur')
             + head('Which one', 'bur', 104) + ital('goes on the<br>next shirt?', 'bur', 96)
             + rule() + small('swipe · comment 1, 2 or 3', 'bur', 30), {})

# Option 2 — reader identity. "pick your fighter" is a native phrase.
P['opt2'] = ('bur', FEED, kicker('dark romance readers', 'bur')
             + head('Pick your', 'bur', 104) + ital('fighter.', 'bur', 140)
             + rule() + small('swipe · comment 1, 2 or 3', 'bur', 30), {})

# Option 3 — the dare. Open loop + callback to the line that already worked.
P['opt3'] = ('bur', FEED, kicker('be honest', 'bur')
             + head('Which one', 'bur', 104) + ital('would you wear<br>in public?', 'bur', 88)
             + rule() + small('swipe · comment 1, 2 or 3', 'bur', 30), {})

if __name__ == '__main__':
    build(P, outdir=OUT)
    sheet(['opt1', 'opt2', 'opt3'], f'{OUT}/vote-options.png', outdir=OUT, cols=3)
    print('done')
