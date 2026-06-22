"""
UTILITY COG - Features 91-100
Ping, Uptime, Bot info, Suggestion, Reminder, etc.
"""
import discord
from discord.ext import commands
import time
import asyncio
import platform
import psutil
from datetime import datetime, timedelta
from utils.embeds import *

class Utility(commands.Cog):
    """🔧 Utility commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    # ===== Feature 91: Ping =====
    @commands.hybrid_command(name="ping", description="Cek ping bot")
    async def ping(self, ctx):
        start = time.time()
        msg = await ctx.send(embed=loading_embed("🏓 Pinging..."))
        end = time.time()
        
        api_latency = round((end - start) * 1000)
        ws_latency = round(self.bot.latency * 1000)
        
        if ws_latency < 100:
            status = "🟢 EXCELLENT"
        elif ws_latency < 200:
            status = "🟡 GOOD"
        else:
            status = "🔴 SLOW"
        
        embed = miku_embed(f"{EMOJIS['ping']} Pong!", f"Status: **{status}**")
        embed.add_field(name="📡 WebSocket", value=f"```{ws_latency}ms```", inline=True)
        embed.add_field(name="📊 API", value=f"```{api_latency}ms```", inline=True)
        embed.add_field(name="🎯 Bar", value=make_progress_bar(max(0, 500-ws_latency), 500), inline=False)
        await msg.edit(embed=embed)
    
    # ===== Feature 92: Uptime =====
    @commands.hybrid_command(name="uptime", description="Berapa lama bot online")
    async def uptime(self, ctx):
        delta = datetime.utcnow() - self.bot.start_time
        seconds = int(delta.total_seconds())
        embed = miku_embed(f"{EMOJIS['uptime']} Bot Uptime", f"⏰ **{format_duration(seconds)}**")
        embed.add_field(name="📅 Started", value=self.bot.start_time.strftime("%d/%m/%Y %H:%M UTC"), inline=False)
        await ctx.send(embed=embed)
    
    # ===== Feature 93: Bot Info =====
    @commands.hybrid_command(name="botinfo", description="Info tentang MikuBot")
    async def botinfo(self, ctx):
        try:
            mem = psutil.Process().memory_info().rss / 1024 / 1024
            cpu = psutil.cpu_percent()
        except:
            mem = 0
            cpu = 0
        
        embed = miku_embed("🤖 MikuBot Information")
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name=f"{EMOJIS['name']} Name", value=self.bot.user.name, inline=True)
        embed.add_field(name=f"{EMOJIS['id']} ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="🎨 Version", value=self.bot.version, inline=True)
        embed.add_field(name="🐍 Python", value=platform.python_version(), inline=True)
        embed.add_field(name="📚 discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="🖥️ OS", value=platform.system(), inline=True)
        embed.add_field(name="🌐 Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="👥 Users", value=sum(g.member_count for g in self.bot.guilds), inline=True)
        embed.add_field(name="📝 Commands", value=len(self.bot.commands), inline=True)
        embed.add_field(name="💾 Memory", value=f"{mem:.1f} MB", inline=True)
        embed.add_field(name="⚙️ CPU", value=f"{cpu}%", inline=True)
        embed.add_field(name="⏱️ Uptime", value=format_duration(int((datetime.utcnow() - self.bot.start_time).total_seconds())), inline=True)
        await ctx.send(embed=embed)
    
    # ===== Feature 94: Invite Link =====
    @commands.hybrid_command(name="invite", description="Link invite bot")
    async def invite(self, ctx):
        perm = discord.Permissions.all()
        url = discord.utils.oauth_url(self.bot.user.id, permissions=perm, scopes=["bot", "applications.commands"])
        embed = miku_embed("🔗 Invite MikuBot", f"[**Klik di sini untuk invite!**]({url})\n\nTerima kasih telah memilih MikuBot! 💖")
        await ctx.send(embed=embed)
    
    # ===== Feature 95: Suggestion System =====
    @commands.hybrid_command(name="suggest", description="Kirim saran untuk server")
    async def suggest(self, ctx, *, suggestion: str):
        s = self.db.get_guild("settings", ctx.guild.id)
        ch_id = s.get("suggestion_channel")
        if not ch_id:
            ch_id = ctx.channel.id
        ch = ctx.guild.get_channel(ch_id) or ctx.channel
        
        embed = miku_embed("💡 New Suggestion")
        embed.description = suggestion
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        msg = await ch.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        if ch != ctx.channel:
            await ctx.send(embed=success_embed("Suggestion Terkirim", f"Cek di {ch.mention}"))
    
    # ===== Feature 96: Set Suggestion Channel =====
    @commands.command(name="setsuggestion")
    @commands.has_permissions(manage_guild=True)
    async def setsuggestion(self, ctx, channel: discord.TextChannel):
        self.db.set_guild("settings", ctx.guild.id, "suggestion_channel", channel.id)
        await ctx.send(embed=success_embed("Suggestion Channel Set", f"Channel: {channel.mention}"))
    
    # ===== Feature 97: Report System =====
    @commands.hybrid_command(name="report", description="Report user (DM ke moderator)")
    async def report(self, ctx, member: discord.Member, *, reason: str):
        s = self.db.get_guild("settings", ctx.guild.id)
        ch_id = s.get("report_channel")
        if not ch_id:
            return await ctx.send(embed=error_embed("Belum Setup", "Admin belum set channel report. Pakai `!setreport`"))
        ch = ctx.guild.get_channel(ch_id)
        if not ch:
            return await ctx.send(embed=error_embed("Error", "Channel report tidak valid"))
        
        embed = error_embed("🚨 New Report")
        embed.add_field(name="Reporter", value=ctx.author.mention, inline=True)
        embed.add_field(name="Reported", value=member.mention, inline=True)
        embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ch.send(embed=embed)
        
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(embed=success_embed("Report Dikirim", "Moderator akan menindaklanjuti"), delete_after=10)
    
    # ===== Feature 98: Set Report Channel =====
    @commands.command(name="setreport")
    @commands.has_permissions(manage_guild=True)
    async def setreport(self, ctx, channel: discord.TextChannel):
        self.db.set_guild("settings", ctx.guild.id, "report_channel", channel.id)
        await ctx.send(embed=success_embed("Report Channel Set", f"Channel: {channel.mention}"))
    
    # ===== Feature 99: Reminder =====
    @commands.hybrid_command(name="remind", description="Set reminder (waktu dalam menit)")
    async def remind(self, ctx, minutes: int, *, message: str):
        if minutes < 1 or minutes > 10080:
            return await ctx.send(embed=error_embed("Gagal", "Range: 1 menit - 1 minggu (10080 menit)"))
        
        await ctx.send(embed=success_embed("⏰ Reminder Set", f"Akan diingatkan dalam **{minutes} menit**\n**Pesan:** {message}"))
        await asyncio.sleep(minutes * 60)
        try:
            embed = miku_embed("⏰ REMINDER!", f"Hai {ctx.author.mention}, ini reminder yang kamu set:\n\n💬 {message}")
            await ctx.send(content=ctx.author.mention, embed=embed)
            try:
                await ctx.author.send(embed=embed)
            except:
                pass
        except:
            pass
    
    # ===== Feature 100: Server Snapshot/Backup Info =====
    @commands.command(name="snapshot")
    @commands.has_permissions(administrator=True)
    async def snapshot(self, ctx):
        g = ctx.guild
        text_channels = [c.name for c in g.text_channels]
        voice_channels = [c.name for c in g.voice_channels]
        roles = [r.name for r in g.roles if r.name != "@everyone"]
        
        snap = {
            "server_name": g.name,
            "owner": str(g.owner),
            "members": g.member_count,
            "text_channels": text_channels,
            "voice_channels": voice_channels,
            "roles": roles,
            "created_at": g.created_at.isoformat(),
            "snapshot_taken": datetime.utcnow().isoformat()
        }
        
        self.db.set_guild("snapshots", g.id, "last_snapshot", snap)
        
        embed = success_embed("📸 Server Snapshot Diambil")
        embed.add_field(name="📝 Text Channels", value=len(text_channels), inline=True)
        embed.add_field(name="🎤 Voice Channels", value=len(voice_channels), inline=True)
        embed.add_field(name="🎭 Roles", value=len(roles), inline=True)
        embed.add_field(name="👥 Members", value=g.member_count, inline=True)
        embed.add_field(name="📅 Snapshot Time", value=datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC"), inline=False)
        embed.set_footer(text="Data tersimpan di database bot")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
