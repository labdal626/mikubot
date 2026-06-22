"""
ECONOMY SYSTEM - Bonus features
Balance, Daily, Weekly, Work, Rob, Leaderboard
"""
import discord
from discord.ext import commands
import random
from datetime import datetime, timedelta
from utils.embeds import *

class Economy(commands.Cog):
    """💰 Economy system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    def get_user(self, guild_id, user_id):
        data = self.db.get_user("economy", guild_id, user_id)
        if "balance" not in data:
            data["balance"] = 0
            self.db.set_user("economy", guild_id, user_id, "balance", 0)
        return data
    
    def add_money(self, guild_id, user_id, amount):
        data = self.get_user(guild_id, user_id)
        new_bal = data.get("balance", 0) + amount
        self.db.set_user("economy", guild_id, user_id, "balance", new_bal)
        return new_bal
    
    @commands.hybrid_command(name="balance", description="Cek saldo coin kamu")
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        data = self.get_user(ctx.guild.id, member.id)
        embed = miku_embed(f"💰 Balance - {member.display_name}", f"**Saldo:** {data.get('balance', 0):,} 🪙")
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="daily", description="Klaim daily reward (100-500 coin)")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        amount = random.randint(100, 500)
        new_bal = self.add_money(ctx.guild.id, ctx.author.id, amount)
        embed = success_embed("🎁 Daily Reward Claimed!", f"Kamu dapat **{amount}** 🪙\nSaldo: **{new_bal:,}** 🪙")
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="weekly", description="Klaim weekly reward (1000-5000 coin)")
    @commands.cooldown(1, 604800, commands.BucketType.user)
    async def weekly(self, ctx):
        amount = random.randint(1000, 5000)
        new_bal = self.add_money(ctx.guild.id, ctx.author.id, amount)
        embed = success_embed("🎁 Weekly Reward!", f"Kamu dapat **{amount}** 🪙\nSaldo: **{new_bal:,}** 🪙")
        await ctx.send(embed=embed)
    
    @commands.command(name="give")
    async def give(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            return await ctx.send(embed=error_embed("Gagal", "Amount harus positif"))
        if member == ctx.author:
            return await ctx.send(embed=error_embed("Gagal", "Tidak bisa kirim ke diri sendiri"))
        if member.bot:
            return await ctx.send(embed=error_embed("Gagal", "Tidak bisa kirim ke bot"))
        
        sender = self.get_user(ctx.guild.id, ctx.author.id)
        if sender.get("balance", 0) < amount:
            return await ctx.send(embed=error_embed("Saldo Kurang", f"Saldo: {sender.get('balance', 0):,} 🪙"))
        
        self.add_money(ctx.guild.id, ctx.author.id, -amount)
        self.add_money(ctx.guild.id, member.id, amount)
        await ctx.send(embed=success_embed("Transfer Berhasil", f"💸 {ctx.author.mention} → {member.mention}: **{amount:,}** 🪙"))
    
    @commands.hybrid_command(name="work", description="Kerja dapat coin (cooldown 1 jam)")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        jobs = [
            ("👨‍💻 Programmer", 200, 800),
            ("🧹 Cleaning", 50, 200),
            ("🍕 Delivery", 100, 400),
            ("🎨 Designer", 150, 600),
            ("🎵 Musisi", 100, 500),
            ("📝 Writer", 150, 500),
            ("🚗 Driver", 80, 300),
            ("👨‍🍳 Chef", 120, 450)
        ]
        job, low, high = random.choice(jobs)
        earned = random.randint(low, high)
        new_bal = self.add_money(ctx.guild.id, ctx.author.id, earned)
        embed = success_embed(f"💼 Kerja Selesai!", f"**Job:** {job}\n**Earned:** {earned:,} 🪙\n**Saldo:** {new_bal:,} 🪙")
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="leaderboard", description="Top 10 richest member")
    async def leaderboard(self, ctx):
        data = self.db.load("economy", {})
        gid = str(ctx.guild.id)
        if gid not in data:
            return await ctx.send(embed=info_embed("Kosong", "Belum ada data ekonomi"))
        
        users = []
        for uid, udata in data[gid].items():
            bal = udata.get("balance", 0)
            if bal > 0:
                member = ctx.guild.get_member(int(uid))
                if member:
                    users.append((member, bal))
        
        users.sort(key=lambda x: x[1], reverse=True)
        users = users[:10]
        
        if not users:
            return await ctx.send(embed=info_embed("Kosong", "Belum ada saldo"))
        
        text = ""
        medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
        for i, (m, b) in enumerate(users):
            text += f"{medals[i]} **{m.display_name}** - {b:,} 🪙\n"
        
        embed = miku_embed("🏆 Richest Leaderboard", text)
        await ctx.send(embed=embed)
    
    @commands.command(name="rob")
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member):
        if member == ctx.author or member.bot:
            return await ctx.send(embed=error_embed("Gagal", "Target tidak valid"))
        
        target = self.get_user(ctx.guild.id, member.id)
        sender = self.get_user(ctx.guild.id, ctx.author.id)
        
        if target.get("balance", 0) < 100:
            return await ctx.send(embed=error_embed("Gagal", f"{member.mention} terlalu miskin (<100)"))
        if sender.get("balance", 0) < 100:
            return await ctx.send(embed=error_embed("Gagal", "Saldo kamu kurang (min 100 untuk rob)"))
        
        if random.random() < 0.5:  # Success
            stolen = random.randint(50, min(target["balance"], 1000))
            self.add_money(ctx.guild.id, member.id, -stolen)
            self.add_money(ctx.guild.id, ctx.author.id, stolen)
            embed = success_embed("🦹 Rob Berhasil!", f"Kamu mencuri **{stolen:,}** 🪙 dari {member.mention}")
        else:  # Fail
            fine = random.randint(50, 200)
            self.add_money(ctx.guild.id, ctx.author.id, -fine)
            embed = error_embed("🚓 Ketangkep Polisi!", f"Kamu kena denda **{fine}** 🪙")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
