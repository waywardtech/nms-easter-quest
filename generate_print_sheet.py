#!/usr/bin/env python3
"""
Generate a printable A4 PDF of all QR codes.
Run AFTER generate_qr.py has created the QR images.

Usage:
    pip3 install reportlab --break-system-packages
    python3 generate_print_sheet.py
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
import sys

QR_DATA = [
    ("qr_start.png",       "QUEST START",   "Hand to player to begin",     "#E6A800"),
    ("qr_stop1.png",       "WAYPOINT 1",    "Fridge / Kitchen",            "#007A75"),
    ("qr_stop2.png",       "WAYPOINT 2",    "Coffee Table / Living Room",  "#007A75"),
    ("qr_stop3.png",       "WAYPOINT 3",    "Stairs / Hallway",            "#007A75"),
    ("qr_stop4.png",       "WAYPOINT 4",    "Garden / Back Door",          "#007A75"),
    ("qr_stop5.png",       "WAYPOINT 5",    "Bathroom / Mirror",           "#6B2FAA"),
    ("qr_stop6.png",       "WAYPOINT 6",    "Airing Cupboard / Linen",     "#CC4400"),
    ("qr_stop7.png",       "WAYPOINT 7",    "Oven / Kitchen",              "#CC4400"),
    ("qr_stop8.png",       "WAYPOINT 8",    "Kitchen Hob",                 "#007A75"),
    ("qr_stop9.png",       "WAYPOINT 9",    "Living Room / Sofa",          "#E6A800"),
    ("qr_stop10.png",      "WAYPOINT 10",   "Bedroom",                     "#E6A800"),
    ("qr_certificate.png", "CERTIFICATE",   "Atlas Seal of the Traveller", "#E6A800"),
]

SRC = os.path.join(os.path.dirname(__file__), "public", "qr")
OUT = os.path.join(os.path.dirname(__file__), "qr_print_sheet.pdf")

PAGE_W, PAGE_H = A4
COLS, ROWS = 3, 4
MARGIN_X = 10 * mm
MARGIN_Y = 12 * mm
avail_w = PAGE_W - 2 * MARGIN_X
avail_h = PAGE_H - 2 * MARGIN_Y - 14 * mm
CELL_W = avail_w / COLS
CELL_H = avail_h / ROWS
QR_SIZE = min(CELL_W, CELL_H) * 0.70
BAR_H   = 9 * mm
PADDING = 2 * mm

def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))

# Check QR images exist
missing = [f for f, *_ in QR_DATA if not os.path.exists(os.path.join(SRC, f))]
if missing:
    print(f"ERROR: Missing QR images: {missing}")
    print("Run generate_qr.py first.")
    sys.exit(1)

c = canvas.Canvas(OUT, pagesize=A4)
c.setFillColorRGB(1, 1, 1)
c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

# Header
c.setFillColorRGB(*hex_rgb("#007A75"))
c.setFont("Helvetica", 7)
c.drawCentredString(PAGE_W/2, PAGE_H - MARGIN_Y + 4*mm,
    "NO MAN'S SKY  ·  EASTER QUEST  ·  Cut out and hide each code at the location shown")
c.setStrokeColorRGB(0.8, 0.8, 0.8)
c.setLineWidth(0.4)
c.line(MARGIN_X, PAGE_H - MARGIN_Y, PAGE_W - MARGIN_X, PAGE_H - MARGIN_Y)

top_y = PAGE_H - MARGIN_Y - 2*mm

for idx, (fname, label, sublabel, colour_hex) in enumerate(QR_DATA):
    col = idx % COLS
    row = idx // COLS
    cell_x = MARGIN_X + col * CELL_W
    cell_y = top_y - (row + 1) * CELL_H
    cx = cell_x + CELL_W / 2
    col_rgb = hex_rgb(colour_hex)

    # Dashed cut border
    c.setStrokeColorRGB(0.75, 0.75, 0.75)
    c.setLineWidth(0.4)
    c.setDash(2, 3)
    c.rect(cell_x + PADDING, cell_y + PADDING, CELL_W - 2*PADDING, CELL_H - 2*PADDING)
    c.setDash()

    # Colour accent stripe
    bar_top = cell_y + CELL_H - PADDING
    bar_bot = bar_top - BAR_H
    c.setFillColorRGB(*col_rgb)
    c.rect(cell_x + PADDING, bar_bot, 2*mm, BAR_H, fill=1, stroke=0)

    # Label
    c.setFillColorRGB(*col_rgb)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(cell_x + PADDING + 3.5*mm, bar_bot + BAR_H*0.55, label)

    c.setFillColorRGB(0.35, 0.35, 0.35)
    c.setFont("Helvetica", 7)
    c.drawString(cell_x + PADDING + 3.5*mm, bar_bot + BAR_H*0.15, sublabel)

    c.setStrokeColorRGB(0.88, 0.88, 0.88)
    c.setLineWidth(0.3)
    c.line(cell_x + PADDING + 1*mm, bar_bot, cell_x + CELL_W - PADDING - 1*mm, bar_bot)

    # QR image
    img_path = os.path.join(SRC, fname)
    remaining_h = CELL_H - BAR_H - 3*PADDING
    qr_draw = min(QR_SIZE, remaining_h - 2*mm)
    qr_x = cx - qr_draw / 2
    qr_y = cell_y + PADDING + (remaining_h - qr_draw) / 2
    c.drawImage(img_path, qr_x, qr_y, qr_draw, qr_draw,
                preserveAspectRatio=True, mask='auto')

# Footer
c.setStrokeColorRGB(0.8, 0.8, 0.8)
c.setLineWidth(0.4)
c.line(MARGIN_X, MARGIN_Y - 2*mm, PAGE_W - MARGIN_X, MARGIN_Y - 2*mm)
c.setFillColorRGB(0.5, 0.5, 0.5)
c.setFont("Helvetica", 6)
c.drawCentredString(PAGE_W/2, MARGIN_Y - 6*mm,
    "Scan with iPhone Camera app  ·  Device must be on home WiFi  ·  raspberrypi.local:3000")

c.save()
print(f"Print sheet saved: {OUT}")
