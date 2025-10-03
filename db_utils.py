import sqlite3
from datetime import datetime
import json
import os
import sys
from pathlib import Path

# LOG_FILE = os.path.abspath("db_debug.log")
# def log_db(message):
#     with open(LOG_FILE, "a", encoding="utf-8") as f:
#         f.write(f"[{datetime.now()}] {message}\n")

# def log_db(message):
#     with open(LOG_FILE, "a", encoding="utf-8") as f:
#         f.write(f"[{datetime.now()}] {message}\n")

# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS  # Always the root of the extracted files
#     except AttributeError:
#         base_path = os.path.abspath(os.path.dirname(sys.argv[0]))  # During dev, root directory

#     # Ensure we resolve from the root, removing subfolder paths like TikTok_Bot_Merge
#     if "TikTok_Bot_Merge" in base_path:
#         base_path = os.path.dirname(base_path)  # Step back to the root directory

#     resolved_path = os.path.join(base_path, relative_path)
#     print(f"resource_path resolved: {resolved_path}")
#     return resolved_path
def resource_path(relative_path):
    """
    Ensure the database is stored in a persistent location.
    This will store the DB in %APPDATA%/YourApp/ or ~/.yourapp/ depending on OS.
    """
    if sys.platform.startswith("win"):
        base_dir = os.getenv('APPDATA') or os.path.expanduser("~\\AppData\\Roaming")
    else:
        base_dir = os.path.expanduser("~/.yourapp")

    app_dir = Path(base_dir) / "TikTokBot"
    app_dir.mkdir(parents=True, exist_ok=True)

    resolved_path = app_dir / relative_path
    print(f"Persistent DB path resolved: {resolved_path}")
    return str(resolved_path)

def get_connection():
    migrate_bundled_db_if_needed()
    db_path = resource_path("shops.db")
    if not os.path.exists(db_path):
        print(f"DB file not found at {db_path}. A new empty DB would be created.")
        raise FileNotFoundError(f"Database file not found: {db_path}")

    print(f"DB file exists at {db_path}. Checking schema...")
    return sqlite3.connect(db_path)

def migrate_bundled_db_if_needed():
    target_path = resource_path("shops.db")
    if not os.path.exists(target_path):
        try:
            bundled_db = os.path.join(sys._MEIPASS, "shops.db")
            if os.path.exists(bundled_db):
                print("Copying bundled DB to persistent location...")
                with open(bundled_db, "rb") as src, open(target_path, "wb") as dst:
                    dst.write(src.read())
        except Exception as e:
            print(f"Error copying default DB: {e}")

# def get_connection():
#     db_path = os.path.join(os.path.dirname(__file__), "shops.db")
#     return sqlite3.connect(db_path)

def init_db():
    conn = get_connection()
    print (f"Db-connection : {conn}")
    cur = conn.cursor()
    #cur.execute("DROP TABLE IF EXISTS uploads")
    # Create shops table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS shops (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            email TEXT,
            phone TEXT,
            message TEXT,
            followup TEXT,
            last_modified TEXT,
            validdate DATE,
            count INTEGER DEFAULT 0
        )
    """)
    # Create uploads table with UNIQUE shop_id
    cur.execute("""
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id TEXT NOT NULL UNIQUE,
            filename TEXT,
            filepath TEXT,
            FOREIGN KEY (shop_id) REFERENCES shops(id) ON DELETE CASCADE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cookies (
            shop_id TEXT PRIMARY KEY,
            cookie_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (shop_id) REFERENCES shops(id) ON DELETE CASCADE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id TEXT NOT NULL,
            name TEXT NOT NULL,
            processed INTEGER,
            FOREIGN KEY (shop_id) REFERENCES shops(id) ON DELETE CASCADE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id TEXT NOT NULL,
            productid TEXT NOT NULL,
            commission TEXT,
            enabled INTEGER DEFAULT 0 CHECK(enabled IN (0,1)),
            FOREIGN KEY (shop_id) REFERENCES shops(id) ON DELETE CASCADE
        )
    """)
    existing_tables = [row[0] for row in cur.fetchall()]
    print("Tables 'shops', 'uploads', 'cookies', 'Users', 'products' exist in the database.")
    conn.commit()
    conn.close()

def fetch_shops():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            s.id, s.name, s.type, s.email, s.phone, s.message, s.followup, last_modified, validdate, count
        FROM shops s
    """)
    rows = cur.fetchall()
    conn.close()
    return [
        dict(zip(
            ["id", "name", "type", "email", "phone", "message", "followup", "last_modified", "validdate", "count"],
            row
        ))
        for row in rows
    ]

def insert_shop(id, name, type, email, phone, message, followup, validdate):
    print(f"Inserting shop: {id}, {name}, {type}")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO shops (id, name, type, email, phone, message, followup, validdate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
            id, name, type, email, phone, message, followup, validdate
    ))
    conn.commit()
    conn.close()

