"""
LEVELING SYSTEM - Bonus features
XP per message, Level up, Rank, Leaderboard
"""
import discord
from discord.ext import commands
import random
import time
import math
from utils.embeds import *

class Leveling(commands.Cog):
    """📊 Leveling system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.cooldowns = {}
    
    def get_user(self, guild_id, user_id):
        data = self.db.get_user("levels", guild_id, user_id)
        if "xp" not in data:
            data["xp"] = 0
            data["level"] = 0
            self.db.set_user("levels", guild_id, user_id, "xp", 0)
            self.db.set_user("levels", guild_id, user_id, "level", 0)
        return data
    
    def xp_for_level(self, level):
        return 5 * (level ** 2) + 50 * level + 100
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        if message.content.startswith("!") or message.content.startswith("/"):
            return
        
        user_id = message.author.id
        key = f"{message.guild.id}_{user_id}"
        now = time.time()
        
        if key in self.cooldowns and now - self.cooldowns[key] < 60:
            return  # 1 minute XP cooldown
        self.cooldowns[key] = now
        
        data = self.get_user(message.guild.id, user_id)
        xp_gain = random.randint(15, 25)
        new_xp = data.get("xp", 0) + xp_gain
        current_level = data.get("level", 0)
        xp_needed = self.xp_for_level(current_level)
        
        if new_xp >= xp_needed:
            new_level = current_level + 1
            self.db.set_user("levels", message.guild.id, user_id, "level", new_level)
            self.db.set_user("levels", message.guild.id, user_id, "xp", new_xp - xp_needed)
            
            # Level up message
            s = self.db.get_guild("settings", message.guild.id)
            ch_id = s.get("levelup_channel")
            ch = message.guild.get_channel(ch_id) if ch_id else message.channel
            
            embed = miku_embed("🎉 LEVEL UP!", f"Selamat {message.author.mention}!\nNaik ke **Level {new_level}** 🚀")
            embed.set_thumbnail(url=message.author.display_avatar.url)
            try:
                await ch.send(embed=embed)
            except:
                pass
            
            # Level rewards
            rewards = s.get("level_rewards", {})
            if str(new_level) in rewards:
                role = message.guild.get_role(rewards[str(new_level)])
                if role:
                    try:
                        await message.author.add_roles(role, reason=f"Level {new_level} reward")
                        await ch.send(embed=success_embed("🎁 Role Reward!", f"{message.author.mention} mendapat role {role.mention}"))
                    except:
                        pass
        else:
            self.db.set_user("levels", message.guild.id, user_id, "xp", new_xp)
    
    @commands.hybrid_command(name="level", description="Cek level kamu")
    async def level(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        data = self.get_user(ctx.guild.id, member.id)
        xp = data.get("xp", 0)
        level = data.get("level", 0)
        needed = self.xp_for_level(level)
        
        embed = miku_embed(f"📊 Level - {member.display_name}")
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="🏆 Level", value=f"**{level}**", inline=True)
        embed.add_field(name="✨ XP", value=f"**{xp}/{needed}**", inline=True)
        embed.add_field(name="📊 Progress", value=make_progress_bar(xp, needed, 25), inline=False)
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="rank", description="Rank kamu di server")
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        data = self.db.load("levels", {})
        gid = str(ctx.guild.id)
        if gid not in data:
            return await ctx.send(embed=info_embed("Belum Ada Data", "Mulai chat untuk dapat XP!"))
        
        users = sorted(data[gid].items(), key=lambda x: (x[1].get("level", 0), x[1].get("xp", 0)), reverse=True)
        rank = next((i+1 for i, (uid, _) in enumerate(users) if int(uid) == member.id), None)
        
        if rank:
            udata = self.get_user(ctx.guild.id, member.id)
            embed = miku_embed(f"🏅 Rank - {member.display_name}")
            embed.add_field(name="Rank", value=f"**#{rank}**", inline=True)
            embed.add_field(name="Level", value=f"**{udata.get('level', 0)}**", inline=True)
            embed.add_field(name="XP", value=f"**{udata.get('xp', 0)}**", inline=True)
            embed.set_thumbnail(url=member.display_avatar.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=info_embed("Tidak Ada Rank", f"{member.mention} belum punya XP"))
    
    @commands.hybrid_command(name="levelboard", description="Top 10 highest level")
    async def levelboard(self, ctx):
        data = self.db.load("levels", {})
        gid = str(ctx.guild.id)
        if gid not in data:
            return await ctx.send(embed=info_embed("Kosong", "Belum ada level"))
        
        users = sorted(data[gid].items(), key=lambda x: (x[1].get("level", 0), x[1].get("xp", 0)), reverse=True)[:10]
        text = ""
        medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
        for i, (uid, udata) in enumerate(users):
            member = ctx.guild.get_member(int(uid))
            if member:
                text += f"{medals[i]} **{member.display_name}** - Lvl {udata.get('level', 0)} ({udata.get('xp', 0)} XP)\n"
        
        embed = miku_embed("🏆 Level Leaderboard", text or "Belum ada data")
        await ctx.send(embed=embed)
    
    @commands.command(name="setlevelup")
    @commands.has_permissions(manage_guild=True)
    async def setlevelup(self, ctx, channel: discord.TextChannel):
        self.db.set_guild("settings", ctx.guild.id, "levelup_channel", channel.id)
        await ctx.send(embed=success_embed("Level Up Channel Set", f"Channel: {channel.mention}"))
    
    @commands.command(name="addlevelreward")
    @commands.has_permissions(manage_guild=True)
    async def addlevelreward(self, ctx, level: int, role: discord.Role):
        s = self.db.get_guild("settings", ctx.guild.id)
        rewards = s.get("level_rewards", {})
        rewards[str(level)] = role.id
        self.db.set_guild("settings", ctx.guild.id, "level_rewards", rewards)
        await ctx.send(embed=success_embed("Level Reward Set", f"Level **{level}** → {role.mention}"))
    
    @commands.command(name="levelrewards")
    async def levelrewards(self, ctx):
        s = self.db.get_guild("settings", ctx.guild.id)
        rewards = s.get("level_rewards", {})
        if not rewards:
            return await ctx.send(embed=info_embed("Tidak Ada", "Belum ada level reward"))
        
        text = ""
        for level, role_id in sorted(rewards.items(), key=lambda x: int(x[0])):
            role = ctx.guild.get_role(role_id)
            if role:
                text += f"🏆 Level **{level}** → {role.mention}\n"
        
        embed = miku_embed("🎁 Level Rewards", text)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leveling(bot))
