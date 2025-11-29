# Discord Bot

This project is a Discord bot developed in Python (`discord.py`).  
The bot enhances server experience with welcome messages, music playback, games, and interactive commands.

---

## Features

- **Welcome System:** Sends an embed message when a new member joins.  
- **Message Listener:** Responds to specific messages (e.g., `"merhaba"`).  
- **Music System (Lavalink):**  
  - `/join` – Connects the bot to a voice channel  
  - `/play` – Plays a song from YouTube and adds it to the playlist  
- **Game Commands:**  
  - `/gtn` – Guess-the-number mini-game  
- **Interactive Commands:**  
  - `/hello` – Sends a greeting  
- **Logging:** Bot activity is saved in `discord.log`.  
- **Secure Configuration:** `.env` file stores bot token and sensitive data.

---

## Requirements

- Python 3.10+  
- `discord.py` (Pycord)  
- `lavalink`  
- `python-dotenv`

You can install dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```
---

## Clone the Repository

```bash
git clone https://github.com/<CreaThor01>/<Discord-Bot-Project>.git
cd <Discord-Bot-Project>
```
---

## Create a .env File

```ini
TOKEN=your_bot_token_here
```
