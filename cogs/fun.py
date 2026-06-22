"""
FUN COG - Features 66-80
Games, Random, Polls, Giveaway, etc.
"""
import discord
from discord.ext import commands
import random
import asyncio
from utils.embeds import *

class Fun(commands.Cog):
    """🎮 Fun commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    # ===== Feature 66: 8Ball =====
    @commands.hybrid_command(name="8ball", description="Tanya bola ajaib")
    async def eightball(self, ctx, *, question: str):
        answers = [
            "✅ Iya, pasti!", "✅ Tentu saja!", "✅ Sudah dipastikan!",
            "🤔 Mungkin...", "🤔 Coba tanya lagi nanti", "🤔 Tidak yakin",
            "❌ Tidak", "❌ Lupakan saja", "❌ Tidak mungkin",
            "✨ Yang penting jangan menyerah!", "💖 Hatsune Miku setuju!", "🎵 Mikuuuu~"
        ]
        embed = miku_embed("🎱 Magic 8Ball")
        embed.add_field(name="❓ Pertanyaan", value=question, inline=False)
        embed.add_field(name="💬 Jawaban", value=random.choice(answers), inline=False)
        await ctx.send(embed=embed)
    
    # ===== Feature 67: Coinflip =====
    @commands.hybrid_command(name="coinflip", description="Lempar koin")
    async def coinflip(self, ctx):
        result = random.choice(["Heads 👑", "Tails 🪙"])
        embed = miku_embed(f"{EMOJIS['coin']} Coinflip", f"Hasil: **{result}**")
        await ctx.send(embed=embed)
    
    # ===== Feature 68: Dice Roll =====
    @commands.hybrid_command(name="dice", description="Roll dadu (sides default 6)")
    async def dice(self, ctx, sides: int = 6):
        if sides < 2 or sides > 1000:
            return await ctx.send(embed=error_embed("Gagal", "Sisi dadu: 2-1000"))
        result = random.randint(1, sides)
        embed = miku_embed(f"{EMOJIS['dice']} Dice Roll", f"🎲 Dadu {sides}-sisi: **{result}**")
        await ctx.send(embed=embed)
    
    # ===== Feature 69: Random Number =====
    @commands.hybrid_command(name="random", description="Random number")
    async def random_num(self, ctx, low: int = 1, high: int = 100):
        if low >= high:
            return await ctx.send(embed=error_embed("Gagal", "Low harus lebih kecil dari high"))
        embed = miku_embed("🎲 Random Number", f"Hasil: **{random.randint(low, high)}**\nRange: {low}-{high}")
        await ctx.send(embed=embed)
    
    # ===== Feature 70: Choose =====
    @commands.hybrid_command(name="choose", description="Pilih random dari opsi (pisah dengan |)")
    async def choose(self, ctx, *, options: str):
        opts = [o.strip() for o in options.split("|") if o.strip()]
        if len(opts) < 2:
            return await ctx.send(embed=error_embed("Gagal", "Minimal 2 opsi dipisah `|`"))
        embed = miku_embed("🎯 Pilihan", f"Aku pilih: **{random.choice(opts)}**\nDari: {', '.join(opts)}")
        await ctx.send(embed=embed)
    
    # ===== Feature 71: Quote =====
    @commands.hybrid_command(name="quote", description="Quote random")
    async def quote(self, ctx):
        quotes = [
            ("Hidup itu seperti coding, kadang error tapi tetap dijalanin.", "Anonim"),
            ("Jangan tunggu sempurna, mulai dulu.", "Productivity"),
            ("Setiap hari adalah lembar baru.", "Wise"),
            ("Tidur cukup, kode lancar.", "Programmer"),
            ("Kesabaran adalah kunci sukses.", "Bijak"),
            ("Senyumlah, dunia akan lebih indah.", "Miku"),
            ("Bug itu bukan musuh, tapi guru.", "Senior Dev"),
            ("Mimpi besar, kerja keras.", "Sukses")
        ]
        q, a = random.choice(quotes)
        embed = miku_embed("💭 Quote of the Moment")
        embed.add_field(name="Quote", value=f"*\"{q}\"*", inline=False)
        embed.add_field(name="— Author", value=a, inline=False)
        await ctx.send(embed=embed)
    
    # ===== Feature 72: Joke =====
    @commands.hybrid_command(name="joke", description="Joke random")
    async def joke(self, ctx):
        jokes = [
            "Kenapa programmer suka kopi? Karena tanpa Java, semua nge-hang!",
            "Programmer punya 2 masalah: cache invalidation, naming things, dan off-by-one errors.",
            "Kenapa Python disebut bahasa pemula? Karena tidak ada {  } yang bikin pusing!",
            "Apa bedanya bug dan fitur? Tergantung yang ditanya developer atau client.",
            "Programmer paling jago olahraga apa? Drag-and-drop!",
            "Apa makanan favorit bot? Token... segar dari Discord Developer Portal!",
            "Kenapa bot Discord males ke gym? Karena udah cukup capek di-run 24/7!"
        ]
        embed = miku_embed("😂 Joke", random.choice(jokes))
        await ctx.send(embed=embed)
    
    # ===== Feature 73: Rock Paper Scissors =====
    @commands.hybrid_command(name="rps", description="Rock Paper Scissors")
    async def rps(self, ctx, choice: str):
        choices = {"rock": "✊", "paper": "✋", "scissors": "✌️"}
        c = choice.lower()
        if c not in choices:
            return await ctx.send(embed=error_embed("Gagal", "Pilih: rock, paper, atau scissors"))
        
        bot_choice = random.choice(list(choices.keys()))
        if c == bot_choice:
            result = "🤝 Seri!"
        elif (c == "rock" and bot_choice == "scissors") or \
             (c == "paper" and bot_choice == "rock") or \
             (c == "scissors" and bot_choice == "paper"):
            result = "🎉 Kamu MENANG!"
        else:
            result = "😢 Kamu KALAH!"
        
        embed = miku_embed("✊✋✌️ Rock Paper Scissors")
        embed.add_field(name="👤 Kamu", value=f"{choices[c]} {c.title()}", inline=True)
        embed.add_field(name="🤖 Bot", value=f"{choices[bot_choice]} {bot_choice.title()}", inline=True)
        embed.add_field(name="Result", value=result, inline=False)
        await ctx.send(embed=embed)
    
    # ===== Feature 74: Trivia =====
    @commands.hybrid_command(name="trivia", description="Mini quiz trivia")
    async def trivia(self, ctx):
        questions = [
            {"q": "Apa siapakah Hatsune Miku?", "a": ["vocaloid", "miku"], "options": "A) Robot, B) Vocaloid, C) Penyanyi Real, D) Game"},
            {"q": "Bahasa pemrograman yang dipakai bot ini?", "a": ["python"], "options": "A) Java, B) Python, C) JavaScript, D) C++"},
            {"q": "Berapa warna pelangi?", "a": ["7", "tujuh", "seven"], "options": "A) 5, B) 6, C) 7, D) 8"},
            {"q": "Planet terbesar di tata surya?", "a": ["jupiter"], "options": "A) Bumi, B) Mars, C) Jupiter, D) Saturnus"},
            {"q": "Tahun berapa Discord dibuat?", "a": ["2015"], "options": "A) 2013, B) 2014, C) 2015, D) 2016"}
        ]
        q = random.choice(questions)
        embed = miku_embed("🧠 Trivia Time!", f"**Pertanyaan:** {q['q']}\n\n{q['options']}\n\n*Reply dengan jawabanmu dalam 30 detik!*")
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            msg = await self.bot.wait_for("message", timeout=30, check=check)
            if any(ans in msg.content.lower() for ans in q["a"]):
                await ctx.send(embed=success_embed("🎉 BENAR!", f"Jawaban: **{q['a'][0]}**"))
            else:
                await ctx.send(embed=error_embed("😢 Salah!", f"Jawaban: **{q['a'][0]}**"))
        except asyncio.TimeoutError:
            await ctx.send(embed=warning_embed("⏰ Waktu Habis", f"Jawaban: **{q['a'][0]}**"))
    
    # ===== Feature 75: Poll =====
    @commands.hybrid_command(name="poll", description="Buat poll (pisah opsi dengan |)")
    async def poll(self, ctx, *, args: str):
        parts = args.split("|")
        if len(parts) < 2:
            return await ctx.send(embed=error_embed("Format", "Format: `pertanyaan | opsi1 | opsi2 ...`"))
        
        question = parts[0].strip()
        options = [p.strip() for p in parts[1:6]]
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
        
        desc = "\n\n".join([f"{emojis[i]} {opt}" for i, opt in enumerate(options)])
        embed = miku_embed(f"📊 Poll", f"**{question}**\n\n{desc}")
        embed.set_footer(text=f"Poll oleh {ctx.author}")
        
        msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await msg.add_reaction(emojis[i])
    
    # ===== Feature 76: Coinflip Animation =====
    @commands.hybrid_command(name="flip", description="Coinflip dengan animasi")
    async def flip(self, ctx):
        msg = await ctx.send(embed=loading_embed("🪙 Flipping coin..."))
        for i in range(3):
            await asyncio.sleep(0.7)
            await msg.edit(embed=loading_embed(f"🪙 {'Flip' * (i+1)}..."))
        await asyncio.sleep(0.7)
        result = random.choice(["Heads 👑", "Tails 🪙"])
        await msg.edit(embed=success_embed("Hasil Coinflip", f"🪙 **{result}**"))
    
    # ===== Feature 77: Say =====
    @commands.command(name="say")
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, message: str):
        try:
            if not ctx.interaction:
                await ctx.message.delete()
        except:
            pass
        await ctx.send(message)
    
    # ===== Feature 78: Embed Say =====
    @commands.command(name="embedsay")
    @commands.has_permissions(manage_messages=True)
    async def embedsay(self, ctx, *, message: str):
        try:
            if not ctx.interaction:
                await ctx.message.delete()
        except:
            pass
        embed = miku_embed("📢 Pengumuman", message)
        embed.set_footer(text=f"Diumumkan oleh {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)
    
    # ===== Feature 79: Reverse Text =====
    @commands.command(name="reverse")
    async def reverse(self, ctx, *, text: str):
        embed = miku_embed("🔄 Reversed", text[::-1])
        await ctx.send(embed=embed)
    
    # ===== Feature 80: Number Game =====
    @commands.hybrid_command(name="numbergame", description="Tebak angka 1-100")
    async def numbergame(self, ctx):
        number = random.randint(1, 100)
        await ctx.send(embed=miku_embed("🎯 Tebak Angka!", "Aku pilih angka 1-100. Coba tebak! (10 attempts)"))
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
        
        for attempt in range(1, 11):
            try:
                msg = await self.bot.wait_for("message", timeout=30, check=check)
                guess = int(msg.content)
                if guess == number:
                    return await ctx.send(embed=success_embed(f"🎉 BENAR!", f"Kamu menebak dalam **{attempt}** percobaan! Angkanya **{number}**"))
                elif guess < number:
                    await ctx.send(embed=info_embed(f"📈 Lebih Tinggi", f"Attempt {attempt}/10"))
                else:
                    await ctx.send(embed=info_embed(f"📉 Lebih Rendah", f"Attempt {attempt}/10"))
            except asyncio.TimeoutError:
                return await ctx.send(embed=warning_embed("⏰ Timeout", f"Angkanya **{number}**"))
        await ctx.send(embed=error_embed("😢 Game Over", f"Habis percobaan! Angkanya **{number}**"))

async def setup(bot):
    await bot.add_cog(Fun(bot))
