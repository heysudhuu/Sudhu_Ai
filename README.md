# Sudhu_Ai
# 🤖 Sudhu Ai – Gemini Powered Telegram Chatbot

**Sudhu Ai** is an intelligent Telegram chatbot built with Python, integrated with the **Gemini 2.0 Flash API** from Google. It acts as a conversational assistant with memory, capable of responding to user queries inside Telegram chats in real-time.

![Sudhu Ai Banner](ChatGPT Image Jul 23, 2025, 09_55_03 PM.png)

---

## 🌟 Features

- 🤖 AI responses powered by Google Gemini
- 📩 Real-time user interaction on Telegram
- 🧠 Contextual chat memory per user session
- 🔒 Secure environment variable handling
- 🪵 Built-in logging for monitoring and debugging

---

## 📦 Project Structure

📁 Sudhu-Ai-Bot
├── index.py # Main bot script
├── .env # Environment variables file (not committed)
├── requirements.txt # Python dependencies
└── README.md # Project documentation (this file)


---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SudhuAi.git
cd SudhuAi
```

**2. Install Dependencies**

```
pip install -r requirements.txt
```
**3. Configure Environment Variables**
Create a .env file in the root directory:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_google_gemini_api_key
```
**4. Run the Bot**
```
python index.py
```
The bot should now be live and listening for user messages via Telegram.


**🧪 Example Usage**
Open Telegram and start a chat with your bot.

Type anything like:
```
/start
Hi Sudhu Ai, what is the capital of Japan?
```
Receive instant AI-powered responses with context memory.

🧠 Tech Stack
Language: Python 3.9+

Bot Framework: python-telegram-bot

AI Engine: Google Gemini API

Async Runtime: asyncio

Security: dotenv + .env configs

🛡️ Security Note
Never expose your API keys in public repos. Use .env files and python-dotenv for safe local development.

**🧑‍💻 Author
Sudhanshu Yadav
📍 Computer Science Engineer | AI & Bots Enthusiast
🔗 GitHub: @heysudhuu
💼 LinkedIn: @heysudhuu**

**📃 License
This project is licensed under the MIT License.
**
“Built by Sudhu, fueled by Gemini – your AI assistant inside Telegram.”

```

---

Let me know if you'd like to auto-generate the `requirements.txt` or want the `preview.png` for LinkedIn/GitHub banners!
```
