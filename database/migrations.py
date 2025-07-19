# database/migrations.py
import asyncio
import json
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime

class Migration:
    """Base migration class"""
    
    def __init__(self, name: str, version: int):
        self.name = name
        self.version = version
    
    async def up(self, db_manager):
        """Apply migration"""
        raise NotImplementedError
    
    async def down(self, db_manager):
        """Rollback migration"""
        raise NotImplementedError

class MigrationManager:
    """Database migration manager"""
    
    def __init__(self, db_manager, migrations_dir: str = "migrations"):
        self.db_manager = db_manager
        self.migrations_dir = Path(migrations_dir)
        self.migrations: List[Migration] = []
    
    async def create_migrations_table(self):
        """Create migrations tracking table"""
        sql = """
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            version INTEGER NOT NULL,
            applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        await self.db_manager.execute(sql)
    
    async def get_applied_migrations(self) -> List[int]:
        """Get list of applied migration versions"""
        await self.create_migrations_table()
        
        sql = "SELECT version FROM migrations ORDER BY version"
        results = await self.db_manager.fetch_all(sql)
        
        return [row[0] for row in results]
    
    async def apply_migration(self, migration: Migration):
        """Apply single migration"""
        print(f"Applying migration: {migration.name}")
        
        try:
            await migration.up(self.db_manager)
            
            # Record migration
            sql = "INSERT INTO migrations (name, version) VALUES (?, ?)"
            await self.db_manager.execute(sql, (migration.name, migration.version))
            
            print(f"✓ Applied migration: {migration.name}")
        except Exception as e:
            print(f"✗ Failed to apply migration {migration.name}: {e}")
            raise
    
    async def rollback_migration(self, migration: Migration):
        """Rollback single migration"""
        print(f"Rolling back migration: {migration.name}")
        
        try:
            await migration.down(self.db_manager)
            
            # Remove migration record
            sql = "DELETE FROM migrations WHERE version = ?"
            await self.db_manager.execute(sql, (migration.version,))
            
            print(f"✓ Rolled back migration: {migration.name}")
        except Exception as e:
            print(f"✗ Failed to rollback migration {migration.name}: {e}")
            raise
    
    async def migrate(self):
        """Apply all pending migrations"""
        applied_versions = await self.get_applied_migrations()
        
        pending_migrations = [
            m for m in self.migrations 
            if m.version not in applied_versions
        ]
        
        pending_migrations.sort(key=lambda m: m.version)
        
        if not pending_migrations:
            print("No pending migrations")
            return
        
        for migration in pending_migrations:
            await self.apply_migration(migration)
    
    def add_migration(self, migration: Migration):
        """Add migration to manager"""
        self.migrations.append(migration)
