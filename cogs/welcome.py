"""
WELCOME COG - Features 81-90
Welcome/Goodbye messages, autorole, boost message, etc.
"""
import discord
from discord.ext import commands
from utils.embeds import *

class Welcome(commands.Cog):
    """👋 Welcome/Goodbye system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    # ===== Feature 81: Set Welcome Channel =====
    @commands.hybrid_command(name="setwelcome", description="Set channel welcome")
    @commands.has_permissions(manage_guild=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        self.db.set_guild("settings", ctx.guild.id, "welcome_channel", channel.id)
        await ctx.send(embed=success_embed("Welcome Channel Set", f"Channel: {channel.mention}"))
    
    # ===== Feature 82: Set Goodbye Channel =====
    @commands.hybrid_command(name="setgoodbye", description="Set channel goodbye")
    @commands.has_permissions(manage_guild=True)
    async def setgoodbye(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        self.db.set_guild("settings", ctx.guild.id, "goodbye_channel", channel.id)
        await ctx.send(embed=success_embed("Goodbye Channel Set", f"Channel: {channel.mention}"))
    
    # ===== Feature 83: Welcome Message Setup =====
    @commands.hybrid_command(name="welcomemsg", description="Set pesan welcome custom (gunakan {user} dan {server})")
    @commands.has_permissions(manage_guild=True)
    async def welcomemsg(self, ctx, *, message: str):
        self.db.set_guild("settings", ctx.guild.id, "welcome_message", message)
        await ctx.send(embed=success_embed("Welcome Message Set", f"Preview: {message.replace('{user}', ctx.author.mention).replace('{server}', ctx.guild.name)}"))
    
    # ===== Feature 84: Goodbye Message Setup =====
    @commands.hybrid_command(name="goodbyemsg", description="Set pesan goodbye custom")
    @commands.has_permissions(manage_guild=True)
    async def goodbyemsg(self, ctx, *, message: str):
        self.db.set_guild("settings", ctx.guild.id, "goodbye_message", message)
        await ctx.send(embed=success_embed("Goodbye Message Set", f"Preview: {message.replace('{user}', ctx.author.name).replace('{server}', ctx.guild.name)}"))
    
    # ===== Feature 85: Test Welcome =====
    @commands.hybrid_command(name="testwelcome", description="Test welcome message")
    @commands.has_permissions(manage_guild=True)
    async def testwelcome(self, ctx):
        await self.on_member_join(ctx.author)
        await ctx.send(embed=success_embed("Test Welcome Dikirim", "Lihat di channel welcome"))
    
    # ===== Feature 86: Set DM Welcome =====
    @commands.command(name="dmwelcome")
    @commands.has_permissions(manage_guild=True)
    async def dmwelcome(self, ctx):
        settings = self.db.get_guild("settings", ctx.guild.id)
        current = settings.get("dm_welcome", False)
        self.db.set_guild("settings", ctx.guild.id, "dm_welcome", not current)
        await ctx.send(embed=success_embed("DM Welcome", f"Status: **{'ON' if not current else 'OFF'}**"))
    
    # ===== Feature 87: Set DM Welcome Message =====
    @commands.command(name="dmwelcomemsg")
    @commands.has_permissions(manage_guild=True)
    async def dmwelcomemsg(self, ctx, *, message: str):
        self.db.set_guild("settings", ctx.guild.id, "dm_welcome_message", message)
        await ctx.send(embed=success_embed("DM Welcome Message Set", f"Preview: {message}"))
    
    # ===== Feature 88: Welcome Settings =====
    @commands.command(name="welcomesettings")
    @commands.has_permissions(manage_guild=True)
    async def welcomesettings(self, ctx):
        s = self.db.get_guild("settings", ctx.guild.id)
        embed = info_embed("⚙️ Welcome Settings")
        wch = s.get("welcome_channel")
        gch = s.get("goodbye_channel")
        embed.add_field(name="📥 Welcome Channel", value=f"<#{wch}>" if wch else "Belum diset", inline=False)
        embed.add_field(name="📤 Goodbye Channel", value=f"<#{gch}>" if gch else "Belum diset", inline=False)
        embed.add_field(name="✉️ Welcome Message", value=s.get("welcome_message", "Default"), inline=False)
        embed.add_field(name="👋 Goodbye Message", value=s.get("goodbye_message", "Default"), inline=False)
        embed.add_field(name="📩 DM Welcome", value="ON" if s.get("dm_welcome") else "OFF", inline=True)
        await ctx.send(embed=embed)
    
    # ===== Feature 89: Boost Message Setup =====
    @commands.command(name="setboostmsg")
    @commands.has_permissions(manage_guild=True)
    async def setboostmsg(self, ctx, channel: discord.TextChannel, *, message: str = None):
        self.db.set_guild("settings", ctx.guild.id, "boost_channel", channel.id)
        if message:
            self.db.set_guild("settings", ctx.guild.id, "boost_message", message)
        await ctx.send(embed=success_embed("Boost Message Set", f"Channel: {channel.mention}"))
    
    # ===== Feature 90: Disable Welcome =====
    @commands.command(name="disablewelcome")
    @commands.has_permissions(manage_guild=True)
    async def disablewelcome(self, ctx):
        self.db.set_guild("settings", ctx.guild.id, "welcome_channel", None)
        self.db.set_guild("settings", ctx.guild.id, "goodbye_channel", None)
        await ctx.send(embed=success_embed("Welcome Disabled", "Welcome dan goodbye dimatikan"))
    
    # ===== Event Listeners =====
    @commands.Cog.listener()
    async def on_member_join(self, member):
        s = self.db.get_guild("settings", member.guild.id)
        ch_id = s.get("welcome_channel")
        if ch_id:
            ch = member.guild.get_channel(ch_id)
            if ch:
                msg_template = s.get("welcome_message", 
                    "🎉 Selamat datang {user} di **{server}**! Kami sekarang **{count}** member ✨")
                msg = msg_template.replace("{user}", member.mention)\
                                   .replace("{server}", member.guild.name)\
                                   .replace("{count}", str(member.guild.member_count))
                
                embed = miku_embed(f"👋 Welcome to {member.guild.name}!")
                embed.description = msg
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.add_field(name="👤 Member Ke", value=f"#{member.guild.member_count}", inline=True)
                embed.add_field(name="📅 Account Dibuat", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
                if member.guild.icon:
                    embed.set_image(url=member.guild.icon.url)
                try:
                    await ch.send(content=member.mention, embed=embed)
                except:
                    pass
        
        # DM Welcome
        if s.get("dm_welcome"):
            dm_msg = s.get("dm_welcome_message", f"Selamat datang di **{member.guild.name}**! 💖")
            try:
                embed = miku_embed(f"Welcome ke {member.guild.name}!", dm_msg)
                await member.send(embed=embed)
            except:
                pass
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        s = self.db.get_guild("settings", member.guild.id)
        ch_id = s.get("goodbye_channel")
        if ch_id:
            ch = member.guild.get_channel(ch_id)
            if ch:
                msg_template = s.get("goodbye_message", 
                    "😢 **{user}** telah meninggalkan server. Selamat tinggal!")
                msg = msg_template.replace("{user}", member.name)\
                                   .replace("{server}", member.guild.name)
                
                embed = base_embed("👋 Goodbye!", msg, 0xFF6B6B)
                embed.set_thumbnail(url=member.display_avatar.url)
                try:
                    await ch.send(embed=embed)
                except:
                    pass
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not before.premium_since and after.premium_since:
            s = self.db.get_guild("settings", after.guild.id)
            ch_id = s.get("boost_channel")
            if ch_id:
                ch = after.guild.get_channel(ch_id)
                if ch:
                    msg = s.get("boost_message", 
                        f"🚀 **{after.mention} baru saja BOOST server!** Terima kasih banyak! 💖")
                    embed = miku_embed("🚀 SERVER BOOSTED! 🎉", msg)
                    embed.set_thumbnail(url=after.display_avatar.url)
                    try:
                        await ch.send(embed=embed)
                    except:
                        pass

async def setup(bot):
    await bot.add_cog(Welcome(bot))
