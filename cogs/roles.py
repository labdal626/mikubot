"""
ROLE MANAGEMENT COG - Features 36-50
"""
import discord
from discord.ext import commands
from utils.embeds import *

class RoleMgmt(commands.Cog):
    """🎭 Role management"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    # ===== Feature 36: Create Role =====
    @commands.hybrid_command(name="createrole", description="Buat role baru")
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, *, name: str):
        try:
            role = await ctx.guild.create_role(name=name)
            await ctx.send(embed=success_embed("Role Dibuat", f"{EMOJIS['role']} {role.mention} berhasil dibuat"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 37: Delete Role =====
    @commands.hybrid_command(name="deleterole", description="Hapus role")
    @commands.has_permissions(manage_roles=True)
    async def deleterole(self, ctx, role: discord.Role):
        try:
            name = role.name
            await role.delete()
            await ctx.send(embed=success_embed("Role Dihapus", f"Role **{name}** berhasil dihapus"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 38: Add Role to User =====
    @commands.hybrid_command(name="addrole", description="Tambah role ke user")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):
        if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send(embed=error_embed("Gagal", "Role lebih tinggi dari role-mu!"))
        try:
            await member.add_roles(role)
            await ctx.send(embed=success_embed("Role Ditambah", f"Role {role.mention} ditambahkan ke {member.mention}"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 39: Remove Role =====
    @commands.hybrid_command(name="removerole", description="Hapus role dari user")
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        try:
            await member.remove_roles(role)
            await ctx.send(embed=success_embed("Role Dihapus", f"Role {role.mention} dihapus dari {member.mention}"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 40: Role Info =====
    @commands.hybrid_command(name="roleinfo", description="Info role")
    async def roleinfo(self, ctx, role: discord.Role):
        embed = info_embed(f"Role: {role.name}")
        embed.color = role.color
        embed.add_field(name=f"{EMOJIS['id']} ID", value=role.id, inline=True)
        embed.add_field(name="🎨 Warna", value=str(role.color), inline=True)
        embed.add_field(name=f"{EMOJIS['members']} Members", value=len(role.members), inline=True)
        embed.add_field(name="📌 Position", value=role.position, inline=True)
        embed.add_field(name="📢 Mentionable", value="Ya" if role.mentionable else "Tidak", inline=True)
        embed.add_field(name="✨ Hoisted", value="Ya" if role.hoist else "Tidak", inline=True)
        embed.add_field(name=f"{EMOJIS['calendar']} Dibuat", value=role.created_at.strftime("%d/%m/%Y"), inline=True)
        await ctx.send(embed=embed)
    
    # ===== Feature 41: Role List =====
    @commands.hybrid_command(name="roles", description="List semua role di server")
    async def roles(self, ctx):
        roles = sorted(ctx.guild.roles, key=lambda r: r.position, reverse=True)
        roles = [r for r in roles if r.name != "@everyone"]
        
        text = "\n".join([f"{r.mention} - {len(r.members)} members" for r in roles[:25]])
        embed = info_embed(f"Roles di {ctx.guild.name}", f"Total: **{len(roles)}** roles")
        embed.description += f"\n\n{text}"
        await ctx.send(embed=embed)
    
    # ===== Feature 42: Auto Role on Join =====
    @commands.hybrid_command(name="autorole", description="Set role otomatis untuk member baru")
    @commands.has_permissions(manage_roles=True, manage_guild=True)
    async def autorole(self, ctx, role: discord.Role = None):
        if role is None:
            self.db.set_guild("settings", ctx.guild.id, "autorole", None)
            return await ctx.send(embed=success_embed("Autorole Disabled", "Autorole dimatikan"))
        
        self.db.set_guild("settings", ctx.guild.id, "autorole", role.id)
        await ctx.send(embed=success_embed("Autorole Set", f"Role {role.mention} akan otomatis diberikan ke member baru"))
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        settings = self.db.get_guild("settings", member.guild.id)
        role_id = settings.get("autorole")
        if role_id:
            role = member.guild.get_role(role_id)
            if role:
                try:
                    await member.add_roles(role, reason="Autorole")
                except:
                    pass
    
    # ===== Feature 43: Role Color =====
    @commands.hybrid_command(name="rolecolor", description="Ubah warna role (hex tanpa #)")
    @commands.has_permissions(manage_roles=True)
    async def rolecolor(self, ctx, role: discord.Role, color_hex: str):
        try:
            color_hex = color_hex.replace("#", "")
            color = discord.Color(int(color_hex, 16))
            await role.edit(color=color)
            await ctx.send(embed=success_embed("Warna Diubah", f"Warna {role.mention} → #{color_hex.upper()}"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 44: Role Rename =====
    @commands.hybrid_command(name="rolerename", description="Rename role")
    @commands.has_permissions(manage_roles=True)
    async def rolerename(self, ctx, role: discord.Role, *, new_name: str):
        old = role.name
        try:
            await role.edit(name=new_name)
            await ctx.send(embed=success_embed("Role Renamed", f"**{old}** → **{new_name}**"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 45: Toggle Hoist =====
    @commands.hybrid_command(name="hoist", description="Toggle hoist (display separately) role")
    @commands.has_permissions(manage_roles=True)
    async def hoist(self, ctx, role: discord.Role):
        try:
            await role.edit(hoist=not role.hoist)
            await ctx.send(embed=success_embed("Hoist Diubah", f"Role {role.mention} hoist: **{role.hoist}**"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 46: Toggle Mentionable =====
    @commands.hybrid_command(name="mentionable", description="Toggle mentionable role")
    @commands.has_permissions(manage_roles=True)
    async def mentionable(self, ctx, role: discord.Role):
        try:
            await role.edit(mentionable=not role.mentionable)
            await ctx.send(embed=success_embed("Mentionable Diubah", f"Role {role.mention} mentionable: **{role.mentionable}**"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    # ===== Feature 47: Mass Add Role =====
    @commands.command(name="massaddrole")
    @commands.has_permissions(manage_roles=True, administrator=True)
    async def massaddrole(self, ctx, role: discord.Role):
        await ctx.send(embed=loading_embed(f"Menambahkan {role.name} ke semua member..."))
        count = 0
        for m in ctx.guild.members:
            if role not in m.roles and not m.bot:
                try:
                    await m.add_roles(role)
                    count += 1
                except:
                    continue
        await ctx.send(embed=success_embed("Selesai", f"Role ditambahkan ke **{count}** members"))
    
    # ===== Feature 48: Mass Remove Role =====
    @commands.command(name="massremoverole")
    @commands.has_permissions(manage_roles=True, administrator=True)
    async def massremoverole(self, ctx, role: discord.Role):
        await ctx.send(embed=loading_embed(f"Menghapus {role.name} dari semua member..."))
        count = 0
        for m in role.members:
            try:
                await m.remove_roles(role)
                count += 1
            except:
                continue
        await ctx.send(embed=success_embed("Selesai", f"Role dihapus dari **{count}** members"))
    
    # ===== Feature 49: Role Members =====
    @commands.command(name="rolemembers")
    async def rolemembers(self, ctx, role: discord.Role):
        members = [m.mention for m in role.members[:30]]
        embed = info_embed(f"Members dengan {role.name}", f"Total: **{len(role.members)}**\n\n" + "\n".join(members) if members else "Tidak ada member dengan role ini")
        await ctx.send(embed=embed)
    
    # ===== Feature 50: Reaction Roles =====
    @commands.command(name="reactionrole")
    @commands.has_permissions(manage_roles=True)
    async def reactionrole(self, ctx, message_id: str, emoji: str, role: discord.Role):
        try:
            msg = await ctx.channel.fetch_message(int(message_id))
            await msg.add_reaction(emoji)
            
            data = self.db.load("reaction_roles", {})
            gid = str(ctx.guild.id)
            if gid not in data:
                data[gid] = {}
            key = f"{message_id}_{emoji}"
            data[gid][key] = role.id
            self.db.save("reaction_roles", data)
            
            await ctx.send(embed=success_embed("Reaction Role Set", 
                f"React dengan {emoji} di pesan untuk dapat role {role.mention}"))
        except Exception as e:
            await ctx.send(embed=error_embed("Error", str(e)))
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member and payload.member.bot:
            return
        data = self.db.load("reaction_roles", {})
        gid = str(payload.guild_id)
        if gid not in data:
            return
        key = f"{payload.message_id}_{payload.emoji}"
        if key in data[gid]:
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(data[gid][key])
            if role and payload.member:
                try:
                    await payload.member.add_roles(role, reason="Reaction Role")
                except:
                    pass
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        data = self.db.load("reaction_roles", {})
        gid = str(payload.guild_id)
        if gid not in data:
            return
        key = f"{payload.message_id}_{payload.emoji}"
        if key in data[gid]:
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(data[gid][key])
            member = guild.get_member(payload.user_id)
            if role and member:
                try:
                    await member.remove_roles(role, reason="Reaction Role Removed")
                except:
                    pass

async def setup(bot):
    await bot.add_cog(RoleMgmt(bot))
