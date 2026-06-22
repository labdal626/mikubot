"""
GIVEAWAY SYSTEM
Create, end, reroll giveaways
"""
import discord
from discord.ext import commands, tasks
import random
import asyncio
from datetime import datetime, timedelta
from utils.embeds import *

class Giveaway(commands.Cog):
    """🎉 Giveaway system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.check_giveaways.start()
    
    def cog_unload(self):
        self.check_giveaways.cancel()
    
    @commands.hybrid_command(name="giveaway", description="Buat giveaway (durasi dalam menit)")
    @commands.has_permissions(manage_messages=True)
    async def giveaway(self, ctx, duration: int, winners: int, *, prize: str):
        if duration < 1 or duration > 10080:
            return await ctx.send(embed=error_embed("Gagal", "Durasi: 1 menit - 1 minggu"))
        if winners < 1 or winners > 20:
            return await ctx.send(embed=error_embed("Gagal", "Winners: 1-20"))
        
        end_time = datetime.utcnow() + timedelta(minutes=duration)
        embed = miku_embed(f"🎉 GIVEAWAY 🎉", f"**Prize:** {prize}")
        embed.add_field(name="🏆 Winners", value=str(winners), inline=True)
        embed.add_field(name="⏰ Berakhir", value=f"<t:{int(end_time.timestamp())}:R>", inline=True)
        embed.add_field(name="👤 Host", value=ctx.author.mention, inline=True)
        embed.add_field(name="📝 Cara Ikut", value="React dengan 🎉 untuk join!", inline=False)
        embed.set_footer(text=f"Giveaway berakhir")
        embed.timestamp = end_time
        
        if ctx.interaction:
            await ctx.interaction.response.send_message("✅ Giveaway dimulai", ephemeral=True)
            msg = await ctx.channel.send(embed=embed)
        else:
            msg = await ctx.send(embed=embed)
        
        await msg.add_reaction("🎉")
        
        giveaways = self.db.load("giveaways", {})
        giveaways[str(msg.id)] = {
            "channel_id": ctx.channel.id,
            "guild_id": ctx.guild.id,
            "prize": prize,
            "winners": winners,
            "end_time": end_time.isoformat(),
            "host": ctx.author.id,
            "ended": False
        }
        self.db.save("giveaways", giveaways)
    
    @tasks.loop(seconds=20)
    async def check_giveaways(self):
        giveaways = self.db.load("giveaways", {})
        changed = False
        
        for msg_id, data in list(giveaways.items()):
            if data.get("ended"):
                continue
            
            end_time = datetime.fromisoformat(data["end_time"])
            if datetime.utcnow() >= end_time:
                try:
                    ch = self.bot.get_channel(data["channel_id"])
                    if not ch:
                        continue
                    msg = await ch.fetch_message(int(msg_id))
                    
                    reaction = discord.utils.get(msg.reactions, emoji="🎉")
                    if not reaction:
                        await ch.send(embed=error_embed("Giveaway Selesai", "Tidak ada peserta"))
                        data["ended"] = True
                        changed = True
                        continue
                    
                    users = [u async for u in reaction.users() if not u.bot]
                    if not users:
                        await ch.send(embed=error_embed("Giveaway Selesai", "Tidak ada peserta"))
                    else:
                        winners_count = min(data["winners"], len(users))
                        winners = random.sample(users, winners_count)
                        winner_mentions = ", ".join([w.mention for w in winners])
                        
                        embed = miku_embed("🎉 GIVEAWAY ENDED 🎉")
                        embed.add_field(name="🎁 Prize", value=data["prize"], inline=False)
                        embed.add_field(name="🏆 Winners", value=winner_mentions, inline=False)
                        await ch.send(content=f"Selamat {winner_mentions}!", embed=embed)
                    
                    data["ended"] = True
                    changed = True
                except Exception as e:
                    print(f"Giveaway error: {e}")
                    data["ended"] = True
                    changed = True
        
        if changed:
            self.db.save("giveaways", giveaways)
    
    @check_giveaways.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()
    
    @commands.hybrid_command(name="reroll", description="Reroll giveaway (paste message ID)")
    @commands.has_permissions(manage_messages=True)
    async def reroll(self, ctx, message_id: str):
        try:
            msg = await ctx.channel.fetch_message(int(message_id))
            reaction = discord.utils.get(msg.reactions, emoji="🎉")
            if not reaction:
                return await ctx.send(embed=error_embed("Gagal", "Pesan bukan giveaway"))
            
            users = [u async for u in reaction.users() if not u.bot]
            if not users:
                return await ctx.send(embed=error_embed("Gagal", "Tidak ada peserta"))
            
            winner = random.choice(users)
            embed = miku_embed("🎲 REROLL!", f"Winner baru: {winner.mention} 🎉")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
