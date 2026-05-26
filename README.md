# whatsappAuto

A terminal-based AI assistant that can send WhatsApp messages using natural language, powered by **Groq API**, **LLaMA**, and **Selenium**.

## How It Works

You type something like *"Send John a message saying I'll be late"* — the AI interprets your intent and automatically sends the message via WhatsApp Web.

## Features

- Natural language to WhatsApp message — no commands needed
- AI decides whether to send a message or just chat normally
- Persists Chrome session so you don't re-scan the QR code every time
- Falls back to normal conversation when no action is needed

## Requirements

```
groq
python-dotenv
selenium
```

```bash
pip install groq python-dotenv selenium
```

Also requires **Google Chrome** and a matching **ChromeDriver** installed.

## Setup

1. Clone the repo
2. Create a `.env` file:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
3. Run the script — on first launch, a Chrome window will open WhatsApp Web
4. Scan the QR code once; the session is saved locally in `chrome_whatsapp/`

## Usage

```bash
python whatsappAuto.py
```

```
You: Send Sarah a message saying I'm on my way
Done...

You: What's the capital of France?
Bot: Paris.
```

Type `exit` to quit.

## ⚠️ Notes

- Keep the Chrome window open while the script runs
- Contact names must match exactly as they appear in WhatsApp
- Tested on WhatsApp Web — behavior may break if WhatsApp updates their UI
