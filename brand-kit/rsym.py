import json
import os
_HERE=os.path.dirname(os.path.abspath(__file__))
_R=json.load(open(os.path.join(_HERE,'traced.json')))
_P={'light':('#3B0E17','#9A2E42','#5A1626','#2A0A10','#0B090A','#3A3236'),
    'dark':('#7A2334','#D9637A','#A33349','#6E1F2E','#D9CFC0','#FFFFFF'),
    'burg':('#B98892','#F4D6DC','#E8B4BE','#C9A2A9','#E9DFD0','#FFFFFF')}
_n=[0]
def rsym(key,pal='light',h=300):
    v=_R[key]; W,H=v['size']; w=round(h*W/H); _n[0]+=1; u=f'{key}{pal}{_n[0]}'
    a,b,c,d,k0,k1=_P[pal]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{w}" height="{h}" style="display: block">'
     f'<defs><linearGradient id="r{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset=".45" stop-color="{b}"/><stop offset=".7" stop-color="{c}"/><stop offset="1" stop-color="{d}"/></linearGradient>'
     f'<linearGradient id="k{u}" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{k0}"/><stop offset=".6" stop-color="{k1}"/><stop offset="1" stop-color="{k0}"/></linearGradient></defs>'
     f'<path d="{v["paths"]["blk"]}" fill="url(#k{u})" fill-rule="evenodd"/><path d="{v["paths"]["red"]}" fill="url(#r{u})" fill-rule="evenodd"/></svg>')
