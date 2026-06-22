"""
AUTO-MODERATION COG
Anti-spam, Anti-link, Anti-invite, Anti-caps, Bad word filter
"""
import discord
from discord.ext import commands
import re
import time
from collections import defaultdict
from utils.embeds import *

DEFAULT_BAD_WORDS = ["badword1", "badword2"]  # admin can add more
INVITE_REGEX = re.compile(r"(?:https?://)?(?:www\.)?(?:discord(?:\.com|app\.com|\.gg)|invite)/(?:\#/)?(\S+)", re.IGNORECASE)
LINK_REGEX = re.compile(r"https?://\S+", re.IGNORECASE)

class AutoMod(commands.Cog):
    """🛡️ Auto-Moderation"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.spam_tracker = defaultdict(list)
        self.mention_tracker = defaultdict(list)
    
    def get_settings(self, guild_id):
        return self.db.get_guild("automod", guild_id)
    
    # ===== Anti-Spam Toggle =====
    @commands.command(name="antispam")
    @commands.has_permissions(manage_guild=True)
    async def antispam(self, ctx):
        s = self.get_settings(ctx.guild.id)
        new = not s.get("antispam", False)
        self.db.set_guild("automod", ctx.guild.id, "antispam", new)
        await ctx.send(embed=success_embed("Anti-Spam", f"Status: **{'ON' if new else 'OFF'}**"))
    
    # ===== Anti-Link =====
    @commands.command(name="antilink")
    @commands.has_permissions(manage_guild=True)
    async def antilink(self, ctx):
        s = self.get_settings(ctx.guild.id)
        new = not s.get("antilink", False)
        self.db.set_guild("automod", ctx.guild.id, "antilink", new)
        await ctx.send(embed=success_embed("Anti-Link", f"Status: **{'ON' if new else 'OFF'}**"))
    
    # ===== Anti-Invite =====
    @commands.command(name="antiinvite")
    @commands.has_permissions(manage_guild=True)
    async def antiinvite(self, ctx):
        s = self.get_settings(ctx.guild.id)
        new = not s.get("antiinvite", False)
        self.db.set_guild("automod", ctx.guild.id, "antiinvite", new)
        await ctx.send(embed=success_embed("Anti-Invite", f"Status: **{'ON' if new else 'OFF'}**"))
    
    # ===== Anti-Caps =====
    @commands.command(name="anticaps")
    @commands.has_permissions(manage_guild=True)
    async def anticaps(self, ctx):
        s = self.get_settings(ctx.guild.id)
        new = not s.get("anticaps", False)
        self.db.set_guild("automod", ctx.guild.id, "anticaps", new)
        await ctx.send(embed=success_embed("Anti-Caps", f"Status: **{'ON' if new else 'OFF'}**"))
    
    # ===== Anti-Mention Spam =====
    @commands.command(name="antimention")
    @commands.has_permissions(manage_guild=True)
    async def antimention(self, ctx):
        s = self.get_settings(ctx.guild.id)
        new = not s.get("antimention", False)
        self.db.set_guild("automod", ctx.guild.id, "antimention", new)
        await ctx.send(embed=success_embed("Anti-Mention", f"Status: **{'ON' if new else 'OFF'}**"))
    
    # ===== Add Bad Word =====
    @commands.command(name="addbadword")
    @commands.has_permissions(manage_guild=True)
    async def addbadword(self, ctx, *, word: str):
        s = self.get_settings(ctx.guild.id)
        words = s.get("badwords", [])
        word = word.lower()
        if word not in words:
            words.append(word)
            self.db.set_guild("automod", ctx.guild.id, "badwords", words)
            await ctx.send(embed=success_embed("Bad Word Ditambah", f"||{word}|| ditambahkan ke filter"))
        else:
            await ctx.send(embed=warning_embed("Sudah Ada", "Kata sudah dalam filter"))
    
    # ===== Remove Bad Word =====
    @commands.command(name="removebadword")
    @commands.has_permissions(manage_guild=True)
    async def removebadword(self, ctx, *, word: str):
        s = self.get_settings(ctx.guild.id)
        words = s.get("badwords", [])
        if word.lower() in words:
            words.remove(word.lower())
            self.db.set_guild("automod", ctx.guild.id, "badwords", words)
            await ctx.send(embed=success_embed("Bad Word Dihapus", f"||{word}|| dihapus"))
        else:
            await ctx.send(embed=info_embed("Tidak Ada", "Kata tidak dalam filter"))
    
    # ===== AutoMod Status =====
    @commands.hybrid_command(name="automod", description="Lihat status auto-mod")
    @commands.has_permissions(manage_guild=True)
    async def automod_status(self, ctx):
        s = self.get_settings(ctx.guild.id)
        embed = info_embed("🛡️ Auto-Mod Status")
        embed.add_field(name="Anti-Spam", value="✅ ON" if s.get("antispam") else "❌ OFF", inline=True)
        embed.add_field(name="Anti-Link", value="✅ ON" if s.get("antilink") else "❌ OFF", inline=True)
        embed.add_field(name="Anti-Invite", value="✅ ON" if s.get("antiinvite") else "❌ OFF", inline=True)
        embed.add_field(name="Anti-Caps", value="✅ ON" if s.get("anticaps") else "❌ OFF", inline=True)
        embed.add_field(name="Anti-Mention", value="✅ ON" if s.get("antimention") else "❌ OFF", inline=True)
        embed.add_field(name="Bad Words", value=f"{len(s.get('badwords', []))} filtered", inline=True)
        await ctx.send(embed=embed)
    
    # ===== Message Listener =====
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        if message.author.guild_permissions.manage_messages:
            return  # mods are immune
        
        s = self.get_settings(message.guild.id)
        if not any([s.get("antispam"), s.get("antilink"), s.get("antiinvite"), 
                    s.get("anticaps"), s.get("antimention"), s.get("badwords")]):
            return
        
        # === Anti-Spam ===
        if s.get("antispam"):
            user_id = message.author.id
            now = time.time()
            self.spam_tracker[user_id] = [t for t in self.spam_tracker[user_id] if now - t < 5]
            self.spam_tracker[user_id].append(now)
            if len(self.spam_tracker[user_id]) > 5:
                try:
                    await message.delete()
                    await message.channel.send(
                        embed=warning_embed("🚫 Anti-Spam", f"{message.author.mention} berhenti spam!"),
                        delete_after=5
                    )
                except:
                    pass
                return
        
        # === Anti-Invite ===
        if s.get("antiinvite") and INVITE_REGEX.search(message.content):
            try:
                await message.delete()
                await message.channel.send(
                    embed=warning_embed("🚫 Anti-Invite", f"{message.author.mention} tidak boleh share Discord invite!"),
                    delete_after=5
                )
                return
            except:
                pass
        
        # === Anti-Link ===
        if s.get("antilink") and LINK_REGEX.search(message.content):
            try:
                await message.delete()
                await message.channel.send(
                    embed=warning_embed("🚫 Anti-Link", f"{message.author.mention} link tidak diizinkan!"),
                    delete_after=5
                )
                return
            except:
                pass
        
        # === Anti-Caps ===
        if s.get("anticaps") and len(message.content) > 10:
            caps = sum(1 for c in message.content if c.isupper())
            if caps / len(message.content) > 0.7:
                try:
                    await message.delete()
                    await message.channel.send(
                        embed=warning_embed("🚫 Anti-Caps", f"{message.author.mention} jangan caps lock!"),
                        delete_after=5
                    )
                    return
                except:
                    pass
        
        # === Anti-Mention Spam ===
        if s.get("antimention") and len(message.mentions) > 5:
            try:
                await message.delete()
                await message.channel.send(
                    embed=warning_embed("🚫 Anti-Mention", f"{message.author.mention} terlalu banyak mention!"),
                    delete_after=5
                )
                return
            except:
                pass
        
        # === Bad Words ===
        badwords = s.get("badwords", [])
        if badwords:
            lower = message.content.lower()
            for word in badwords:
                if word in lower:
                    try:
                        await message.delete()
                        await message.channel.send(
                            embed=warning_embed("🚫 Bad Word", f"{message.author.mention} jaga ucapanmu!"),
                            delete_after=5
                        )
                        return
                    except:
                        pass

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
