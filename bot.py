import discord
import google.generativeai as genai
from discord.ext import commands

TOKEN = "discord_api"
GEMINI_API_KEY = "gemini_api"


genai.configure(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        print(f"📩 Received message: {message.content}")

        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(message.content)

        if hasattr(response, "text"):
            reply = response.text[:2000]
        else:
            reply = "⚠️ No valid response received."

        print(f"✅ Gemini Response: {reply[:100]}...")
        await message.channel.send(reply)

    except Exception as e:
        await message.channel.send(f"❌ Error: {e}")
        print(f"⚠️ Error: {e}")

emoji_dict = {
    "oni": "<:ONICHAN:1353066271989829795>",
    "onichan": "<:ONICHAN:1353066271989829795>",
    "spotify": "<:spotify:1353066234886885508>",
    "hein": "<:hein:1353066175847727226>"
}

@bot.command()
async def emoji(ctx, name: str):
    emoji = emoji_dict.get(name.lower())  # Convert input to lowercase for flexibility
    if emoji:
        await ctx.send(f"{emoji}")
    else:
        await ctx.send("Emoji not found! 😢")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    emoji_dict = {
        "onichan": "<:ONICHAN:1353066271989829795>",
        "music": "<:spotify:1353066234886885508>",
        "hein": "<:hein:1353066175847727226>"
    }

    for word, emoji in emoji_dict.items():
        if word in message.content.lower():
            await message.add_reaction(emoji)

    await bot.process_commands(message)




from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()


bot.run(TOKEN)
