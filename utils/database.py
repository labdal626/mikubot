"""
Simple JSON-based database for persistent storage.
Handles warnings, settings, economy, levels, tickets, etc.
"""
import json
import os
import asyncio
from typing import Any, Dict, Optional

class Database:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self._cache = {}
        self._lock = asyncio.Lock()
    
    def _get_path(self, name: str) -> str:
        return os.path.join(self.data_dir, f"{name}.json")
    
    def load(self, name: str, default: Any = None) -> Dict:
        """Load data from JSON file"""
        if default is None:
            default = {}
        
        if name in self._cache:
            return self._cache[name]
        
        path = self._get_path(name)
        if not os.path.exists(path):
            self._cache[name] = default
            self.save(name, default)
            return default
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._cache[name] = data
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            self._cache[name] = default
            return default
    
    def save(self, name: str, data: Any) -> bool:
        """Save data to JSON file"""
        try:
            path = self._get_path(name)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self._cache[name] = data
            return True
        except Exception as e:
            print(f"DB Save Error: {e}")
            return False
    
    def get_guild(self, name: str, guild_id: int) -> Dict:
        """Get guild-specific data"""
        data = self.load(name, {})
        gid = str(guild_id)
        if gid not in data:
            data[gid] = {}
            self.save(name, data)
        return data[gid]
    
    def set_guild(self, name: str, guild_id: int, key: str, value: Any) -> bool:
        """Set guild-specific value"""
        data = self.load(name, {})
        gid = str(guild_id)
        if gid not in data:
            data[gid] = {}
        data[gid][key] = value
        return self.save(name, data)
    
    def get_user(self, name: str, guild_id: int, user_id: int) -> Dict:
        """Get user-specific data within a guild"""
        guild_data = self.get_guild(name, guild_id)
        uid = str(user_id)
        if uid not in guild_data:
            guild_data[uid] = {}
            self.set_guild(name, guild_id, uid, {})
        return guild_data[uid]
    
    def set_user(self, name: str, guild_id: int, user_id: int, key: str, value: Any) -> bool:
        """Set user-specific value within a guild"""
        data = self.load(name, {})
        gid = str(guild_id)
        uid = str(user_id)
        if gid not in data:
            data[gid] = {}
        if uid not in data[gid]:
            data[gid][uid] = {}
        data[gid][uid][key] = value
        return self.save(name, data)
