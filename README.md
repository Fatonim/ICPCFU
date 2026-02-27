# 🎮 ICPCFU – Codeforces Gamified Telegram Bot

A Telegram bot that gamifies competitive programming practice on Codeforces.

Built in 2023 using Python, aiogram, and SQLite.

---

## 🚀 Features

- Registration via Codeforces nickname
- Random problem generator (800–3500 difficulty)
- Automatic submission verification
- In-game economy (coins)
- Experience and leveling system
- Temporary EXP multipliers (shop system)
- Leaderboard ranking
- Persistent user data storage

---

## 🧠 Game Mechanics

- Coins formula: `4 * difficulty + 1`
- EXP formula: `2 * difficulty + 1`
- Level requirement: `level * (level - 1) + 2`
- Bonus multipliers up to x4.2
- Time-limited bonuses (15 min – 12 hours)

---

## 🏗 Architecture

- **Telegram Framework:** aiogram (v2)
- **Database:** SQLite3 (file-based)
- **Web Scraping:** requests + BeautifulSoup
- **Data Storage:** custom SQLite abstraction layer (`db.py`)
- **Game Logic:** separated into utility module (`func.py`)

---

## 📂 Project Structure

```
ICPCFU/
├── bot.py              # Main Telegram bot logic
├── func.py             # Game logic & Codeforces parsing
├── db.py               # SQLite database abstraction
├── config.py           # Environment configuration
├── requirements.txt
├── README.md
└── database/           # SQLite database file (not tracked)
```

---

## ⚙️ Installation

1. Clone repository:

```
git clone https://github.com/Fatonim/ICPCFU.git
cd ICPCFU
```

2. Create virtual environment:

```
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Set Bot Token to your telegram bot token.

5. Run bot:

```
python bot.py
```

---

## 📊 Commands

- `/reg <nickname>` – Register Codeforces account
- `/get <difficulty>` – Get random problem
- `/check <submission_link>` – Validate solution
- `/profile` – View level and stats
- `/shop` – View bonus shop
- `/buy <bonus_name>` – Purchase EXP multiplier
- `/leaders` – View leaderboard
- `/help` – Command overview

---

Developed by fatonims (2023)
