from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ── Page margins (tight for 1 page) ──────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(1.2)
    section.bottom_margin = Cm(1.2)
    section.left_margin   = Cm(1.8)
    section.right_margin  = Cm(1.8)

# ── Colours ───────────────────────────────────────────────────────────────────
NAVY    = RGBColor(0x0D, 0x2B, 0x55)   # name / section titles
BLUE    = RGBColor(0x16, 0x6D, 0xBE)   # accent / links
GRAY    = RGBColor(0x55, 0x65, 0x80)   # secondary text
BLACK   = RGBColor(0x1A, 0x1A, 0x1A)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sp(para, before=0, after=0, line=None):
    pPr = para._p.get_or_add_pPr()
    spc = OxmlElement("w:spacing")
    spc.set(qn("w:before"), str(before))
    spc.set(qn("w:after"),  str(after))
    if line:
        spc.set(qn("w:line"),     str(line))
        spc.set(qn("w:lineRule"), "auto")
    pPr.append(spc)

def run(para, text, bold=False, italic=False, color=BLACK,
        size=Pt(9), font="Calibri", underline=False):
    r = para.add_run(text)
    r.bold      = bold
    r.italic    = italic
    r.underline = underline
    r.font.name  = font
    r.font.size  = size
    r.font.color.rgb = color
    return r

def hyperlink(para, url, text, color=BLUE, size=Pt(9)):
    part = para.part
    rid  = part.relate_to(url,
           "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
           is_external=True)
    hl  = OxmlElement("w:hyperlink")
    hl.set(qn("r:id"), rid)
    nr  = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    # colour
    c = OxmlElement("w:color")
    c.set(qn("w:val"), f"{color[0]:02X}{color[1]:02X}{color[2]:02X}")
    rPr.append(c)
    # underline
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rPr.append(u)
    # size
    sz   = OxmlElement("w:sz");   sz.set(qn("w:val"),   str(int(size.pt*2))); rPr.append(sz)
    szCs = OxmlElement("w:szCs"); szCs.set(qn("w:val"), str(int(size.pt*2))); rPr.append(szCs)
    # font
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), "Calibri")
    rFonts.set(qn("w:hAnsi"), "Calibri")
    rPr.append(rFonts)
    nr.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    nr.append(t)
    hl.append(nr)
    para._p.append(hl)

def no_border_table(table):
    tbl   = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement("w:tblPr")
    brd   = OxmlElement("w:tblBorders")
    for side in ("top","left","bottom","right","insideH","insideV"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"),   "none")
        el.set(qn("w:sz"),    "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        brd.append(el)
    tblPr.append(brd)
    if tbl.tblPr is None:
        tbl.insert(0, tblPr)

def set_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex_color)
    tcPr.append(shd)

def bottom_border(para, color="166DBE"):
    """Add a bottom border to a paragraph."""
    pPr = para._p.get_or_add_pPr()
    pb  = OxmlElement("w:pBdr")
    bot = OxmlElement("w:bottom")
    bot.set(qn("w:val"),   "single")
    bot.set(qn("w:sz"),    "6")
    bot.set(qn("w:space"), "1")
    bot.set(qn("w:color"), color)
    pb.append(bot)
    pPr.append(pb)

def section_title(doc, title):
    p = doc.add_paragraph()
    sp(p, before=100, after=40)
    bottom_border(p)
    r = p.add_run(title.upper())
    r.bold = True
    r.font.name  = "Calibri"
    r.font.size  = Pt(9.5)
    r.font.color.rgb = NAVY

def bullet_item(doc, text, before=0, after=30):
    p = doc.add_paragraph()
    sp(p, before=before, after=after)
    # manual bullet
    run(p, "▪  ", color=BLUE, size=Pt(8))
    run(p, text, color=BLACK, size=Pt(8.5))
    return p

def two_col_row(doc, left_text, right_text,
                left_bold=True, left_color=NAVY,
                right_color=GRAY, size=Pt(9)):
    tbl = doc.add_table(rows=1, cols=2)
    no_border_table(tbl)
    tbl.columns[0].width = Cm(12.0)
    tbl.columns[1].width = Cm(5.0)
    lp = tbl.cell(0,0).paragraphs[0]
    rp = tbl.cell(0,1).paragraphs[0]
    rp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    sp(lp, before=0, after=0)
    sp(rp, before=0, after=0)
    run(lp, left_text,  bold=left_bold,  color=left_color,  size=size)
    run(rp, right_text, bold=False,      color=right_color, size=Pt(8.5))
    return tbl

# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════════════════════
name_p = doc.add_paragraph()
name_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sp(name_p, before=0, after=20)
run(name_p, "ISHTIAK AHMED", bold=True, color=NAVY, size=Pt(20), font="Calibri")

title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sp(title_p, before=0, after=30)
run(title_p, "Full Stack Web Developer  ·  Python | Django | React",
    italic=True, color=BLUE, size=Pt(10))

# Contact line
contact_p = doc.add_paragraph()
contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sp(contact_p, before=0, after=20)
run(contact_p, "Dhaka, Bangladesh  |  moonishtiak03@gmail.com  |  +880 1624407867  |  ", color=GRAY, size=Pt(8.5))
hyperlink(contact_p, "https://sites.google.com/diu.edu.bd/moon123/home", "Portfolio", size=Pt(8.5))
run(contact_p, "  |  ", color=GRAY, size=Pt(8.5))
hyperlink(contact_p, "http://linkedin.com/in/moon-ishtiak-b98745304", "LinkedIn", size=Pt(8.5))
run(contact_p, "  |  ", color=GRAY, size=Pt(8.5))
hyperlink(contact_p, "https://github.com/Ishtiak-Ahmed886", "GitHub", size=Pt(8.5))

# Thin divider
div = doc.add_paragraph()
sp(div, before=20, after=0)
bottom_border(div, color="0D2B55")

# ═══════════════════════════════════════════════════════════════════════════════
#  CAREER OBJECTIVE
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, "Career Objective")
obj = doc.add_paragraph()
sp(obj, before=20, after=0, line=252)
run(obj, ("Motivated junior full-stack developer with expertise in Python, Django, and React.js. "
    "Skilled in backend REST APIs and frontend development with React, and experienced with "
    "PostgreSQL and MongoDB. Seeking an internship opportunity to contribute to a collaborative "
    "team, apply technical skills, and grow professionally while delivering high-quality software solutions."),
    color=BLACK, size=Pt(8.8))

# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIENCE
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, "Experience")
two_col_row(doc,
    "ACCELX INC  —  Full-Stack Web Developer (Onsite Intern)",
    "Nov 2023 – Jan 2024  |  Dhaka",
    left_color=NAVY, size=Pt(9))
bullet_item(doc, "Contributed to real-world projects focusing on user experience and performance.", before=20)
bullet_item(doc, "Played a key role in developing features for Examely, enhancing its functionality and usability.")

# ═══════════════════════════════════════════════════════════════════════════════
#  TECHNICAL SKILLS
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, "Technical Skills")

skills_tbl = doc.add_table(rows=4, cols=2)
no_border_table(skills_tbl)
skills_tbl.columns[0].width = Cm(4.5)
skills_tbl.columns[1].width = Cm(12.5)

skill_rows = [
    ("Languages",   "C, C++, Java, JavaScript, TypeScript"),
    ("Frontend",    "React.js, Next.js, Tailwind CSS, Bootstrap, Redux Toolkit, React-Router-DOM, Firebase, Axios, JWT"),
    ("Backend",     "Node.js, Express.js, REST APIs, Mongoose, Prisma, Zod, Django"),
    ("Databases",   "MongoDB, PostgreSQL, SQL"),
]
for i, (label, value) in enumerate(skill_rows):
    lp = skills_tbl.cell(i, 0).paragraphs[0]
    vp = skills_tbl.cell(i, 1).paragraphs[0]
    sp(lp, before=20, after=20)
    sp(vp, before=20, after=20)
    run(lp, label, bold=True, color=NAVY, size=Pt(8.8))
    run(vp, value, color=BLACK, size=Pt(8.8))

# ═══════════════════════════════════════════════════════════════════════════════
#  PROJECTS  (most impactful 2, brief bullets)
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, "Projects")

projects = [
    {
        "name":   "Amar-Shop",
        "live":   "https://amar-shop-client.vercel.app",
        "client": "https://github.com/Utsho11/amar-shop-client.git",
        "server": "https://github.com/Utsho11/amar-shop-server.git",
        "tech":   "React, Redux Toolkit, TypeScript, Express, Prisma, JWT, PostgreSQL",
        "points": [
            "Full e-commerce platform with product browsing, cart management, and secure checkout.",
            "Integrated real-time order tracking with detailed order history.",
        ]
    },
    {
        "name":   "Book-My-Court",
        "live":   "https://book-my-court.vercel.app",
        "client": "https://github.com/Utsho11/facility-booking-client.git",
        "server": "https://github.com/Utsho11/facility-booking-backend-system.git",
        "tech":   "React, Redux Toolkit, Shadcn UI, TypeScript, Express, Mongoose, Zod, JWT, MongoDB",
        "points": [
            "Court booking system with time-slot search, user profile management, and booking history.",
            "Admin panel for managing court bookings and users with role-based access.",
        ]
    },
    {
        "name":   "Evergreen-Nursery",
        "live":   "https://evergreen-nursery-client.vercel.app",
        "client": "https://github.com/Utsho11/evergreen-nursery-client.git",
        "server": "https://github.com/Utsho11/evergreen-nursery-server.git",
        "tech":   "React, Redux Toolkit, TypeScript, Node.js, Express, Mongoose, MongoDB",
        "points": [
            "Plant e-commerce with advanced search, filtering, and detailed product pages.",
            "Streamlined cart and checkout flow for seamless purchasing experience.",
        ]
    },
]

