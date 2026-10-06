# 🔴 Shutdown Program — System Termination Protocol

Ek hacker-style **fullscreen countdown** program jo timer khatam hone par PC ko automatically **shutdown** kar deta hai. Countdown ke dauran poora keyboard aur mouse **lock** ho jata hai — sirf `Ctrl + S` se safely band hota hai.

Python + Tkinter me bana hai. Red neon hacker theme, dot-matrix clock, glowing ring aur background GIF ke saath.

---

## ✨ Features

- **Fullscreen countdown** — dot-matrix clock upar + glowing ring center me.
- **Auto shutdown** — timer `0` hote hi PC band (Windows / Linux / macOS).
- **Full input lock** — countdown ke time keyboard + mouse + touchpad block.
- **Safe exit** — sirf `Ctrl + S` dabane par countdown ruk jata hai (shutdown cancel).
- **Hacker effects** — random hex data, scan lines, glitch blocks.
- **Background GIF** — red tint ke saath (`KAALCHANDRA.gif`).
- **Touchpad OFF** — supported Windows Precision Touchpad hardware level par temporarily disable, exit par wapas ON.

---

## 📦 Requirements

- **Python 3.x**
- **Pillow** (optional, GIF smooth + red tint ke liye):

```bash
pip install pillow
```

> Pillow na ho to program chalega, bs GIF basic mode me dikhegi.

---

## ▶️ How to Run

1. Repo download/clone karo.
2. `KAALCHANDRA.gif` ko same folder me rakho (program ke saath).
3. Terminal me chalao:

```bash
python Shutdown_Program.py
```

---

## ⚙️ Settings (code me upar `CONFIGURATION` section)

| Setting | Kaam | Default |
|---|---|---|
| `TOTAL_SECONDS` | Kitne second ka countdown | `15` |
| `DO_SHUTDOWN` | `False` karo to sirf timer chalega, PC band nahi hoga | `True` |
| `LOCK_ALL_INPUT` | Keyboard/mouse lock ON/OFF | `True` |
| `TOGGLE_PRECISION_TOUCHPAD` | Touchpad hardware OFF karna | `True` |
| `BACKGROUND_GIF` | GIF file ka naam | `KAALCHANDRA.gif` |
| `SHOW_HACKER_EFFECTS` | Hex/glitch effects | `True` |

> **Testing karte waqt** `DO_SHUTDOWN = False` rakho, taaki galti se PC band na ho.

---

## 🛑 Exit Kaise Kare

Countdown ke dauran **`Ctrl + S`** dabao — countdown turant band ho jayega aur shutdown cancel ho jayega.

---

## ⚠️ Warning

- Program chalte hi PC ki saari input lock ho jaati hai.
- Agar `DO_SHUTDOWN = True` hai to timer khatam hone par **PC sach me band ho jayega** — apna kaam pehle save kar lo.
- `Ctrl + Alt + Delete` Windows ka secure shortcut hai, wo block nahi hota (safety ke liye).

---

## 🧩 Platform Support

| OS | Shutdown | Input Lock |
|---|---|---|
| Windows | ✅ | ✅ (full) |
| Linux | ✅ | ⚠️ limited |
| macOS | ✅ | ⚠️ limited |

---

Made with 🔴 by [erenyeager94](https://github.com/erenyeager94)
