
import os, sqlite3
from contextlib import contextmanager
from datetime import datetime

DB_PATH = os.getenv("SQLITE_PATH", "./ai_ceo_saas.db")

@contextmanager
def connect():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()

def init_autopilot_tables():
    """Initialize autopilot-specific tables"""
    with connect() as c:
        # Activity tracking table
        c.execute("""CREATE TABLE IF NOT EXISTS activities(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,        -- 'ideation' | 'validation' | 'build' | 'launch' | 'sale' | 'ad' | 'error'
            detail TEXT,
            amount REAL,      -- revenue or cost (+/-)
            meta JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user(id)
        )""")
        c.execute("""CREATE INDEX IF NOT EXISTS idx_act_user ON activities(user_id)""")
        
        # User autopilot settings
        c.execute("""CREATE TABLE IF NOT EXISTS user_autopilot_settings(
            user_id INTEGER PRIMARY KEY,
            autopilot_enabled BOOLEAN DEFAULT 1,
            last_autopilot_run TIMESTAMP,
            cycle_interval_minutes INTEGER DEFAULT 30,
            FOREIGN KEY(user_id) REFERENCES user(id)
        )""")
        
        # Business tracking
        c.execute("""CREATE TABLE IF NOT EXISTS autopilot_businesses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            platform TEXT,    -- 'shopify' | 'gumroad' | 'teachable' | etc
            product_id TEXT,
            status TEXT DEFAULT 'active',
            meta JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user(id)
        )""")

# ---- User autopilot helpers ----
def get_autopilot_users():
    """Get users with autopilot enabled"""
    with connect() as c:
        rows = c.execute("""
            SELECT u.id, u.email FROM user u
            LEFT JOIN user_autopilot_settings uas ON u.id = uas.user_id
            WHERE (uas.autopilot_enabled = 1 OR uas.autopilot_enabled IS NULL)
            AND u.role != 'suspended'
        """).fetchall()
        return [{"id": r["id"], "email": r["email"]} for r in rows]

def set_autopilot(user_id: int, enabled: bool):
    """Enable/disable autopilot for user"""
    with connect() as c:
        c.execute("""
            INSERT INTO user_autopilot_settings(user_id, autopilot_enabled) 
            VALUES(?, ?)
            ON CONFLICT(user_id) DO UPDATE SET autopilot_enabled=excluded.autopilot_enabled
        """, (user_id, 1 if enabled else 0))

def update_last_autopilot_run(user_id: int):
    """Update last autopilot run timestamp"""
    with connect() as c:
        c.execute("""
            INSERT INTO user_autopilot_settings(user_id, last_autopilot_run) 
            VALUES(?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET last_autopilot_run=CURRENT_TIMESTAMP
        """, (user_id,))

# ---- Activity tracking ----
def record_activity(user_id: int, type_: str, detail: str, amount: float = 0.0, meta_json: str = ""):
    """Record user activity"""
    with connect() as c:
        c.execute("INSERT INTO activities(user_id,type,detail,amount,meta) VALUES(?,?,?,?,?)",
                  (user_id, type_, detail, amount, meta_json))

def activities_since(user_id: int, since_ts: str):
    """Get activities since timestamp"""
    with connect() as c:
        rows = c.execute("""
            SELECT type, detail, amount, created_at FROM activities
            WHERE user_id=? AND datetime(created_at) > datetime(?)
            ORDER BY id ASC
        """,(user_id, since_ts)).fetchall()
        return [dict(r) for r in rows]

def get_recent_activity(user_id: int, limit: int = 5):
    """Get recent activities for user"""
    with connect() as c:
        rows = c.execute("""
            SELECT type, detail, amount, created_at FROM activities
            WHERE user_id=? ORDER BY id DESC LIMIT ?
        """, (user_id, limit)).fetchall()
        return [dict(r) for r in rows]

# ---- Business tracking ----
def record_business(user_id: int, name: str, platform: str, product_id: str = "", meta_json: str = ""):
    """Record new business/product"""
    with connect() as c:
        c.execute("""
            INSERT INTO autopilot_businesses(user_id, name, platform, product_id, meta) 
            VALUES(?,?,?,?,?)
        """, (user_id, name, platform, product_id, meta_json))

def get_user_businesses(user_id: int):
    """Get user's autopilot businesses"""
    with connect() as c:
        rows = c.execute("""
            SELECT * FROM autopilot_businesses WHERE user_id=? ORDER BY created_at DESC
        """, (user_id,)).fetchall()
        return [dict(r) for r in rows]
