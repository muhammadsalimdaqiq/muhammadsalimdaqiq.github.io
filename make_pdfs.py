#!/usr/bin/env python3
"""Generates the downloadable Executive CV and Biography PDFs from the same verified content as the site."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import build as B
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle

F = os.path.join(os.path.dirname(__file__), "fonts")
for n in ["Manrope-Regular", "Manrope-SemiBold", "Manrope-ExtraBold", "Cormorant-Medium", "Cormorant-SemiBold", "Cormorant-Italic"]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(F, n + ".ttf")))

NAVY, INK, GOLD, CHAMP, MUTED, LINE = HexColor("#070d1c"), HexColor("#141a2a"), HexColor("#b08d47"), HexColor("#e6d3a3"), HexColor("#5d6575"), HexColor("#e3dccb")
OUT = os.path.join(B.ROOT, "assets", "documents", "cv")
os.makedirs(OUT, exist_ok=True)
W, H = A4
M = 18 * mm

def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    return s.replace("&amp;", "&amp;").replace("&middot;", "·").replace("&nbsp;", " ")

st = dict(
 body=ParagraphStyle("b", fontName="Manrope-Regular", fontSize=9.2, leading=13.4, textColor=INK),
 small=ParagraphStyle("s", fontName="Manrope-Regular", fontSize=8.2, leading=11.5, textColor=MUTED),
 h=ParagraphStyle("h", fontName="Manrope-ExtraBold", fontSize=8, leading=10, textColor=GOLD, spaceBefore=12, spaceAfter=7, letterSpacing=None),
 role=ParagraphStyle("r", fontName="Cormorant-SemiBold", fontSize=14.5, leading=17, textColor=NAVY, spaceAfter=3),
 org=ParagraphStyle("o", fontName="Manrope-SemiBold", fontSize=8.4, leading=11, textColor=MUTED),
 date=ParagraphStyle("d", fontName="Manrope-SemiBold", fontSize=8.2, leading=11, textColor=GOLD),
 bullet=ParagraphStyle("bl", fontName="Manrope-Regular", fontSize=8.8, leading=12.4, textColor=INK, leftIndent=9, bulletIndent=0),
 quote=ParagraphStyle("q", fontName="Cormorant-Italic", fontSize=13, leading=17, textColor=NAVY),
)

def H_(t): return Paragraph("&nbsp;&nbsp;&nbsp;".join(" ".join(w) for w in t.upper().replace("&","&amp;").split(" ")).replace("&amp; ","&amp;"), st["h"])

def chrome(title):
    def draw(c, doc):
        c.saveState()
        if doc.page == 1:
            c.setFillColor(NAVY); c.rect(0, H - 52 * mm, W, 52 * mm, stroke=0, fill=1)
            c.setFillColor(GOLD); c.rect(M, H - 52 * mm, 30 * mm, 0.8 * mm, stroke=0, fill=1)
            c.setStrokeColor(GOLD); c.setLineWidth(.7); c.circle(W - M - 11 * mm, H - 24 * mm, 11 * mm)
            c.setFont("Cormorant-SemiBold", 17); c.setFillColor(CHAMP); c.drawCentredString(W - M - 11 * mm, H - 25.6 * mm, "D")
            c.setFont("Manrope-ExtraBold", 7.5); c.setFillColor(CHAMP); c.drawString(M, H - 15 * mm, title.upper())
            c.setFont("Cormorant-Medium", 30); c.setFillColor(HexColor("#f7f5f0")); c.drawString(M, H - 28 * mm, "Muhammad Salim Daqiq")
            c.setFont("Manrope-Regular", 8.8); c.setFillColor(HexColor("#c3c8d2"))
            c.drawString(M, H - 36 * mm, "International Entrepreneur  ·  Founder  ·  Executive Leader  ·  Human Rights Advocate  ·  Development Strategist")
            c.setFillColor(CHAMP); c.drawString(M, H - 43.5 * mm, f"{B.EMAIL}   ·   daqiq.af   ·   {B.BASE.replace('https://', '')}")
        c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(M, 13 * mm, W - M, 13 * mm)
        c.setFont("Manrope-Regular", 7); c.setFillColor(MUTED)
        c.drawString(M, 9 * mm, f"Muhammad Salim Daqiq — {title}"); c.drawRightString(W - M, 9 * mm, f"Page {doc.page}")
        c.restoreState()
    return draw

def doc(path, title):
    d = BaseDocTemplate(path, pagesize=A4, title=f"Muhammad Salim Daqiq — {title}", author="Muhammad Salim Daqiq", subject=title,
                        leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=18 * mm)
    first = Frame(M, 18 * mm, W - 2 * M, H - 52 * mm - 8 * mm - 18 * mm, id="f1")
    later = Frame(M, 18 * mm, W - 2 * M, H - M - 18 * mm, id="f2")
    d.addPageTemplates([PageTemplate("first", [first], onPage=chrome(title), autoNextPageTemplate="later"), PageTemplate("later", [later], onPage=chrome(title))])
    return d

def cv():
    path = os.path.join(OUT, "Muhammad-Salim-Daqiq-Executive-CV.pdf")
    s = [H_("Profile"), Paragraph(clean(B.BIO_150), st["body"])]
    s += [H_("Founder roles and professional experience")]
    for e in B.EXPERIENCE:
        rows = [[Paragraph(clean(e["date"]), st["date"]), [Paragraph(clean(e["title"]), st["role"]), Paragraph(clean(e["org"]), st["org"]), Spacer(1, 3),
                 Paragraph(clean(e["text"]), st["body"])] + [Paragraph(clean(r), st["bullet"], bulletText="–") for r in e["resp"]]]]
        t = Table(rows, colWidths=[36 * mm, W - 2 * M - 36 * mm])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                               ("LINEBELOW", (0, 0), (-1, -1), .4, LINE), ("TOPPADDING", (0, 0), (-1, -1), 6)]))
        s.append(KeepTogether(t))
    s += [H_("Education")]
    rows = [[Paragraph(clean(y) or "—", st["date"]), Paragraph(f"<font name='Cormorant-SemiBold' size='12.5' color='#070d1c'>{clean(l)} — {clean(f)}</font><br/>{clean(i)}", st["body"])] for l, f, i, y, k in B.EDUCATION]
    t = Table(rows, colWidths=[36 * mm, W - 2 * M - 36 * mm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LINEBELOW", (0, 0), (-1, -1), .4, LINE)]))
    s.append(t)
    s += [H_("Core capabilities"), Paragraph("Institution building and governance · International trade and sourcing · Humanitarian logistics and supply chain · Executive administration and official communication · Community engagement and volunteer mobilization · Project management and proposal writing · Women’s and youth empowerment · Psychosocial support", st["body"])]
    s += [H_("Languages"), Paragraph("English · Persian (Dari) · Turkish · Hindi", st["body"])]
    doc(path, "Executive CV").build(s)
    return path

def bio():
    path = os.path.join(OUT, "Muhammad-Salim-Daqiq-Biography.pdf")
    s = [Paragraph("“Building enterprises. Empowering communities. Creating opportunities.”", st["quote"]), Spacer(1, 6)]
    s += [H_("Full biography (150 words)"), Paragraph(clean(B.BIO_150), st["body"])]
    s += [H_("Medium biography (60 words)"), Paragraph(clean(B.BIO_60), st["body"])]
    s += [H_("Short biography (25 words)"), Paragraph(clean(B.BIO_25), st["body"])]
    s += [H_("Organizations"),
          Paragraph("<b>DAQIQ INTERNATIONAL</b> — Founder & Executive Leader. International import and export, global sourcing, agricultural commodities, food products, industrial supplies and wholesale distribution. daqiq.af · info@daqiq.af", st["body"]), Spacer(1, 5),
          Paragraph("<b>The Changemakers</b> (formerly Change in Youths Social Assembly, +CYSA) — Founder & Organizational Leader. Founded in Kandahar in 2015; formally registered in 2018; continued as The Changemakers after August 2021. Human rights, youth leadership, women’s empowerment, girls’ education, child protection and community development.", st["body"])]
    s += [Spacer(1, 10), Paragraph(f"Official website: {B.BASE}", st["small"])]
    doc(path, "Professional Biography").build(s)
    return path

if __name__ == "__main__":
    print(cv()); print(bio())