for proj in projects:
    # Title + links row
    pt = doc.add_paragraph()
    sp(pt, before=30, after=0)
    run(pt, proj["name"] + "  ", bold=True, color=NAVY, size=Pt(9))
    hyperlink(pt, proj["live"],   "Live", size=Pt(8.5))
    run(pt, "  |  ", color=GRAY, size=Pt(8.5))
    hyperlink(pt, proj["client"], "Client", size=Pt(8.5))
    run(pt, "  |  ", color=GRAY, size=Pt(8.5))
    hyperlink(pt, proj["server"], "Server", size=Pt(8.5))
    run(pt, f"   ·  Tech: ", color=GRAY, size=Pt(8.2))
    run(pt, proj["tech"], italic=True, color=GRAY, size=Pt(8.2))

    for b in proj["points"]:
        bullet_item(doc, b, before=10, after=10)

# ═══════════════════════════════════════════════════════════════════════════════
#  EDUCATION  +  CERTIFICATIONS  (two columns)
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, "Education & Certifications")

ec_tbl = doc.add_table(rows=1, cols=2)
no_border_table(ec_tbl)
ec_tbl.columns[0].width = Cm(9.5)
ec_tbl.columns[1].width = Cm(7.5)
ec_tbl.cell(0,0).vertical_alignment = WD_ALIGN_VERTICAL.TOP
ec_tbl.cell(0,1).vertical_alignment = WD_ALIGN_VERTICAL.TOP

edu_cell  = ec_tbl.cell(0,0)
cert_cell = ec_tbl.cell(0,1)

# Education entries
edu_items = [
    ("H.S.C – 5.00/5.00", "Haji Nurul Haque Nonni Poragau Moytry College", "2020"),
    ("S.S.C – 4.83/5.00", "Taragonj Pilot High School", "2018"),
]
for degree, inst, year in edu_items:
    dp = edu_cell.add_paragraph()
    sp(dp, before=20, after=0)
    run(dp, f"{degree}  ", bold=True, color=NAVY, size=Pt(8.8))
    run(dp, f"({year})", color=GRAY, size=Pt(8.5))
    ip = edu_cell.add_paragraph()
    sp(ip, before=0, after=20)
    run(ip, inst, color=BLACK, size=Pt(8.5))

edu_cell.paragraphs[0].clear()  # remove leading blank

# Certifications
certs = [
    ("Complete Web Development Course", "https://drive.google.com/file/d/106UgM_SNhKcL4GaJXd5qgsJGhcbVuGI1/view?usp=sharing"),
    ("Next Level Web Development – NoSQL Track", "https://drive.google.com/file/d/10fue6-G2-KyuQu77gQFy7Q4O9mp3Kihc/view?usp=sharing"),
]
cert_cell.paragraphs[0].clear()
for name, link in certs:
    cp = cert_cell.add_paragraph()
    sp(cp, before=20, after=20)
    run(cp, "▪  ", color=BLUE, size=Pt(8))
    run(cp, name + "  ", color=BLACK, size=Pt(8.5))
    hyperlink(cp, link, "[cert]", size=Pt(8.5))
    run(cp, "  – Programming Hero", color=GRAY, size=Pt(8.2))

# ═══════════════════════════════════════════════════════════════════════════════
#  SOFT SKILLS  +  LANGUAGES  (inline, compact)
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, "Soft Skills & Languages")

sl_tbl = doc.add_table(rows=1, cols=2)
no_border_table(sl_tbl)
sl_tbl.columns[0].width = Cm(9.5)
sl_tbl.columns[1].width = Cm(7.5)

ss_cell = sl_tbl.cell(0,0)
la_cell = sl_tbl.cell(0,1)
ss_cell.paragraphs[0].clear()
la_cell.paragraphs[0].clear()

ss_p = ss_cell.add_paragraph()
sp(ss_p, before=20, after=0)
run(ss_p, "Communication · Teamwork · Adaptability · Problem Solving", color=BLACK, size=Pt(8.8))

la_p = la_cell.add_paragraph()
sp(la_p, before=20, after=0)
run(la_p, "Bangla", bold=True, color=NAVY, size=Pt(8.8))
run(la_p, " (Native)  ·  ", color=GRAY, size=Pt(8.5))
run(la_p, "English", bold=True, color=NAVY, size=Pt(8.8))
run(la_p, " (Professional)  ·  ", color=GRAY, size=Pt(8.5))
run(la_p, "Hindi", bold=True, color=NAVY, size=Pt(8.8))
run(la_p, " (Conversational)", color=GRAY, size=Pt(8.5))

# ── Save ──────────────────────────────────────────────────────────────────────
out = r"c:\Users\Istiak\Downloads\portfolio\Ishtiak_Ahmed_Resume.docx"
doc.save(out)
print(f"OK  Saved to: {out}")
