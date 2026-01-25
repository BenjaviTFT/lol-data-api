import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import get_connection
from riot.match_ingestion import (
    ensure_fact_player_match_table,
    ensure_dim_player_table,
    ensure_match_game_table
)

def ensure_reference_tables():
    """Create reference tables (dim_champion, dim_item)"""
    print("Creating reference tables...")
    conn = get_connection()
    cur = conn.cursor()

    # Table dim_champion
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS riot_dim;
        
        CREATE TABLE IF NOT EXISTS riot_dim.dim_champion (
            champion_id INT PRIMARY KEY,
            champion_name TEXT NOT NULL,
            champion_key TEXT NOT NULL,
            title TEXT
        );
    """)

    # Table dim_item
    cur.execute("""
        CREATE TABLE IF NOT EXISTS riot_dim.dim_item (
            item_id INT PRIMARY KEY,
            item_name TEXT NOT NULL,
            description TEXT,
            total_gold INT,
            tags TEXT[]
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Reference tables created.")

def run_initialization():
    print(">>> STARTING VPS DATABASE INITIALIZATION <<<")
    
    try:
        # 1. Ensure Reference Tables
        ensure_reference_tables()
        
        # 2. Ensure Match/Player Tables (using existing logic)
        print("Creating match and player tables...")
        ensure_dim_player_table()
        ensure_match_game_table()
        ensure_fact_player_match_table()
        print("Match and player tables created.")
        
        print(">>> INITIALIZATION COMPLETED SUCCESSFULLY <<<")
        print("You can now run the view deployment script.")
        
    except Exception as e:
        print(f"!!! INITIALIZATION FAILED: {e} !!!")
        sys.exit(1)

if __name__ == "__main__":
    run_initialization()
