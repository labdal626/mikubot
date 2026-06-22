"""
CHANNEL MANAGEMENT COG - Features 21-35
"""
import discord
from discord.ext import commands
from utils.embeds import *

class ChannelMgmt(commands.Cog):
    """📝 Channel management"""
    
    def __init__(self, bot):
        self.bot = bot
    
    # ===== Feature 21: Create Text Channel =====
    @commands.hybrid_command(name="createchannel", description="Buat text channel baru")
    @commands.has_permissions(manage_channels=True)
    async def createchannel(self, ctx, *, name: str):
        try:
            channel = await ctx.guild.create_text_channel(name)
            await ctx.send(embed=success_embed("Channel Dibuat", f"{EMOJIS['channel']} {channel.mention} berhasil dibuat"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 22: Create Voice Channel =====
    @commands.hybrid_command(name="createvoice", description="Buat voice channel baru")
    @commands.has_permissions(manage_channels=True)
    async def createvoice(self, ctx, *, name: str):
        try:
            vc = await ctx.guild.create_voice_channel(name)
            await ctx.send(embed=success_embed("Voice Channel Dibuat", f"{EMOJIS['voice']} **{vc.name}** berhasil dibuat"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 23: Create Category =====
    @commands.hybrid_command(name="createcategory", description="Buat category baru")
    @commands.has_permissions(manage_channels=True)
    async def createcategory(self, ctx, *, name: str):
        try:
            cat = await ctx.guild.create_category(name)
            await ctx.send(embed=success_embed("Category Dibuat", f"{EMOJIS['category']} **{cat.name}** berhasil dibuat"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 24: Delete Channel =====
    @commands.hybrid_command(name="deletechannel", description="Hapus channel (default: channel saat ini)")
    @commands.has_permissions(manage_channels=True)
    async def deletechannel(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        try:
            await ctx.send(embed=success_embed("Channel akan Dihapus", f"Channel **{channel.name}** dihapus dalam 5 detik..."))
            await discord.utils.sleep_until(discord.utils.utcnow() + __import__('datetime').timedelta(seconds=5))
            await channel.delete()
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 25: Rename Channel =====
    @commands.hybrid_command(name="rename", description="Rename channel saat ini")
    @commands.has_permissions(manage_channels=True)
    async def rename(self, ctx, *, new_name: str):
        old = ctx.channel.name
        try:
            await ctx.channel.edit(name=new_name)
            await ctx.send(embed=success_embed("Channel Renamed", f"**{old}** → **{new_name}**"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 26: Set Topic =====
    @commands.hybrid_command(name="topic", description="Set topic channel")
    @commands.has_permissions(manage_channels=True)
    async def topic(self, ctx, *, topic: str = ""):
        try:
            await ctx.channel.edit(topic=topic)
            await ctx.send(embed=success_embed("Topic Diubah", f"**Topic baru:** {topic or '(kosong)'}"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 27: NSFW Toggle =====
    @commands.hybrid_command(name="nsfw", description="Toggle NSFW channel")
    @commands.has_permissions(manage_channels=True)
    async def nsfw(self, ctx):
        try:
            new = not ctx.channel.is_nsfw()
            await ctx.channel.edit(nsfw=new)
            status = "🔞 NSFW ON" if new else "✅ SFW"
            await ctx.send(embed=success_embed("Channel Diupdate", f"Status: **{status}**"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 28: Clone Channel =====
    @commands.hybrid_command(name="clone", description="Clone channel saat ini")
    @commands.has_permissions(manage_channels=True)
    async def clone(self, ctx):
        try:
            new = await ctx.channel.clone()
            await ctx.send(embed=success_embed("Channel Cloned", f"Channel baru: {new.mention}"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 29: Nuke Channel =====
    @commands.command(name="nuke")
    @commands.has_permissions(manage_channels=True, administrator=True)
    async def nuke(self, ctx):
        ch = ctx.channel
        pos = ch.position
        try:
            new_ch = await ch.clone()
            await new_ch.edit(position=pos)
            await ch.delete()
            embed = success_embed("💥 NUKED!", "Channel berhasil di-reset!\n\n*All messages have been cleared.*")
            embed.set_image(url="https://media.tenor.com/jJtKkqMVE74AAAAd/explosion-anime.gif")
            await new_ch.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 30: Channel Info =====
    @commands.hybrid_command(name="channelinfo", description="Info channel")
    async def channelinfo(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        embed = info_embed(f"Info Channel: #{channel.name}")
        embed.add_field(name=f"{EMOJIS['id']} ID", value=channel.id, inline=True)
        embed.add_field(name=f"{EMOJIS['category']} Category", value=channel.category.name if channel.category else "None", inline=True)
        embed.add_field(name="🔞 NSFW", value="Yes" if channel.is_nsfw() else "No", inline=True)
        embed.add_field(name="⏱️ Slowmode", value=f"{channel.slowmode_delay}s", inline=True)
        embed.add_field(name=f"{EMOJIS['calendar']} Dibuat", value=channel.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="📌 Topic", value=channel.topic or "Tidak ada", inline=False)
        await ctx.send(embed=embed)
    
    # ===== Feature 31: Channel List =====
    @commands.hybrid_command(name="channels", description="List semua channel di server")
    async def channels(self, ctx):
        text = [f"{EMOJIS['channel']} {c.name}" for c in ctx.guild.text_channels[:20]]
        voice = [f"{EMOJIS['voice']} {c.name}" for c in ctx.guild.voice_channels[:20]]
        embed = info_embed(f"Channels di {ctx.guild.name}")
        embed.add_field(name=f"Text ({len(ctx.guild.text_channels)})", value="\n".join(text) or "Tidak ada", inline=True)
        embed.add_field(name=f"Voice ({len(ctx.guild.voice_channels)})", value="\n".join(voice) or "Tidak ada", inline=True)
        await ctx.send(embed=embed)
    
    # ===== Feature 32: Hide Channel =====
    @commands.hybrid_command(name="hide", description="Sembunyikan channel dari @everyone")
    @commands.has_permissions(manage_channels=True)
    async def hide(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=success_embed("Channel Disembunyikan", "👻 Channel sekarang tersembunyi dari @everyone"), delete_after=10)
    
    # ===== Feature 33: Unhide Channel =====
    @commands.hybrid_command(name="unhide", description="Tampilkan channel ke @everyone")
    @commands.has_permissions(manage_channels=True)
    async def unhide(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = None
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=success_embed("Channel Ditampilkan", "👁️ Channel sekarang terlihat oleh @everyone"))
    
    # ===== Feature 34: Set Channel Position =====
    @commands.command(name="setposition")
    @commands.has_permissions(manage_channels=True)
    async def setposition(self, ctx, position: int):
        try:
            await ctx.channel.edit(position=position)
            await ctx.send(embed=success_embed("Posisi Diubah", f"Posisi channel: **{position}**"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 35: Channel Stats =====
    @commands.command(name="channelstats")
    async def channelstats(self, ctx):
        g = ctx.guild
        embed = info_embed(f"📊 Channel Stats - {g.name}")
        embed.add_field(name=f"{EMOJIS['channel']} Text", value=len(g.text_channels), inline=True)
        embed.add_field(name=f"{EMOJIS['voice']} Voice", value=len(g.voice_channels), inline=True)
        embed.add_field(name=f"{EMOJIS['category']} Category", value=len(g.categories), inline=True)
        embed.add_field(name="📢 Stage", value=len(g.stage_channels), inline=True)
        embed.add_field(name="🧵 Forum", value=len(g.forums) if hasattr(g, 'forums') else 0, inline=True)
        embed.add_field(name="📊 Total", value=len(g.channels), inline=True)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ChannelMgmt(bot))
