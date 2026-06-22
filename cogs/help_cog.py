"""
HELP SYSTEM - Beautiful animated help command
"""
import discord
from discord.ext import commands
from utils.embeds import *

class HelpView(discord.ui.View):
    def __init__(self, bot, ctx):
        super().__init__(timeout=180)
        self.bot = bot
        self.ctx = ctx
        self.current = "main"
    
    @discord.ui.select(
        placeholder="🎯 Pilih kategori command...",
        options=[
            discord.SelectOption(label="🏠 Main Menu", value="main", emoji="🏠", description="Halaman utama"),
            discord.SelectOption(label="🛡️ Moderasi", value="moderation", emoji="🛡️", description="Kick, Ban, Mute, Warn..."),
            discord.SelectOption(label="📝 Channel", value="channel", emoji="📝", description="Manage channel"),
            discord.SelectOption(label="🎭 Role", value="role", emoji="🎭", description="Manage role"),
            discord.SelectOption(label="ℹ️ Info", value="info", emoji="ℹ️", description="User/Server info"),
            discord.SelectOption(label="🎮 Fun", value="fun", emoji="🎮", description="Games & fun"),
            discord.SelectOption(label="👋 Welcome", value="welcome", emoji="👋", description="Welcome/Goodbye"),
            discord.SelectOption(label="🔧 Utility", value="utility", emoji="🔧", description="Ping, Uptime, etc."),
            discord.SelectOption(label="🎫 Ticket", value="ticket", emoji="🎫", description="Ticket system"),
            discord.SelectOption(label="🎉 Giveaway", value="giveaway", emoji="🎉", description="Giveaway"),
            discord.SelectOption(label="🛡️ Auto-Mod", value="automod", emoji="🛡️", description="Auto moderation"),
            discord.SelectOption(label="📋 Logging", value="logging", emoji="📋", description="Server logs"),
            discord.SelectOption(label="💰 Economy", value="economy", emoji="💰", description="Coin system"),
            discord.SelectOption(label="📊 Leveling", value="leveling", emoji="📊", description="XP & Level")
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message("❌ Bukan kamu yang panggil help!", ephemeral=True)
        
        self.current = select.values[0]
        embed = self.get_embed(self.current)
        await interaction.response.edit_message(embed=embed, view=self)
    
    def get_embed(self, page):
        prefix = "!"
        
        if page == "main":
            embed = miku_embed("✨ MikuBot Help Menu ✨", 
                f"Halo! Aku **MikuBot** 🎵 - Bot moderasi & manajemen Discord lengkap!\n\n"
                f"**Total Commands:** 100+\n"
                f"**Prefix:** `{prefix}` atau slash `/`\n"
                f"**Servers:** {len(self.bot.guilds)}\n\n"
                f"📌 **Gunakan dropdown di bawah untuk pilih kategori!**")
            embed.add_field(name="🛡️ Moderasi", value="`kick`, `ban`, `mute`, `warn`...", inline=True)
            embed.add_field(name="📝 Channel", value="`createchannel`, `lock`, `purge`...", inline=True)
            embed.add_field(name="🎭 Role", value="`createrole`, `addrole`, `autorole`...", inline=True)
            embed.add_field(name="ℹ️ Info", value="`userinfo`, `serverinfo`, `avatar`...", inline=True)
            embed.add_field(name="🎮 Fun", value="`8ball`, `dice`, `poll`, `trivia`...", inline=True)
            embed.add_field(name="🔧 Utility", value="`ping`, `uptime`, `remind`...", inline=True)
            embed.add_field(name="🎫 Ticket", value="`ticketsetup`, `ticketclose`...", inline=True)
            embed.add_field(name="🎉 Giveaway", value="`giveaway`, `reroll`...", inline=True)
            embed.add_field(name="💰 Economy", value="`balance`, `daily`, `give`...", inline=True)
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        elif page == "moderation":
            embed = miku_embed("🛡️ Moderation Commands")
            cmds = [
                ("kick", "Kick member dari server"),
                ("ban", "Ban member dari server"),
                ("unban", "Unban user dengan ID"),
                ("mute", "Mute member (timeout) dalam menit"),
                ("unmute", "Unmute member"),
                ("warn", "Warn member"),
                ("warnings", "Lihat warnings member"),
                ("clearwarnings", "Hapus warnings"),
                ("masskick", "Kick banyak member"),
                ("massban", "Ban banyak member"),
                ("lock", "Lock channel"),
                ("unlock", "Unlock channel"),
                ("slowmode", "Set slowmode (detik)"),
                ("purge", "Hapus pesan (max 100)"),
                ("purgeuser", "Hapus pesan dari user"),
                ("purgebots", "Hapus pesan bot"),
                ("lockdown", "Lock semua channel"),
                ("unlockall", "Unlock semua channel"),
                ("nick", "Ubah nickname"),
                ("softban", "Softban (ban + unban)")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=True)
        
        elif page == "channel":
            embed = miku_embed("📝 Channel Commands")
            cmds = [
                ("createchannel", "Buat text channel"),
                ("createvoice", "Buat voice channel"),
                ("createcategory", "Buat category"),
                ("deletechannel", "Hapus channel"),
                ("rename", "Rename channel"),
                ("topic", "Set topic"),
                ("nsfw", "Toggle NSFW"),
                ("clone", "Clone channel"),
                ("nuke", "Nuke channel"),
                ("channelinfo", "Info channel"),
                ("channels", "List channels"),
                ("hide", "Sembunyikan channel"),
                ("unhide", "Tampilkan channel"),
                ("setposition", "Set posisi"),
                ("channelstats", "Statistik channel")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=True)
        
        elif page == "role":
            embed = miku_embed("🎭 Role Commands")
            cmds = [
                ("createrole", "Buat role"),
                ("deleterole", "Hapus role"),
                ("addrole", "Tambah role ke user"),
                ("removerole", "Hapus role dari user"),
                ("roleinfo", "Info role"),
                ("roles", "List roles"),
                ("autorole", "Set autorole"),
                ("rolecolor", "Ubah warna role"),
                ("rolerename", "Rename role"),
                ("hoist", "Toggle hoist"),
                ("mentionable", "Toggle mentionable"),
                ("massaddrole", "Tambah ke semua"),
                ("massremoverole", "Hapus dari semua"),
                ("rolemembers", "List member role"),
                ("reactionrole", "Setup reaction role")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=True)
        
        elif page == "info":
            embed = miku_embed("ℹ️ Info Commands")
            cmds = [
                ("userinfo", "Info user"),
                ("serverinfo", "Info server"),
                ("avatar", "Tampilkan avatar"),
                ("banner", "Tampilkan banner"),
                ("membercount", "Hitung member"),
                ("stats", "Stats server"),
                ("joindate", "Tanggal join"),
                ("accountage", "Umur akun"),
                ("permissions", "Cek permissions"),
                ("servericon", "Icon server"),
                ("serverbanner", "Banner server"),
                ("online", "Member online"),
                ("botcount", "Hitung bot"),
                ("emojis", "List emoji"),
                ("boosters", "List booster")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=True)
        
        elif page == "fun":
            embed = miku_embed("🎮 Fun Commands")
            cmds = [
                ("8ball", "Magic 8ball"),
                ("coinflip", "Lempar koin"),
                ("dice", "Roll dadu"),
                ("random", "Random number"),
                ("choose", "Pilih opsi random"),
                ("quote", "Quote random"),
                ("joke", "Joke random"),
                ("rps", "Rock Paper Scissors"),
                ("trivia", "Mini quiz"),
                ("poll", "Buat poll"),
                ("flip", "Coinflip animasi"),
                ("say", "Bot ngomong"),
                ("embedsay", "Bot ngomong embed"),
                ("reverse", "Balik teks"),
                ("numbergame", "Tebak angka 1-100")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=True)
        
        elif page == "welcome":
            embed = miku_embed("👋 Welcome System")
            cmds = [
                ("setwelcome", "Set channel welcome"),
                ("setgoodbye", "Set channel goodbye"),
                ("welcomemsg", "Set pesan welcome"),
                ("goodbyemsg", "Set pesan goodbye"),
                ("testwelcome", "Test welcome"),
                ("dmwelcome", "Toggle DM welcome"),
                ("dmwelcomemsg", "Set DM welcome"),
                ("welcomesettings", "Lihat settings"),
                ("setboostmsg", "Set boost message"),
                ("disablewelcome", "Disable welcome")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=True)
        
        elif page == "utility":
            embed = miku_embed("🔧 Utility Commands")
            cmds = [
                ("ping", "Cek ping bot"),
                ("uptime", "Uptime bot"),
                ("botinfo", "Info bot"),
                ("invite", "Link invite"),
                ("suggest", "Kirim saran"),
                ("setsuggestion", "Set suggestion channel"),
                ("report", "Report user"),
                ("setreport", "Set report channel"),
                ("remind", "Set reminder"),
                ("snapshot", "Snapshot server")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=True)
        
        elif page == "ticket":
            embed = miku_embed("🎫 Ticket System")
            cmds = [
                ("ticketsetup", "Setup ticket panel"),
                ("ticketclose", "Tutup ticket"),
                ("ticketadd", "Tambah user ke ticket"),
                ("ticketremove", "Hapus user dari ticket")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=False)
        
        elif page == "giveaway":
            embed = miku_embed("🎉 Giveaway System")
            cmds = [
                ("giveaway <menit> <winners> <prize>", "Buat giveaway"),
                ("reroll <message_id>", "Reroll winner")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=False)
        
        elif page == "automod":
            embed = miku_embed("🛡️ Auto-Mod Commands")
            cmds = [
                ("antispam", "Toggle anti-spam"),
                ("antilink", "Toggle anti-link"),
                ("antiinvite", "Toggle anti-invite"),
                ("anticaps", "Toggle anti-caps"),
                ("antimention", "Toggle anti-mention spam"),
                ("addbadword", "Tambah bad word"),
                ("removebadword", "Hapus bad word"),
                ("automod", "Lihat status auto-mod")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=True)
        
        elif page == "logging":
            embed = miku_embed("📋 Logging System")
            cmds = [
                ("setlog", "Set log channel"),
                ("disablelog", "Disable logging")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=False)
            embed.add_field(name="📊 Yang dilog", 
                value="• Message delete/edit\n• Member join/leave\n• Ban/Unban\n• Role changes\n• Nickname changes\n• Channel create/delete\n• Voice channel activity",
                inline=False)
        
        elif page == "economy":
            embed = miku_embed("💰 Economy System")
            cmds = [
                ("balance", "Cek saldo"),
                ("daily", "Klaim daily reward"),
                ("weekly", "Klaim weekly reward"),
                ("give", "Kirim coin ke user"),
                ("leaderboard", "Top richest"),
                ("work", "Kerja dapat coin"),
                ("rob", "Rob user lain (risky!)")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=True)
        
        elif page == "leveling":
            embed = miku_embed("📊 Leveling System")
            cmds = [
                ("level", "Cek level kamu"),
                ("rank", "Rank kamu"),
                ("levelboard", "Top level"),
                ("setlevelup", "Set channel level up"),
                ("levelrewards", "Lihat reward role per level")
            ]
            for name, desc in cmds:
                embed.add_field(name=f"`{prefix}{name}`", value=desc, inline=True)
        
        embed.set_footer(text=f"✨ MikuBot • {len(self.bot.commands)} commands loaded • Powered by Hatsune Miku 💖")
        return embed
    
    @discord.ui.button(label="🏠 Home", style=discord.ButtonStyle.secondary, row=1)
    async def home(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message("❌ Bukan kamu!", ephemeral=True)
        self.current = "main"
        await interaction.response.edit_message(embed=self.get_embed("main"), view=self)
    
    @discord.ui.button(label="❌ Tutup", style=discord.ButtonStyle.danger, row=1)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message("❌ Bukan kamu!", ephemeral=True)
        await interaction.response.edit_message(content="Help ditutup.", embed=None, view=None)
        self.stop()

class Help(commands.Cog):
    """❓ Help"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="help", description="Tampilkan menu help interaktif")
    async def help(self, ctx):
        view = HelpView(self.bot, ctx)
        # Add link button for invite dynamically
        try:
            url = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions.all(), scopes=["bot", "applications.commands"])
            view.add_item(discord.ui.Button(label="🔗 Invite Bot", style=discord.ButtonStyle.link, url=url, row=1))
        except:
            pass
        embed = view.get_embed("main")
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))
