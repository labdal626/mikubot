"""
MODERATION COG - Features 1-20
Kick, Ban, Mute, Warn, Purge, Lock, Slowmode, etc.
"""
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from utils.embeds import *

class Moderation(commands.Cog):
    """🛡️ Moderation commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    # ===== Feature 1: Kick =====
    @commands.hybrid_command(name="kick", description="Kick member dari server")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "Tidak ada alasan"):
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send(embed=error_embed("Gagal", "Kamu tidak bisa kick member dengan role yang sama atau lebih tinggi!"))
        if member == ctx.guild.owner:
            return await ctx.send(embed=error_embed("Gagal", "Tidak bisa kick owner server!"))
        
        try:
            try:
                dm_embed = error_embed(f"Kamu di-kick dari {ctx.guild.name}", f"**Alasan:** {reason}")
                await member.send(embed=dm_embed)
            except:
                pass
            await member.kick(reason=f"{ctx.author}: {reason}")
            embed = success_embed("Member Kicked", f"{EMOJIS['kick']} **{member}** telah di-kick\n**Alasan:** {reason}\n**Moderator:** {ctx.author.mention}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 2: Ban =====
    @commands.hybrid_command(name="ban", description="Ban member dari server")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "Tidak ada alasan"):
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send(embed=error_embed("Gagal", "Role member lebih tinggi atau sama dengan kamu!"))
        if member == ctx.guild.owner:
            return await ctx.send(embed=error_embed("Gagal", "Tidak bisa ban owner!"))
        
        try:
            try:
                dm = error_embed(f"Kamu di-ban dari {ctx.guild.name}", f"**Alasan:** {reason}")
                await member.send(embed=dm)
            except:
                pass
            await member.ban(reason=f"{ctx.author}: {reason}", delete_message_days=0)
            embed = success_embed("Member Banned", f"{EMOJIS['ban']} **{member}** telah di-ban\n**Alasan:** {reason}\n**Moderator:** {ctx.author.mention}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 3: Unban =====
    @commands.hybrid_command(name="unban", description="Unban user dengan ID")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: str, *, reason: str = "Tidak ada alasan"):
        try:
            user_id = int(user_id)
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=f"{ctx.author}: {reason}")
            embed = success_embed("User Unbanned", f"{EMOJIS['success']} **{user}** telah di-unban\n**Alasan:** {reason}")
            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send(embed=error_embed("Gagal", "User tidak ditemukan atau tidak sedang di-ban"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 4: Mute (Timeout) =====
    @commands.hybrid_command(name="mute", description="Mute member (timeout) dalam menit")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int = 10, *, reason: str = "Tidak ada alasan"):
        if minutes < 1 or minutes > 40320:  # max 28 days
            return await ctx.send(embed=error_embed("Gagal", "Durasi harus antara 1 - 40320 menit (28 hari)"))
        
        try:
            until = datetime.utcnow() + timedelta(minutes=minutes)
            await member.timeout(until, reason=f"{ctx.author}: {reason}")
            embed = success_embed("Member Muted", 
                f"{EMOJIS['mute']} **{member}** di-mute selama **{minutes} menit**\n**Alasan:** {reason}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 5: Unmute =====
    @commands.hybrid_command(name="unmute", description="Unmute member")
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = "Tidak ada alasan"):
        try:
            await member.timeout(None, reason=f"{ctx.author}: {reason}")
            embed = success_embed("Member Unmuted", f"{EMOJIS['unmute']} **{member}** telah di-unmute")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 6: Warn =====
    @commands.hybrid_command(name="warn", description="Warn member")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "Tidak ada alasan"):
        warns = self.db.load("warnings", {})
        gid, uid = str(ctx.guild.id), str(member.id)
        if gid not in warns:
            warns[gid] = {}
        if uid not in warns[gid]:
            warns[gid][uid] = []
        
        warn_data = {
            "reason": reason,
            "moderator": str(ctx.author),
            "moderator_id": ctx.author.id,
            "timestamp": datetime.utcnow().isoformat(),
            "id": len(warns[gid][uid]) + 1
        }
        warns[gid][uid].append(warn_data)
        self.db.save("warnings", warns)
        
        count = len(warns[gid][uid])
        embed = warning_embed("Warning Diberikan",
            f"{EMOJIS['warn']} **{member}** telah di-warn\n"
            f"**Alasan:** {reason}\n"
            f"**Total Warnings:** {count}")
        await ctx.send(embed=embed)
        
        try:
            dm = warning_embed(f"Warning di {ctx.guild.name}", 
                f"**Alasan:** {reason}\n**Total Warnings:** {count}")
            await member.send(embed=dm)
        except:
            pass
    
    # ===== Feature 7: View Warnings =====
    @commands.hybrid_command(name="warnings", description="Lihat warnings member")
    async def warnings(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        warns = self.db.load("warnings", {})
        gid, uid = str(ctx.guild.id), str(member.id)
        
        user_warns = warns.get(gid, {}).get(uid, [])
        if not user_warns:
            return await ctx.send(embed=info_embed("Tidak Ada Warning", f"{member.mention} tidak punya warning"))
        
        embed = warning_embed(f"Warnings untuk {member}", f"Total: **{len(user_warns)}** warning(s)")
        for w in user_warns[-10:]:
            ts = datetime.fromisoformat(w["timestamp"]).strftime("%d/%m/%Y %H:%M")
            embed.add_field(
                name=f"#{w['id']} - {ts}",
                value=f"**Alasan:** {w['reason']}\n**Mod:** {w['moderator']}",
                inline=False
            )
        await ctx.send(embed=embed)
    
    # ===== Feature 8: Clear Warnings =====
    @commands.hybrid_command(name="clearwarnings", description="Hapus semua warnings member")
    @commands.has_permissions(manage_messages=True)
    async def clearwarnings(self, ctx, member: discord.Member):
        warns = self.db.load("warnings", {})
        gid, uid = str(ctx.guild.id), str(member.id)
        if gid in warns and uid in warns[gid]:
            count = len(warns[gid][uid])
            warns[gid][uid] = []
            self.db.save("warnings", warns)
            await ctx.send(embed=success_embed("Warnings Cleared", f"Berhasil menghapus **{count}** warning dari {member.mention}"))
        else:
            await ctx.send(embed=info_embed("Tidak Ada Warning", f"{member.mention} tidak punya warning"))
    
    # ===== Feature 9: Mass Kick =====
    @commands.command(name="masskick")
    @commands.has_permissions(kick_members=True, administrator=True)
    async def masskick(self, ctx, members: commands.Greedy[discord.Member], *, reason: str = "Mass kick"):
        if not members:
            return await ctx.send(embed=error_embed("Gagal", "Mention member yang mau di-kick"))
        
        kicked = 0
        for m in members[:10]:
            try:
                await m.kick(reason=f"{ctx.author}: {reason}")
                kicked += 1
            except:
                continue
        await ctx.send(embed=success_embed("Mass Kick Selesai", f"Berhasil kick **{kicked}/{len(members)}** members"))
    
    # ===== Feature 10: Mass Ban =====
    @commands.command(name="massban")
    @commands.has_permissions(ban_members=True, administrator=True)
    async def massban(self, ctx, members: commands.Greedy[discord.Member], *, reason: str = "Mass ban"):
        if not members:
            return await ctx.send(embed=error_embed("Gagal", "Mention member yang mau di-ban"))
        
        banned = 0
        for m in members[:10]:
            try:
                await m.ban(reason=f"{ctx.author}: {reason}", delete_message_days=0)
                banned += 1
            except:
                continue
        await ctx.send(embed=success_embed("Mass Ban Selesai", f"Berhasil ban **{banned}/{len(members)}** members"))
    
    # ===== Feature 11: Lock Channel =====
    @commands.hybrid_command(name="lock", description="Lock channel saat ini")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, *, reason: str = "Locked"):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=reason)
        await ctx.send(embed=success_embed("Channel Locked", f"{EMOJIS['lock']} Channel ini telah di-lock\n**Alasan:** {reason}"))
    
    # ===== Feature 12: Unlock Channel =====
    @commands.hybrid_command(name="unlock", description="Unlock channel saat ini")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=success_embed("Channel Unlocked", f"{EMOJIS['unlock']} Channel ini telah di-unlock"))
    
    # ===== Feature 13: Slowmode =====
    @commands.hybrid_command(name="slowmode", description="Set slowmode channel (detik, 0 untuk disable)")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        if seconds < 0 or seconds > 21600:
            return await ctx.send(embed=error_embed("Gagal", "Slowmode: 0-21600 detik"))
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send(embed=success_embed("Slowmode Disabled", "Slowmode telah dimatikan"))
        else:
            await ctx.send(embed=success_embed("Slowmode Diaktifkan", f"⏱️ Slowmode set ke **{seconds} detik**"))
    
    # ===== Feature 14: Purge (Bulk Delete) =====
    @commands.hybrid_command(name="purge", description="Hapus sejumlah pesan (max 100)")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if amount < 1 or amount > 100:
            return await ctx.send(embed=error_embed("Gagal", "Jumlah harus antara 1-100"))
        
        if ctx.interaction:
            await ctx.defer(ephemeral=True)
            deleted = await ctx.channel.purge(limit=amount)
        else:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=amount)
        
        msg = await ctx.send(embed=success_embed("Pesan Dihapus", f"🗑️ **{len(deleted)}** pesan dihapus"))
        try:
            await msg.delete(delay=5)
        except:
            pass
    
    # ===== Feature 15: Purge by User =====
    @commands.hybrid_command(name="purgeuser", description="Hapus pesan dari user spesifik")
    @commands.has_permissions(manage_messages=True)
    async def purgeuser(self, ctx, member: discord.Member, amount: int = 50):
        if amount < 1 or amount > 100:
            return await ctx.send(embed=error_embed("Gagal", "Jumlah harus 1-100"))
        
        def check(m):
            return m.author == member
        
        if ctx.interaction:
            await ctx.defer(ephemeral=True)
        else:
            await ctx.message.delete()
        
        deleted = await ctx.channel.purge(limit=amount, check=check)
        msg = await ctx.send(embed=success_embed("Pesan User Dihapus", f"🗑️ **{len(deleted)}** pesan dari {member.mention} dihapus"))
        try:
            await msg.delete(delay=5)
        except:
            pass
    
    # ===== Feature 16: Purge Bots =====
    @commands.hybrid_command(name="purgebots", description="Hapus pesan dari bot")
    @commands.has_permissions(manage_messages=True)
    async def purgebots(self, ctx, amount: int = 50):
        if amount < 1 or amount > 100:
            return await ctx.send(embed=error_embed("Gagal", "Jumlah harus 1-100"))
        
        if ctx.interaction:
            await ctx.defer(ephemeral=True)
        else:
            await ctx.message.delete()
        
        deleted = await ctx.channel.purge(limit=amount, check=lambda m: m.author.bot)
        msg = await ctx.send(embed=success_embed("Pesan Bot Dihapus", f"🤖 **{len(deleted)}** pesan bot dihapus"))
        try:
            await msg.delete(delay=5)
        except:
            pass
    
    # ===== Feature 17: Lockdown All =====
    @commands.command(name="lockdown")
    @commands.has_permissions(administrator=True)
    async def lockdown(self, ctx):
        await ctx.send(embed=loading_embed("Mengunci semua channel..."))
        count = 0
        for channel in ctx.guild.text_channels:
            try:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                count += 1
            except:
                continue
        await ctx.send(embed=success_embed("Lockdown Aktif", f"🔒 **{count}** channel telah di-lock"))
    
    # ===== Feature 18: Unlock All =====
    @commands.command(name="unlockall")
    @commands.has_permissions(administrator=True)
    async def unlockall(self, ctx):
        await ctx.send(embed=loading_embed("Membuka semua channel..."))
        count = 0
        for channel in ctx.guild.text_channels:
            try:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = None
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                count += 1
            except:
                continue
        await ctx.send(embed=success_embed("Lockdown Dicabut", f"🔓 **{count}** channel telah di-unlock"))
    
    # ===== Feature 19: Nick (Change Nickname) =====
    @commands.hybrid_command(name="nick", description="Ubah nickname member")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, new_nick: str = None):
        old = member.display_name
        try:
            await member.edit(nick=new_nick)
            await ctx.send(embed=success_embed("Nickname Diubah", 
                f"**Member:** {member.mention}\n**Sebelum:** {old}\n**Sesudah:** {new_nick or member.name}"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 20: Softban (Ban + Unban for message cleanup) =====
    @commands.hybrid_command(name="softban", description="Softban (ban + unban) untuk hapus pesan")
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason: str = "Softban"):
        try:
            await member.ban(reason=f"{ctx.author}: SOFTBAN - {reason}", delete_message_days=7)
            await ctx.guild.unban(member, reason="Softban auto-unban")
            await ctx.send(embed=success_embed("Member Softbanned", 
                f"{EMOJIS['ban']} **{member}** di-softban (pesan 7 hari dihapus)\n**Alasan:** {reason}"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))

async def setup(bot):
    await bot.add_cog(Moderation(bot))
