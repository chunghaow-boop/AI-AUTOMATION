import sys, io
from weasyprint import HTML, CSS
src,out = sys.argv[1], sys.argv[2]

# WeasyPrint does NOT resolve CSS custom properties used as SVG *presentation
# attributes* (fill="var(--acc2)"), so every framing diagram printed near-black.
# Resolve them to hex for the PDF only; the HTML keeps its CSS vars and themes.
PALETTE = {'--bg':'#0f1115','--card':'#171a21','--card2':'#1d212b','--line':'#2a2f3a',
           '--txt':'#e8eaf0','--mut':'#9aa3b2','--acc':'#e11d48','--acc2':'#f59e0b',
           '--ok':'#10b981','--blue':'#3b82f6'}
_html = io.open(src, encoding='utf-8').read()
for _k, _v in PALETTE.items():
    _html = _html.replace('"var(%s)"' % _k, '"%s"' % _v)
# optional 3rd arg: the week's date range for the running footer
RANGE = sys.argv[3] if len(sys.argv) > 3 else "24–30 Ogos 2026"
# Phone-shaped pages: content area is ~344px wide, so the document's own
# max-width:760px mobile layout applies naturally — diagram on top, rows stacked.
PHONE = CSS(string="""
@page { size: A4; margin: 10mm 9mm 12mm; background:#0f1115;
  @bottom-center { content:"Urban Auto Hub · Weekly Trend Plan + Shooting Scripts · """ + RANGE + """   ·   " counter(page) " / " counter(pages);
                   font-size:6pt; color:#9aa3b2; } }
body{padding:0!important;font-size:9.4pt;line-height:1.44}
.wrap{max-width:none!important}
h1{font-size:17pt;line-height:1.22}.sub{font-size:7.6pt;margin:5px 0 9px}
h2{font-size:11pt;margin:14px 0 7px}
h3{font-size:8pt;margin:11px 0 6px}
.rules{gap:5px}.rule{padding:3px 8px;font-size:7.2pt}
.note{padding:8px 10px;font-size:8.2pt;margin:6px 0}
li,.find li{font-size:8.2pt;margin:3px 0}
.src{font-size:7pt}
.dayblk{break-before:page;padding:11px 11px 8px;margin-bottom:0}
.dayhead{margin-bottom:6px}.badge,.expb,.fmt{font-size:7.4pt;padding:2px 7px}
.daytitle{font-size:12pt}
.tag{font-size:7pt;padding:2px 6px}
.cell{padding:8px 10px}.cell h4{font-size:7pt;margin-bottom:5px}
/* one shot per page — swipe through the shoot */
.shot{break-inside:avoid;margin-bottom:7px}
.shead{padding:6px 9px;gap:6px}
.snum{font-size:7pt;padding:2px 6px}.stime{font-size:8pt}.stitle{font-size:8.6pt}
.sbody{padding:9px 10px;gap:8px}
.sbody{grid-template-columns:120px 1fr;gap:12px;padding:10px 11px}
.row{grid-template-columns:104px 1fr;gap:9px;padding:5px 0}
.row{padding:5px 0}
.k{font-size:6.4pt;letter-spacing:.6px}
.v{font-size:8.7pt}
.dlg{padding:5px 8px;margin:3px 0}.who{font-size:6.4pt}.line{font-size:8.6pt}
.lock,.flexb{font-size:6.2pt;padding:0 4px}
code{font-size:7.8pt;padding:0 4px}
th,td{padding:5px 7px;font-size:7.8pt}th{font-size:6.8pt}
.nav{display:none}.legend{font-size:7.2pt;gap:8px}
.cap{font-size:8.4pt}
table{font-size:7.8pt}
""")
HTML(string=_html, base_url=src).write_pdf(out, stylesheets=[PHONE])
print("written",out)
