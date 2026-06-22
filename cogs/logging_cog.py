"""
LOGGING SYSTEM
Log all server events to a logging channel
"""
import discord
from discord.ext import commands
from utils.embeds import *

class Logging(commands.Cog):
    """📋 Server logging"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    @commands.command(name="setlog")
    @commands.has_permissions(manage_guild=True)
    async def setlog(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        self.db.set_guild("settings", ctx.guild.id, "log_channel", channel.id)
        await ctx.send(embed=success_embed("Log Channel Set", f"Channel: {channel.mention}"))
    
    @commands.command(name="disablelog")
    @commands.has_permissions(manage_guild=True)
    async def disablelog(self, ctx):
        self.db.set_guild("settings", ctx.guild.id, "log_channel", None)
        await ctx.send(embed=success_embed("Logging Disabled", "Logging dimatikan"))
    
    async def send_log(self, guild, embed):
        s = self.db.get_guild("settings", guild.id)
        ch_id = s.get("log_channel")
        if not ch_id:
            return
        ch = guild.get_channel(ch_id)
        if ch:
            try:
                await ch.send(embed=embed)
            except:
                pass
    
    # ===== Message Events =====
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild:
            return
        embed = warning_embed("🗑️ Pesan Dihapus")
        embed.add_field(name="Author", value=f"{message.author.mention} (`{message.author.id}`)", inline=False)
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)
        embed.add_field(name="Content", value=message.content[:1000] or "*(empty/attachment)*", inline=False)
        if message.attachments:
            embed.add_field(name="Attachments", value="\n".join([a.url for a in message.attachments[:3]]), inline=False)
        await self.send_log(message.guild, embed)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or not before.guild or before.content == after.content:
            return
        embed = info_embed("✏️ Pesan Diedit")
        embed.add_field(name="Author", value=f"{before.author.mention}", inline=False)
        embed.add_field(name="Channel", value=before.channel.mention, inline=False)
        embed.add_field(name="Sebelum", value=before.content[:500] or "*(empty)*", inline=False)
        embed.add_field(name="Sesudah", value=after.content[:500] or "*(empty)*", inline=False)
        embed.add_field(name="🔗 Jump", value=f"[Pesan]({after.jump_url})", inline=False)
        await self.send_log(before.guild, embed)
    
    # ===== Member Events =====
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = success_embed("📥 Member Join", f"{member.mention} bergabung")
        embed.add_field(name="User", value=f"{member} (`{member.id}`)", inline=False)
        embed.add_field(name="Account Dibuat", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)
        embed.add_field(name="Member Ke", value=f"#{member.guild.member_count}", inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        await self.send_log(member.guild, embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = error_embed("📤 Member Leave", f"{member} meninggalkan server")
        embed.add_field(name="User", value=f"{member} (`{member.id}`)", inline=False)
        roles = [r.mention for r in member.roles[1:]][:10]
        if roles:
            embed.add_field(name="Roles", value=" ".join(roles), inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)
        await self.send_log(member.guild, embed)
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = error_embed("🔨 Member Banned", f"{user} di-ban")
        embed.add_field(name="User", value=f"{user} (`{user.id}`)", inline=False)
        await self.send_log(guild, embed)
    
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        embed = success_embed("✅ Member Unbanned", f"{user} di-unban")
        embed.add_field(name="User", value=f"{user} (`{user.id}`)", inline=False)
        await self.send_log(guild, embed)
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            embed = info_embed("📝 Nickname Diubah")
            embed.add_field(name="User", value=after.mention, inline=False)
            embed.add_field(name="Sebelum", value=before.nick or before.name, inline=True)
            embed.add_field(name="Sesudah", value=after.nick or after.name, inline=True)
            await self.send_log(after.guild, embed)
        
        # Role changes
        added = set(after.roles) - set(before.roles)
        removed = set(before.roles) - set(after.roles)
        if added:
            embed = success_embed("🎭 Role Ditambah", f"User: {after.mention}")
            embed.add_field(name="Roles", value=" ".join([r.mention for r in added]), inline=False)
            await self.send_log(after.guild, embed)
        if removed:
            embed = warning_embed("🎭 Role Dihapus", f"User: {after.mention}")
            embed.add_field(name="Roles", value=" ".join([r.mention for r in removed]), inline=False)
            await self.send_log(after.guild, embed)
    
    # ===== Channel Events =====
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = success_embed("➕ Channel Dibuat")
        embed.add_field(name="Name", value=channel.name, inline=True)
        embed.add_field(name="Type", value=str(channel.type), inline=True)
        embed.add_field(name="ID", value=channel.id, inline=True)
        await self.send_log(channel.guild, embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        embed = error_embed("➖ Channel Dihapus")
        embed.add_field(name="Name", value=channel.name, inline=True)
        embed.add_field(name="Type", value=str(channel.type), inline=True)
        await self.send_log(channel.guild, embed)
    
    # ===== Role Events =====
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        embed = success_embed("➕ Role Dibuat")
        embed.add_field(name="Name", value=role.name, inline=True)
        embed.add_field(name="Color", value=str(role.color), inline=True)
        await self.send_log(role.guild, embed)
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        embed = error_embed("➖ Role Dihapus")
        embed.add_field(name="Name", value=role.name, inline=True)
        await self.send_log(role.guild, embed)
    
    # ===== Voice Events =====
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        if before.channel != after.channel:
            if before.channel is None and after.channel is not None:
                embed = success_embed("🎤 Voice Join", f"{member.mention} masuk **{after.channel.name}**")
            elif before.channel is not None and after.channel is None:
                embed = warning_embed("🎤 Voice Leave", f"{member.mention} keluar dari **{before.channel.name}**")
            else:
                embed = info_embed("🎤 Voice Move", f"{member.mention}: **{before.channel.name}** → **{after.channel.name}**")
            await self.send_log(member.guild, embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))
