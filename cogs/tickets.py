"""
TICKET SYSTEM
Open, Close, Add, Remove ticket users
"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import *

class TicketView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label="🎫 Buka Ticket", style=discord.ButtonStyle.green, custom_id="ticket_open_persistent")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user
        
        # Check existing
        existing = discord.utils.get(guild.channels, name=f"ticket-{user.name.lower()}")
        if existing:
            return await interaction.response.send_message(
                embed=error_embed("Sudah Ada Ticket", f"Ticket kamu: {existing.mention}"),
                ephemeral=True
            )
        
        # Find/create ticket category
        category = discord.utils.get(guild.categories, name="🎫 Tickets")
        if not category:
            category = await guild.create_category("🎫 Tickets")
        
        # Permission overwrites
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }
        
        # Add staff roles
        for role in guild.roles:
            if role.permissions.manage_messages and not role.is_default():
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
        
        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            category=category,
            overwrites=overwrites,
            topic=f"Ticket dari {user} ({user.id})"
        )
        
        embed = miku_embed(f"🎫 Ticket Dibuka", 
            f"Halo {user.mention}!\n\nSilakan jelaskan masalah/pertanyaan kamu di sini.\nStaff akan segera merespons.\n\nKlik tombol **🔒 Tutup** untuk menutup ticket.")
        
        close_view = TicketCloseView(self.bot)
        await channel.send(content=user.mention, embed=embed, view=close_view)
        
        await interaction.response.send_message(
            embed=success_embed("Ticket Dibuat", f"Ticket: {channel.mention}"),
            ephemeral=True
        )

class TicketCloseView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label="🔒 Tutup Ticket", style=discord.ButtonStyle.red, custom_id="ticket_close_persistent")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = warning_embed("Ticket akan ditutup", "Channel akan dihapus dalam 5 detik...")
        await interaction.response.send_message(embed=embed)
        await __import__('asyncio').sleep(5)
        try:
            await interaction.channel.delete(reason=f"Ticket ditutup oleh {interaction.user}")
        except:
            pass

class Tickets(commands.Cog):
    """🎫 Ticket system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    async def cog_load(self):
        self.bot.add_view(TicketView(self.bot))
        self.bot.add_view(TicketCloseView(self.bot))
    
    @commands.hybrid_command(name="ticketsetup", description="Setup panel ticket di channel ini")
    @commands.has_permissions(manage_channels=True)
    async def ticketsetup(self, ctx):
        embed = miku_embed("🎫 Support Ticket System", 
            "Butuh bantuan? Punya pertanyaan?\n\nKlik tombol di bawah untuk membuka ticket privat dengan staff.")
        embed.add_field(name="📌 Tips", value="• Jelaskan masalah dengan jelas\n• Sabar menunggu respons staff\n• Tutup ticket jika sudah selesai", inline=False)
        embed.set_footer(text="MikuBot Ticket System")
        
        view = TicketView(self.bot)
        await ctx.send(embed=embed, view=view)
        if ctx.interaction:
            await ctx.interaction.response.send_message("✅ Panel ticket dibuat", ephemeral=True)
    
    @commands.hybrid_command(name="ticketclose", description="Tutup ticket saat ini")
    @commands.has_permissions(manage_channels=True)
    async def ticketclose(self, ctx):
        if not ctx.channel.name.startswith("ticket-"):
            return await ctx.send(embed=error_embed("Bukan Ticket", "Command ini hanya di channel ticket"))
        await ctx.send(embed=warning_embed("Closing Ticket", "Channel akan dihapus dalam 5 detik..."))
        await __import__('asyncio').sleep(5)
        await ctx.channel.delete()
    
    @commands.hybrid_command(name="ticketadd", description="Tambah user ke ticket")
    @commands.has_permissions(manage_channels=True)
    async def ticketadd(self, ctx, member: discord.Member):
        if not ctx.channel.name.startswith("ticket-"):
            return await ctx.send(embed=error_embed("Bukan Ticket", "Hanya di channel ticket"))
        await ctx.channel.set_permissions(member, view_channel=True, send_messages=True)
        await ctx.send(embed=success_embed("User Ditambahkan", f"{member.mention} telah ditambahkan ke ticket"))
    
    @commands.hybrid_command(name="ticketremove", description="Hapus user dari ticket")
    @commands.has_permissions(manage_channels=True)
    async def ticketremove(self, ctx, member: discord.Member):
        if not ctx.channel.name.startswith("ticket-"):
            return await ctx.send(embed=error_embed("Bukan Ticket", "Hanya di channel ticket"))
        await ctx.channel.set_permissions(member, overwrite=None)
        await ctx.send(embed=success_embed("User Dihapus", f"{member.mention} telah dihapus dari ticket"))

async def setup(bot):
    await bot.add_cog(Tickets(bot))
