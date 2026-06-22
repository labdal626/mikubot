"""
Beautiful embed builders with Miku-themed styling
"""
import discord
from datetime import datetime

# Miku theme colors
MIKU_TEAL = 0x39C5BB
MIKU_PINK = 0xFF69B4
SUCCESS = 0x00FF7F
ERROR = 0xFF4444
WARNING = 0xFFD700
INFO = 0x00BFFF

# Beautiful emojis
EMOJIS = {
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "loading": "⏳",
    "miku": "🎵",
    "star": "✨",
    "heart": "💖",
    "fire": "🔥",
    "crown": "👑",
    "shield": "🛡️",
    "hammer": "🔨",
    "lock": "🔒",
    "unlock": "🔓",
    "ban": "🔨",
    "kick": "👢",
    "mute": "🔇",
    "unmute": "🔊",
    "warn": "⚠️",
    "online": "🟢",
    "offline": "⚫",
    "idle": "🟡",
    "dnd": "🔴",
    "bot": "🤖",
    "human": "👤",
    "channel": "📝",
    "voice": "🎤",
    "category": "📁",
    "role": "🎭",
    "ping": "🏓",
    "uptime": "⏱️",
    "calendar": "📅",
    "id": "🆔",
    "name": "📛",
    "owner": "👑",
    "members": "👥",
    "boost": "🚀",
    "level": "📊",
    "money": "💰",
    "ticket": "🎫",
    "giveaway": "🎉",
    "poll": "📊",
    "music": "🎶",
    "game": "🎮",
    "dice": "🎲",
    "coin": "🪙",
    "magic": "✨",
    "sparkle": "💫"
}

def base_embed(title: str = None, description: str = None, color: int = MIKU_TEAL) -> discord.Embed:
    """Create a base styled embed"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text="✨ MikuBot • Made with 💖", icon_url=None)
    return embed

def success_embed(title: str, description: str = None) -> discord.Embed:
    """Success embed"""
    return base_embed(f"{EMOJIS['success']} {title}", description, SUCCESS)

def error_embed(title: str, description: str = None) -> discord.Embed:
    """Error embed"""
    return base_embed(f"{EMOJIS['error']} {title}", description, ERROR)

def warning_embed(title: str, description: str = None) -> discord.Embed:
    """Warning embed"""
    return base_embed(f"{EMOJIS['warning']} {title}", description, WARNING)

def info_embed(title: str, description: str = None) -> discord.Embed:
    """Info embed"""
    return base_embed(f"{EMOJIS['info']} {title}", description, INFO)

def miku_embed(title: str, description: str = None) -> discord.Embed:
    """Miku-themed embed"""
    return base_embed(f"{EMOJIS['miku']} {title}", description, MIKU_TEAL)

def loading_embed(text: str = "Memproses...") -> discord.Embed:
    """Loading embed"""
    return base_embed(f"{EMOJIS['loading']} {text}", color=INFO)

def make_progress_bar(current: int, total: int, length: int = 20) -> str:
    """Create a visual progress bar"""
    if total == 0:
        return "▱" * length
    filled = int(length * current / total)
    bar = "▰" * filled + "▱" * (length - filled)
    percentage = (current / total) * 100
    return f"{bar} `{percentage:.1f}%`"

def format_duration(seconds: int) -> str:
    """Format seconds to human-readable duration"""
    intervals = [
        ('tahun', 31536000),
        ('bulan', 2592000),
        ('minggu', 604800),
        ('hari', 86400),
        ('jam', 3600),
        ('menit', 60),
        ('detik', 1)
    ]
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append(f"{value} {name}")
        if len(result) >= 2:
            break
    return ", ".join(result) if result else "0 detik"
