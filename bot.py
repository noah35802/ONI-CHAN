import discord
import google.generativeai as genai
from discord.ext import commands
from flask import Flask
from threading import Thread

# 🔑 API Keys (hidden for security)
TOKEN = "bot_api"
GEMINI_API_KEY = "gemini_api"

# 🔹 Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# 🔹 Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 🔹 Emoji Dictionary
emoji_dict = {
    "oni": "<:ONICHAN:1353066271989829795>",
    "onichan": "<:ONICHAN:1353066271989829795>",
    "spotify": "<:spotify:1353066234886885508>",
    "hein": "<:hein:1353066175847727226>"
}

# ✅ Bot Ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# 🔹 Auto Reply & Emoji Reactions
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore bot's own messages

    # Emoji reactions
    emoji_dict = {
        "onichan": "<:ONICHAN:1353066271989829795>",
        "music": "<:spotify:1353066234886885508>",
        "hein": "<:hein:1353066175847727226>"
    }
    for word, emoji in emoji_dict.items():
        if word in message.content.lower():
            await message.add_reaction(emoji)

    # AI Response
    try:
        print(f"📩 Received message: {message.content}")
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(message.content)

        if hasattr(response, "text"):
            reply = response.text[:2000]  # Limit to 2000 characters
        else:
            reply = "⚠️ No valid response received."

        print(f"✅ Gemini Response: {reply[:100]}...")
        await message.channel.send(reply)

    except Exception as e:
        print(f"⚠️ Error: {e}")
        await message.channel.send(f"❌ Error: {e}")

    await bot.process_commands(message)  # Ensure other commands still work


# Activity Status
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    activity = discord.Game("Playing with NOAH 🎮")
    await bot.change_presence(status=discord.Status.online, activity=activity)



# 🎭 Emoji Command
@bot.command()
async def emoji(ctx, name: str):
    emoji = emoji_dict.get(name.lower())
    if emoji:
        await ctx.send(emoji)
    else:
        await ctx.send("Emoji not found! 😢")

# 🔹 Flask Server for UptimeRobot
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 🟢 Keep bot alive
keep_alive()

# 🚀 Run Bot
bot.run(TOKEN)
