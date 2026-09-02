import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import google.generativeai as genai
from pyrogram import Client, filters

# Render Web Service ke liye dummy HTTP server (port bind karne ke liye)
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Server ko background thread me start kar rahe hain
threading.Thread(target=run_server, daemon=True).start()

# Render Environment Variables se credentials
API_ID = int(os.getenv("API_ID", "36055068"))
API_HASH = os.getenv("API_HASH", "e62c399663de4721efb786f7cfc64022")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Telegram Bot Setup
app = Client(
    "gemini_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.text & ~filters.forwarded)
async def chat_with_gemini(client, message):
    user_text = message.text
    try:
        response = model.generate_content(user_text)
        await message.reply_text(response.text)
    except Exception as e:
        await message.reply_text(f"Arre bhai error aa gaya: {e}")

if name == "main":
    print("Bot Web Service par live ho raha hai...")
    app.run()