def update_shop(shop):
    print("Updating shop:", shop["id"], shop["name"])
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE shops SET name=?, type=?, email=?, phone=?, message=?, followup=?, validdate=?
        WHERE id=?
    """, (
        shop["name"], shop["type"], shop.get("email", ""), shop.get("phone", ""),
        shop.get("message", ""), shop.get("followup", ""),shop.get("validdate",""),
        shop["id"]
    ))
        # Update uploads table for filename
    if "filename" in shop:
        cur.execute("""
            INSERT INTO uploads (shop_id, filename) VALUES (?, ?)
            ON CONFLICT(shop_id) DO UPDATE SET filename=excluded.filename
        """, (shop["id"], shop["filename"]))
    conn.commit()
    conn.close()

def delete_shop(shop_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM shops WHERE id=?", (shop_id,))
    conn.commit()
    conn.close()

def get_all_shops():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM shops")
    shops = [row[0] for row in cursor.fetchall()]
    conn.close()
    return shops

def fetch_shop_by_name(shop_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shops WHERE name = ?", (shop_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "type": row[2],
            "email": row[3],
            "phone": row[4],
            "message": row[5],
            "followup": row[6],
            "last_modified":row[7],
            "validdate":row[8],
            "count":row[9],
        }
    else:
        return None

def get_uploads_by_shop(shop_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT filename, filepath FROM uploads WHERE shop_id = ?", (shop_id,))
    uploads = cur.fetchall()

    conn.close()
    return uploads

def get_usernames_by_shop(shop_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM users WHERE shop_id = ?", (shop_id,))
    users = [row[0] for row in cur.fetchall()]
    conn.close()
    return users

def mark_user_processed(shop_id, username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users SET processed = 1 WHERE shop_id = ? AND name = ?
    """, (shop_id, username))
    conn.commit()
    conn.close()

