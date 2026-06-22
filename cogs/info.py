"""
INFO COG - Features 51-65
User Info, Server Info, Avatar, Stats, etc.
"""
import discord
from discord.ext import commands
from datetime import datetime
from utils.embeds import *

class Info(commands.Cog):
    """ℹ️ Information commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    # ===== Feature 51: User Info =====
    @commands.hybrid_command(name="userinfo", description="Info user")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        roles = [r.mention for r in member.roles[1:]][:10]
        
        embed = info_embed(f"User Info: {member}")
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.color = member.color if member.color != discord.Color.default() else MIKU_TEAL
        embed.add_field(name=f"{EMOJIS['id']} ID", value=member.id, inline=True)
        embed.add_field(name=f"{EMOJIS['name']} Nickname", value=member.display_name, inline=True)
        embed.add_field(name=f"{EMOJIS['bot']} Bot", value="Ya" if member.bot else "Tidak", inline=True)
        embed.add_field(name=f"{EMOJIS['calendar']} Account Dibuat", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)
        embed.add_field(name=f"📥 Join Server", value=member.joined_at.strftime("%d/%m/%Y %H:%M") if member.joined_at else "Unknown", inline=True)
        embed.add_field(name=f"{EMOJIS['online']} Status", value=str(member.status).title(), inline=True)
        embed.add_field(name=f"{EMOJIS['role']} Roles [{len(roles)}]", value=" ".join(roles) if roles else "Tidak ada", inline=False)
        if member.premium_since:
            embed.add_field(name=f"{EMOJIS['boost']} Boost Server", value=member.premium_since.strftime("%d/%m/%Y"), inline=True)
        await ctx.send(embed=embed)
    
    # ===== Feature 52: Server Info =====
    @commands.hybrid_command(name="serverinfo", description="Info server")
    async def serverinfo(self, ctx):
        g = ctx.guild
        embed = info_embed(f"Server Info: {g.name}")
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)
        if g.banner:
            embed.set_image(url=g.banner.url)
        
        embed.add_field(name=f"{EMOJIS['id']} ID", value=g.id, inline=True)
        embed.add_field(name=f"{EMOJIS['owner']} Owner", value=g.owner.mention if g.owner else "Unknown", inline=True)
        embed.add_field(name=f"{EMOJIS['calendar']} Dibuat", value=g.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name=f"{EMOJIS['members']} Members", value=g.member_count, inline=True)
        embed.add_field(name=f"{EMOJIS['human']} Humans", value=sum(1 for m in g.members if not m.bot), inline=True)
        embed.add_field(name=f"{EMOJIS['bot']} Bots", value=sum(1 for m in g.members if m.bot), inline=True)
        embed.add_field(name=f"{EMOJIS['channel']} Text", value=len(g.text_channels), inline=True)
        embed.add_field(name=f"{EMOJIS['voice']} Voice", value=len(g.voice_channels), inline=True)
        embed.add_field(name=f"{EMOJIS['role']} Roles", value=len(g.roles), inline=True)
        embed.add_field(name=f"{EMOJIS['boost']} Boost Tier", value=f"Level {g.premium_tier}", inline=True)
        embed.add_field(name=f"{EMOJIS['boost']} Boosts", value=g.premium_subscription_count, inline=True)
        embed.add_field(name="✅ Verification", value=str(g.verification_level).title(), inline=True)
        await ctx.send(embed=embed)
    
    # ===== Feature 53: Avatar =====
    @commands.hybrid_command(name="avatar", description="Tampilkan avatar user")
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = info_embed(f"Avatar: {member}")
        embed.set_image(url=member.display_avatar.url)
        embed.description = f"[Download Link]({member.display_avatar.url})"
        await ctx.send(embed=embed)
    
    # ===== Feature 54: Banner =====
    @commands.hybrid_command(name="banner", description="Tampilkan banner user")
    async def banner(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user = await self.bot.fetch_user(member.id)
        if not user.banner:
            return await ctx.send(embed=info_embed("Tidak Ada Banner", f"{member} tidak punya banner"))
        embed = info_embed(f"Banner: {member}")
        embed.set_image(url=user.banner.url)
        await ctx.send(embed=embed)
    
    # ===== Feature 55: Member Count =====
    @commands.hybrid_command(name="membercount", description="Jumlah member")
    async def membercount(self, ctx):
        g = ctx.guild
        total = g.member_count
        humans = sum(1 for m in g.members if not m.bot)
        bots = total - humans
        online = sum(1 for m in g.members if m.status != discord.Status.offline)
        
        embed = info_embed(f"👥 Member Count - {g.name}")
        embed.add_field(name="📊 Total", value=f"**{total}**", inline=True)
        embed.add_field(name=f"{EMOJIS['human']} Humans", value=f"**{humans}**", inline=True)
        embed.add_field(name=f"{EMOJIS['bot']} Bots", value=f"**{bots}**", inline=True)
        embed.add_field(name=f"{EMOJIS['online']} Online", value=f"**{online}**", inline=True)
        embed.add_field(name=f"{EMOJIS['offline']} Offline", value=f"**{total - online}**", inline=True)
        embed.add_field(name="📈 Bar", value=make_progress_bar(online, total), inline=False)
        await ctx.send(embed=embed)
    
    # ===== Feature 56: Server Stats =====
    @commands.hybrid_command(name="stats", description="Statistik lengkap server")
    async def stats(self, ctx):
        g = ctx.guild
        embed = info_embed(f"📊 Stats: {g.name}")
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)
        
        embed.add_field(name="👥 Total Members", value=g.member_count, inline=True)
        embed.add_field(name="📝 Channels", value=len(g.channels), inline=True)
        embed.add_field(name="🎭 Roles", value=len(g.roles), inline=True)
        embed.add_field(name="😀 Emojis", value=len(g.emojis), inline=True)
        embed.add_field(name="🎵 Stickers", value=len(g.stickers), inline=True)
        embed.add_field(name=f"{EMOJIS['boost']} Boosts", value=g.premium_subscription_count, inline=True)
        await ctx.send(embed=embed)
    
    # ===== Feature 57: Join Date =====
    @commands.hybrid_command(name="joindate", description="Kapan member join server")
    async def joindate(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        if not member.joined_at:
            return await ctx.send(embed=error_embed("Gagal", "Tidak bisa dapatkan tanggal join"))
        days = (datetime.utcnow() - member.joined_at.replace(tzinfo=None)).days
        embed = info_embed(f"📥 Join Date - {member}")
        embed.add_field(name="Tanggal Join", value=member.joined_at.strftime("%d %B %Y %H:%M UTC"), inline=False)
        embed.add_field(name="Sudah Berapa Lama", value=f"**{days}** hari", inline=False)
        await ctx.send(embed=embed)
    
    # ===== Feature 58: Account Age =====
    @commands.hybrid_command(name="accountage", description="Umur akun Discord")
    async def accountage(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        days = (datetime.utcnow() - member.created_at.replace(tzinfo=None)).days
        embed = info_embed(f"📅 Account Age - {member}")
        embed.add_field(name="Dibuat", value=member.created_at.strftime("%d %B %Y"), inline=False)
        embed.add_field(name="Umur Akun", value=f"**{days}** hari (~{days//365} tahun)", inline=False)
        await ctx.send(embed=embed)
    
    # ===== Feature 59: Permissions =====
    @commands.hybrid_command(name="permissions", description="Cek permissions user")
    async def permissions(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        perms = [p[0].replace("_", " ").title() for p in member.guild_permissions if p[1]]
        embed = info_embed(f"🔑 Permissions - {member}")
        embed.description = "✅ " + "\n✅ ".join(perms) if perms else "Tidak ada"
        await ctx.send(embed=embed)
    
    # ===== Feature 60: Server Icon =====
    @commands.hybrid_command(name="servericon", description="Icon server")
    async def servericon(self, ctx):
        if not ctx.guild.icon:
            return await ctx.send(embed=info_embed("Tidak Ada", "Server ini tidak punya icon"))
        embed = info_embed(f"🖼️ Icon {ctx.guild.name}")
        embed.set_image(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)
    
    # ===== Feature 61: Server Banner =====
    @commands.hybrid_command(name="serverbanner", description="Banner server")
    async def serverbanner(self, ctx):
        if not ctx.guild.banner:
            return await ctx.send(embed=info_embed("Tidak Ada", "Server ini tidak punya banner"))
        embed = info_embed(f"🎨 Banner {ctx.guild.name}")
        embed.set_image(url=ctx.guild.banner.url)
        await ctx.send(embed=embed)
    
    # ===== Feature 62: Online Count =====
    @commands.hybrid_command(name="online", description="Hitung member online")
    async def online(self, ctx):
        statuses = {"online": 0, "idle": 0, "dnd": 0, "offline": 0}
        for m in ctx.guild.members:
            statuses[str(m.status)] = statuses.get(str(m.status), 0) + 1
        
        embed = info_embed(f"📊 Status Members - {ctx.guild.name}")
        embed.add_field(name=f"{EMOJIS['online']} Online", value=statuses['online'], inline=True)
        embed.add_field(name=f"{EMOJIS['idle']} Idle", value=statuses['idle'], inline=True)
        embed.add_field(name=f"{EMOJIS['dnd']} DND", value=statuses['dnd'], inline=True)
        embed.add_field(name=f"{EMOJIS['offline']} Offline", value=statuses['offline'], inline=True)
        await ctx.send(embed=embed)
    
    # ===== Feature 63: Bot Count =====
    @commands.command(name="botcount")
    async def botcount(self, ctx):
        bots = [m for m in ctx.guild.members if m.bot]
        embed = info_embed(f"🤖 Bots di {ctx.guild.name}", f"Total: **{len(bots)}**")
        embed.description += "\n\n" + "\n".join([f"• {b.mention}" for b in bots[:20]])
        await ctx.send(embed=embed)
    
    # ===== Feature 64: Emoji List =====
    @commands.command(name="emojis")
    async def emojis(self, ctx):
        if not ctx.guild.emojis:
            return await ctx.send(embed=info_embed("Tidak Ada", "Server tidak punya emoji custom"))
        chunks = [str(e) for e in ctx.guild.emojis[:50]]
        embed = info_embed(f"😀 Emojis - {ctx.guild.name}", f"Total: **{len(ctx.guild.emojis)}**\n\n" + " ".join(chunks))
        await ctx.send(embed=embed)
    
    # ===== Feature 65: Boosters List =====
    @commands.command(name="boosters")
    async def boosters(self, ctx):
        boosters = [m for m in ctx.guild.members if m.premium_since]
        if not boosters:
            return await ctx.send(embed=info_embed("Tidak Ada Booster", "Belum ada yang boost server"))
        text = "\n".join([f"{EMOJIS['boost']} {m.mention} - {m.premium_since.strftime('%d/%m/%Y')}" for m in boosters[:20]])
        embed = info_embed(f"🚀 Boosters {ctx.guild.name}", f"Total: **{len(boosters)}**\n\n{text}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
