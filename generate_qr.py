#!/usr/bin/env python3
"""
NMS Easter Quest v2 — QR Code Generator
Run this AFTER you know your Raspberry Pi's IP address.

Usage:
  1. Find your RPi IP:  hostname -I
  2. Edit RPI_IP below
  3. Run: python3 generate_qr.py
  4. QR codes appear in public/qr/
"""

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont
import os

# ── CHANGE THIS to your Raspberry Pi's local IP address ──
RPI_IP = "192.168.5.206"
PORT   = 3000
OUT    = "public/qr"
os.makedirs(OUT, exist_ok=True)

# (slug, url_path, label, subtitle, fg_colour)
PAGES = [
    ("start",       "/",              "QUEST START",     "Hand to Ellis to begin",          "#FFD700", "#050A14"),
    ("stop1",       "/stop/1",        "WAYPOINT 1",      "Fridge / Kitchen",                "#00D4C8", "#050A14"),
    ("stop2",       "/stop/2",        "WAYPOINT 2",      "Coffee Table / Living Room",      "#00D4C8", "#050A14"),
    ("stop3",       "/stop/3",        "WAYPOINT 3",      "Stairs / Hallway",                "#00D4C8", "#050A14"),
    ("stop4",       "/stop/4",        "WAYPOINT 4",      "Garden / Back Door",              "#00D4C8", "#050A14"),
    ("stop5",       "/stop/5",        "WAYPOINT 5",      "Bathroom / Mirror",               "#7B2FBE", "#050A14"),
    ("stop6",       "/stop/6",        "WAYPOINT 6",      "Airing Cupboard / Linen",         "#FF6B35", "#050A14"),
    ("stop7",       "/stop/7",        "WAYPOINT 7",      "Oven / Kitchen",                  "#FF6B35", "#050A14"),
    ("stop8",       "/stop/8",        "WAYPOINT 8",      "Kitchen Hob",                     "#00D4C8", "#050A14"),
    ("stop9",       "/stop/9",        "WAYPOINT 9",      "Living Room / Sofa",              "#FFD700", "#050A14"),
    ("stop10",      "/stop/10",       "WAYPOINT 10",     "Bedroom",                         "#FFD700", "#050A14"),
    ("certificate", "/certificate",   "CERTIFICATE",     "Atlas Seal of the Traveller",     "#FFD700", "#050A14"),
]

try:
    FONT_BOLD  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    FONT_REG   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
except OSError:
    FONT_BOLD  = ImageFont.load_default()
    FONT_REG   = ImageFont.load_default()

for (slug, path, label, subtitle, fg, bg) in PAGES:
    url = f"http://{RPI_IP}:{PORT}{path}"

    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        fill_color=fg,
        back_color=bg,
    ).convert("RGB")

    w, h = img.size
    panel_h = 72
    total = Image.new("RGB", (w, h + panel_h), color=bg)
    total.paste(img, (0, 0))

    draw = ImageDraw.Draw(total)

    # Divider line
    draw.rectangle([(0, h), (w, h + 2)], fill=fg)

    # Label
    draw.text((w // 2, h + 14), label,    fill=fg,      font=FONT_BOLD, anchor="mm")
    draw.text((w // 2, h + 36), subtitle, fill="#4a6a80", font=FONT_REG,  anchor="mm")
    draw.text((w // 2, h + 56), url,      fill="#223344", font=FONT_REG,  anchor="mm")

    # Border
    draw.rectangle([(0, 0), (w - 1, h + panel_h - 1)], outline=fg, width=2)

    out_path = os.path.join(OUT, f"qr_{slug}.png")
    total.save(out_path)
    print(f"  ✓  {out_path}")
    print(f"      → {url}")

print(f"\n✅  {len(PAGES)} QR codes generated in ./{OUT}/")
print(f"\n⚠️  QR codes point to: http://{RPI_IP}:{PORT}")
print(f"    If that's not your RPi's IP, edit RPI_IP and run again.\n")

print("📋  WHERE TO HIDE EACH QR CODE:")
locations = [
    ("qr_start.png",       "Glue onto the printed Starting Clue Card → hand to Ellis"),
    ("qr_stop1.png",       "Hide near or on the FRIDGE"),
    ("qr_stop2.png",       "Hide near the COFFEE TABLE / LIVING ROOM FLOOR"),
    ("qr_stop3.png",       "Hide near the STAIRS or HALLWAY"),
    ("qr_stop4.png",       "Hide near the BACK DOOR or GARDEN"),
    ("qr_stop5.png",       "Hide near the BATHROOM MIRROR"),
    ("qr_stop6.png",       "Hide in or near the AIRING CUPBOARD / LINEN"),
    ("qr_stop7.png",       "Hide near the OVEN"),
    ("qr_stop8.png",       "Hide near the KITCHEN HOB"),
    ("qr_stop9.png",       "Hide under a SOFA CUSHION"),
    ("qr_stop10.png",      "Hide in / under the BED or BEDROOM"),
    ("qr_certificate.png", "Optional: include with the final prize pile"),
]
for fname, loc in locations:
    print(f"  {fname:<22}  {loc}")