def get_unprocessed_usernames(shop_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT name FROM users WHERE shop_id = ? AND processed = 0
    """, (shop_id,))
    users = [row[0] for row in cur.fetchall()]
    conn.close()
    return users

def get_processed_users(shop_id):
    from db_utils import get_connection  # assuming you have this utility

    conn = get_connection()
    cur = conn.cursor()

    # Select users where processed is True (non-zero)
    cur.execute("""
        SELECT name FROM users
        WHERE shop_id = ? AND processed != 0
    """, (shop_id,))

    # Fetch all matching user names as a list
    processed_users = [row[0] for row in cur.fetchall()]

    conn.close()
    return processed_users

def del_usernames(shop_id, usernames):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE shop_id = ? AND username = ?", (shop_id, usernames))
    conn.commit()
    conn.close()

def insert_new_usernames(shop_id, usernames):
    conn = get_connection()
    cur = conn.cursor()
    for username in usernames:
        cur.execute("""
            INSERT OR IGNORE INTO users (shop_id, username, processed)
            VALUES (?, ?, 0)
        """, (shop_id, username))
    conn.commit()
    conn.close()

def get_invite_details_from_db(shop_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT name, email, phone, message, validdate
        FROM shops
        WHERE id = ?
    """, (shop_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row  
    else:
        raise ValueError(f"No invite data for username: {shop_id}")

def get_shop_summary(shop_name):
    """Return summary dict (total messages, daily, weekly, monthly) for a specific shop by name."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM shops WHERE name=?", (shop_name,))
    result = cursor.fetchone()
    conn.close()

    total_messages = int(result[0]) if result and result[0] is not None else 0
    daily = total_messages // 10
    weekly = total_messages // 3
    monthly = total_messages
    return {
        "Total messages sent": total_messages,
        "Daily message sent": daily,
        "Weekly message sent": weekly,
        "Monthly message sent": monthly,
    }

def get_combined_summary():
    """Return combined summary for all shops by summing their 'message' counts."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(count) FROM shops")
    result = cursor.fetchone()
    conn.close()

    total_messages = result[0] if result and result[0] is not None else 0
    daily = total_messages // 10
    weekly = total_messages // 3
    monthly = total_messages
    return {
        "Total messages sent": total_messages,
        "Daily message sent": daily,
        "Weekly message sent": weekly,
        "Monthly message sent": monthly,
    }

def get_shop_last_modified(shop_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT last_modified FROM shops WHERE name=?", (shop_name,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0]:
        return result[0]
    else:
        return "Not Modified Yet"

def update_last_modified(shop_id):
    conn = get_connection()
    cur = conn.cursor()
    today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"Attempting to update last_modified to: {today}")
    cur.execute("UPDATE shops SET last_modified=? WHERE id=?", (today, shop_id))
    conn.commit()
    conn.close()
    print(f"last_modified updated to {today} for shop_id: {shop_id}")

def save_upload(shop_id, filename, filepath):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO uploads (shop_id, filename, filepath)
        VALUES (?, ?, ?)
        ON CONFLICT(shop_id) DO UPDATE SET
            filename = excluded.filename,
            filepath = excluded.filepath
    """, (shop_id, filename, filepath))

    conn.commit()
    conn.close()

def insert_cookie(shop_id, cookie_text):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    try:
        if isinstance(cookie_text, str):
            logging.warning("cookie_text was a string. Attempting to parse JSON.")
            cookie_text = json.loads(cookie_text)

        if not isinstance(cookie_text, list):
            raise ValueError("cookie_text should be a list of cookies")
        
        cookie_json = json.dumps(cookie_text, ensure_ascii=False) 
        conn = get_connection()
        cur = conn.cursor()
        logging.debug(f"Attempting to insert cookie for shop_id={shop_id}")
        
        cur.execute("""
            INSERT INTO cookies (shop_id, cookie_text)
            VALUES (?, ?)
            ON CONFLICT(shop_id) DO UPDATE SET cookie_text = excluded.cookie_text
        """, (shop_id, cookie_json))
    
        conn.commit()
        conn.close()
        
        logging.info(f"Inserted cookie for shop_id={shop_id} successfully.")
        return True
    except Exception as e:
        logging.error(f"Error inserting cookie for shop_id={shop_id}: {e}")
        return False

def get_cookie_for_shop(shop_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT cookie_text FROM cookies WHERE shop_id = ?
        ORDER BY created_at DESC LIMIT 1
    """, (shop_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        print(f"No cookies found for shop_id={shop_id}")
        return None
    try:
        cookies = json.loads(row[0])  # parse JSON text into Python list
        if isinstance(cookies, list) and all(isinstance(c, dict) for c in cookies):
            # Clean up unwanted fields that Selenium does not support
            for cookie in cookies:
                cookie.pop("storeId", None)
                cookie.pop("hostOnly", None)
                cookie.pop("session", None)
                # Fix sameSite if needed
                if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                    cookie["sameSite"] = "None"
            return cookies
    except json.JSONDecodeError as e:
        print(f"Error decoding cookies JSON: {e}")
    
    return None   

def get_products_for_shop(shop_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT productid, commission FROM products
        WHERE shop_id = ? AND enabled = 1
    """, (shop_id,))
    results = cur.fetchall()
    conn.close()
    return results

def debug_print_uploads():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM uploads")
    rows = cur.fetchall()
    conn.close()
    print("Uploads Table:", rows)

def debug_print(shop_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, processed FROM users WHERE shop_id = ?", (shop_id,))
    for row in cur.fetchall():
        print(row)
    conn.close()

def alter_table():
    conn = get_connection()
    cur = conn.cursor()
    try:
        #cur.execute("DROP TABLE IF EXISTS cookies")
        cur.execute("ALTER TABLE shops DROP COLUMN driver")
        print("count added to 'shops'")
    except sqlite3.OperationalError:
        print("'processed' column already exists")
    conn.commit()
    conn.close()

def print_table_columns(table_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = cur.fetchall()
    conn.close()
    for col in columns:
        print(f"Column: {col[1]} (Type: {col[2]})")

def get_user_names():
    """Fetch and print all names from the 'users' table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    names = cursor.fetchall()
    conn.close()
    return [name[0] for name in names] 

def increment_shop_count(shop_id):
    conn = get_connection()
    cur = conn.cursor()
    # First, retrieve the current count
    cur.execute("SELECT count FROM shops WHERE id = ?", (shop_id,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        raise ValueError(f"No shop found with ID: {shop_id}")

    current_count = row[0] if row[0] is not None else 0
    new_count = current_count + 1
    # Update the count
    cur.execute("UPDATE shops SET count = ? WHERE id = ?", (new_count, shop_id))
    conn.commit()
    conn.close()
    return new_count

def increment_count(shop_id, count):
    conn = get_connection()
    cur = conn.cursor()
    # First, retrieve the current count
    cur.execute("SELECT count FROM shops WHERE id = ?", (shop_id,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        raise ValueError(f"No shop found with ID: {shop_id}")

    current_count = row[0] if row[0] is not None else 0
    new_count = current_count + count
    # Update the count
    cur.execute("UPDATE shops SET count = ? WHERE id = ?", (new_count, shop_id))
    conn.commit()
    conn.close()
    return new_count

def reset_tables(table_names):
    conn = get_connection()
    cur = conn.cursor()

    for table in table_names:
        # Disable foreign key constraints temporarily to avoid issues
        cur.execute("PRAGMA foreign_keys = OFF;")
        cur.execute(f"DELETE FROM {table};")
        cur.execute("PRAGMA foreign_keys = ON;")

    conn.commit()
    conn.close()
    #how to use reset_tables(['users', 'uploads', 'cookies'])

def get_products_by_shop(shop_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT productid, commission, enabled FROM products WHERE shop_id = ?", (shop_id,))
    rows = cur.fetchall()
    return [{"productid": r[0], "commission": r[1], "enabled": int(r[2])} for r in rows]

def add_product(shop_id, productid, commission, enabled=1):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (shop_id, productid, commission, enabled) VALUES (?, ?, ?, ?)",
        (shop_id, productid, commission, enabled)
    )
    conn.commit()

def update_product_enabled(shop_id, productid, enabled):
    print(f"Updating product '{productid}' enabled to {enabled} for shop {shop_id}")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE products SET enabled = ? WHERE shop_id = ? AND productid = ?",
        (enabled, shop_id, productid)
    )
    conn.commit()

def delete_product(shop_id, productid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE shop_id = ? AND productid = ?", (shop_id, productid))
    conn.commit()
