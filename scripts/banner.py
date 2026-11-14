"""Animated dot-matrix banner for the README (pure SVG + CSS, no JS: GitHub renders it in <img>)."""
from pathlib import Path
F = {
 "V": ["1...1","1...1","1...1","1...1","1...1",".1.1.","..1.."],
 "I": ["11111","..1..","..1..","..1..","..1..","..1..","11111"],
 "B": ["1111.","1...1","1...1","1111.","1...1","1...1","1111."],
 "E": ["11111","1....","1....","1111.","1....","1....","11111"],
 "-": [".....",".....",".....","11111",".....",".....","....."],
 "C": [".111.","1...1","1....","1....","1....","1...1",".111."],
 "H": ["1...1","1...1","1...1","11111","1...1","1...1","1...1"],
 "K": ["1...1","1..1.","1.1..","11...","1.1..","1..1.","1...1"],
}
WORD = "VIBE-CHECK"; P = 13; R = 4.1; W, H = 900, 270
cols = len(WORD) * 6 - 1
x0 = (W - (cols - 1) * P) / 2; y0 = 46
off, on = [], []
for ci, ch in enumerate(WORD):
    for r, row in enumerate(F[ch]):
        for c, v in enumerate(row):
            col = ci * 6 + c
            x, y = x0 + col * P, y0 + r * P
            (on if v == "1" else off).append((col, x, y))
    if ci < len(WORD) - 1:
        for r in range(7):
            col = ci * 6 + 5; off.append((col, x0 + col * P, y0 + r * P))
dots_off = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R*0.62:.1f}"/>' for _, x, y in off)
dots_on = "".join(f'<circle class="d c{col}" cx="{x:.1f}" cy="{y:.1f}" r="{R}"/>' for col, x, y in on)
dots_glow = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R}"/>' for _, x, y in on)
delays = "".join(f".c{c}{{animation-delay:{0.15 + c*0.022:.3f}s}}" for c in range(cols))
sub = "PRE-LAUNCH AUDIT FOR AI-BUILT APPS"
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="vibe-check: pre-launch audit for AI-built apps">
<title>vibe-check: pre-launch audit for AI-built apps</title>
<defs>
<linearGradient id="sweep" gradientUnits="userSpaceOnUse" x1="-260" y1="0" x2="0" y2="0">
<stop offset="0" stop-color="#22c55e" stop-opacity="0"/><stop offset="0.7" stop-color="#4ade80" stop-opacity="1"/><stop offset="0.85" stop-color="#dcfce7" stop-opacity="1"/><stop offset="1" stop-color="#4ade80" stop-opacity="0"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;0 0;{W+260} 0;{W+260} 0" keyTimes="0;0.3;0.75;1" dur="5s" begin="1.6s" repeatCount="indefinite"/>
</linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="type"><rect x="0" y="150" height="40" width="0"><animate attributeName="width" from="0" to="{W}" dur="1.4s" begin="1.5s" fill="freeze" calcMode="spline" keySplines="0.3 0 0.4 1" keyTimes="0;1"/></rect></clipPath>
</defs>
<style>
.bg{{fill:#0b0b0c}} .off{{fill:#232326}} .on{{fill:#e9e9ea}}
.d{{opacity:0;animation:pop .45s cubic-bezier(.2,.9,.3,1.4) forwards}}
@keyframes pop{{0%{{opacity:0;transform:scale(.2)}}100%{{opacity:1;transform:scale(1)}}}}
.d{{transform-box:fill-box;transform-origin:center}}
{delays}
.sw{{fill:url(#sweep)}}
.sub{{font:600 15px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;letter-spacing:6px;fill:#a1a1aa}}
.cur{{fill:#22c55e;animation:blink 1s steps(1) infinite;animation-delay:2.9s;opacity:0}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
.tag{{font:600 11px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;letter-spacing:3px;fill:#71717a}}
.live{{fill:#22c55e;animation:pulse 2s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
.fade{{opacity:0;animation:in .8s ease forwards;animation-delay:3s}}
@keyframes in{{to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.d,.fade{{animation:none;opacity:1}}.cur,.live{{animation:none;opacity:1}}.sw{{display:none}}}}
</style>
<rect class="bg" width="{W}" height="{H}" rx="18"/>
<g class="off">{dots_off}</g>
<g class="on">{dots_on}</g>
<g class="sw" filter="url(#glow)">{dots_glow}</g>
<g clip-path="url(#type)"><text class="sub" x="{W/2}" y="172" text-anchor="middle">{sub}</text></g>
<rect class="cur" x="{W/2 + 262}" y="158" width="9" height="17"/>
<g class="fade">
<circle class="live" cx="{W/2 - 232}" cy="226" r="4.5"/>
<text class="tag" x="{W/2 - 220}" y="230">SECURITY · PRIVACY · LEGAL · RELIABILITY · LAUNCH</text>
</g>
</svg>'''
(Path(__file__).resolve().parent.parent / "assets" / "banner.svg").write_text(svg)
print(len(svg), "bytes,", len(on), "lit dots")
