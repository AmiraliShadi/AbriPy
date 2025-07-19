# database/orm.py
import asyncio
import json
from typing import Dict, List, Any, Optional, Type, TypeVar
from dataclasses import dataclass, field
import sqlite3
import aiosqlite
from abc import ABC, abstractmethod

T = TypeVar('T', bound='Model')

@dataclass
class Field:
    """Database field descriptor"""
    field_type: str
    primary_key: bool = False
    nullable: bool = True
    default: Any = None
    max_length: Optional[int] = None
    unique: bool = False

class Model(ABC):
    """Base model class"""
    
    _table_name: str = ""
    _fields: Dict[str, Field] = {}
    _db_manager: 'DatabaseManager' = None
    
    def __init__(self, **kwargs):
        for field_name, field in self._fields.items():
            value = kwargs.get(field_name, field.default)
            setattr(self, field_name, value)
    
    @classmethod
    def set_db_manager(cls, db_manager: 'DatabaseManager'):
        """Set database manager"""
        cls._db_manager = db_manager
    
    @classmethod
    async def create_table(cls):
        """Create table in database"""
        if not cls._db_manager:
            raise ValueError("Database manager not set")
        
        fields_sql = []
        for field_name, field in cls._fields.items():
            field_sql = f"{field_name} {field.field_type}"
            
            if field.primary_key:
                field_sql += " PRIMARY KEY"
            if not field.nullable:
                field_sql += " NOT NULL"
            if field.unique:
                field_sql += " UNIQUE"
            if field.default is not None:
                field_sql += f" DEFAULT {field.default}"
            
            fields_sql.append(field_sql)
        
        sql = f"CREATE TABLE IF NOT EXISTS {cls._table_name} ({', '.join(fields_sql)})"
        await cls._db_manager.execute(sql)
    
    @classmethod
    async def find_by_id(cls: Type[T], id_value: Any) -> Optional[T]:
        """Find record by ID"""
        primary_key_field = None
        for field_name, field in cls._fields.items():
            if field.primary_key:
                primary_key_field = field_name
                break
        
        if not primary_key_field:
            raise ValueError("No primary key field found")
        
        sql = f"SELECT * FROM {cls._table_name} WHERE {primary_key_field} = ?"
        result = await cls._db_manager.fetch_one(sql, (id_value,))
        
        if result:
            return cls(**dict(result))
        return None
    
    @classmethod
    async def find_all(cls: Type[T]) -> List[T]:
        """Find all records"""
        sql = f"SELECT * FROM {cls._table_name}"
        results = await cls._db_manager.fetch_all(sql)
        
        return [cls(**dict(row)) for row in results]
    
    async def save(self):
        """Save record to database"""
        if not self._db_manager:
            raise ValueError("Database manager not set")
        
        # Check if record exists (has primary key value)
        primary_key_field = None
        primary_key_value = None
        
        for field_name, field in self._fields.items():
            if field.primary_key:
                primary_key_field = field_name
                primary_key_value = getattr(self, field_name, None)
                break
        
        if primary_key_value:
            # Update existing record
            set_clauses = []
            values = []
            
            for field_name in self._fields:
                if field_name != primary_key_field:
                    set_clauses.append(f"{field_name} = ?")
                    values.append(getattr(self, field_name))
            
            values.append(primary_key_value)
            sql = f"UPDATE {self._table_name} SET {', '.join(set_clauses)} WHERE {primary_key_field} = ?"
        else:
            # Insert new record
            field_names = [name for name in self._fields if name != primary_key_field or getattr(self, name, None) is not None]
            placeholders = ', '.join(['?' for _ in field_names])
            values = [getattr(self, name) for name in field_names]
            
            sql = f"INSERT INTO {self._table_name} ({', '.join(field_names)}) VALUES ({placeholders})"
        
        await self._db_manager.execute(sql, values)
    
    async def delete(self):
        """Delete record"""
        primary_key_field = None
        primary_key_value = None
        
        for field_name, field in self._fields.items():
            if field.primary_key:
                primary_key_field = field_name
                primary_key_value = getattr(self, field_name, None)
                break
        
        if not primary_key_value:
            raise ValueError("Cannot delete record without primary key")
        
        sql = f"DELETE FROM {self._table_name} WHERE {primary_key_field} = ?"
        await self._db_manager.execute(sql, (primary_key_value,))

class DatabaseManager:
    """Database connection manager"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.connection = None
    
    async def connect(self):
        """Connect to database"""
        if self.database_url.startswith('sqlite'):
            db_path = self.database_url.replace('sqlite://', '')
            self.connection = await aiosqlite.connect(db_path)
        else:
            raise ValueError("Only SQLite supported currently")
    
    async def disconnect(self):
        """Disconnect from database"""
        if self.connection:
            await self.connection.close()
    
    async def execute(self, sql: str, params: tuple = None):
        """Execute SQL statement"""
        if not self.connection:
            await self.connect()
        
        async with self.connection.execute(sql, params or ()) as cursor:
            await self.connection.commit()
            return cursor.lastrowid
    
    async def fetch_one(self, sql: str, params: tuple = None):
        """Fetch one record"""
        if not self.connection:
            await self.connect()
        
        async with self.connection.execute(sql, params or ()) as cursor:
            return await cursor.fetchone()
    
    async def fetch_all(self, sql: str, params: tuple = None):
        """Fetch all records"""
        if not self.connection:
            await self.connect()
        
        async with self.connection.execute(sql, params or ()) as cursor:
            return await cursor.fetchall()

# Example model usage
class User(Model):
    _table_name = "users"
    _fields = {
        'id': Field('INTEGER', primary_key=True),
        'username': Field('VARCHAR(50)', nullable=False, unique=True),
        'email': Field('VARCHAR(100)', nullable=False),
        'created_at': Field('DATETIME', default='CURRENT_TIMESTAMP')
    }
