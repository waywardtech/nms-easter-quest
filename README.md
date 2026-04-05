# 🌌 No Man's Sky Easter Quest

A QR-code-driven scavenger hunt web game for kids, hosted on a Raspberry Pi and inspired by **No Man's Sky**. Kids scan QR codes hidden around the house to unlock story-driven puzzles, hunt Whispering Eggs, dock at the Space Anomaly, genetically engineer a companion, and cook three real egg recipes — all wrapped in the voice and visual style of the game.

Built by [Dan Gomes / The Far Edge](https://thefaredge.com) for Easter 2026.

---

## ✨ What it is

A 10-waypoint scavenger hunt served from a local Node.js server on a Raspberry Pi. Kids scan QR codes with an iPhone (or any phone), complete on-screen puzzles, decode riddles to find the next location, and collect hidden Easter eggs and treats along the way.

**The full quest arc:**

| # | Location | What happens |
|---|----------|-------------|
| 1 | Fridge | Tap-game — harvest Whispering Eggs, dodge Biological Horrors |
| 2 | Coffee Table | Maths — refine Larval Cores into Nanites |
| 3 | Stairs | Quiz — dock at the Space Anomaly, meet Nada & Polo |
| 4 | Back Door | Feed-game — tame a creature, receive a Companion Egg |
| 5 | Mirror/Bathroom | Egg Sequencer — 4-slot genetic engineering UI |
| 6 | Airing Cupboard | Tap-to-hatch — incubate and hatch your companion |
| 7 | Oven | Real recipe — make scrambled eggs |
| 8 | Kitchen Hob | Real recipe — boiled egg + egg salad sandwich (includes timer) |
| 9 | Sofa | Real recipe — fried egg on toast |
| 10 | Bedroom | Type "ATLAS" — star-burst finale + animated certificate |

Everything is written in plain HTML/CSS/JS. No frameworks. No build step. No npm install. Pure Node.js HTTP server — runs fine on a Raspberry Pi 3.

---

## 🛠 Requirements

- Raspberry Pi (3 or later) running Raspberry Pi OS
- Node.js v14 or higher
- Python 3 + pip (only needed to regenerate QR codes)
- iPhone/Android on the same WiFi network

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/waywardtech/nms-easter-quest.git
cd nms-easter-quest
```

### 2. Find your Raspberry Pi's IP address

```bash
hostname -I
# Example output: 192.168.1.42
```

### 3. Generate QR codes

Install the QR dependencies (one-time):

```bash
pip3 install qrcode[pil] pillow --break-system-packages
```

Edit `generate_qr.py` and change line 16 to your RPi's IP:

```python
RPI_IP = "192.168.1.42"   # ← your actual IP here
```

Then run it:

```bash
python3 generate_qr.py
```

QR codes are saved to `public/qr/`. The script also prints where to hide each one.

### 4. Start the server

```bash
node server.js
```

You should see:
```
NMS Easter Quest running on http://0.0.0.0:3000
```

### 5. Test it

On a phone connected to the same WiFi, open Safari/Chrome and go to:
```
http://192.168.1.42:3000
```

Or using the Pi's hostname:
```
http://raspberrypi.local:3000
```

---

## 🔁 Auto-start on boot (optional)

Find your Node path:
```bash
which node
# or: /home/pi/.nvm/versions/node/v22.22.0/bin/node
```

Add to crontab:
```bash
crontab -e
```

Add this line (adjust paths as needed):
```
@reboot sleep 10 && /home/pi/.nvm/versions/node/v22.22.0/bin/node /home/pi/nms-easter-quest/server.js >> /tmp/quest.log 2>&1 &
```

To check it started:
```bash
cat /tmp/quest.log
```

---

## 🖨 Print sheet

To generate a printable PDF of all 12 QR codes on one A4 page:

```bash
pip3 install reportlab --break-system-packages
python3 generate_print_sheet.py
```

Output: `qr_print_sheet.pdf`

---

## 📁 File structure

```
nms-easter-quest/
├── server.js                  ← Node.js HTTP server
├── generate_qr.py             ← QR code generator
├── generate_print_sheet.py    ← Printable PDF generator
├── public/
│   ├── index.html             ← Start page
│   ├── certificate.html       ← Completion certificate
│   ├── starting-clue.html     ← Printable clue card for the first riddle
│   ├── css/quest.css          ← Shared NMS-style CSS
│   ├── js/quest.js            ← Shared puzzle logic
│   ├── stops/
│   │   ├── stop1.html         ← Waypoint 1: Fridge
│   │   ├── stop2.html         ← Waypoint 2: Coffee Table
│   │   ├── stop3.html         ← Waypoint 3: Stairs
│   │   ├── stop4.html         ← Waypoint 4: Back Door
│   │   ├── stop5.html         ← Waypoint 5: Mirror
│   │   ├── stop6.html         ← Waypoint 6: Airing Cupboard
│   │   ├── stop7.html         ← Waypoint 7: Oven
│   │   ├── stop8.html         ← Waypoint 8: Hob
│   │   ├── stop9.html         ← Waypoint 9: Sofa
│   │   └── stop10.html        ← Waypoint 10: Bedroom
│   └── qr/                    ← Generated QR codes (gitignored — run generate_qr.py)
```

---

## 🎨 Design notes

All artwork is inline SVG — no image files to manage. The NMS aesthetic (dark space background, teal/orange/gold palette, Orbitron font, animated Atlas orb, star fields, scanline effect) is entirely CSS and SVG, keeping the whole thing self-contained and fast on a local network.

The game uses `localStorage` to track puzzle completion across pages, so progress persists through the session.

---

## 🔧 Customisation

**Change the locations** — edit the riddle text at the bottom of each `stop*.html` file.

**Change the number of waypoints** — add or remove stop HTML files and update the `PAGES` list in `generate_qr.py`.

**Change the IP/port** — edit `RPI_IP` in `generate_qr.py` and `PORT` in `server.js`, then regenerate QR codes.

**Change the player name** — search for "Ellis" across the HTML files and replace.

---

## 📄 Licence

MIT — do whatever you like with it. If you build something cool from this, I'd love to hear about it.

---

## 🙏 Credits

CSS Built with [Claude](https://claude.ai) by Dan Gomes. Inspired by Hello Games' extraordinary No Man's Sky. No affiliation with Hello Games.
