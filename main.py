"""
███╗   ███╗██╗██╗  ██╗██╗   ██╗██████╗  ██████╗ ████████╗
████╗ ████║██║██║ ██╔╝██║   ██║██╔══██╗██╔═══██╗╚══██╔══╝
██╔████╔██║██║█████╔╝ ██║   ██║██████╔╝██║   ██║   ██║   
██║╚██╔╝██║██║██╔═██╗ ██║   ██║██╔══██╗██║   ██║   ██║   
██║ ╚═╝ ██║██║██║  ██╗╚██████╔╝██████╔╝╚██████╔╝   ██║   
╚═╝     ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝   
                    Discord Server Manager v1.0
                    100+ Features | Stable | Free
"""
import discord
from discord.ext import commands
import asyncio
import os
import json
import logging
from datetime import datetime
from utils.keep_alive import keep_alive
from utils.database import Database

# ===== Logging Setup =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mikubot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('MikuBot')

# ===== Load Config =====
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        default_config = {
            "prefix": "!",
            "owner_id": 0,
            "embed_color": 0xFF69B4,
            "success_color": 0x00FF7F,
            "error_color": 0xFF4444,
            "warning_color": 0xFFD700,
            "info_color": 0x00BFFF,
            "miku_color": 0x39C5BB
        }
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
        return default_config

config = load_config()

# ===== Bot Intents =====
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.messages = True
intents.reactions = True
intents.presences = True
intents.voice_states = True

# ===== Bot Initialization =====
class MikuBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.get("prefix", "!")),
            intents=intents,
            help_command=None,
            case_insensitive=True,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="✨ /help | MikuBot Online"
            ),
            status=discord.Status.online
        )
        self.config = config
        self.db = Database()
        self.start_time = datetime.utcnow()
        self.version = "1.0.0"

    async def setup_hook(self):
        """Load all cogs on startup"""
        cogs_to_load = [
            'cogs.moderation',
            'cogs.channel',
            'cogs.roles',
            'cogs.info',
            'cogs.fun',
            'cogs.welcome',
            'cogs.utility',
            'cogs.tickets',
            'cogs.giveaway',
            'cogs.automod',
            'cogs.logging_cog',
            'cogs.help_cog',
            'cogs.economy',
            'cogs.leveling'
        ]
        
        loaded = 0
        for cog in cogs_to_load:
            try:
                await self.load_extension(cog)
                logger.info(f"✅ Loaded: {cog}")
                loaded += 1
            except Exception as e:
                logger.error(f"❌ Failed to load {cog}: {e}")
        
        logger.info(f"📦 Total cogs loaded: {loaded}/{len(cogs_to_load)}")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"🔄 Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"Failed to sync: {e}")

    async def on_ready(self):
        """Bot ready event with beautiful banner"""
        banner = f"""
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   ███╗   ███╗██╗██╗  ██╗██╗   ██╗                    ║
║   ████╗ ████║██║██║ ██╔╝██║   ██║                    ║
║   ██╔████╔██║██║█████╔╝ ██║   ██║                    ║
║   ██║╚██╔╝██║██║██╔═██╗ ██║   ██║                    ║
║   ██║ ╚═╝ ██║██║██║  ██╗╚██████╔╝                    ║
║   ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝                     ║
║                                                       ║
║   Bot Name : {self.user.name:<40} ║
║   Bot ID   : {self.user.id:<40} ║
║   Servers  : {len(self.guilds):<40} ║
║   Users    : {sum(g.member_count for g in self.guilds):<40} ║
║   Version  : {self.version:<40} ║
║   Status   : ✅ ONLINE                                ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
        """
        print(banner)
        logger.info(f"Bot is ready! Logged in as {self.user}")

    async def on_command_error(self, ctx, error):
        """Global error handler"""
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Akses Ditolak",
                description=f"Kamu tidak punya izin untuk menggunakan command ini.\n**Required:** {', '.join(error.missing_permissions)}",
                color=config["error_color"]
            )
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="⚠️ Argumen Kurang",
                description=f"Argumen yang dibutuhkan: `{error.param.name}`\nGunakan `!help {ctx.command}` untuk info.",
                color=config["warning_color"]
            )
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="⏰ Cooldown",
                description=f"Tunggu **{error.retry_after:.1f}s** sebelum pakai command ini lagi.",
                color=config["warning_color"]
            )
            await ctx.send(embed=embed, delete_after=5)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="🤖 Bot Kurang Izin",
                description=f"Bot butuh izin: {', '.join(error.missing_permissions)}",
                color=config["error_color"]
            )
            await ctx.send(embed=embed, delete_after=10)
        else:
            logger.error(f"Error in {ctx.command}: {error}")
            embed = discord.Embed(
                title="❌ Terjadi Error",
                description=f"```{str(error)[:1000]}```",
                color=config["error_color"]
            )
            await ctx.send(embed=embed, delete_after=15)

# ===== Run Bot =====
async def main():
    bot = MikuBot()
    
    # Start keep-alive web server
    keep_alive()
    logger.info("🌐 Keep-alive server started")
    
    # Get token
    token = os.environ.get('TOKEN') or os.environ.get('DISCORD_TOKEN')
    if not token:
        logger.error("❌ TOKEN tidak ditemukan! Set environment variable TOKEN di Render.")
        return
    
    try:
        await bot.start(token)
    except discord.LoginFailure:
        logger.error("❌ Token Discord tidak valid!")
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
