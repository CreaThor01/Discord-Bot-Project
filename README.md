# Discord Bot

This repository contains a Discord bot developed using Python (`discord.py`).  
The bot features automated greetings, interactive commands, polls, and logging, designed for server engagement and moderation.

---

## Features

- **Welcome System:** Sends an embed message when a new member joins the server.  
- **Message Listener:** Responds to specific messages (e.g., `"merhaba"`).  
- **Interactive Commands:**  
  - `/gtn` – Guess-the-number mini-game  
  - `/poll` – Creates a reaction-based poll  
  - `/hello` – Sends a simple greeting  
- **Logging:** Captures detailed bot activity in `discord.log`.  
- **Secure Configuration:** Uses `.env` for sensitive data like bot token.  

---

## Architecture

- **Bot Framework:** discord.py (Pycord)  
- **Configuration:** `.env` environment file  
- **Logging:** Python `logging` module  
- **Command Handling:** Bot commands with `@bot.command` and `@bot.event`  

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/<CreaThor01>/<Discord-Bot-Project>.git
cd <Discord-Bot-Project>
