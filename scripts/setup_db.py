import sqlite3
from pathlib import Path

def setup_database():

    db_path = Path('articles.db')
    schema_path = Path(__file__).parent.parent / "lib" / "db" / "schema.sql"
    
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found at {schema_path}")
    
    if db_path.exists():
        try:
            db_path.unlink()
        except PermissionError as e:
            raise RuntimeError(f"Could not remove existing database: {e}")

    try:
        conn = sqlite3.connect(str(db_path))
        conn.execute("PRAGMA foreign_keys = ON")
        
        with open(schema_path) as f:
            schema_sql = f.read()
        
        conn.executescript(schema_sql)
        conn.commit()
        print(f"Database created successfully at {db_path.absolute()}")
        
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    try:
        setup_database()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)