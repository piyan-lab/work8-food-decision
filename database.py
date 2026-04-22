import sqlite3
from datetime import datetime
import math

DB_PATH = "food_decider.db"

def haversine(lat1, lon1, lat2, lon2):
    """計算兩點間的公尺距離"""
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 建立自建餐廳表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        lat REAL NOT NULL,
        lng REAL NOT NULL,
        price_level INTEGER NOT NULL,
        rating REAL,
        address TEXT
    )
    ''')
    
    # 無痛升級：嘗試加入 city 欄位
    try:
        cursor.execute("ALTER TABLE restaurants ADD COLUMN city TEXT")
        cursor.execute("UPDATE restaurants SET city = '台北市' WHERE city IS NULL")
    except sqlite3.OperationalError:
        pass # 欄位已存在
    
    # User tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    # History tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS eat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        restaurant_id TEXT,
        restaurant_name TEXT NOT NULL,
        item_name TEXT NOT NULL,
        spent_amount INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    
    # 檢查是否有測試資料，若無則寫入種子資料
    cursor.execute("SELECT COUNT(*) FROM restaurants")
    if cursor.fetchone()[0] == 0:
        seed_data = [
            ("巷口乾麵", 25.0480, 121.5165, 1, 4.2, "台北市中正區忠孝西路一段1號", "台北市"),
            ("豪華牛排", 25.0490, 121.5180, 3, 4.8, "台北市中正區忠孝西路一段2號", "台北市"),
            ("阿嬤滷肉飯", 25.0470, 121.5160, 1, 4.5, "台北市中正區忠孝西路一段3號", "台北市"),
            ("文青咖啡", 25.0465, 121.5175, 2, 4.0, "台北市中正區忠孝西路一段4號", "台北市"),
            ("連鎖速食", 25.0475, 121.5185, 2, 3.8, "台北市中正區忠孝西路一段5號", "台北市"),
            ("日式壽司", 25.0500, 121.5150, 4, 4.6, "台北市中正區忠孝西路一段6號", "台北市"),
            ("健康餐盒", 25.0450, 121.5190, 2, 4.1, "台北市中正區忠孝西路一段7號", "台北市"),
        ]
        cursor.executemany('''
            INSERT INTO restaurants (name, lat, lng, price_level, rating, address, city)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', seed_data)
        
    conn.commit()
    conn.close()

def get_nearby_restaurants(user_lat, user_lng, radius_m, max_price_level):
    """查詢預算內的餐廳，並根據距離過濾"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM restaurants WHERE price_level <= ?", (max_price_level,))
    all_restaurants = cursor.fetchall()
    conn.close()
    
    results = []
    for r in all_restaurants:
        dist = haversine(user_lat, user_lng, r['lat'], r['lng'])
        if dist <= radius_m:
            res_dict = dict(r)
            res_dict['distance'] = round(dist)
            results.append(res_dict)
            
    return results

# 管理員 CRUD 餐廳功能
def get_all_restaurants():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants ORDER BY id DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def add_restaurant(name, lat, lng, price_level, rating, address, city):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO restaurants (name, lat, lng, price_level, rating, address, city)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, lat, lng, price_level, rating, address, city))
    conn.commit()
    conn.close()

def update_restaurant(res_id, name, lat, lng, price_level, rating, address, city):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE restaurants 
        SET name=?, lat=?, lng=?, price_level=?, rating=?, address=?, city=?
        WHERE id=?
    ''', (name, lat, lng, price_level, rating, address, city, res_id))
    conn.commit()
    conn.close()

def delete_restaurant(res_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM restaurants WHERE id=?", (res_id,))
    conn.commit()
    conn.close()

# 會員與歷史紀錄功能
def create_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    row = cursor.fetchone()
    conn.close()
    return row['id'] if row else None

def get_username(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row['username'] if row else None

def add_history(user_id, place_id, restaurant_name, item_name, spent_amount):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO eat_history (user_id, restaurant_id, restaurant_name, item_name, spent_amount)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, place_id, restaurant_name, item_name, spent_amount))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT restaurant_name, item_name, spent_amount, created_at 
        FROM eat_history 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
